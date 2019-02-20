from django.utils.deprecation import MiddlewareMixin


class UserAgent(MiddlewareMixin):
    def process_request(self, request):
        if request.user and request.user.is_authenticated:
            request.session['user_agent'] = request.META.get('HTTP_USER_AGENT')
