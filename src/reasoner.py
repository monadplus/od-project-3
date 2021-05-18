#!/usr/bin/env python
# -*- coding: utf-8 -*-

import owlready2 as owl
from tbox import *

# reasoner debug options
no_debug = 0
show_debug = 2

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


# owl.sync_reasoner_hermit()
owl.sync_reasoner_pellet([onto],
                         infer_property_values = True,
                         infer_data_property_values = True,
                         debug=show_debug)

print('Inconsisten classes:', list(owl.default_world.inconsistent_classes()))

# The reasoner infered that the Draft was an AcceptedDraft
print(draft1.__class__)

# For more complex queries: use SPARQL with RDFlib
print('Subclasses of :Person = ', onto.search(subclass_of=onto.Person))
