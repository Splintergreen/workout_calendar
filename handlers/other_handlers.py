from aiogram.types import Message
from aiogram import Router

router: Router = Router()


@router.message()
async def send_some(message: Message):
    await message.delete()
