from flask import Flask, render_template

from app import config
from app.core import core


def start():
	app = Flask(__name__)
	app.config.from_object(config.Config)
	register_blueprints(app)
	return app

def register_blueprints(app):
	app.register_blueprint(core)
