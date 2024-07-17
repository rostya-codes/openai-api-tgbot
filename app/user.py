from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user
import app.keyboards as kb
from app.states import Chat
from app.generators import gpt_text
# from middlewares import BaseMiddleware

user = Router()

# user.message.middleware(BaseMiddleware())


@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    await message.answer('🦾 Hi! I\'m Rostya AI.', reply_markup=kb.main)


@user.message(F.text == 'Chat')
async def chatting_handler(message: Message, state: FSMContext):
    """Chatting handler"""
    await state.set_state(Chat.text)
    await message.answer('❔ Enter your request')


@user.message(Chat.text)
async def chat_response_handler(message: Message, state: FSMContext):
    """Chat response handler"""
    await state.set_state(Chat.wait)
    response = await gpt_text(message.text, 'gpt-4o')
    await message.answer(response)
    await state.clear()


@user.message(Chat.wait)
async def wait_handler(message: Message):
    await message.answer('🫸 Answer for your first request is generating now, please wait a bit.')
