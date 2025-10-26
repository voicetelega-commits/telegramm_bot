from aiogram import Router, types, F

from keyboards.main_menu import get_pars_user_keyboard, get_main_keyboard


router = Router()


@router.callback_query(F.data == 'parse_members')
async def pars_user(callback: types.CallbackQuery):
    pars_text = 'Какие нужны аккаунты?'
    await callback.message.edit_text(pars_text, reply_markup=get_pars_user_keyboard())
    await callback.answer()


@router.callback_query(F.data == 'back_to_main')
async def to_main_start(callback: types.CallbackQuery):
    await callback.message.delete()
    menu_text = "Выберите функцию:"
    await callback.message.edit_text(menu_text, reply_markup=get_main_keyboard())
    await callback.answer()