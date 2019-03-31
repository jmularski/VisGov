from flask import Flask, jsonify, request
from pymongo import MongoClient
import re
from json import dumps
#app = Flask(__name__)

client = MongoClient()
db = client.bundestag_analysis
data = db.data

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
    body = request[u'json']
    intent = body[u'intent'][u'displayName']
    parameters = body[u'parameters']
    if intent == 'date/party': return jsonify(getAttendanceAtDate(parameters[u'date'], parameters[u'party']))
    elif intent == 'date/total': return jsonify(getAttendanceAtDate(parameters[u'date']))
    elif intent == 'data/speaking_time': return jsonify(getSpeakingTime(parameters[u'date'], parameters[u'person']))
    elif intent == 'date/speaking_time_total': return jsonify(getSpeakingTime(parameters[u'person']))
    elif intent == 'party/topics': return jsonify(getMostDiscussedTopics(parameters[u'party']))

if __name__ == "__main__":
    app.run()
