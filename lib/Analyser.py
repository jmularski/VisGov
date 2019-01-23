# -*- coding: utf-8 -*-

import numpy as np
from CommentAnalyser import CommentAnalyser
from FileHandler import FileHandler
import pandas as pd
from pymongo import MongoClient
import re

CommentAnalyser = CommentAnalyser()
class Analyser:
    def __init__(self, file, date):
        client = MongoClient()
        db = client.bundestag_analysis
        posts = db.posts
        self.data_analysis(file, date, posts)

    def return_speaker_data(self, name):
        if name is not None and len(name.getchildren()) != 0:
            name = name[0][0]
            first_name = name.find('vorname').text if name.find('vorname') is not None else ''
            last_name = name.find('nachname').text if name.find('vorname') is not None else ''
            fraction_or_title = name.find('fraktion').text if name.find('fraktion') is not None else name.find('rolle')[0].text
            return {'name': first_name + " " +last_name, 'fraction_or_title': fraction_or_title}
        else:
            text = re.sub("Präsident|Dr.|Vizepräsidentin|Vizepräsident|:", "", name.text)
            for letter in text:
              if text.startswith(' '): text = text[1:]
            return {'name': text, 'fraction_or_title': 'Vizeprasidentin/Viceprasident'}
    
    #It's broken
    #Karin Maag, 28.11.2018 - broken at last entry
    def analyse_speech(self, date, topic, speech, db):
        topic = topic.replace('\xa0', " ")
        basic_current_speaker = {'date': date, 'topic': topic}
        current_speaker = basic_current_speaker
        for children in speech.getchildren():
            if children is None:
                continue
            #print(children)
            if children.tag == 'name' or (children.tag == 'p' and children.attrib['klasse'] == 'redner'):
                print(current_speaker.setdefault('name', ''), self.return_speaker_data(children))
                current_speaker.update(self.return_speaker_data(children))
                if current_speaker != {} and current_speaker != {'date': date, 'topic': topic.replace('\xa0', " ")} and len(current_speaker) > 5:
                    db.insert_one(current_speaker)
                    del current_speaker['_id']
                    current_speaker = basic_current_speaker
            elif children.tag == 'p':
                current_speaker['text'] = current_speaker.setdefault('text', '') + children.text.replace('\xa0', " ")
            elif children.tag == 'kommentar':
                data = CommentAnalyser.parse_comment(children.text)
                if data is None: continue
                else:
                    current_speaker['comments'] = data
                    db.insert_one(current_speaker)
                    del current_speaker['_id'] 
                    del current_speaker['text']
                    del current_speaker['comments']

    def data_analysis(self, file, date, db):
        global_date = date
        all_speeches = []
        topics = file.findall('.//tagesordnungspunkt')
        for topic in topics:
            topic_name = topic.findall(".//p[@klasse='T_fett']")
            topic_name = " - ".join([topic.text for topic in topic_name])
            #topic_name = topic_name[topic_name != np.array(None)]
            speeches = topic.findall(".//rede")
            print(topic_name, len(speeches))
            for speech in speeches:
                self.analyse_speech(date, topic_name, speech, db)
