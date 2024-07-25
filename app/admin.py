from aiogram import F, Router
from aiogram.filters import Command, CommandStart, Filter
from aiogram.types import CallbackQuery, Message

admin = Router()


class Admin(Filter):
    def __init__(self):
        self.admins = [123, 456]

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


@admin.message(Admin(), Command('admin'))
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бот, администратор!')
