from app.configs import Config

app = Config().init_app()
database = Config().database

app.secret_key = 'iniadalahkoderahasiaaplikasiku'

from modules import routes