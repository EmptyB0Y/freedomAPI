from django.shortcuts import render
from django.http import JsonResponse
from login.models import User
from rest_framework.decorators import api_view
from django.core.mail import send_mail
import json
import random
import string
from env import PASSWORD,EMAIL

def get_random_string(length,email):
    # choose from all lowercase letter
    letters = string.ascii_lowercase + email
    return ''.join(random.choice(letters) for i in range(length))
    
@api_view(['POST'])
def register(req):
    body = json.loads(req.body.decode('utf-8'))
    if('name' in body and 'email' in body and 'password' in body and 'confirmPassword' in body):
        if (body['password'] == body['confirmPassword']):
                userCreated = User()
                userCreated.name = body['name']
                userCreated.email = body['email']
                userCreated.password = body['password']
                userCreated.confirmationKey = get_random_string(16,body["email"])
                userCreated.save()
                email = body["email"]
                print(email)
                #Fix : ProtonMail does not allow automated mailing
                #send_mail('Account confirmation','Click the link to confirm your email : https://127.0.0.1/confirm?token={userCreated.confirmationKey}?email={email}',{EMAIL},{PASSWORD})
                print("email sent")
                return JsonResponse({"response":"OK"})

    return JsonResponse({"response":"NOT OK"})

@api_view(['GET'])
def confirm(req):
        token = req.GET.get('token')
        print(token)
        userConfirmed = User.objects.get(req.GET.get('email'))
        if(token == userConfirmed.confirmationKey):
                userConfirmed.isConfirmed = True
                userConfirmed.save()
                return JsonResponse({"response":"OK"})
        return JsonResponse({"response":"NOT OK"})
