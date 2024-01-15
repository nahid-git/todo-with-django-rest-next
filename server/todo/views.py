from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


class HomeView(ListAPIView):
    serializer_class = None

    def list(self, request, *args, **kwargs):
        api_list = {
            "signup": f"{request.build_absolute_uri()}signup",
            "login": f"{request.build_absolute_uri()}login",
            "profile": f"{request.build_absolute_uri()}profile",
            "todos": f"{request.build_absolute_uri()}todos",
        }
        return Response(api_list, status=status.HTTP_200_OK)


class UserProfile(ListAPIView):
    serializer_class = CustomUserSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return CustomUser.objects.filter(id=user_id)


class RegisterUser(CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = CustomUser.objects.create_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            return Response({'message': 'User registration successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.data['email'])
            user.save()
            refresh = RefreshToken.for_user(user)
            token = {
                'access': str(refresh.access_token),
            }
            return Response({
                'token': token,
                'email': user.email
            })
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class TodoView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        request.data['title'] = request.data.get('title', '').strip()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Todo added Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user_id=user).order_by('-id')

        # return super().update(request, *args, **kwargs)


class TodoSingle(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'todo_id'
    queryset = Todo.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.request.user
        todo_instance = self.get_object()

        request.data['user'] = user.id
        super().update(request, *args, **kwargs)
        return Response({'message': 'Todo update successfully!'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'Todo delete successfully!'}, status=status.HTTP_200_OK)
