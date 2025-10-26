from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



# Главное меню
def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='🔍 Поиск чатов/групп', callback_data='search_chats'),
        InlineKeyboardButton(text='👥 Парсинг активных участников', callback_data='parse_members'),  
        InlineKeyboardButton(text='📚 История моих запросов', callback_data='show_history'))
    builder.adjust(1)
    return builder.as_markup() 

#Менюю поиска каналов
def get_search_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder() 
    builder.add(
        InlineKeyboardButton(text='🔒 Приватные', callback_data='search_private'),
        InlineKeyboardButton(text='🔓 Публичные', callback_data='search_public'),
        InlineKeyboardButton(text='🌐 Все чаты', callback_data='search_all'),
        InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    builder.adjust(2, 1, 1)
    return builder.as_markup() 


#Фильтр парсинга 
def get_pars_user_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='⭐ Premium', callback_data='parse_premium'),
        InlineKeyboardButton(text='👤 Обычные', callback_data='parse_regular'),
        InlineKeyboardButton(text='🌐 Все', callback_data='parse_all'),
        InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    builder.adjust(1)
    return builder.as_markup()
