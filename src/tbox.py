#!/usr/bin/env python
# -*- coding: utf-8 -*-

import owlready2 as owl
import operator
from functools import reduce

onto = owl.get_ontology("http://localhost:7200/publications")

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

# disjointness([Full, Short, Demo])
owl.AllDisjoint([Full, Short, Demo])

# disjointness([OtherPaper, Poster])
owl.AllDisjoint([OtherPaper, Poster])

# disjointness([Workshop, Symposium, ExpertGroup, RegularConference])
owl.AllDisjoint([Workshop, Symposium, ExpertGroup, RegularConference])

# disjointness([Edition, Volume])
owl.AllDisjoint([Edition, Volume])

# disjointness([Chair, Editor])
owl.AllDisjoint([Chair, Editor])

if __name__ == "__main__":
    file = "out/publications.rdf"
    onto.save(file=file, format="rdfxml")
    print(f'TBox saved into {file}')
