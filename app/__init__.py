from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman

app = Flask(__name__)
app.config.from_object(Config)
Talisman(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


# login = LoginManager(app)
# login.login_view = 'login'

bootstrap = Bootstrap(app)

#These are at the bottom because of the chance for circular dependancies. What are those?

#THIS LINE COMMENTED OUT TEMPORARILY BECAUSE THERE ARE NO MODELS YET
from app import routes, models

    # with app.app_context():
    #     from app import routes
    #      # Import Dash application
    #     from app.PlotlyDash.regents_score_heatmap import create_dashboard
    #     app = create_dashboard(app)
    #
    #     return app
