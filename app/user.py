import os
import uuid
from decimal import Decimal

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.keyboards as kb
from app.database.requests import calculate, get_user, set_user
from app.generators import gpt_image, gpt_text, gpt_vision
from app.states import Chat, Image

# from middlewares import BaseMiddleware

user = Router()

model = 'gpt-4o-mini'

# user.message.middleware(BaseMiddleware())


@user.message(F.text == '✖️ Cancel')
@user.message(Command('cancel'))
@user.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await set_user(message.from_user.id, message.from_user.username)
    await message.answer('🦾 Hi! I\'m Rostya AI.', reply_markup=kb.main)
    await state.clear()


@user.message(F.text == '💬 Chat')
async def chatting_handler(message: Message, state: FSMContext):
    """Chatting handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Chat.text)
        await message.answer('❔ Enter your request', reply_markup=kb.cancel)
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(Chat.text, F.photo)
async def chat_response_handler(message: Message, state: FSMContext):
    """Chat response handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Chat.wait)
        file = await message.bot.get_file(message.photo[-1].file_id)
        file_path = file.file_path
        file_name = uuid.uuid4()
        await message.bot.download_file(file_path, f'{file_name}.jpeg')
        response = await gpt_vision(message.caption, model, f'{file_name}.jpeg')
        await calculate(message.from_user.id, response['usage'], model, tg_user)
        await message.answer(response['response'])
        await state.set_state(Chat.text)
        os.remove(f'{file_name}.jpeg')
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(Chat.text)
async def chat_response_handler(message: Message, state: FSMContext):
    """Chat response handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Chat.wait)
        response = await gpt_text(message.text, model)
        await calculate(message.from_user.id, response['usage'], model, tg_user)
        await message.answer(response['response'])
        await state.set_state(Chat.text)
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(F.text == '🖼️ Image generation')
async def chatting_image_handler(message: Message, state: FSMContext):
    """Chatting handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Image.text)
        await message.answer('❔ Enter your request', reply_markup=kb.cancel)
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(Image.text)
async def chat_response_image_handler(message: Message, state: FSMContext):
    """Chat response handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Image.wait)
        response = await gpt_image(message.text, 'dall-e-3')
        await calculate(message.from_user.id, response['usage'], 'dall-e-3', tg_user)
        print(response)
        try:
            await message.answer_photo(response['response'])
        except Exception as e:
            print(e)
            await message.answer(response['response'])
        await state.set_state(Image.text)
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(Image.wait)
@user.message(Chat.wait)
async def wait_handler(message: Message):
    """Send notification message after the first request before AI answer"""
    await message.answer('🫸 Answer for your first request is generating now, please wait a bit.')
