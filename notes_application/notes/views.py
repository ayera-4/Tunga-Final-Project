from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Notes, CustomUser
from .serializers import NotesSerializer, UserRegistrationSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Note List':'/note-list/',
        'Note View':'/note-view/<str:pk>/',
        'Create':'/note-add/',
        'Update':'/note-update/<str:pk>/',
        'Delete':'/note-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def noteList(request):
    notes = Notes.objects.all()
    serializer = NotesSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def noteView(request, pk):
    note = Notes.objects.get(id=pk)
    serializer = NotesSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def noteAdd(request):
    serializer = NotesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def noteUpdate(request, pk):
    note = Notes.objects.get(id=pk)
    serializer = NotesSerializer(instance=note, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def noteDelete(request, pk):
    note = Notes.objects.get(id=pk)
    note.delete()
    return Response("Note deleted")

"""@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = None
        if '@' in email:
            try:
                user = CustomUser.objects.get(email=email)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
