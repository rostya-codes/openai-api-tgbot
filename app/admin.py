from aiogram import F, Router
from aiogram.filters import Command, CommandStart, Filter
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

from app.database.requests import get_users
from app.states import Newsletter

admin = Router()


class Admin(Filter):
    def __init__(self):
        self.admins = [6083807927]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.message(Admin(), Command('newsletter'))
async def newsletter_admin_handler(message: Message, state: FSMContext):
    await state.set_state(Newsletter.message)
    await message.answer('Type newsletter message 💬')


@admin.message(Newsletter.message)
async def newsletter_message_admin_handler(message: Message, state: FSMContext):
    await state.clear()
    users = await get_users()

    await message.answer('Newsletter started ↪️')
    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
        except Exception as e:
            print(e)
    await message.answer('Newsletter ended ↩️')
