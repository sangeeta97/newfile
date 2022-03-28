from flask import Flask
from ionos.config import Config
from flask_bootstrap import Bootstrap
import os


basedir = os.path.abspath(os.path.dirname(__file__))

print(basedir)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from ionos.dna.views import dna
    from ionos.blog.views import blog
    from ionos.main.views import main
    app.register_blueprint(dna)
    app.register_blueprint(blog)
    app.register_blueprint(main)
    bootstrap = Bootstrap(app)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
    app.config["uploads"] = os.path.join(basedir, "uploads")
    app.config["output"] = os.path.join(basedir, "output")
    app.config["static"] = os.path.join(basedir, "static")
    app.config["images"] = os.path.join(basedir, "static", "images")
    app.config["templates"] = os.path.join(basedir, "templates")

    return app
