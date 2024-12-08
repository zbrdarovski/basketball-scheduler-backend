
from flask import Flask, request, jsonify
import json
from datetime import time, date, datetime
import requests

app = Flask(__name__)


def get_matches():

    matches = []
    URL = "url"
    r = requests.get(url=URL)
    data = r.json()

    for d in data:
        try:
            arr = d[3].split(':')
            hour = arr[0]
            minute = arr[1][:-1]

            hour_true = int(hour) + 18
            if hour_true >= 24:
                hour_true -= 24

            hour = str(hour_true)
            if len(hour) == 1:
                hour = "0" + hour

            time = hour + "::" + minute + "::00"

            matches.append({"team1": d[0], "team2": d[1], "time": time})
        except:
            pass

    print(matches)
    return matches


@app.route("/nba_api", methods=["GET"])
def process_request():

    mathes_result = []

    teams = []
    players = []
    times = []

    if request.args.get('teams') is not None:
        teams_num = len(request.args.get('teams').split(','))
        for i in range(0, teams_num):
            teams.append(request.args.get('teams').split(',')[i])
        print(teams)

    if request.args.get('players') is not None:
        players_num = len(request.args.get('players').split(','))
        for i in range(0, players_num):
            players.append(request.args.get('players').split(',')[i])
        print(players)

    if request.args.get('times') is not None:
        times_num = len(request.args.get('times').split(','))
        for i in range(0, times_num):
            time_str = request.args.get('times').split(',')[i]

            times.append(time_str)
        print(times)

    matches = get_matches()

    for i in range(0, len(matches)):
        if (matches[i]["time"] in times) and (len(teams) == 0):
            mathes_result.append(matches[i])
        elif ((matches[i]["team1"] in teams) or (matches[i]["team2"] in teams)) and (len(times) == 0):
            mathes_result.append(matches[i])
        elif ((matches[i]["team1"] in teams) or (matches[i]["team2"] in teams)) and (matches[i]["time"] in times):
            mathes_result.append(matches[i])

    return jsonify({'matches': mathes_result})
    #return jsonify({'teams': teams}, {'players': players}, {'times': times}, {'matches': mathes_result})


if __name__ == "__main__":
    app.run(port=5000)
