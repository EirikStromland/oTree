# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

doc = """
Matching pennies. Single treatment. Two players are given a penny each, and will at the same time choose either heads or tails.
One player wants the outcome to match; the other wants the outcome not to match.
If the outcomes match, the former player gets both pennies; if the outcomes do not match, the latter player gets both pennies.

<p>Source code <a href="https://github.com/wickens/ptree_library/tree/master/matching_pennies">here</a></p>
"""



class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'matching_pennies'


class Treatment(ptree.models.BaseTreatment):

    subsession = models.ForeignKey(Subsession)

    initial_amount = models.MoneyField(
        null=True,
        doc="""The value of the pennies given to each player"""
    )

class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    penny_side = models.CharField(
        max_length=5,
        choices=['heads', 'tails'],
        doc="""Heads or tails"""
    )

    def other_participant(self):
        """Returns the opponent of the current player"""
        return self.other_participants_in_match()[0]

    def set_payoff(self):
        """Calculates payoffs"""

        pennies_match = self.penny_side == self.other_participant().penny_side

        if (self.role() == 'matcher' and pennies_match) or (self.role() == 'mismatcher' and not pennies_match):
            self.payoff = self.treatment.initial_amount * 2
        else:
            self.payoff = 0

    def role(self):
        if self.index_among_participants_in_match == 1:
            return 'matcher'
        if self.index_among_participants_in_match == 2:
            return 'mismatcher'


def treatments():

    return [Treatment.create(initial_amount=1.00)]