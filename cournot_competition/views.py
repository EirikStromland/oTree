# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
def variables_for_all_templates(self):

    return {'total_capacity': Constants.total_capacity,
            'max_units_per_player': Constants.max_units_per_player,
            'total_q': 1}


class Introduction(Page):

    template_name = 'cournot_competition/Introduction.html'


class Question1(Page):

    template_name = 'cournot_competition/Question.html'

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class Feedback1(Page):

    template_name = 'cournot_competition/Feedback.html'

    def variables_for_template(self):
        return {'num_q': 1,
                'question': """Suppose firm Q produced 20 units and firm P produced 30 units. What would be the profit for firm P?""",
                'answer': self.player.training_question_1,
                'correct': Constants.training_1_correct,
                'explanation': """Total units produced were 20 + 30 = 50. The unit selling price was 60 – 50 = 10.
                                  The profit for firm P would be the product of the unit selling price and the unit produced by firm P, that is 10 × 30 = 300""",
                'is_correct': self.player.is_training_question_1_correct()}


class Decide(Page):

    template_name = 'cournot_competition/Decide.html'

    form_model = models.Player
    form_fields = ['units']


class ResultsWaitPage(WaitPage):



    def body_text(self):
        return "Waiting for the other participant to decide."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'cournot_competition/Results.html'

    def variables_for_template(self):

        return {'units': self.player.units,
                'other_units': self.player.other_player().units,
                'total_units': self.group.total_units,
                'total_capacity': Constants.total_capacity,
                'price': self.group.price,
                'payoff': self.player.payoff,
                'base_points': Constants.base_points,
                'total_plus_base': self.player.payoff + Constants.base_points}


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Decide,
            ResultsWaitPage,
            Results]
