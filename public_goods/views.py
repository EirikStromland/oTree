# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants

def variables_for_all_templates(self):
    return {'endowment': Constants.endowment,
            'players_per_group': Constants.players_per_group,
            'efficiency_factor': Constants.efficiency_factor}


class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def variables_for_template(self):
        return {'no_of_players': Constants.players_per_group,
                'efficiency_factor': Constants.efficiency_factor}


class Question(Page):
    template_name = 'public_goods/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    template_name = 'public_goods/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'answer': self.player.question,
                'is_correct': self.player.question_correct(),
                }


class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    auto_submit_values = {'contribution': c(Constants.endowment/2)}

    template_name = 'public_goods/Contribute.html'


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return "Waiting for other participants to contribute."


class Results(Page):

    """Players payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def variables_for_template(self):

        return {
            'current_player': self.player,
            'other_players': self.player.get_others_in_group(),
            'total_contribution': self.group.total_contribution,
            'total_earnings': self.group.total_contribution * Constants.efficiency_factor,
            'individual_share': self.group.individual_share,
            'individual_earnings': self.player.payoff - Constants.base_points,
            'base_points': Constants.base_points,
            'total_points': self.player.payoff
        }

def pages():

    return [Introduction,
            Question,
            Feedback,
            Contribute,
            ResultsWaitPage,
            Results]
