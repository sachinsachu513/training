from django.http import HttpResponse, Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import registerserializer
from .models import register

# Create your views here.
@api_view(['GET'])
def get_user(request):
    obj=register.objects.all()
    serializer=registerserializer(obj,many=True )
    return Response(serializer.data)

@api_view(['POST'])
def post_user(request):
    newuser=registerserializer(data=request.data)
    if newuser.is_valid():
        newuser.save()
    return Response(newuser.data)

from rest_framework import status
@api_view(['Delete'])
def delete_user(request,id):
    user=register.objects.get(id=id)
    new_user=registerserializer(data=request.data)
    user.delete()
    return Response(new_user.error_messages,status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_user(request,id):
    user=register.objects.get(id=id)
    new_user=registerserializer(user,data=request.data)
    if new_user.is_valid():
        new_user.save()
        return Response(new_user.data,status=status.HTTP_200_OK)

from .models import combine
from .serializer import combine_serializer

@api_view(["GET","POST"])
def getandpost(request):
    if request.method=="GET":
        obj=combine.objects.all()
        show=combine_serializer(obj,many=True)
        return Response(show.data)
    elif request.method=="POST":
        new=combine_serializer(data=request.data)
        if new.is_valid():
            new.save()
            return Response(new.data,status=status.HTTP_201_CREATED)
        return Response(new.errors,status=status.HTTP_400_BAD_REQUEST)


from django.core.exceptions import ObjectDoesNotExist
@api_view(["GET","POST","DELETE","PUT"])
def complete(request,id):
    try:
        req=combine.objects.get(id=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    if request.method=='GET':
        obj = combine.objects.all()
        serializer = combine_serializer(obj, many=True)
        return Response(serializer.data)

    elif request.method=="POST":
        newuser=combine_serializer(data=request.data)
        if newuser.is_valid():
          newuser.save()
          return Response(newuser.data,status=status.HTTP_201_CREATED)

    elif request.method=="PUT":
        new_user=combine_serializer(req,data=request.data)
        if new_user.is_valid():
            new_user.save()
            return Response(new_user.data,status=status.HTTP_200_OK)
        return Response(new_user.data, status=status.HTTP_202_BAD_REQUEST)

    elif request.method=="DELETE":
        user=combine.objects.get(id=id)
        dele=combine_serializer(user,data=request.data)
        user.delete()
        return Response(dele.error_messages,status=status.HTTP_204_NO_CONTENT)
    return Response(combine_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from .models import profile
from .serializer import methodserializer



@api_view(["GET"])
def get_account(request):
    obj=profile.objects.all()
    serializer=methodserializer(obj,many=True)
    return Response(serializer.data)


@api_view(["GET"])
def account_detail(request,id):
    try:
        obj=profile.objects.get(id=id)
    except profile.DoesNotExist:
        return HttpResponse("does not exist")

    obj1=methodserializer(obj)
    return Response(obj1.data)


from .models import snippet
from .serializer import snippet_serializer
from rest_framework.views import APIView


class snippet_get(APIView):
    def get(self,request):
     obj=snippet.objects.all()
     serial=snippet_serializer(obj,many=True)
     return Response(serial.data)
    def post(self,request):
        obj=snippet_serializer(data=request.data)
        if obj.is_valid():
            obj.save()
            return Response(obj.data,status=status.HTTP_201_CREATED)


class multiple(APIView):
    def get_obj(self,id):
        try:
           return snippet.objects.get(id=id)
        except snippet.DoesNotExist:
            raise Http404

    def get(self,request,id,format=None):
        new=self.get_obj(id)
        ser=snippet_serializer(new)
        return Response(ser.data)

    def put(self,request,id,format=None):
        ide=self.get_obj(id)
        new=snippet_serializer(ide,data=request.data)
        if new.is_valid():
            new.save()
            return Response(new.data,status=status.HTTP_200_OK)


    def delete(self,request,id,format=None):
        ide=self.get_obj(id)
        ser1=snippet_serializer(ide,data=request.data)
        ide.delete()
        return Response(ser1.error_messages,status=status.HTTP_204_NO_CONTENT)

from rest_framework import generics

# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#
# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

class genric_create(generics.CreateAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer


class snipetlist(generics.ListAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

class snipet2(generics.ListCreateAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

class snipet3(generics.DestroyAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer


class snipet4(generics.UpdateAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

class snipet5(generics.RetrieveAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

class snipet6(generics.RetrieveDestroyAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer


class snipet7(generics.RetrieveUpdateAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

class snipet8(generics.RetrieveUpdateDestroyAPIView):
    queryset = snippet.objects.all()
    serializer_class = snippet_serializer

from.serializer import miscellanceserializer
from .models import miscellance


# class read_only(generics.RetrieveUpdateAPIView):
#     queryset = miscellance.objects.all()
#     serializer_class = miscellanceserializer
class read_only(APIView):
    def post(self,request):
        myobj=miscellanceserializer(data=request.data)
        if myobj.is_valid():
            myobj.save()
            return Response(myobj.data,status=status.HTTP_201_CREATED)

from .models import Hiddenfield
from.serializer import hiddenserializer

class hidden_get(APIView):
    def get(self,request):
        obj=Hiddenfield.objects.all()
        ser=hiddenserializer(obj,many=True)
        return Response(ser.data)

from .models import studentdetails
from.serializer import studentserializer,sourceserializer

class twomethod(APIView):
    def get(self,request):
        obj=studentdetails.objects.all()
        ser=studentserializer(obj,many=True)
        return Response(ser.data)

class source(APIView):
    def get(self,request):
        obj=studentdetails.objects.all()
        ser=sourceserializer(obj,many=True)
        return Response(ser.data)

# print(snippet.objects.filter(username='shami'))
# print(snippet.objects.exclude(username='shami'))























































































