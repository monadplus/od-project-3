#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import random
from tbox import *
from tbox import onto
from typing import Dict, Tuple
from collections import defaultdict
import urllib

dataDir = "../data/"
random.seed(0)

_min = min

def assignRandomType(uri : str, options):
    clazz = random.choice(options)
    return clazz(sanitizeURI(uri))

def randomPaperType(uri: str, isVolume: bool):
    if isVolume:
        options = [Full, Short, Demo]
    else:
        options = [Full, Short, Demo, Poster]
    return assignRandomType(uri, options)

def randomConferenceType(uri: str):
    options = [Workshop, Symposium, ExpertGroup, RegularConference]
    return assignRandomType(uri, options)

def createChair(n : int):
    chairInstance = Chair(sanitizeURI(uri = f'chair_{n}'))
    chairInstance.fullname = f"Chair {n}"
    return chairInstance

def createEditor(n : int):
    editorInstance = Editor(sanitizeURI(uri = f'editor_{n}'))
    editorInstance.fullname = f"Editor {n}"
    return editorInstance

def sample(options, min = 1, max = None):
    if max:
        maxK = _min(max, len(options) - 1)
    else:
        maxK = len(options) - 1
    k = random.randint(min, maxK)
    return random.sample(options, k)

# https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote
def sanitizeURI(uri):
    return urllib.parse.quote(uri,safe=[])

def abox():
    """
    Generate the ABox from the datasets.
    """
    personDict : Dict[str, Person] = dict()
    topicDict : Dict[str, Topic] = dict()
    conferenceDict : Dict[str, Conference] = dict()
    journalDict : Dict[str, Journal] = dict()
    editionDict : Dict[str, Edition] = dict()
    volumeDict : Dict[str, Volume] = dict()
    chairs : list[Chair] = [createChair(n) for n in range(1, 4)]
    editors : list[Editor] = [createEditor(n) for n in range(1, 4)]
    paperVenueDict : Dict[str, Tuple[bool, str]] = dict() # false = Edition, true = Volume
    paperReviewersDict : Dict[str, list[str]] = defaultdict(list)
    editionConferenceDict : Dict[str, str] = dict()
    volumeJournalDict : Dict[str, str] = dict()
    conferenceChairsDict : Dict[str, list[Chair]] = dict()
    journalEditorsDict : Dict[str, list[Editor]] = dict()
    paperAuthorsDict : Dict[str, list[str]] = defaultdict(list)

    ################ Relationships

    with open(dataDir + 'coauthors_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            authorId = row['authorId']
            paperDoi = row['doi']
            paperAuthorsDict[paperDoi].append(authorId)

    with open(dataDir + 'article_edition_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            articleDoi = row['article']
            editionName = row['edition']
            paperVenueDict[articleDoi] = (False, editionName)

    with open(dataDir + 'article_volume_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            articleDoi = row['article']
            volumeName = row['volume']
            paperVenueDict[articleDoi] = (True, volumeName)

    with open(dataDir + 'conference_edition_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            conferenceName = row['conference']
            editionName = row['edition']
            editionConferenceDict[editionName] = conferenceName

    with open(dataDir + 'journal_volume_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            journalName = row['journal']
            volumeName = row['volume']
            volumeJournalDict[volumeName] = journalName

    with open(dataDir + 'reviewers_rel.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            authorId = row['authorId']
            paperDoi = row['doi']
            paperReviewersDict[paperDoi].append(authorId)

    ################ Classes

    # Authors & Reviewers
    with open(dataDir + 'authors.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            authorId = row['authorId']
            person = Person(sanitizeURI(uri = authorId))
            person.fullname = row['name']
            # person.authorOf is found at paper
            personDict[authorId] = person

    # Topics
    with open(dataDir + 'keywords.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            name = row['name']
            topic = Topic(sanitizeURI(uri = name))
            topic.fullname = name
            topicDict[name] = topic

    # Conferences
    with open(dataDir + 'conferences.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            name = row['name']
            conference = randomConferenceType(uri = name)
            conference.fullname = name
            someChairs = sample(chairs)
            conference.directedBy = someChairs
            conferenceChairsDict[name] = someChairs
            conferenceDict[name] = conference

    # Journals
    with open(dataDir + 'journals.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            name = row['name']
            journal = Journal(sanitizeURI(uri = name))
            journal.fullname = name
            someEditors = sample(editors)
            journal.editedBy = someEditors
            journalEditorsDict[name] = someEditors
            journalDict[name] = journal

    # Editions
    with open(dataDir + 'editions.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            name = row['name']
            edition = Edition(sanitizeURI(uri = name))
            edition.fullname = name
            edition.hasTopic = sample(list(topicDict.values()), max=4)
            conference = conferenceDict[editionConferenceDict[name]]
            edition.editionOf = [conference]
            editionDict[name] = edition

    # Volumes
    with open(dataDir + 'volumes.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            name = row['name']
            volume = Volume(sanitizeURI(uri = name))
            volume.fullname = name
            volume.hasTopic = sample(list(topicDict.values()), max=4)
            journal = journalDict[volumeJournalDict[name]]
            volume.volumeOf = [journal]
            volumeDict[name] = volume

    # Paper and Draft
    with open(dataDir + 'articles.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile, delimiter=','):
            doi = row['doi']
            # Some papers are not published in our dataset.
            if doi in paperVenueDict:
                isVolume, venueName = paperVenueDict[doi]

                # Paper
                paper = randomPaperType(doi, isVolume)
                paper.title = row['title']
                paper.hasTopic = sample(list(topicDict.values()), max=4)
                authors = list(map(personDict.get, paperAuthorsDict[doi]))
                paper.authoredBy = authors
                # paper.submittedTo below

                # Draft
                draft = Draft(uri = f'draft_{doi}')
                draft.title = row['title'] # same as paper
                reviewers = list(map(personDict.get, sample(list(paperReviewersDict[doi]))))
                draft.isReviewedBy = reviewers
                paper.submittedTo = [draft]
                isAccepted = random.choice([False, True])
                draft.accepted = isAccepted
                if isAccepted:
                    if isVolume:
                        volume = volumeDict[venueName]
                        draft.published = [volume]
                    else:
                        edition = editionDict[venueName]
                        draft.published = [edition]
                if isVolume:
                    editors = journalEditorsDict[volumeJournalDict[venueName]]
                    draft.supervisedBy = editors
                else:
                    chairs = conferenceChairsDict[editionConferenceDict[venueName]]
                    draft.supervisedBy = chairs

if __name__ == "__main__":
    abox()
    file = "out/publications.rdf"
    onto.save(file=file, format="rdfxml")
    print(f'TBox & ABox saved into {file}')
