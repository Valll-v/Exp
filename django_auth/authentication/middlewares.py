from rest_framework.request import Request


class LastActiveMiddleware(object):
    """
    Middlewate to set timestampe when a user
    has been last seen
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        from django.utils.datetime_safe import datetime
        response = self.get_response(request)

        user = request.user

        if user.is_authenticated:
            user.last_seen = datetime.now()
            user.save()

        return response
