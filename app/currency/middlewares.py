from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        self._activate_timezone(request)
        response = self.get_response(request)

        return response

    def _activate_timezone(self, request):
        tzname = request.COOKIES.get('user-timezone')

        if tzname:
            timezone.activate(tzname)
        else:
            timezone.deactivate()
