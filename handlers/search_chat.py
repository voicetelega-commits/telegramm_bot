import asyncio
from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.main_menu import get_categories_keyboard, get_search_keyboard
from database.chats_db import chats_db

router = Router()

user_pages = {}

class SearchStates(StatesGroup):
    waiting_for_keyword = State()

# Меню категорий
@router.callback_query(F.data == 'search_by_category') 
async def menu_categories(callback: types.CallbackQuery):
    text_menu = 'Выберите категорию:'
    await callback.message.edit_text(text_menu, reply_markup=get_categories_keyboard())
    await callback.answer()

# Обработчик категорий с пагинацией
@router.callback_query(F.data.startswith('cat_'))
async def show_category_channels(callback: types.CallbackQuery):
    category_id = callback.data
    user_id = callback.from_user.id
    user_pages[user_id] = {category_id: 0}
    await show_category_page(callback, category_id, 0)
    await callback.answer()

# Показать страницу категории
async def show_category_page(callback: types.CallbackQuery, category_id: str, page: int):
    user_id = callback.from_user.id  # noqa: F841 - переменная для будущего использования
    limit = 5
    
    category_info = chats_db.get_category_info(category_id)
    channels = chats_db.get_channels_by_category(category_id, limit=limit, offset=page * limit)
    total_channels = chats_db.get_channels_count_by_category(category_id)
    
    if not category_info or not channels:
        await callback.answer("Категория не найдена или пуста")
        return

    text = f"<b>{category_info['name']}</b>\n\n"
    
    for i, channel in enumerate(channels, 1):
        text += f"<b>{channel['name']}</b>\n"
        text += f"{channel['username']} [{channel['subscribers']}]\n\n"
    
    # Добавляем информацию о странице
    current_page = page + 1
    total_pages = (total_channels + limit - 1) // limit
    text += f"📄 Страница {current_page}/{total_pages}\n"
    text += "#crypto"
    
    # Создаем клавиатуру с пагинацией
    builder = InlineKeyboardBuilder()
    
    # Кнопки пагинации
    if page > 0:
        builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data=f"page_{category_id}_{page-1}"))
    
    if (page + 1) * limit < total_channels:
        builder.add(InlineKeyboardButton(text="Вперед ▶️", callback_data=f"page_{category_id}_{page+1}"))
    
    builder.add(InlineKeyboardButton(text="◀️ Назад к категориям", callback_data="back_to_search"))
    builder.adjust(2, 1)  # 2 кнопки в первом ряду, затем 1
    
    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode='HTML'
    )

# Обработчик пагинации
@router.callback_query(F.data.startswith('page_'))
async def handle_pagination(callback: types.CallbackQuery):
    # page_cat_crypto_1 -> ['page', 'cat_crypto', '1']
    parts = callback.data.split('_')
    if len(parts) >= 3:
        category_id = f"{parts[1]}_{parts[2]}"  # cat_crypto
        page = int(parts[3]) if len(parts) > 3 else 0
        
        await show_category_page(callback, category_id, page)
    await callback.answer()

# Кнопка назад
@router.callback_query(F.data == 'back_to_search')
async def to_main_start(callback: types.CallbackQuery):
    text_menu = 'Выберите способ поиска:'
    await callback.message.edit_text(text_menu, reply_markup=get_search_keyboard())
    await callback.answer()

# Поиск по ключевым словам
@router.callback_query(F.data == 'search_by_keyword')
async def start_keyword_search(callback: types.CallbackQuery, state: FSMContext):
    text = "🔍 <b>Поиск по ключевым словам:</b>\n\n"
    text += "Введите ключевое слово для поиска:\n"
    text += "• Название канала\n"
    text += "• Username\n"
    text += "• Тематику\n\n"
    text += "<i>Пример: crypto, bitcoin, news</i>"

    builder = InlineKeyboardBuilder()  
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_search"))  
    builder.adjust(1)

    # УДАЛЯЕМ предыдущее сообщение и отправляем новое
    await callback.message.delete()
    await callback.message.answer(
        text, 
        reply_markup=builder.as_markup(), 
        parse_mode='HTML'
    )
    
    await state.set_state(SearchStates.waiting_for_keyword)
    await callback.answer()

