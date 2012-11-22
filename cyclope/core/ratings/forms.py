from django import forms
from django.template.loader import render_to_string
from django.template import RequestContext
from ratings.forms import VoteForm
from ratings.forms.widgets import BaseWidget
from ratings import handlers

class LikeDislikeWidget(BaseWidget):

    def __init__(self, min_value, max_value, step, instance=None,
        can_delete_vote=True, key='', read_only=False,
        template='ratings/likedislike_widget.html', attrs=None):
        super(LikeDislikeWidget, self).__init__(attrs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.instance = instance
        self.can_delete_vote = can_delete_vote
        self.read_only = read_only
        self.template = template
        self.key = key

    def _get_score_annotated(self):
        handler = handlers.ratings.get_handler(type(self.instance))
        score = handler.get_score(self.instance, self.key)
        if score is not None:
            score.num_positives = int((score.total + score.num_votes) / 2)
            score.num_negatives = abs(score.total - score.num_positives)
        else:
            score = {"num_positives":0, "num_negatives":0, "total":0}
        return score

    def get_context(self, name, value, attrs=None):
        from cyclope import settings as cyc_settings
        attrs['type'] = 'hidden'
        return {
            'can_delete_vote': self.can_delete_vote,
            'read_only': self.read_only,
            'parent': super(LikeDislikeWidget, self).render(name, value, attrs),
            'parent_id': self.get_parent_id(name, attrs),
            'value': value,
            'widget_id': self.get_widget_id('likedislike', name, self.key),
            'score': self._get_score_annotated(),
            'cyc_settings': cyc_settings,
        }

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs or {})
        return render_to_string(self.template, context)


class LikeDislikeVoteForm(VoteForm):
    """
    Handle voting using a like/dislike widget.
    """
    def __init__(self, *args, **kwargs):
        super(LikeDislikeVoteForm, self).__init__(*args, **kwargs)
        self.score_range = (-1, 1)

    def get_score_widget(self, score_range, score_step, can_delete_vote):
        return LikeDislikeWidget(self.score_range[0], self.score_range[1], score_step,
            instance=self.target_object, can_delete_vote=can_delete_vote, key=self.key)
