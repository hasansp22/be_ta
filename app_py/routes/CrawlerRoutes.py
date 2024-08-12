from app_py import app
from app_py.controller.CrawlerController import *

@app.route("/scrape")
def scrape():
    simpan_crawler()
    return jsonify(output_data)

@app.route("/display_option")
def display():
    return display_option()
