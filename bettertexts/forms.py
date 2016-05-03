from django_comments.forms import CommentForm

from django import forms
from django.utils.translation import ugettext_lazy as _
from bettertexts.models import TextComment


class TextCommentForm(CommentForm):

    def __init__(self, *args, **kwargs):
        super(TextCommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _("Name")
        self.fields['email'].label = _("Email address")
        self.fields['comment'].label = _('Comment')

    inform = forms.BooleanField(required=False,
                                label=_('Hou me op de hoogte'))

    class Meta:
        fields = ['name', 'email', 'inform', 'comment']

    def get_comment_model(self):
        """
        override to provide a custom comment model.
        """
        return TextComment

    def get_comment_create_data(self):
        """
        Override to add inform field
        """
        data = super(TextCommentForm, self).get_comment_create_data()
        data.update({'inform': True})
        return data
