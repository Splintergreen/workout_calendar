import calendar
from datetime import datetime, timedelta
from typing import Union
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from workouts_calendar.calendar_types import (
    SimpleCalendarCallback,
    SimpleCalendarAction,
    WEEKDAYS
    )
from database import users


class SimpleCalendar:
    @staticmethod
    async def start_calendar(
            user_id: int,
            year: int = datetime.now().year,
            month: int = datetime.now().month
    ) -> InlineKeyboardMarkup:
        workout_dates = []
        for d in users[user_id]:
            date = ''.join(list(d.keys()))
            workout_dates.append(date)
        markup = []
        ignore_callback = SimpleCalendarCallback(
            act=SimpleCalendarAction.IGNORE,
            year=year,
            month=month,
            day=0)

        markup.append(
            [
                InlineKeyboardButton(
                    text="<<",
                    callback_data=SimpleCalendarCallback(
                        act=SimpleCalendarAction.PREV_YEAR,
                        year=year, month=month,
                        day=1).pack()
                ),
                InlineKeyboardButton(
                    text=f'{calendar.month_name[month]} {str(year)}',
                    callback_data=ignore_callback.pack()
                ),
                InlineKeyboardButton(
                    text=">>",
                    callback_data=SimpleCalendarCallback(
                        act=SimpleCalendarAction.NEXT_YEAR,
                        year=year,
                        month=month,
                        day=1).pack()
                )
            ]
        )

        markup.append(
            [InlineKeyboardButton(
                text=day,
                callback_data=ignore_callback.pack()
                ) for day in WEEKDAYS]
        )

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            calendar_row = []
            for day in week:
                if day == 0:
                    calendar_row.append(InlineKeyboardButton(
                        text=" ",
                        callback_data=ignore_callback.pack())
                        )
                    continue
                current_date = f'{day}/{month}/{year}'
                if current_date in workout_dates:
                    calendar_row.append(InlineKeyboardButton(
                        text='💪🏻',
                        callback_data=SimpleCalendarCallback(
                            act=SimpleCalendarAction.DAY,
                            year=year,
                            month=month,
                            day=day).pack()))
                    continue
                calendar_row.append(InlineKeyboardButton(
                    text=str(day),
                    callback_data=SimpleCalendarCallback(
                        act=SimpleCalendarAction.DAY,
                        year=year,
                        month=month,
                        day=day).pack()
                ))
            markup.append(calendar_row)

        markup.append(
            [
                InlineKeyboardButton(
                    text="<",
                    callback_data=SimpleCalendarCallback(
                        act=SimpleCalendarAction.PREV_MONTH,
                        year=year,
                        month=month,
                        day=day).pack()
                ),
                InlineKeyboardButton(
                    text="Назад",
                    callback_data='start'),
                InlineKeyboardButton(
                    text=">",
                    callback_data=SimpleCalendarCallback(
                        act=SimpleCalendarAction.NEXT_MONTH,
                        year=year,
                        month=month,
                        day=day).pack()
                )
            ]
        )

        inline_kb = InlineKeyboardMarkup(inline_keyboard=markup, row_width=7)
        return inline_kb

    async def process_selection(
            self,
            query: CallbackQuery,
            data: Union[CallbackData, SimpleCalendarCallback],
            user_id: int
            ) -> tuple:
        return_data = (False, None)
        temp_date = datetime(int(data.year), int(data.month), 1)
        if data.act == SimpleCalendarAction.IGNORE:
            await query.answer(cache_time=60)
        if data.act == SimpleCalendarAction.DAY:
            await query.message.delete_reply_markup()
            return_data = True, datetime(
                int(data.year),
                int(data.month),
                data.day
                )
        if data.act == SimpleCalendarAction.PREV_YEAR:
            prev_date = datetime(int(data.year) - 1, int(data.month), 1)
            markup = await self.start_calendar(
                user_id=user_id,
                year=int(prev_date.year),
                month=int(prev_date.month),
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        if data.act == SimpleCalendarAction.NEXT_YEAR:
            next_date = datetime(int(data.year) + 1, int(data.month), 1)
            markup = await self.start_calendar(
                user_id=user_id,
                year=int(next_date.year),
                month=int(next_date.month),
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        if data.act == SimpleCalendarAction.PREV_MONTH:
            prev_date = temp_date - timedelta(days=1)
            markup = await self.start_calendar(
                user_id=user_id,
                year=int(prev_date.year),
                month=int(prev_date.month),
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        if data.act == SimpleCalendarAction.NEXT_MONTH:
            next_date = temp_date + timedelta(days=31)
            markup = await self.start_calendar(
                user_id=user_id,
                year=int(next_date.year),
                month=int(next_date.month),
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        return return_data
