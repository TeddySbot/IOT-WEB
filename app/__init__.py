from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change_me"  # clé pour sessions / flash

    from .routes import main
    app.register_blueprint(main)

    return app
