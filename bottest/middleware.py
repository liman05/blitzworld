
from django.http  import HttpResponseGone, Http410

class MyGoneMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, Http410):
            return HttpResponseGone("Gone!")
        return None
