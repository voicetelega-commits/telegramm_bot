from aiogram import Router, types, F
from aiogram.filters import Command

from keyboards.main_menu import get_main_keyboard, get_search_keyboard


router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    menu_text = "Выберите функцию:"
    await message.answer(menu_text, reply_markup=get_main_keyboard())


@router.callback_query(F.data == 'back_to_main')
async def to_main_start(callback: types.CallbackQuery):
    await callback.message.delete()
    menu_text = "Выберите функцию:"
    await callback.message.answer(menu_text, reply_markup=get_main_keyboard())
    await callback.answer()



@router.callback_query(F.data == 'search_chats')
async def search_chats_handler(callback: types.CallbackQuery):
    search_text = "Выберите тип чатов для поиска:"
    await callback.message.edit_text(search_text, reply_markup=get_search_keyboard())
    await callback.answer()


