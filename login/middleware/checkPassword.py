from django.http import JsonResponse
import json
import re

class checkPasswordMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if(request.build_absolute_uri().endswith('register/')):
            method = request.method
            body = json.loads(request.body.decode('utf-8'))
            if(method == 'POST' and "password" in body):
                password = body["password"]
                if len(password) < 8:
                    return JsonResponse({"error":"Make sure your password is at lest 8 letters long"})
                elif re.search('[0-9]',password) is None:    
                    return JsonResponse({"error":"Make sure your password has a number in it"})
                elif re.search('[A-Z]',password) is None:    
                    return JsonResponse({"error":"Make sure your password has a capital letter in it"})
        return self.get_response(request)