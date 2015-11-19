from hello.models import Requests


class GetRequestsMiddleware(object):

    def process_request(self, request):
        '''
        Get request and store it in db
        '''

        if not request.is_ajax() and request.path != 'requests':
            request_entry = Requests(
                path=request.path,
                method=request.method,
                user_agent=request.META.get('HTTP_USER_AGENT',
                                            None),
                remote_addr=request.META.get('REMOTE_ADDR',
                                             None),
                is_secure=request.is_secure(),
                is_ajax=request.is_ajax()
            )
            request_entry.save()
        return
