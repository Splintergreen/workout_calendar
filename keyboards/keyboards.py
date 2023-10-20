from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import workout_names


def start_keyboard():
    button_0: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить тренировку(сегодня)',
        callback_data='add_workout_now'
    )
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить тренировку(выбор даты)',
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
            [button_0],
            [button_1],
            [button_2],
            [button_3],
            [button_4]
        ]
    )
    return keybord


def workout_type_keyboard():
    buttons = [
        InlineKeyboardButton(text=name, callback_data=workout)
        for workout, name in workout_names.items()
        ]
    buttons.append(InlineKeyboardButton(text='Назад', callback_data='start'))
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()


def stat_keyboard():
    stat_button_0: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить тренировку(сегодня)',
        callback_data='add_workout_now')
    stat_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить тренировку(выбор даты)',
        callback_data='add_workout')
    stat_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Редактировать',
        callback_data='edit_workout')
    stat_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Удалить',
        callback_data='delete_workout')
    stat_button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='Назад',
        callback_data='month_workouts')

    stat_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [stat_button_0],
            [stat_button_1],
            [stat_button_2],
            [stat_button_3],
            [stat_button_4],

        ]
    )
    return stat_keyboard


def another_workup():
    button_0: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить другую тренировку(сегодня)?',
        callback_data='add_workout_now')
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Добавить другую тренировку(выбор даты)?',
        callback_data='add_workout')
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Показать тренировки за месяц',
        callback_data='month_workouts')
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Основное меню',
        callback_data='start')
    another_workup_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_0],
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


def edit_workout_keyboard(workouts):
    buttons = [
        [InlineKeyboardButton(text=name, callback_data='call_edit_'+name)]
        for name in workouts
        ]
    buttons.append([InlineKeyboardButton(text='Назад', callback_data='start')])
    edit_workout_keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=buttons

    )
    return edit_workout_keyboard


def cardio_keyboard():
    button_0: InlineKeyboardButton = InlineKeyboardButton(
        text='Жиросжигание(FatBurn)',
        callback_data='cardio_fat_burn'
    )
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Кардио(Cardio)',
        callback_data='cardio_cardio'
    )
    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Подъем(Hill)',
        callback_data='cardio_hill'
    )
    button_3: InlineKeyboardButton = InlineKeyboardButton(
        text='Произвольная(Random)',
        callback_data='cardio_random'
    )
    button_4: InlineKeyboardButton = InlineKeyboardButton(
        text='На одной скорости',
        callback_data='cardio_one_speed'
    )
    button_5: InlineKeyboardButton = InlineKeyboardButton(
        text='Назад',
        callback_data='start'
    )
    keybord: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_0],
            [button_1],
            [button_2],
            [button_3],
            [button_4],
            [button_5]
        ]
    )
    return keybord
