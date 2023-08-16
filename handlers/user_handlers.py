from aiogram import Router
from aiogram.filters import StateFilter, Text, CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from workouts_calendar import SimpleCalendar
from workouts_calendar import SimpleCalendarCallback
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from database import User, session, Workout
from sqlalchemy import literal
from keyboards import (
    start_keyboard,
    workut_type_keyboard,
    stat_keyboard,
    another_workup,
    main_menu,
    deletion_confirm,
    back_to_month_workouts,
    edit_workout_keyboard
)
from lexicon import command_text, workout_names
from utils import delete_current_and_previous_message

router: Router = Router()


class FSMWorkout(StatesGroup):
    date = State()
    workout_type = State()
    approaches_num = State()
    repetitions_num = State()
    weight = State()
    comment = State()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    user_id_find = session.query(User).filter(User.id == message.from_user.id)
    user_exist_check = session.query(
        literal(True)
        ).filter(user_id_find.exists()).scalar()
    if user_exist_check is None:
        session.add(User(id=message.from_user.id))
        session.commit()
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


@router.callback_query(Text(text=['edit_workout']))
async def edit_workout_call(call: CallbackQuery):
    user_id = call.from_user.id
    user = session.query(User).filter(User.id.ilike(user_id)).first()
    selected_date = user.selected_date
    this_date_workouts = session.query(Workout).filter(Workout.date.ilike(selected_date)).all()
    workout_types = [w.workout_type for w in this_date_workouts]
    text = f'Тренировки за {selected_date}.\nВыберите какую редактировать:'
    await call.message.answer(text, reply_markup=edit_workout_keyboard(workout_types))


@router.callback_query(Text(startswith=['call_edit_']))
async def edit_selected_workout_call(call: CallbackQuery):
    user_id = call.from_user.id
    user = session.query(User).filter(User.id.ilike(user_id)).first()
    selected_date = user.selected_date
    workout_name = call.data[10:]
    print(workout_name)




@router.callback_query(Text(text=['delete_workout']))
async def delete_workout_call(call: CallbackQuery):
    await call.message.edit_text('Вы уверены?', reply_markup=deletion_confirm)


@router.callback_query(Text(text=['delete_yes']))
async def delete_yes_call(call: CallbackQuery):
    user_id = call.from_user.id
    user = session.query(User).filter(User.id.ilike(user_id)).first()
    selected_date = user.selected_date
    session.query(Workout).filter(
            Workout.user_id.ilike(user_id),
            Workout.date.ilike(selected_date)
        ).delete(synchronize_session='fetch')
    session.commit()
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
    text = command_text.get('/month_workouts')
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
    user = session.query(User).filter(User.id.ilike(user_id)).first()
    dates = set([workout.date for workout in user.workouts])
    workout_days_total = len(dates)
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
        user = session.query(User).filter(User.id.ilike(user_id)).first()
        user.selected_date = selected_date
        session.commit()
        dates = [workout.date for workout in user.workouts]
        text = callback_query.message.text
        if selected_date in dates and '🏆' in text:
            await state.clear()
            text = f'Ваши тренировки за {selected_date}'

            for workout in user.workouts:
                if workout.date == selected_date:
                    text += (
                            f'\n{workout.workout_type}:\n'
                            f'Количество подходов - {workout.approaches_num}\n'
                            f'{workout.repetitions_num} повторения, вес - {workout.weight}\n'
                            f'Комментарий: {workout.comment}'
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
    await state.update_data(workout_type=workout_names[call.data])
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
        'Укажите количество повторений:',
        reply_markup=main_menu
        )
    await state.set_state(FSMWorkout.repetitions_num)


@router.message(StateFilter(FSMWorkout.approaches_num))
async def wrong_approaches_num_callback(message: Message):
    await delete_current_and_previous_message(message)
    await message.answer('Укажите ЧИСЛО подходов!')


@router.message(
        StateFilter(FSMWorkout.repetitions_num),
        lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200
        )
async def repetitions_num_callback(message: Message, state: FSMContext):
    await state.update_data(repetitions_num=message.text)
    await delete_current_and_previous_message(message)
    await message.answer(
        'Укажите с каким весом выполнялись повторения:',
        reply_markup=main_menu
        )
    await state.set_state(FSMWorkout.weight)


@router.message(StateFilter(FSMWorkout.repetitions_num))
async def wrong_repetitions_num_callback(message: Message):
    await delete_current_and_previous_message(message)
    await message.answer('Укажите ЧИСЛО повторений!')


@router.message(
        StateFilter(FSMWorkout.weight),
        lambda x: x.text.replace('.', '', 1).isdigit() or x.text.replace(',', '', 1).isdigit() and 0 <= float(x.text.replace(',', '.', 1)) <= 200
        )
async def weight_num_callback(message: Message, state: FSMContext):
    await state.update_data(weight=message.text.replace(',', '.', 1))
    await delete_current_and_previous_message(message)
    await message.answer(
        'Укажите комментарий к тренировке:',
        reply_markup=main_menu
        )
    await state.set_state(FSMWorkout.comment)


@router.message(StateFilter(FSMWorkout.weight))
async def wrong_weight_num_callback(message: Message):
    await delete_current_and_previous_message(message)
    await message.answer('Укажите вес ЧИСЛОМ!')


@router.message(StateFilter(FSMWorkout.comment))
async def comment_callback(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    workout_state = await state.get_data()
    user_id = message.from_user.id
    session.add(
        Workout(
            user_id=user_id,
            workout_type=workout_state['workout_type'],
            approaches_num=workout_state['approaches_num'],
            repetitions_num=workout_state['repetitions_num'],
            weight=workout_state['weight'],
            comment=workout_state['comment'],
            date=workout_state['date']
        ))
    session.commit()

    await delete_current_and_previous_message(message)
    await state.clear()
    await message.answer(
        'Тренировка добавлена!',
        reply_markup=another_workup()
    )
