import cfbd
from django.conf import settings

_cfbd_configuration = cfbd.Configuration()
_cfbd_configuration.api_key['Authorization'] = settings.CFBD_API_KEY
_cfbd_configuration.api_key_prefix['Authorization'] = 'Bearer'
_cfbd_client_configuration = cfbd.ApiClient(_cfbd_configuration)

cfbd_games_api = cfbd.GamesApi(_cfbd_client_configuration)
cfbd_bet_api = cfbd.BettingApi(_cfbd_client_configuration)
