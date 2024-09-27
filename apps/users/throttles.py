from rest_framework.throttling import AnonRateThrottle
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet 

class RegisterRateThrottle(AnonRateThrottle):
    rate = '10/hour'

    def get_cache_key(self, request: Request, view: ViewSet) -> str:
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.data['phone_number'] if 'phone_number' in request.data else "no_phone_number"
        }
