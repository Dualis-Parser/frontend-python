import app
import secret_config

if (__name__ == "__main__"):
    server = app.server
    server.secret_key = secret_config.app_secret

    server.run(port=8888)
