import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Bot tokenini kiriting
API_TOKEN = ""

# Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Dummy data - filmlar
movies = [
    {"name": "Elementary (2023)", "photo": "https://via.placeholder.com/300x400",
     "link": "https://example.com/movie1"},
    {"name": "John Carter (2012)", "photo": "https://via.placeholder.com/300x400",
     "link": "https://example.com/movie2"},
    {"name": "Home Alone 2 (1992)", "photo": "https://via.placeholder.com/300x400",
     "link": "https://example.com/movie3"},
    {"name": "The Avengers (2012)", "photo": "https://via.placeholder.com/300x400",
     "link": "https://example.com/movie4"},
    {"name": "Titanic (1997)", "photo": "https://via.placeholder.com/300x400",
     "link": "https://example.com/movie5"},
]

# Routerni o‘rnatish
router = Router()


# Start komandasi
@router.message(Command("start"))
async def start_command_handler(message: types.Message):
    await message.answer("🔍 Qidiruv uchun film nomini yozing:")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Search Movies", callback_data="search_movies")]
    ])
    await message.answer("🎥 Welcome to Midnight Cinema!\nChoose an option below:", reply_markup=keyboard)


@dp.callback_query(F.data == "search_movies")
async def show_movies(callback_query: types.CallbackQuery):
    await callback_query.message.answer("🎬 Available Movies:")
    for movie in movies:
        # Inline tugma tayyorlash
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎬 Watch", url=movie["link"])]
        ])
        # Rasm va tavsif yuborish
        await callback_query.message.answer_photo(photo=movie["photo"], caption=f"{movie['name']}",
                                                  reply_markup=keyboard)


# Qidiruv funksiyasi
@router.message(F.text)
async def search_movies(message: types.Message):
    query = message.text.lower()
    matched_movies = [movie for movie in movies if query in movie["name"].lower()]

    if matched_movies:
        for movie in matched_movies:
            # Inline tugma bilan rasm yuborish
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🎥 Filmni ko'rish", url=movie["link"])]
                ]
            )
            await message.answer_photo(
                photo=movie["photo"],
                caption=f"*{movie['name']}*\n\n[🎥 Havola orqali kirish]({movie['link']})",
                reply_markup=keyboard,
                parse_mode="Markdown",
            )
    else:
        await message.answer("🔍 Hech narsa topilmadi. Yana urinib ko‘ring.")


dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
