from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_seeder import FlaskSeeder

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
seeds = FlaskSeeder(app)
seeds.init_app(app, db)

from app_py.scrape.crawl.spiders.post_scrape import PostSpider
# from app_py.crawling.crawling.spiders.post_scrape import PostSpider
from app_py.model import KategoriModel, KriteriaModel, AdminModel, LaptopModel
from app_py.routes import KategoriRoutes, KriteriaRoutes, AdminRoutes, CrawlerRoutes
# from app_py.model import *
# from app_py.routes import *
from app_py.seeds import seeds