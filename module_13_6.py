from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api =''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.row(button1)
kb.insert(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.\nНапишите <Рассчитать> для продолжения')


@dp.message_handler(text='Рассчитать')
async def info(message):
    await message.answer('Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text='formulas')
async def form(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) - 5 x возраст (г) - 161.')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес в килограммах:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=int(message.text))
    await message.answer('Укажите свой пол М или Ж')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories (message, state):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data["gender"] == 'Ж':
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) - 161
    else:
        calories = (10 * data['weight']) + (6.25 * data['growth']) - (5 * data['age']) + 5

    await message.answer(f"Ваша норма калорий в день составляет- {calories}")
    await message.answer('Спасибо, что воспользовались ботом')
    await state.finish()
@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
if __name__ =='__main__':
    executor.start_polling(dp, skip_updates=True)


