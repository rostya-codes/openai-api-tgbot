from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='💬 Chat')
    ],
    [
        KeyboardButton(text='🖼️ Image generation')
    ]
], resize_keyboard=True, input_field_placeholder='Select point from menu.')


cancel = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='✖️ Cancel')
    ]
], resize_keyboard=True)
