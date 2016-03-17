from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from bettertexts.models import Text
from bettertexts.models import Rating
import json
import random
import string


class Rate(View):
    model = Rating

    @staticmethod
    def generate_id(size=9, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def post(self, request, *args, **kwargs):
        if 'id' in request.session:
            uid = request.session['id']
        else:
            uid = request.session['id'] = Rate.generate_id()

        return_url = request.GET.get('next', '/')
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR') or '0.0.0.0'
        data = json.loads(request.body.decode())
        score = data.get('score')
        try:
            text = Text.objects.get(slug=self.kwargs.get('slug'))
            question = text.type.question_set.get(pk=self.kwargs.get('question_id'))
            rating = self.model.objects.rate(text, question, score, uid, ip)
            if request.is_ajax():
                result = rating.to_dict()
                result['user_rating'] = int(score)
                return JsonResponse(data=result, status=200)
            else:
                return HttpResponseRedirect(return_url)
        except ValidationError as err:
            if request.is_ajax():
                return JsonResponse(data={'error': err.message}, status=400)
            else:
                return HttpResponseRedirect(return_url)
