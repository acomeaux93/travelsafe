from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_talisman import Talisman

app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

csp = {
 'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        '*.trusted.com',
        'https://www.google.com/jsapi',

    ],
 'script-src': [
        '\'self\'',
        'https://www.google.com/jsapi',
        'https://tools.cdc.gov/TemplatePackage/contrib/widgets/tp-widget-external-loader.js',
        'https://tools.cdc.gov/TemplatePackage/contrib/libs/jquery/1.12.4/jquery.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
        'https://www.gstatic.com/charts/loader.js',
        'https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.3/d3.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/topojson/1.6.9/topojson.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/datamaps/0.5.9/datamaps.all.min.js'

    ],
  'img-src': [
        '*',
        'https://www.google-analytics.com/',
  ],

  'style-src': [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
        'https://www.gstatic.com/charts/48.1/css/util/util.css',
        'stackpath.bootstrapcdn.com',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js',
        'https://www.gstatic.com/charts/48.1/css/core/tooltip.css',
        'https://www.google.com/uds/api/visualization/1.0/36558b280aac4fa99ed8215e60015cff/ui+en.css',
        'https://ajax.googleapis.com/ajax/static/modules/gviz/1.0/core/tooltip.css',
        'https://ajax.googleapis.com/ajax/static/modules/gviz/1.0/core/tooltip.css',
        'code.jquery.com',
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        '*.trusted.com',
        'https://www.google.com/jsapi'
  ],

  'frame-src':[
    '\'self\'',
    'https://www.cdc.gov/',
  ]


}


# login = LoginManager(app)
# login.login_view = 'login'

talisman = Talisman(app, content_security_policy=csp, content_security_policy_nonce_in=['script-src'])
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
