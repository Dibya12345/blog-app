from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Blog
from .serializers import BlogSerializer, UserSerializer
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly  
from django.contrib.auth import authenticate
from rest_framework.views import APIView




class BlogListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()



class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response_data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


