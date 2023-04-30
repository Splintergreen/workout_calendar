from aiogram import Router
from aiogram.filters import StateFilter, Text, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from workouts_calendar import SimpleCalendar
from workouts_calendar import SimpleCalendarCallback
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from pprint import pprint
from database import users, workout_names
from keyboards import (
    start_keyboard,
    workut_type_keyboard,
    stat_keyboard,
    another_workup,
    main_menu,
    deletion_confirm,
    back_to_month_workouts
)
from lexicon import command_text
from utils import (
    get_workout_dates,
    get_workout_data,
    add_workout_data,
    delete_current_and_previous_message
    )


router: Router = Router()


class FSMWorkout(StatesGroup):
    date = State()
    workout_type = State()
    approaches_num = State()
    comment = State()


selected_workout_date = ''


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = []
    text = command_text.get('/start')(message.from_user.full_name)
    await message.delete()
    await message.answer(text, reply_markup=start_keyboard())


@router.callback_query(Text(text=['start']))
async def start_call(call: CallbackQuery, state: FSMContext):
    text = 'Дневник тренировок - основное меню.'
    await call.message.edit_text(text, reply_markup=start_keyboard())
    await state.clear()


@router.callback_query(Text(text=['add_workout']), StateFilter(default_state))
async def add_workout_call(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    text = command_text.get('/add_workout')
    await call.message.edit_text(
        text,
        reply_markup=await SimpleCalendar().start_calendar(user_id))
    await state.set_state(FSMWorkout.date)


@router.callback_query(Text(text=['end_workout']))
async def end_workout_call(call: CallbackQuery):
    text = command_text.get('/end_workout')  # допилить клавиатуру
    await call.message.answer(text)


@router.callback_query(Text(text=['delete_workout']))
async def delete_workout_call(call: CallbackQuery):
    await call.message.edit_text('Вы уверены?', reply_markup=deletion_confirm)


@router.callback_query(Text(text=['delete_yes']))
async def delete_yes_call(call: CallbackQuery):
    user_id = call.from_user.id
    selected_date = selected_workout_date
    workout_dates = users[user_id]
    for index, date in enumerate(workout_dates):
        if ''.join(list(date.keys())) == selected_date:
            workout_dates.pop(index)
    await call.message.edit_text(
        'Тренировка удалена!',
        reply_markup=back_to_month_workouts
        )


@router.callback_query(Text(text=['delete_no']))
async def delete_no_call(call: CallbackQuery):
    await call.message.edit_text(
        'Передумали, так передумали!',
        reply_markup=back_to_month_workouts
        )


@router.callback_query(
    Text(text=['month_workouts']), StateFilter(default_state)
    )
async def show_month_workout_call(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    month_count = 10  # дописать счетчик тренировок за месяц
    text = command_text.get('/month_workouts')(month_count)
    await call.message.edit_text(
        text,
        reply_markup=await SimpleCalendar().start_calendar(user_id)
    )
    await state.set_state(FSMWorkout.date)


@router.callback_query(Text(text=['about']), StateFilter(default_state))
async def help_command_call(call: CallbackQuery, state: FSMContext):
    await state.clear()
    text = command_text.get('/about')
    await call.message.edit_text(text, reply_markup=main_menu)


@router.callback_query(Text(text=['stat']), StateFilter(default_state))
async def stat_call(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    workout_days_total = len(users[user_id])
    await state.clear()
    text = command_text.get('/stat')(workout_days_total)
    await call.message.edit_text(text, reply_markup=main_menu)


@router.callback_query(
        SimpleCalendarCallback.filter(), StateFilter(FSMWorkout.date)
        )
async def process_simple_calendar(
    callback_query: CallbackQuery,
    callback_data: dict, state: FSMContext
):
    selected, date = await SimpleCalendar().process_selection(
        callback_query,
        callback_data,
        user_id=callback_query.from_user.id
    )
    if selected:
        selected_date = f'{date.strftime("%-d/%-m/%Y")}'
        user_id = callback_query.from_user.id
        dates = get_workout_dates(user_id)
        text = callback_query.message.text
        if selected_date in dates and 'тренировок в этом месяце' in text:
            await state.clear()
            global selected_workout_date  # временный костыль пока нет БД
            selected_workout_date = selected_date
            workouts = get_workout_data(user_id, selected_date)
            text = f'Ваши тренировки за {selected_date}'
            for workout in workouts:
                for type, info in workout.items():
                    num = info['approaches_num']
                    comment = info['comment']
                    workout_name = workout_names[type]
                    text += (
                        f'\n{workout_name}:\n'
                        f'Количество подходов - {num}\n'
                        f'Комментарий: {comment}'
                        )
            markup = stat_keyboard()
        else:
            await state.update_data(date=selected_date)
            markup = workut_type_keyboard()
            text = 'Укажите тип тренировки:'
            await state.set_state(FSMWorkout.workout_type)
        await callback_query.message.edit_text(
            text,
            reply_markup=markup
        )
        await callback_query.answer()


@router.callback_query(StateFilter(FSMWorkout.workout_type))
async def workout_call(call: CallbackQuery, state: FSMContext):
    await state.update_data(workout_type=call.data)
    await call.message.edit_text(
        'Укажите количество подходов:',
        reply_markup=main_menu
        )
    await call.answer()
    await state.set_state(FSMWorkout.approaches_num)


@router.message(
        StateFilter(FSMWorkout.approaches_num),
        lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200
    )
async def approaches_num_callback(message: Message, state: FSMContext):
    await state.update_data(approaches_num=message.text)
    await delete_current_and_previous_message(message)
    await message.answer(
        'Укажите комментарий к тренировке:',
        reply_markup=main_menu
        )
    await state.set_state(FSMWorkout.comment)


@router.message(StateFilter(FSMWorkout.approaches_num))
async def wrong_approaches_num_callback(message: Message):
    await delete_current_and_previous_message(message)
    await message.answer('Укажите ЧИСЛО подходов!')


@router.message(StateFilter(FSMWorkout.comment))
async def comment_callback(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    workout_state = await state.get_data()
    user_id = message.from_user.id
    add_workout_data(workout_state, user_id)
    await delete_current_and_previous_message(message)
    await state.clear()
    pprint(users)
    await message.answer(
        'Тренировка добавлена!',
        reply_markup=another_workup()
    )
