from aiogram import Bot, Dispatcher, filters, F
from dotenv import load_dotenv
import os
import random
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

keyboard_button_practice = KeyboardButton(text="Практика")
keyboard_button_cancel = KeyboardButton(text="Отмена")

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[[keyboard_button_practice, keyboard_button_cancel]],
    resize_keyboard=True
)

class Practice(StatesGroup):
    waiting_translation = State()

words = dict(apple='яблоко', cat="кот", house="дом")

@dp.message(filters.CommandStart())
async def start(message):
    first_name = message.from_user.first_name
    greeting = make_greeting(first_name)
    await message.answer(greeting, reply_markup=menu_keyboard)

@dp.message(F.text == "Практика")
async def practice(message, state: FSMContext):
    word = random.choice(list(words))
    await state.update_data(correct_answer=words[word])
    await state.set_state(Practice.waiting_translation)
    await message.answer(f"Переведи слово: {word}")


@dp.message(F.text == "Отмена")
async def cancel(message, state: FSMContext):
    await state.clear()
    await message.answer("Практика отменена")

def make_greeting(name):
    return f"Привет, {name}! Давай учить английский!"

def check_translation(answer, correct_answer):
    check = answer.strip().lower()
    return check == correct_answer

@dp.message(Practice.waiting_translation, F.text)
async def translate(message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data["correct_answer"]
    if check_translation(message.text, correct_answer):
        await message.answer("Верно!")
    else:
        await message.answer(f"Неверно. Правильный ответ: {correct_answer}")
    await state.clear()

async def main():
    await dp.start_polling(bot)
asyncio.run(main())