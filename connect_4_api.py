import requests
import json

class Connect_4_API:
    GET_URL = "https://connect4.gamesolver.org/solve?pos=1"
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
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        print("hi")
        #blah

    #returns a normalized average optimality score and the std dev of optimal moves made by opponent
    def rateOppMoves(state):

    #send move made by AI based on player simulation
    #def postNextMove(move):
        #blah

'''
for i in range(100):
    r = requests.get("https://connect4.gamesolver.org/solve?pos=1", headers=headers)
    print(r.text)
'''
#data = r.json()
#jsonStr = json.dumps(data)
#print(jsonStr)