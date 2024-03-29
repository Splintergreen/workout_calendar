def start_command(name: str) -> str:
    return f'Привет {name}, это бот-календарь тренировок!'


def stat_command(days: str) -> str:
    return f'Дней тренировок за все время: {days}'


command_text = {
    '/start': start_command,
    '/add_workout': 'Выберите дату  добавляемой тренировки:',
    '/end_workout': 'Жду вас после следующего посещения фитнеса!',
    '/month_workouts': (
        'Выберите 🏆 для просмотра тренировок за день.\n'
        'Или выберите другую дату чтоб добавить тренировку.'
        ),
    '/about': (
        'Бот для ведения статистики тренировок.\n'
        'Успешного вам тренировочного прогресса!'
        ),
    '/stat': stat_command,
}

workout_names = {
    'chest': 'Грудь',
    'biceps': 'Бицепсы',
    'back': 'Спина',
    'latissimus': 'Широчайшие',
    'triceps': 'Трицепсы',
    'forearm': 'Предплечья',
    'trapezius': 'Трапеция',
    'shoulders': 'Плечи',
    'abs': 'Пресс',
    'hip_flexers': 'Бедра',
    'calf_muscles': 'Икры',
    'gluteal': 'Ягодицы',
    'warmup': 'Разминка',
    'cardio': 'Кардио',
    'other': 'Другое',
}

cardio_names = {
    'cardio_fat_burn': 'Жиросжигание(FatBurn)',
    'cardio_cardio': 'Кардио(Cardio)',
    'cardio_hill': 'Подъем(Hill)',
    'cardio_random': 'Произвольная(Random)',
    'cardio_one_speed': 'На одной скорости',
}
