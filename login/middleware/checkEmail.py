from django.http import JsonResponse
from email_validator import validate_email, EmailNotValidError
import json

class checkEmailMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if(request.build_absolute_uri().endswith('register/')):
            method = request.method
            body = json.loads(request.body.decode('utf-8'))
            if(method == 'POST' and "email" in body):
                try:
                    # Validate & take the normalized form of the email
                    # address for all logic beyond this point (especially
                    # before going to a database query where equality
                    # does not take into account normalization).
                    validate_email(body["email"]).email
                except EmailNotValidError as e:
                    # email is not valid, exception message is human-readable
                    print(str(e))
                    return JsonResponse({"error":"wrong email format"})
        return self.get_response(request)