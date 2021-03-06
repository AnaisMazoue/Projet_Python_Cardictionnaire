# coding: utf-8
from warnings import warn

RESULTATS_PAR_PAGE = 5
SECRET_KEY = "JE SUIS UN SECRET !"
API_ROUTE = "/api"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

'''class _TEST:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False'''


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données
    SQLALCHEMY_DATABASE_URI = 'mysql://gazetteer_user:password@localhost/gazetteer'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}'''