import calendar
from datetime import datetime, timedelta
import emoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from calendar_types import (
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
        workout_days = []
        for d in users[user_id]:
            date = ''.join(list(d.keys()))
            workout_days.append(int(date[0:date.find('/')]))
        # print(workout_days)
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
                if day in workout_days:
                    calendar_row.append(InlineKeyboardButton(
                        text='💪🏻', #emoji.emojize(':flexed_biceps_light_skin_tone:'),
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
                    text=" ",
                    callback_data=ignore_callback.pack()),
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
            data: [CallbackData, SimpleCalendarCallback]
            ) -> tuple:
        return_data = (False, None)
        temp_date = datetime(int(data.year), int(data.month), 1)
        # processing empty buttons, answering with no action
        if data.act == SimpleCalendarAction.IGNORE:
            await query.answer(cache_time=60)
        # user picked a day button, return date
        if data.act == SimpleCalendarAction.DAY:
            await query.message.delete_reply_markup()
            return_data = True, datetime(
                int(data.year),
                int(data.month),
                data.day
                )
        # user navigates to previous year, editing message with new calendar
        if data.act == SimpleCalendarAction.PREV_YEAR:
            prev_date = datetime(int(data.year) - 1, int(data.month), 1)
            markup = await self.start_calendar(
                int(prev_date.year),
                int(prev_date.month),
                user_id=682315225
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        # user navigates to next year, editing message with new calendar
        if data.act == SimpleCalendarAction.NEXT_YEAR:
            next_date = datetime(int(data.year) + 1, int(data.month), 1)
            markup = await self.start_calendar(
                int(next_date.year),
                int(next_date.month)
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        # user navigates to previous month, editing message with new calendar
        if data.act == SimpleCalendarAction.PREV_MONTH:
            prev_date = temp_date - timedelta(days=1)
            markup = await self.start_calendar(
                int(prev_date.year),
                int(prev_date.month)
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        # user navigates to next month, editing message with new calendar
        if data.act == SimpleCalendarAction.NEXT_MONTH:
            next_date = temp_date + timedelta(days=31)
            markup = await self.start_calendar(
                int(next_date.year),
                int(next_date.month)
                )
            await query.message.edit_reply_markup(reply_markup=markup)
        # at some point user clicks DAY button, returning date
        return return_data
