__version__ = "0.0.1"

default_app_config = "bettertexts.apps.ImprovetextAppConfig"


# Override get_model in django_comments
def get_model():
    from bettertexts.models import TextComment

    """
    Returns the comment model class.
    """
    return TextComment


def get_form():
    from bettertexts.forms import TextCommentForm

    """
    Returns the comment ModelForm class.
    """
    return TextCommentForm
