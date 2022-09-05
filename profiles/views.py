from ast import Delete
from django.http import JsonResponse
from rest_framework.decorators import api_view
from users.models import User
from profiles.models import Profile
import json


# Create your views here.

@api_view(['POST'])
def createProfile(req):
    body = json.loads(req.body.decode('utf-8'))
    if("name" in body):
        profileCreated = Profile()
        profileCreated.name = body["name"]
        profileCreated.UserId = User.objects.get(id=body["id"])
        if("description" in body):
            profileCreated.description = body["description"]
        profileCreated.save()
        return JsonResponse({"message":"Profile created"})
    return JsonResponse({"error":"Missing fields"})

@api_view(['DELETE'])
def deleteProfile(req):
    body = json.loads(req.body.decode('utf-8'))
    if("name" in body):
        profiledDeleted = Profile.objects.get(name=body["name"])
        if(profiledDeleted != None):
            if(str(profiledDeleted.UserId.id) == body["id"]):
                profiledDeleted.delete()
                return JsonResponse({"message":"Profile deleted"})
            return JsonResponse({"error":"You don't have the permission to do do that"})
        return JsonResponse({"error":"Profile not found"})
    return JsonResponse({"error":"Missing fields"})
