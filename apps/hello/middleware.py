import random

from hello.models import Requests


class GetRequestsMiddleware(object):

    def process_request(self, request):
        '''
        Get request and store it in db
        '''
        # Ignore ajax requests on requests page
        if request.is_ajax() and request.path == '/requests/':
            return

        Requests.objects.create(
            path=request.path,
            method=request.method,
            user_agent=request.META.get('HTTP_USER_AGENT',
                                        None),
            remote_addr=request.META.get('REMOTE_ADDR',
                                         None),
            is_secure=request.is_secure(),
            is_ajax=request.is_ajax(),
            priority=random.randint(0, 5)
        )
