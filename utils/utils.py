# from aiogram.types import Message, CallbackQuery
# from database import users
from aiogram import Bot
from config import load_config, Config

config: Config = load_config()
bot: Bot = Bot(token=config.bot_token.token)


# def get_workout_data(user_id, date):
#     date_index = get_workout_dates(user_id).index(date)
#     workout_this_day = users[user_id][date_index][date]
#     return workout_this_day


# def add_workout_data(state, user_id):
#     workout = state.pop('workout_type', None)
#     workout_data = {workout: state}
#     new_date = state.pop('date', None)
#     training_dates = get_workout_dates(user_id)
#     if new_date in training_dates:
#         date_index = training_dates.index(new_date)
#         users[user_id][date_index][new_date].append(workout_data)
#     else:
#         users.setdefault(user_id, [])
#         users[user_id].append({new_date: [workout_data]})


# def get_workout_dates(user_id):
#     if users.get(user_id) is None:
#         return ''
#     return [''.join(list(d.keys())) for d in users[user_id]]


# def msg_or_call_check(msg_or_call):
#     if isinstance(msg_or_call, CallbackQuery):
#         message = msg_or_call.message
#         user_id = msg_or_call.from_user.id
#     elif isinstance(msg_or_call, Message):
#         message = msg_or_call
#         user_id = message.from_user.id
#     if user_id not in users:
#         users[user_id] = []
#     return message, user_id


async def delete_current_and_previous_message(message):
    try:
        await message.delete()
        await bot.delete_message(
            chat_id=message.chat.id, message_id=message.message_id-1
            )
    except Exception as ex:
        print(ex)
        pass
