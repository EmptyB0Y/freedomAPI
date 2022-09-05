from asyncio.windows_events import NULL
from django.http import JsonResponse
import json
import jwt
from dotenv import dotenv_values

config = dotenv_values(".env")
routes = ["/delete_account","/create_profile","/delete_profile"]

class checkAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        uriBuild = request.build_absolute_uri().split('/')
        uri = ""
        i = 0
        for s in uriBuild:
            i += 1
            if(i == 4):
                uri += '/'+ s
        if(uri in routes):
            print("Checking authentication")
            method = request.method
            body = json.loads(request.body.decode('utf-8'))
            token = request.headers.get('Authorization').split(' ')[1]
            if(token != None and "id" in body):
                decoded_jwt = jwt.decode(token, config["TOKEN_KEY"], algorithms=['HS256'])
                if(decoded_jwt["id"] == body["id"]):
                    return self.get_response(request)
            return JsonResponse({"error":"Authentication failed"})
        return self.get_response(request)



