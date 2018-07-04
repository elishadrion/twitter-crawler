class Config(object):
	SECRET_KEY = "0"
	DEBUG = False # has to be "False" for production
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEMPLATES_AUTO_RELOAD = True
