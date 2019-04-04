from flask import Flask, jsonify, request
from pymongo import MongoClient
import re
from json import dumps, loads
#app = Flask(__name__)

client = MongoClient()
db = client.bundestag_analysis
data = db.data

possibleDates = 

def routeIntents(intent, parameters){
    if intent == 'date/party': return getAttendanceAtDate(parameters[u'date'], parameters[u'party'])
    elif intent == 'date/total': return getAttendanceAtDate(parameters[u'date'])
    elif intent == 'data/speaking_time': return getSpeakingTime(parameters[u'date'], parameters[u'person'])
    elif intent == 'date/speaking_time_total': return getSpeakingTime(parameters[u'person'])
    elif intent == 'party/topics': return getMostDiscussedTopics(parameters[u'party'])
}


def getAttendanceAtDate(date, party=None):
    unique_speakers = []
    query = {"date": date}
    if party is not None:
        query['fraction_or_title'] = party
    speakers = data.find(query, {"_id": 0, "name": 1})
    for speaker in speakers:
        if speaker['name'] not in unique_speakers:
            unique_speakers.append(speaker['name'])
    result = { 'fulfillmentText': "That many: " + str(len(unique_speakers)) }
    return result


def getSpeakingTime(person, date=""):
    time = 0.0
    query = {"name": person}
    if date is not None:
        query['date'] = date
    texts = data.find(query, {"_id": 0, "text": 1})
    for text in texts:
        time += len(text['text']) / 130
    result = { 'fulfillmentText': 'Person ' + parameters[u'person'] + ' was speaking at this meeting for ' + str(time) + ' minutes.' }
    return result


def getMostDiscussedTopics(party):
    texts = data.find({"party": party}, {"_id": 0, "text": 1})
    result = { 'fulfillmentText': json.dumps(texts) }
    return result

@app.route('/', methods = ['POST'])
def dialogflow():
    body = json.loads(request.get_json())[u'queryResult']
    intent = body[u'intent'][u'displayName']
    parameters = body[u'parameters']
    return jsonify(routeIntents)


if __name__ == "__main__":
    app.run()
