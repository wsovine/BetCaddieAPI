import cfbd
import pytz
from django.conf import settings
from dateutil import parser
from datetime import datetime, timedelta


# CFBD
_cfbd_configuration = cfbd.Configuration()
_cfbd_configuration.api_key['Authorization'] = settings.CFBD_API_KEY
_cfbd_configuration.api_key_prefix['Authorization'] = 'Bearer'
_cfbd_client_configuration = cfbd.ApiClient(_cfbd_configuration)

cfbd_games_api = cfbd.GamesApi(_cfbd_client_configuration)
cfbd_bet_api = cfbd.BettingApi(_cfbd_client_configuration)


def cfbd_current_week() -> dict:
    today = datetime.utcnow().replace(tzinfo=pytz.utc)
    cur_year = today.year

    cal = cfbd_games_api.get_calendar(cur_year)
    while len(cal) <= 0:
        cur_year -= 1
        cal = cfbd_games_api.get_calendar(cur_year)

    cur_week = cfbd.Week()
    if today.date() > parser.isoparse(cal[-1].last_game_start).date():
        cur_week = cal[-1]
    elif today.date() < parser.isoparse(cal[0].first_game_start).date():
        cur_week = cal[0]
    else:
        for week in cal:
            start = parser.isoparse(week.first_game_start)
            end = parser.isoparse(week.last_game_start) + timedelta(hours=4)
            if start <= today <= end:
                cur_week = week
                break
        if not cur_week.week:
            for week in cal:
                end = parser.isoparse(week.last_game_start) + timedelta(hours=4)
                if today >= end:
                    cur_week = cal[cal.index(week) + 1]
    return cur_week.to_dict()


# FantasyData.io / SportsData.io
fd_base_url = 'https://api.sportsdata.io/api/cfb/odds/json/'
fd_headers = {
    'Ocp-Apim-Subscription-Key': settings.SD_CFB_API_KEY
}
