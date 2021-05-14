#!/usr/bin/env python
# -*- coding: utf-8 -*-

import owlready2 as owl
import operator
from functools import reduce

onto = owl.get_ontology("http://localhost:7200/publications")

##########################
######### ABox ###########
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
    domain = [Paper, Conference, Journal]
    range = [Topic]

###### Attributes

# FunctionalProperty: single value for a given instance

class name(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = [Author]
    range = [str]

class title(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = [Paper]
    range = [str]

class subtitle(title):
    namespace = onto
    domain = [Paper]
    range = [str]

class accepted(owl.DataProperty, owl.FunctionalProperty):
    namespace = onto
    domain = [Draft]
    range = [bool]

###### Property restrictions

Draft.is_a.append(isReviewedBy.min(2, Reviewer))

Paper.is_a.append(hasTopic.min(1, Topic))
Conference.is_a.append(hasTopic.min(1, Topic))
Journal.is_a.append(hasTopic.min(1, Topic))

Chair.is_a.append(chairOf.min(1, Conference))
Editor.is_a.append(editorOf.min(1, Journal))


# TODO
# TODO
# TODO
# TODO
# TODO
# TODO
# TODO
# TODO
# TODO


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
disjointness([Full, Short, Demo])
# owl.AllDisjoint([Full, Short, Demo])

# Paper
disjointness([OtherPaper, Poster])
# owl.AllDisjoint([OtherPaper, Poster])

# Workshop
disjointness([Workshop, Symposium, ExpertGroup, RegularConference])
# owl.AllDisjoint([Workshop, Symposium, ExpertGroup, RegularConference])

# Venue
disjointness([Edition, Volume])
# owl.AllDisjoint([Edition, Volume])

# Authority
disjointness([Chair, Editor])
# owl.AllDisjoint([Chair, Editor])


##########################
######### ABox ###########
##########################

author1 = Author("author_1")
author1.name = "Marc"
paper1 = Paper("paper1")
paper1.title = "Principia Matematica"
paper1.subtitle = "From first principle"
author1.authorOf = [paper1]

onto.save(file="publications.rdf", format="rdfxml")
