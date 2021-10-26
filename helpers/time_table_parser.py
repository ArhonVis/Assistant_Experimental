import requests
import datetime
import re
from bs4 import BeautifulSoup
from Assistant_Experimental.api import ApiConfig


def get_timetable_by_date(date1: str = "", date2: str = "", group: str = ""):
    date1 = date1 if date1 else datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d")
    date2 = date2 if date2 else date1
    config = ApiConfig.Helpers['parser']
    url = config['url'] % {
        'year': config['year_default'],
        'semester': config['semester_default'],
        'group': group if group else config.get("group_default"),
        'date1': date1,
        'date2': date2
    }
    r = requests.get(url)
    html = r.text.encode('utf8')
    soup = BeautifulSoup(html)
    res = soup.find('tbody')
    if res:
        data = {}
        rows = res.find_all('tr')
        date = ''
        for row in rows:
            find_date = row.find('td', {'class': 'day'})
            if find_date:
                date, summary = tuple(find_date.text.split(', '))
                data[date] = [summary]
            else:
                data[date] += list(map(lambda x: x.text, row.find_all('td')))
        data = {day: '\n'.join(values) for day, values in data.items()}
        res = ""
        for day, lessons in data.items():
            if res != "":
                res += "\n\n"
            res += day + "\n" + lessons
        return res
    else:
        return "Not found"
