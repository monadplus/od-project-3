#!/usr/bin/env python
# -*- coding: utf-8 -*-

import owlready2 as owl
import operator
from functools import reduce

# reasoner debug options
show_debug = 2
no_debug = 0

onto = owl.get_ontology("http://localhost:7200/publications")

##########################
######### TBox ###########
##########################

###### Classes

class Person(owl.Thing):
    namespace = onto

class Reviewer(Person):
    namespace = onto

class Author(Person):
    namespace = onto

class Authority(Person):
    namespace = onto

class Chair(Authority):
    namespace = onto

class Editor(Authority):
    namespace = onto

class Topic(owl.Thing):
    namespace = onto

class Paper(owl.Thing):
    namespace = onto

class Poster(Paper):
    namespace = onto

class OtherPaper(Paper):
    namespace = onto

class Full(OtherPaper):
    namespace = onto

class Short(OtherPaper):
    namespace = onto

class Demo(OtherPaper):
    namespace = onto

class Draft(owl.Thing):
    namespace = onto

class AcceptedDraft(Draft):
    namespace = onto

class Venue(owl.Thing):
    namespace = onto

class Edition(Venue):
    namespace = onto

class Volume(Venue):
    namespace = onto

class Journal(owl.Thing):
    namespace = onto

class Conference(owl.Thing):
    namespace = onto

class Workshop(Conference):
    namespace = onto

class Symposium(Conference):
    namespace = onto

class ExpertGroup(Conference):
    namespace = onto

class RegularConference(Conference):
    namespace = onto

###### Properties

class chairOf(owl.ObjectProperty):
    namespace = onto
    domain = [Chair]
    range = [Conference]

class editorOf(owl.ObjectProperty):
    namespace = onto
    domain = [Editor]
    range = [Journal]

class editionOf(owl.ObjectProperty):
    namespace = onto
    domain = [Edition]
    range = [Conference]

class volumeOf(owl.ObjectProperty):
    namespace = onto
    domain = [Volume]
    range = [Journal]

class published(owl.ObjectProperty):
    namespace = onto
    domain = [AcceptedDraft]
    range = [Venue]

class submitted(owl.ObjectProperty):
    namespace = onto
    domain = [Paper]
    range = [Draft]

class responsibleFor(owl.ObjectProperty):
    namespace = onto
    domain = [Authority]
    range = [Draft]

class supervisedBy(owl.ObjectProperty):
    namespace = onto
    domain = [Draft]
    range = [Authority]
    inverse_property = responsibleFor

class reviews(owl.ObjectProperty):
    namespace = onto
    domain = [Reviewer]
    range = [Draft]

class isReviewedBy(owl.ObjectProperty):
    namespace = onto
    domain = [Draft]
    range = [Reviewer]
    inverse_property = reviews

class authorOf(owl.ObjectProperty):
    namespace = onto
    domain = [Author]
    range = [Paper]

class authoredBy(owl.ObjectProperty):
    namespace = onto
    domain = [Paper]
    range = [Author]
    inverse_property = authorOf

class hasTopic(owl.ObjectProperty):
    namespace = onto
    domain = [Paper | Conference | Journal]
    range = [Topic]

###### Attributes

# FunctionalProperty: single value for a given instance

