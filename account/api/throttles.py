from rest_framework.throttling import AnonRateThrottle


class RegisterThrottle(AnonRateThrottle):
    scope = 'registerthrottle'
