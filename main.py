import json
import random
from numpy.lib.function_base import average
import requests
import numpy as np

from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "PLZWORK"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Arenas(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    coor_x = db.Column(db.Float())
    coor_y = db.Column(db.Float())
    leaderBoards = db.relationship('LeaderBoards', backref='author', lazy=True)
    #children = db.relationship("Child")

    def __init__(self, id, coor_x, coor_y):
        self.id = id
        self.coor_x = coor_x
        self.coor_y = coor_y
    
    """
    def __init__(self, coor_x, coor_y):
        self.coor_x = coor_x
        self.coor_y = coor_y
    """

class LeaderBoards(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    users = db.relationship('Users', backref='author', lazy=True)
    arena_id = db.Column(db.Integer, db.ForeignKey(Arenas.id), nullable=False)
    #Column('person_id', Integer, ForeignKey(tbl_person.c.id), primary_key=True)

    def __init__(self, arena_id):
        self.arena_id = arena_id


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    average = db.Column(db.Float())
    standardDev = db.Column(db.Float())
    leaderboards_id = db.Column(db.Integer, db.ForeignKey(LeaderBoards.id), nullable=False)
    
    """
    def __init__(self, id, username, average, standardDev, leaderboards_id):
        self.username = username
        self.average = average
        self.standardDev = standardDev
        self.leaderboards_id = leaderboards_id
    """
    
    def __init__(self, username, average, standardDev, leaderboards_id):
        self.username = username
        self.average = average
        self.standardDev = standardDev
        self.leaderboards_id = leaderboards_id


    def __repr__(self):
        return f"users('{self.username}') avg({self.average}) std({self.standardDev})"



#app = Flask(__name__)


@app.route("/initialize")
def initializeDatabase():
    
    global_arena = Arenas(0, 0, 0)
    initial_leaderBoard = LeaderBoards(global_arena.id)
    perfect_player = Users("perfect_player", 1.0, 0.1, initial_leaderBoard.id)
    
    #perfect_player = Users(username="perfect_player", average=1, standardDev=0.1, leaderboards_id=initial_leaderBoard.id)
    
    db.session.add(global_arena)
    db.session.commit()
    db.session.add(initial_leaderBoard)
    db.session.commit()
    db.session.add(perfect_player)
    db.session.commit()





class Connect_4_API:
    GET_URL = "https://connect4.gamesolver.org/solve?pos="
    GET_HEADER = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "connect4.gamesolver.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"

    }
    users = {"id": {"std": 0.1, "avg": 1}}
    database = {}
    #{arena: {location: (x, y), users: [(id, avg, std)]}}


    @app.route("/generateNextMove/<jsonStr>")
    def generateNextMove(jsonStr):
        obj = json.loads(jsonStr)
        board = obj["board"]
        player = obj["player"]
        #generate random num based on players ability
        avg = Connect_4_API.users[player]["avg"]
        std = Connect_4_API.users[player]["std"]
        rand_num = np.random.normal(loc = avg, scale = std, size = 1)

        #get request 
        r = requests.get(url=Connect_4_API.GET_URL + board, headers=Connect_4_API.GET_HEADER)
        print(r)
        data = r.json()
        move_and_vals = {}#{"score": "moves"}
        scores = []

        for i in range(1, len(data["score"]) + 1):
            score = data["score"][i - 1]
            if score == 100:
                continue
            if score not in move_and_vals.keys():
                scores.append(score)
                move_and_vals[score] = []
            move_and_vals[score].append(i)
        scores.sort(reverse=False)
        sum_of_score = 0
        for i in range(len(scores)):
            sum_of_score += (1 / len(scores))
            if sum_of_score > rand_num:
                
                return str(random.choice(move_and_vals[scores[i]]))
        return str(random.choice(move_and_vals[scores[-1]]))

    
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        pass

    """
    #usrID
    @app.route("/createNewUser/<usrID>")
    def createNewUser(usrID):
        try:
            global_leaderBoard = LeaderBoards.query.filter_by(arena_id = 0).first()
            for user in LeaderBoards.users:
                user.id
                user.average
                user.standardDev

            new_user = Users(username=usrID, average=0, standardDev=0, leaderboards_id=global_leaderBoard.id)
            
            db.session.add(new_user)
            db.session.commit()

            found_user = Users.query.filter_by(username = usrID).first()
            print(found_user)
            
            return "SUCCESS"
        except:
            return "FAILURE"
    """

    @app.route("/addArena/<arena_name>/<locationX>/<locationY>")
    def addArena(arena_name, locationX, locationY):
        Connect_4_API.database[arena_name] = {"location": (locationX, locationY), "users": []}
        print(Connect_4_API.database)
        return "works"
    
    @app.route("/addUserToArena/<user>/<arena>")
    def addUserToArena(user, arena):
        if arena not in Connect_4_API.database.keys():
            return
        
        avg = Connect_4_API.users[user]["avg"]
        std = Connect_4_API.users[user]["std"]

        Connect_4_API.database[arena]["users"].append((user, avg, std))
        print(Connect_4_API.database)
        return "works"

    
    @app.route("/rateOppMoves/<state>/<userID>")

    #returns tuple of normalized average optimality score and the std dev of optimal moves made by opponent
    def rateOppMoves(state, userID):
        moveScores = []
        for i in range(0, len(state), 2):
            r = requests.get(Connect_4_API.GET_URL + state[:i], headers=Connect_4_API.GET_HEADER)
            data = r.json()
            colScores = data['score']
            scoreFreq = {}
            numChoices = 0
            for score in colScores:
                if score != 100:
                    scoreFreq[score] = scoreFreq.get(score, 0) + 1
                    numChoices += 1

            scores = [(k, scoreFreq[k]) for k in reversed(scoreFreq.keys())]
            moveScore = colScores[int(state[i]) - 1]
            movesBetterThan = numChoices

            for i in range(len(scores)):
                if scores[i][0] > moveScore:
                    movesBetterThan -= scores[i][1]
                else:
                    moveScores.append(movesBetterThan / numChoices)
        
        Connect_4_API.users[userID] = {"avg": np.mean(moveScores), "std": np.std(moveScores)}
        print(Connect_4_API.users)
        return "works"
      

    def getArenaLeaderboard(arenaID):
        #{arena: {location: (x, y), users: [(id, avg, std)]}}
        users = database[arenaID]['users'].copy()
        users.sort(key=lambda u : (-u[1], u[2]))
        return [user[0] for user in users]

db.create_all()

if __name__ == '__main__':
    obj = {"board": "1121", "player": "id"}
    jsonStr = json.dumps(obj)
    print(jsonStr)
    app.run(host='0.0.0.0', port=80)

