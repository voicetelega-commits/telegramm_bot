from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.chats_db import chats_db



# Главное меню
def get_main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🔍 Поиск чатов/групп', callback_data='search_chats'),)
    builder.adjust(1)
    return builder.as_markup() 


#Менюю поиска чатов
def get_search_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder() 
    builder.add(
        InlineKeyboardButton(text='🧭 Поиск по категориям', callback_data='search_by_category'),
        InlineKeyboardButton(text='🔑 Поиск по ключевым словам', callback_data='search_by_keyword'),
        InlineKeyboardButton(text='➕ Мои чаты', callback_data='add_chat'),
        InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main'))
    builder.adjust(1)
    return builder.as_markup() 


#Категории чатов
def get_categories_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    categories = chats_db.get_all_categories()
    for category in categories:
        builder.add(InlineKeyboardButton(
            text=category['name'], 
            callback_data=category['id']))


    builder.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_search"))
    builder.adjust(2)  
    return builder.as_markup() 
