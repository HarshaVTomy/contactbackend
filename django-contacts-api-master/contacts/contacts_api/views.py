from rest_framework.views import APIView
from contacts_api.models import Contact 
from contacts_api.serializer import ContactSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import authenticate


class ContactList(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

class ContactCreate(APIView):
    def post(self, request):
        serializer = ContactSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDetail(APIView):
    def get_contact_by_pk(self, pk):
        try:
            contact = Contact.objects.get(pk=pk)
            return contact
        except:
            return Response({
            'error':'Contact not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        contact = self.get_contact_by_pk(pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def put(self, request, pk):
        contact = self.get_contact_by_pk(pk)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contact = self.get_contact_by_pk(pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         try:
#             data = JSONParser().parse(request)  # data is a dictionary
#             user = User.objects.create_user(username=data['username'], password=data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#             return JsonResponse({'token': str(token)}, status=201)
#         except IntegrityError:
#             return JsonResponse({'error': 'username taken. choose another username'}, status=400)
#     elif request.method == 'GET':  # Return empty response for GET requests
#         return JsonResponse({}, status=200)
    

# @csrf_exempt
# def login(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         user = authenticate(request, username=data['username'], password=data['password'])
#         if user is None:
#             return JsonResponse({'error': 'unable to login. check username and password'}, status=400)
#         else:  # return user token
#             try:
#                 token = Token.objects.get(user=user)
#             except Token.DoesNotExist:  # if token not in db, create a new one
#                 token = Token.objects.create(user=user)
#             return JsonResponse({'token': str(token)}, status=201)
#     elif request.method == 'GET':
#         return JsonResponse({'error': 'GET method not allowed'}, status=405)