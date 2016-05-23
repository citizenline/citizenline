from django_comments.forms import CommentForm

from django import forms
from django.utils.translation import ugettext_lazy as _
from bettertexts.models import TextComment


class TextCommentForm(CommentForm):

    def __init__(self, *args, **kwargs):
        super(TextCommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _("Name")
        self.fields['name'].required = True
        self.fields['email'].label = _("Email address")
        self.fields['email'].required = True
        self.fields['comment'].label = _('Comment')
        self.fields['comment'].required = True
        self.fields['url'].widget = forms.HiddenInput()

    inform = forms.BooleanField(required=False,
                                label=_('Keep me informed'),
                                widget=forms.CheckboxInput)

    involved = forms.BooleanField(required=False,
                                  label=_('Keep me involved'),
                                  widget=forms.CheckboxInput)

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