# Обработчик ввода ключевого слова
@router.message(SearchStates.waiting_for_keyword)
async def process_keyword_search(message: types.Message, state: FSMContext):
    keyword = message.text.strip()

    # УДАЛЯЕМ сообщение пользователя
    await message.delete()

    if len(keyword) < 2:
        # Отправляем временное сообщение об ошибке (удалится через 3 секунды)
        msg = await message.answer("❌ Слишком короткий запрос. Введите минимум 2 символа.")
        await asyncio.sleep(3)
        await msg.delete()
        return

    results = chats_db.search_channels(keyword)
    
    if not results:
        text = f"🔍 <b>Результаты поиска по запросу:</b> '{keyword}'\n\n"
        text += "❌ Ничего не найдено.\n\n"
        text += "Попробуйте:\n"
        text += "• Другие ключевые слова\n"
        text += "• Более общий запрос\n"
        text += "• Поиск по категориям"

        builder = InlineKeyboardBuilder() 
        builder.add(InlineKeyboardButton(text='🔍 Новый поиск', callback_data='new_keyword_search'))  # Изменили callback_data
        builder.add(InlineKeyboardButton(text='🧭 Поиск по категориям', callback_data='search_by_category'))
        builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_search")) 
        builder.adjust(1)

        await message.answer(text, reply_markup=builder.as_markup(), parse_mode='HTML')

    else:
        text = f"🔍 <b>Результаты поиска по запросу:</b> '{keyword}'\n\n"

        for i, channel in enumerate(results[:10], 1):  
            text += f"<b>{channel['name']}</b>\n"
            text += f"{channel['username']} [{channel['subscribers']}]\n"
            text += f"📁 {channel['emoji']} {channel['category_name']}\n\n"           

        if len(results) > 10:
            text += f"<i>Показано 10 из {len(results)} результатов</i>\n\n"

        text += "💡 <i>Используйте поиск по категориям для более точных результатов</i>"
        
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="🔍 Новый поиск", callback_data="new_keyword_search"))  # Изменили callback_data
        builder.add(InlineKeyboardButton(text="🧭 Поиск по категориям", callback_data="search_by_category"))
        builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_search"))
        builder.adjust(1)
        
        await message.answer(
            text,
            reply_markup=builder.as_markup(),
            parse_mode='HTML'
        )

    await state.clear()

# Новый обработчик для кнопки "Новый поиск" (удаляет предыдущее сообщение)
@router.callback_query(F.data == 'new_keyword_search')
async def new_keyword_search(callback: types.CallbackQuery, state: FSMContext):
    text = "🔍 <b>Поиск по ключевым словам:</b>\n\n"
    text += "Введите ключевое слово для поиска:\n"
    text += "• Название канала\n"
    text += "• Username\n"
    text += "• Тематику\n\n"
    text += "<i>Пример: crypto, bitcoin, news</i>"

    builder = InlineKeyboardBuilder()  
    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_search"))  
    builder.adjust(1)

    # УДАЛЯЕМ предыдущее сообщение с результатами и отправляем новое
    await callback.message.delete()
    await callback.message.answer(
        text, 
        reply_markup=builder.as_markup(), 
        parse_mode='HTML'
    )
    
    await state.set_state(SearchStates.waiting_for_keyword)
    await callback.answer()

# Обработчик отмены поиска
@router.callback_query(F.data == "back_to_search", SearchStates.waiting_for_keyword)
async def cancel_search(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text_menu = 'Выберите способ поиска:'
    await callback.message.edit_text(text_menu, reply_markup=get_search_keyboard())
    await callback.answer()