from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    try:
        mars_data = mongo.db.mars_data.find_one()    
        return render_template("index.html", mars_data=mars_data)

    except:
        return """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
        integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
        <div class="container" style="background: lightgray;">
            <div class="row">
                <div class="col-12">
                    <div class="jumbotron text-center bg-dark text-light">
                        <h1 class="display-4">Mission to Mars</h1>
                        <br>
                        <a class="btn btn-primary btn-lg" href="/scrape" role="button">Scrape new data</a>
                    </div>
                </div>
            </div>
        """


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
