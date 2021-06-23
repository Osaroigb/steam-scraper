from flask import Flask, render_template, request, flash, url_for, redirect
import requests
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":

        return render_template("index.html")

    elif request.method == "POST":

        response = requests.get(url="http://127.0.0.1:9080/crawl.json?start_requests=true&spider_name=topsellers")
        response.raise_for_status()

        data = response.json()
        return render_template("index.html", games=data.get("items"))
    else:
        flash("The data couldn't be scraped!")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
