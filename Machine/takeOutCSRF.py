# -*- coding: utf-8 -*-

class DisableCSRFCheck(object):
    """
    屏蔽csrf验证
    """
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)