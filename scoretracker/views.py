from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import *
from .serializers import *

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')

class HoleViewSet(viewsets.ModelViewSet):
    queryset = Hole.objects.all()
    serializer_class = HoleSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Hole.objects.all()
        course = self.request.query_params.get('selected_course')
        print('COURSE IS', course)
        if course is not None:
            queryset = queryset.filter(course_id=course)
        return queryset

class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')

class HoleScoreViewSet(viewsets.ModelViewSet):
    queryset = HoleScore.objects.all()
    serializer_class = HoleScoreSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')