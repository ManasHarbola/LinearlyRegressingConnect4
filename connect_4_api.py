import requests
import random
import json
import numpy as np

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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0"
    }
    users = {"id": {"std": 0.1, "avg": 1}}
    def __init__(self):
        users = {"id": {"std": 0.1, "avg": .89}}

    def generateNextMove(self, board, player):
        #generate random num based on players ability
        avg = self.users[player]["avg"]
        std = self.users[player]["std"]
        rand_num = np.random.normal(loc = avg, scale = std, size = 1)

        #get request 
        r = requests.get(url=self.GET_URL + board, headers=self.GET_HEADER)
        data = r.json()
        move_and_vals = {}#{"score": "moves"}
        scores = []

        for i in range(len(data["score"])):
            score = data["score"][i]
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
                
                return random.choice(move_and_vals[scores[i]])
        return random.choice(move_and_vals[scores[-1]])

    def testGetReq(self, board):
        r = requests.get(url=self.GET_URL + board, headers=self.GET_HEADER)
        data = r.json()
        print("text ", r.text)
        print(data["score"])
        #print(r.text)

    
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        print("hi")
        #blah

    #returns a normalized average optimality score and the std dev of optimal moves made by opponent
    def rateOppMoves(state):
        print("hi")
    #send move made by AI based on player simulation
    #def postNextMove(move):
        #blah

"""
print("hello")
api = Connect_4_API()

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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0"
}
r = requests.get("https://connect4.gamesolver.org/solve?pos=1", headers=GET_HEADER)
print(r.text)
api.testGetReq("444447123311")

"""
api = Connect_4_API()
s = "444447123311215666611673322237657452355775"
s = "44"
for i in range(len(s)):
    api.testGetReq(s[:i + 1])
    print(api.generateNextMove(s[:i + 1], "id"))



'''
for i in range(100):
    r = requests.get("https://connect4.gamesolver.org/solve?pos=1", headers=headers)
    print(r.text)
'''
#data = r.json()
#jsonStr = json.dumps(data)
#print(jsonStr)