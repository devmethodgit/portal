from portal import create_app
from config import ConfigApp

app = create_app()

if __name__ == "__main__":
    app.run(debug=ConfigApp.Web.DEBUG, host=ConfigApp.Web.HOST, port=ConfigApp.Web.PORT)
