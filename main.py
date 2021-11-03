import datetime

from api.TeleBot.main import TeleBot, BaseHandler
from api.TeleBot.main import Answer

from api import ApiConfig
from api.ApiException import ApiException
from helpers import time_table_parser

exc_handler = ApiException().exc_handler


class TimeTable(BaseHandler):
    CurrWeek = 'CurrentWeek'
    NextWeek = 'NextWeek'
    Today = 'Today'
    Tomorrow = 'Tomorrow'

    @exc_handler
    def go(self, **params) -> Answer:
        cmd: str = params['cmd']
        date1 = datetime.date.today()
        weekday = date1.weekday()
        if self.CurrWeek in cmd:
            date1 = date1 + datetime.timedelta(days=-weekday) if weekday != 0 else date1
            delta = 6
        elif self.NextWeek in cmd:
            date1 = date1 + datetime.timedelta(days=7-weekday)
            delta = 6
        elif self.Tomorrow in cmd:
            date1 = date1 + datetime.timedelta(days=1)
            delta = 0
        else:
            delta = 0
        date2 = date1 + datetime.timedelta(days=delta)
        date2 = date2.strftime("%Y-%m-%d")
        date1 = date1.strftime("%Y-%m-%d")
        res = time_table_parser.get_timetable_by_date(date1=date1, date2=date2)
        return {'text': res}


class Hello(BaseHandler):

    @exc_handler
    def go(self, **params):
        return {'text': "Hello!"}


hello = Hello()
timetable = TimeTable()

routs = {
    'timetableToday': timetable,
    'timetableTomorrow': timetable,
    'timetableCurrentWeek': timetable,
    'timetableNextWeek': timetable,
    'hello': hello,
    'start': hello
}
bot = TeleBot(ApiConfig.Libraries['tele_bot']['token'], routs)
keyboard = [
    [
        ("На сегодня", '/timetableToday'),
        ("На завтра", '/timetableTomorrow'),
    ],
    [
        ("На неделю", '/timetableCurrentWeek'),
        ("На след. неделю", '/timetableNextWeek')
     ],
]
bot.set_default_button(keyboard)
bot.run()
