import hashlib
import json

from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_mongoengine import MongoEngine
from datetime import timedelta
from files import getTeamUrls
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml

global allTeams

app = Flask(__name__)
app.secret_key = "secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)
app.config['MONGODB_SETTINGS'] = {
    'db': 'db_name',
    'host': 'host_ip',
    # 'username': 'username',
    # 'password': 'password',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    username = db.StringField()
    password = db.StringField()


class Team(db.Document):
    name = db.StringField()
    url = db.StringField()


def createUser(username, password):
    user = User(username=username, password=hashlib.sha256(
        password.encode("utf-8")).hexdigest())
    user.save()


def createTeam(name, url):
    team = Team(name=name, url=url)
    team.save()


@app.route("/", methods=["GET"])
def home():
    r = requests.get("url")
    teams = r.json()
    for i in range(1):
        print(str(teams[i]))
        getScadule(teams[i])
        return str(teams[0])
    # Tako se preveri password z tistim v bazi (username, password sta variables, ki jih moraw dobit)
    # user = User.objects(username=username, password=hashlib.sha256(password.encode("utf-8")).hexdigest()).first()


@app.route("/teams/", methods=["GET", "POST"])
def teams():
    if request.method == "GET":
        teamName = str(request.args.get("team"))
        teamName = teamName.lower()
        team = Team.objects(name=teamName).first()
        team.url = team.url.replace("\n", "")
        return jsonify({"url": team.url})


def getScadule(item):
    url = str(item[1])
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "html.parser")
    test_table = soup.find('table', class_="stats_table")
    test = pd.read_html(str(test_table))[0]
    del test["G"]
    del test["Unnamed: 3"]
    del test["Unnamed: 4"]
    del test["Unnamed: 5"]
    del test["Unnamed: 7"]
    del test["Unnamed: 8"]
    del test["Tm"]
    del test["Opp"]
    del test["W"]
    del test["L"]
    del test["Streak"]
    del test["Notes"]
    test2 = test.drop([85])
    nekaj = pd.DataFrame(test2)
    parse = nekaj.to_json()
    result = json.loads(parse)
    #print(json.dumps(result, indent=4))
    print(test2)
    requests.post("http://142.93.141.65/update?team=" + str(item[0]), json=json.dumps(result))
    #return pd.DataFrame.to_json(test)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