class name(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = [Person | Reviewer | Author \
              | Authority | Chair | Editor \
              | Topic | Venue | Edition \
              | Volume | Conference | Journal \
              | Workshop | Symposium | ExpertGroup | RegularConference
              ]
    range = [str]

class title(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = \
        [Paper | Poster | OtherPaper | Full | Short | Demo | Draft | AcceptedDraft]
    range = [str]

# subproperty
# class subtitle(title):
#     pass

class accepted(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = [Draft | AcceptedDraft]
    range = [bool]

###### Property restrictions

Paper.is_a.append(authoredBy.some(Author))
Paper.is_a.append(hasTopic.some(Topic))

Chair.is_a.append(chairOf.some(Conference))
Conference.is_a.append(owl.Inverse(chairOf).some(Chair))
Conference.is_a.append(hasTopic.some(Topic))

Editor.is_a.append(editorOf.some(Journal))
Journal.is_a.append(owl.Inverse(editorOf).some(Editor))
Journal.is_a.append(hasTopic.some(Topic))

Edition.is_a.append(editionOf.exactly(1, Conference))
Volume.is_a.append(volumeOf.exactly(1, Journal)) # volumeOf.min(1, Journal) & volumeOf.max(1, Journal)

Draft.is_a.append(isReviewedBy.min(2, Reviewer))
Draft.is_a.append(owl.Inverse(submitted).exactly(1, Paper))
Draft.is_a.append(supervisedBy.exactly(1, Authority))

AcceptedDraft.is_a.append(published.exactly(1, Venue))
AcceptedDraft.equivalent_to.append(Draft & accepted.value(True))

###### Class disjoiness

def disjointness(classes: [owl.Thing]) -> None:
    """Adds the disjointness constraint to a group of classes."""
    assert (len(classes) > 1), "disjointness only works for 2 or more classes."
    for claz in classes:
        restOf = [owl.Not(c) for c in classes if c != claz]
        claz.equivalent_to.append(reduce(operator.and_, restOf))

# NOTE both are expressing the same concept
# but disjointness uses a restriction while AllDisjoint uses an OWL2 class

# OtherPaper
# disjointness([Full, Short, Demo])
owl.AllDisjoint([Full, Short, Demo])

# Paper
# disjointness([OtherPaper, Poster])
owl.AllDisjoint([OtherPaper, Poster])

# Workshop
# disjointness([Workshop, Symposium, ExpertGroup, RegularConference])
owl.AllDisjoint([Workshop, Symposium, ExpertGroup, RegularConference])

# Venue
# disjointness([Edition, Volume])
owl.AllDisjoint([Edition, Volume])

# Authority
# disjointness([Chair, Editor])
owl.AllDisjoint([Chair, Editor])


##########################
######### ABox ###########
##########################

# For inverse properties you only need to create one of the sides.

author1 = Author("author_1")
author1.name = "Marc"

reviewer1 = Reviewer("reviewer_1")
reviewer1.name = "Antonio"

reviewer2 = Reviewer("reviewer_2")
reviewer2.name = "Antonio 2"

chair = Authority("chair_1")
chair.name = "Paco"

editor = Authority("editor_1")
editor.name = "Manolo"

topic1 = Topic("topic_1")
topic1.name = "Topic 1"

topic2 = Topic("topic_2")
topic2.name = "Topic 2"

# owl.AllDifferent([topic1, topic2])

paper1 = Full("paper_1")
paper1.title = "Paper 1"
paper1.authoredBy = [author1]
paper1.hasTopic = [topic1]

paper2 = Demo("paper_2")
paper2.title = "Paper 2"
paper2.authoredBy = [author1]
paper2.hasTopic = [topic1, topic2]

workshop = Workshop('workshop_1')
workshop.name = "Workshop 1"
workshop.topic = [topic1]

journal = Journal('journal_1')
journal.name = "Journal 1"
journal.topic = [topic2]

edition = Edition('edition_1')
edition.name = "Edition 1"
edition.editionOf = [workshop]

volume = Volume('volume_1')
volume.name = "Volume 1"
volume.volumeOf = [journal]

draft1 = Draft("draft_1")
draft1.isReviewedBy = [reviewer1, reviewer2]
draft1.supervisedBy = [chair]
draft1.accepted = True
draft1.published = [edition]

draft2 = Draft("draft_2")
draft2.isReviewedBy = [reviewer1, reviewer2]
draft2.supervisedBy = [chair]
draft2.accepted = True
draft2.published = [volume]

paper1.submitted = [draft1]
paper2.submitted = [draft2]

chair.chairOf = [workshop]
editor.editorOf = [journal]

# When the reasoner is activated,
# if you set the draft to not accepted (i.e. draft1.accepted = False)
# then the draft cannot be published to an edition!
#
# Restrictions are also checked, for example paper2.submitted = [draft1] will fail.


# Save the ontology into a file
onto.save(file="out/publications.rdf", format="rdfxml")


##########################
###### Querying ##########
##########################

# owl.sync_reasoner_hermit()
owl.sync_reasoner_pellet([onto],
                         infer_property_values = True,
                         infer_data_property_values = True,
                         debug=show_debug)

print('Inconsisten classes:', list(owl.default_world.inconsistent_classes()))
# The reasoner infered that the Draft was an AcceptedDraft
print(draft1.__class__)


# For more complex queries: use SPARQL with RDFlib
#
# print(onto.search(subclass_of=onto.Person))
