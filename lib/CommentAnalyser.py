# -*- coding: utf-8 -*-

import re


class CommentAnalyser:

    party_list = ["FDP", "CDU", "SPD", "AfD", "LINKE", "B", "CSU", "GRÜNE"]

    def __init__(self):
        pass

    def get_person_data(self, person):
        if person[0] == " ":
            person = person[1:]

        person = person.replace('Abg. ', '')

        # check if is member of party
        if "[" in person:
            name_party_split = person.split("[")
            party = name_party_split[len(name_party_split) - 1][:-1]

        # if not, then assume that it's member of court
        if "[" not in person:
            name_party_split = person.split(",")
            party = name_party_split[len(name_party_split) - 1][1:]

        # delete space at beginning
        # including len instead of 1, due to bundestag format
        name = name_party_split[0][:-1]
        return {"name": name, "party": party}

    def parse_reaction_comments(self, comment_text):
        parties = []
        people = []
        for word in re.split("der|des|dem|beim", comment_text):
            if word[0] == ' ':
                word = word[1:]
            # getting parties
            text_spaces = word.split(" ")
            if text_spaces[0] != "Beifall" and text_spaces[0] != "Heiterkeit" and text_spaces[0] != "Lachen" and "[" not in word:
                parties.append(text_spaces[0])
            # getting people
            elif text_spaces[0] != "Beifall" and text_spaces[0] != "Heiterkeit" and text_spaces[0] != "Lachen":
                people.append(word)
        parties = [party.replace("\xa0", "") for party in parties]
        people = [person.replace("\xa0", "") for person in people]

        # workaround for BUNDNIS 90 and DIE LINKEN being writen wrongly
        parties = [
            party.replace(
                "BÜNDNIS90/DIE",
                "BÜNDNIS 90/DIE GRUNE") for party in parties]
        parties = [
            party.replace(
                "BÜNDNISSES90/DIE",
                "BÜNDNIS90/DIE GRÜNEN") for party in parties]
        parties = [party.replace("LINKEN", "DIE LINKEN") for party in parties]
        # deleting unnecesary commas
        parties = [party.replace(",", "") for party in parties]

        conotation = "positive" if "Beifall" in comment_text else "negative"

        people = [self.get_person_data(person) for person in people]

        if "Beifall" in comment_text:
            comment_type = "Beifall"
        elif "Heiterkeit" in comment_text:
            comment_type = "Heiterkeit"
        else:
            comment_type = "Lachen"

        return {"party_involved": parties, "person": people,
                "original_text": comment_text, "conotation": conotation, "type": comment_type}

    def parse_zuruf(self, comment_text):
        # Actually parsing Zuruf is hard, so pushing it back until after alpha
        # release
        pass

    def parse_zwischenruf(self, comment_text):
        # Why do I use this [1:] and [:-1]:
        # German protocol tend to have spaces after interpunction
        # And I want my data to be standardized

        person_text_split = re.split(":", comment_text)

        name_and_party = person_text_split[0]
        text = person_text_split[1][1:]

        person = self.get_person_data(name_and_party)

        return {"person": person, "original_text": text, "type": "Zwischenruf"}

    def parse_single_comment(self, comment_text):
        if comment_text[0] == " ":
            comment_text = comment_text[1:]
        if re.match("Beifall und Heiterkeit|Heiterkeit und Beifall",
                    comment_text):
            return None  # "Edge"
        elif "Gegenruf" in comment_text:
            return None  # Another edge
        elif re.match("Beifall|Heiterkeit|Lachen", comment_text):
            return self.parse_reaction_comments(comment_text)
        elif "Zuruf" in comment_text:
            return None  # self.parse_zuruf(comment_text)
        elif ":" in comment_text:
            return self.parse_zwischenruf(comment_text)

    def parse_comment(self, comment):
        # getting rid of useless braces
        comment = comment.replace("(", "")
        comment = comment.replace(")", "")
        if "–" in comment:
            # splitting on – by its unicode char which is super weird
            # workaround
            simple_comments = re.split(u"\u2013", comment)
            return [self.parse_single_comment(comment)
                    for comment in simple_comments]
        else:
            return self.parse_single_comment(comment)
