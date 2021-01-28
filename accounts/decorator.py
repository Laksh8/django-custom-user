import functools
from rest_framework import status
from rest_framework.response import Response

def Authentication(request):
    if request.user.is_authenticated and "Bearer "+request.user.token == request.headers.get("Authorization"):
        return True
    return False

def AuthenticationCheck(method):

    def inner(self,request,*args,**kwargs):
        if Authentication(request):
            return method(self,request,*args,**kwargs)
        
        return Response({"error":"User not Allowed"},401)
    
    return inner
