from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import JsonResponse
from users.models import User
from rest_framework.decorators import api_view
from django.core.mail import send_mail
import json
import random
import string
from dotenv import dotenv_values
import hashlib
import jwt

config = dotenv_values(".env")

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
                salt = str(userCreated.id)
                userCreated.password = hashlib.pbkdf2_hmac(
                    'sha256', # The hash digest algorithm for HMAC
                    body["password"].encode('utf-8'), # Convert the password to bytes
                    bytes(salt.encode('utf-8')), # Provide the salt
                    100000, # It is recommended to use at least 100,000 iterations of SHA-256 
                    dklen=128 # Get a 128 byte key
                )
                userCreated.confirmationKey = get_random_string(16,body["email"])
                userCreated.save()
                email = body["email"]
                print(email)
                print(userCreated.confirmationKey)
                #Fix : ProtonMail does not allow automated mailing
                #send_mail('Account confirmation','Click the link to confirm your email : https://127.0.0.1/confirm?token={userCreated.confirmationKey}&email={email}',{env.EMAIL},{env.PASSWORD})
                print("email sent")
                return JsonResponse({"response":"OK"})

    return JsonResponse({"response":"NOT OK"})

@api_view(['GET'])
def confirm(req):
        token = req.GET.get('token')
        email = req.GET.get('email')
        print(token)
        print(email)
        userConfirmed = User.objects.get(email=email)
        if(token == userConfirmed.confirmationKey):
                userConfirmed.isConfirmed = True
                userConfirmed.save()
                return JsonResponse({"response":"OK"})
        return JsonResponse({"response":"NOT OK"})

@api_view(['POST'])
def login(req):
    body = json.loads(req.body.decode('utf-8'))
    userLogged = NULL
    if("name" in body):
        userLogged = User.objects.get(name=body["name"])
    elif("email" in body):
        userLogged = User.objects.get(email=body["email"])

    if(userLogged != NULL):
        salt = str(userLogged.id)
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            body["password"].encode('utf-8'), # Convert the password to bytes
            bytes(salt.encode('utf-8')), # Provide the salt
            100000, # It is recommended to use at least 100,000 iterations of SHA-256 
            dklen=128 # Get a 128 byte key
        )
        encoded_jwt = jwt. encode({'id': str(userLogged.id)}, config["TOKEN_KEY"], algorithm='HS256')
        if(str(userLogged.password) == str(hashed_password) and userLogged.isConfirmed):
            return JsonResponse({"token": encoded_jwt,"id":str(userLogged.id)})
    return JsonResponse({"response":"NOT OK"})

@api_view(['DELETE'])
def deleteAccount(req):
    body = json.loads(req.body.decode('utf-8'))
    userDeleted = User.objects.get(id=body["id"])
    if(userDeleted != None):
        userDeleted.delete()
        return JsonResponse({"response":"Account deleted"})
    return JsonResponse({"error":"User not found"})

    
    


