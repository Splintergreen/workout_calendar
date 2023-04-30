from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import workout_names


def start_keyboard():
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить тренировку',
        callback_data='add_workout'
    )
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Тренировки за месяц',
        callback_data='month_workouts'
    )
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Статистика за все время',
        callback_data='stat'
    )
    button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='About',
        callback_data='about'
    )
    keybord: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_1],
            [button_2],
            [button_3],
            [button_4]
        ]
    )
    return keybord


def workut_type_keyboard():
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=workout)]
        for workout, name in workout_names.items()
        ]
    workut_type_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=buttons

    )
    return workut_type_keyboard


def stat_keyboard():
    stat_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Удалить',
        callback_data='delete_workout')
    stat_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать',
        callback_data='edit_workout')
    stat_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Назад',
        callback_data='month_workouts')
    stat_button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='Закрыть',
        callback_data='end_workout')

    stat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [stat_button_1],
            [stat_button_2],
            [stat_button_3],
            [stat_button_4],

        ]
    )
    return stat_keyboard


def another_workup():
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить другую тренировку?',
        callback_data='add_workout')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Показать тренировки за месяц',
        callback_data='month_workouts')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Завершить',
        callback_data='end_workout')
    another_workup_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_1],
            [button_2],
            [button_3],
        ]
    )
    return another_workup_keyboard


main_menu: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='start')]
    ]
)

deletion_confirm: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='delete_yes')],
        [InlineKeyboardButton(text='Нет', callback_data='delete_no')]
    ]
)

back_to_month_workouts: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='month_workouts')]
    ]
)