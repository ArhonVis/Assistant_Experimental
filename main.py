import datetime

from api.TeleBot.main import TeleBot, BaseHandler
from api.TeleBot.main import Answer

from api import ApiConfig
from helpers import time_table_parser


class TimeTable(BaseHandler):
    Week = 'Week'
    Today = 'Today'
    Tomorrow = 'Tomorrow'

    def go(self, **params) -> Answer:
        cmd: str = params['cmd']
        date1 = datetime.date.today()
        weekday = date1.weekday()
        date1 = date1 + datetime.timedelta(days=1) if weekday == 6 else date1
        if self.Week in cmd:
            date1 = date1 + datetime.timedelta(days=-weekday) if weekday != 0 else date1
            delta = 6
        elif self.Tomorrow in cmd:
            delta = 1
        else:
            delta = 0
        date2 = date1 + datetime.timedelta(days=delta)
        res = time_table_parser.get_timetable_by_date(date1=date1, date2=date2)
        return {'text': res}


class Hello(BaseHandler):
    def go(self, **params):
        return {'text': "Hello!"}


hello = Hello()
timetable = TimeTable()

routs = {
    'timetableToday': timetable,
    'timetableTomorrow': timetable,
    'timetableWeek': timetable,
    'hello': hello
}
bot = TeleBot(ApiConfig.Libraries['tele_bot']['token'], routs)
keyboard = [
    [
        ("На сегодня", '/timetableToday'),
        ("На завтра", '/timetableTomorrow'),
    ],
    [("На неделю", '/timetableWeek')],
]
bot.set_default_button(keyboard)
bot.run()
