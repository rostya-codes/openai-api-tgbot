from decimal import Decimal

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user, get_user, calculate
import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
# from middlewares import BaseMiddleware

user = Router()

# user.message.middleware(BaseMiddleware())


@user.message(F.text == '✖️ Cancel')
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


@user.message(Chat.text)
async def chat_response_handler(message: Message, state: FSMContext):
    """Chat response handler"""
    tg_user = await get_user(message.from_user.id)
    if Decimal(tg_user.balance) > 0:
        await state.set_state(Chat.wait)
        response = await gpt_text(message.text, 'gpt-4o')
        await calculate(message.from_user.id, response['usage'], 'gpt-4o')
        await message.answer(response['response'])
        await state.set_state(Chat.text)
    else:
        await message.answer('🪙❌ Insufficient funds on balance.')


@user.message(Chat.wait)
async def wait_handler(message: Message):
    await message.answer('🫸 Answer for your first request is generating now, please wait a bit.')
