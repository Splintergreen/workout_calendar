def start_command(name: str) -> str:
    return f'Привет {name}, это бот-календарь тренировок!'


def month_workouts_command(count: int) -> str:
    return (
        f'У вас {count} тренировок в этом месяце.\n'
        'Выберите 💪🏻 для просмотра тренировок за день.\n'
        'Или выберите другую дату чтоб добавить тренировку.'
        )


def stat_command(days: str) -> str:
    return f'Ваши тренировки за все время: {days}'


command_text = {
    '/start': start_command,
    '/add_workout': 'Выберите дату  добавляемой тренировки:',
    '/end_workout': 'Жду вас после следующего посещения фитнеса!',
    '/month_workouts': month_workouts_command,
    '/about': ('Бот для ведения статистики тренировок.\n'
               'Успешного вам тренировочного прогресса!'),
    '/stat': stat_command,
}
