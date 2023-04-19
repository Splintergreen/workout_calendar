from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter, Text, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from simple_calendar import SimpleCalendar
from calendar_types import SimpleCalendarCallback
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from pprint import pprint
from database import users, workout_names
from keyboards import (
    start_keyboard,
    train_keyboard,
    stat_keyboard,
    another_workup
)

load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')

storage: MemoryStorage = MemoryStorage()

bot: Bot = Bot(token=TG_TOKEN)
dp: Dispatcher = Dispatcher()


class FSMWorkout(StatesGroup):
    date = State()
    workout_type = State()
    approaches_num = State()
    comment = State()


@dp.message(CommandStart())
async def start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = []
    text = (
        f'Привет {message.from_user.full_name}, это бот-календарь тренировок!'
        '\nЧтобы добавить тренировку - /add_workout'
        '\nСтатистика тренировок за все время- /stat'
        '\nСтатистика тренировок за месяц - /show_month_workouts'
        '\nПомощь - /help'
        )
    await message.answer(text, reply_markup=start_keyboard)


@dp.message(Command(commands=['add_workout']), StateFilter(default_state))
@dp.callback_query(Text(text=['add_workout']), StateFilter(default_state))
async def add_train_press(msg_or_call, state: FSMContext):
    message, user_id = msg_or_call_check(msg_or_call)
    await message.answer(
        'Выберите дату тренировки:',
        reply_markup=await SimpleCalendar().start_calendar(user_id))
    await state.set_state(FSMWorkout.date)


@dp.callback_query(Text(text=['end_workout']))
async def end_workout_press(callback: CallbackQuery):
    await callback.message.answer(
        'Жду вас после следующего посещения фитнеса!'
        )


@dp.message(Command(commands=['month_workouts']), StateFilter(default_state))
@dp.callback_query(Text(text=['month_workouts']), StateFilter(default_state))
async def show_month_train_command(msg_or_call, state: FSMContext):
    message, user_id = msg_or_call_check(msg_or_call)
    month_count = 10 # !!!!!!!!!!!!!!!!!!!!!!!!
    print(users[user_id])
    text = (
        f'У вас {month_count} тренировок в этом месяце.\n'
        'Выберите 💪🏻 для просмотра тренировок за день.\n'
        'Или выберите другую дату чтоб добавить тренировку.'
        )
    await message.answer(
        text,
        reply_markup=await SimpleCalendar().start_calendar(
            user_id
        )
    )
    await state.set_state(FSMWorkout.date)


@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer('Тут будет список комманд!')


@dp.message(Command(commands=['stat']))
async def stat_command(message: Message):
    workout_days_total = len(get_training_dates(message.from_user.id))
    text = f'Ваши тренировки за все время: {workout_days_total}'
    await message.answer(text)


@dp.callback_query(SimpleCalendarCallback.filter(), StateFilter(FSMWorkout.date))
async def process_simple_calendar(
    callback_query: CallbackQuery,
    callback_data: dict, state: FSMContext
):
    selected, date = await SimpleCalendar().process_selection(
        callback_query,
        callback_data
    )
    if selected:
        selected_date = f'{date.strftime("%d/%m/%Y")}'
        user_id = callback_query.from_user.id
        training_dates = get_training_dates(user_id)
        if selected_date in training_dates and 'тренировок в этом месяце' in callback_query.message.text:
            await state.clear()
            workouts = get_workout_data(user_id, selected_date)
            text = f'Ваши тренировки за {selected_date}'
            for workout in workouts:
                for type, info in workout.items():
                    num = info['approaches_num']
                    comment = info['comment']
                    workout_name = workout_names[type]
                    text += f'\n{workout_name}:\nКоличество подходов - {num}\nКомментарий: {comment}'
            markup = stat_keyboard()
        else:
            await state.update_data(date=selected_date)
            markup = train_keyboard()
            text = 'Укажите тип тренировки:'
            await state.set_state(FSMWorkout.workout_type)
        await callback_query.message.answer(
            text,
            reply_markup=markup
        )
        await callback_query.answer()


@dp.callback_query(StateFilter(FSMWorkout.workout_type))
async def workout_callback(callback_data: CallbackQuery, state: FSMContext):
    await state.update_data(workout_type=callback_data.data)
    await callback_data.message.answer('Укажите количество подходов:')
    await callback_data.answer()
    await state.set_state(FSMWorkout.approaches_num)


@dp.message(
        StateFilter(FSMWorkout.approaches_num),
        lambda x: x.text.isdigit() and 0 <= int(x.text) <= 100
    )
async def approaches_num_callback(message: Message, state: FSMContext):
    await state.update_data(approaches_num=message.text)
    await message.answer('Укажите комментарий к тренировке:')
    await state.set_state(FSMWorkout.comment)


@dp.message(StateFilter(FSMWorkout.comment))
async def comment_callback(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    workout_state = await state.get_data()
    user_id = message.from_user.id
    add_workout_data(workout_state, user_id)
    await state.clear()
    await message.answer(
        'Тренировка добавлена!',
        reply_markup=another_workup()
    )
    pprint(users)


def get_workout_data(user_id, date):
    date_index = get_training_dates(user_id).index(date)
    workout_this_day = users[user_id][date_index][date]
    return workout_this_day


def add_workout_data(state, user_id):
    workout = state.pop('workout_type', None)
    workout_data = {workout: state}
    new_date = state.pop('date', None)
    training_dates = get_training_dates(user_id)
    if new_date in training_dates:
        date_index = training_dates.index(new_date)
        users[user_id][date_index][new_date].append(workout_data)
    else:
        users.setdefault(user_id, [])
        users[user_id].append({new_date: [workout_data]})


def get_training_dates(user_id):
    if users.get(user_id) is None:
        return ''
    return [''.join(list(d.keys())) for d in users[user_id]]


def msg_or_call_check(msg_or_call):
    if isinstance(msg_or_call, CallbackQuery):
        print("callback")
        message = msg_or_call.message
        user_id = msg_or_call.from_user.id
    elif isinstance(msg_or_call, Message):
        print('message')
        message = msg_or_call
        user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = []
    return message, user_id


if __name__ == '__main__':
    dp.run_polling(bot)
