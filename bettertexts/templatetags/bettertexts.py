from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import smart_text

import bettertexts

register = template.Library()


class RenderQuestionListNode(template.Node):
    """
    Insert a list of questions took mechanism
    from https://github.com/django/django-contrib-comments/blob/master/django_comments/templatetags/comments.py
    """

    @classmethod
    def handle_token(cls, parser, token):
        """Class method to parse render_comment_list and return a Node."""
        return "output of handle_token()"

    def render(self, context):
#        qs = self.get_queryset(context)
#        context[self.as_varname] = self.get_context_value_from_queryset(context, qs)
        return ''


@register.tag
def render_question_list(parser, token):
    """
    Render the comment list (as returned by ``{% get_comment_list %}``)
    through the ``comments/list.html`` template
    Syntax::
        {% render_comment_list for [object] %}
        {% render_comment_list for [app].[model] [object_id] %}
    Example usage::
        {% render_comment_list for event %}
    """
    return RenderQuestionListNode.handle_token(parser, token)


@register.filter(name='add_class')
def add_class(field, classes):
    return field.as_widget(attrs={"class": classes})
