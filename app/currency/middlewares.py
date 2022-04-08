from time import time


class RequestResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        start = time()
        response = self.get_response(request)
        end = time()
        print(f'View took to execute: {end - start}')  # noqa: T001

        # Code to be executed for each request/response after
        # the view is called.

        return response
