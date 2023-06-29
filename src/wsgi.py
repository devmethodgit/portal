from portal import create_app
from config import ConfigApp

Config = ConfigApp()
app = create_app()


if __name__ == "__main__":
    app.run(debug=Config.Web.DEBUG, host=Config.Web.HOST, port=Config.Web.PORT)
