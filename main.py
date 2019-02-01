from flask import Flask, jsonify, request
from pymongo import MongoClient
import re
#app = Flask(__name__)

client = MongoClient()
db = client.bundestag_analysis
posts = db.posts

# Include regex


def getAttendanceAtDate(date, party=None):
    unique_speakers = []
    query = {"date": date}
    if party is not None:
        query['fraction_or_title'] = party
    speakers = posts.find(query, {"_id": 0, "name": 1})
    print(speakers)
    for speaker in speakers:
        if speaker['name'] not in unique_speakers:
            unique_speakers.append(speaker['name'])
    return unique_speakers


def getSpeakingTime(date="", person):
    time = 0.0
    query = {"name": person}
    if date is not None:
        query['date'] = date
    texts = posts.find(query, {"_id": 0, "text": 1})
    for text in texts:
        time += len(text['text']) / 130
    return time


def getMostDiscussedTopics(party):
    texts = posts.find({"party": party}, {"_id": 0, "text": 1})
    for text in texts

# @app.route('/', methods = ['POST'])


def dialogflow():
    body = request.json[u'queryResult']
    intent = body[u'intent'][u'displayName']
    parameters = body[u'parameters']
    if intent == 'date/party':
        result = getAttendanceAtDate(parameters[u'date'], parameters[u'party'])
        result = {
            'fulfillmentText': "That many: " + str(result)
        }
        return jsonify(result)
    elif intent == 'date/total':
        result = getAttendanceAtDate(parameters[u'date'])
        result = {
            'fulfillmentText': 'In total: ' + str(result[1])
        }
        return jsonify(result)
    elif intent == 'data/speaking_time':
        result = getSpeakingTime(parameters[u'date'], parameters[u'person'])
        result = {
            'fulfillmentText': 'Person ' + parameters[u'person'] + ' was speaking at this meeting for ' + str(result) + ' minutes.'
        }
        return jsonify(result)
    elif intent == 'date/speaking_time_total':
        result = getSpeakingTime(parameters[u'person'])
        result = {
            'fulfillmentText': json.dumps(result)
        }
        return jsonify(result)
    elif intent == 'party/topics':
        result = getMostDiscussedTopics(parameters[u'party'])
        result = {
            'fulfillmentText': json.dumps(result)
        }
        return jsonify(result)


if __name__ == "__main__":
    app.run()
