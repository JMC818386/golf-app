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
from django.db.models import Sum

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

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Round.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



    # def get_queryset(self, request, round_id):
    #     queryset = Round.objects.all()
    #     unique_round = Round.objects.get(id=round_id)
    #     course_name = unique_round.course.name
    #     date = unique_round.date.strftime("%m-%d-%Y")
    #     total_score = unique_round.total_score
    #     total_putts = unique_round.holescore_set.aggregate(total_putts=models.Sum('putts'))['total_putts']
    #     par = unique_round.course.par
    #     round_length = unique_round.round_length
    #     holes = Hole.objects.filter(course=unique_round.course)
    #     hole_scores = HoleScore.objects.filter(hole_round=unique_round)

    #     hole_data = []
    #     for hole in holes:
    #         hole_score = hole_scores.get(hole=hole)
    #         hole_data.append({'hole_number': hole.number, 'par': hole.par, 'strokes': hole_score.strokes, 'putts': hole_score.putts, 'score_difference': hole_score.strokes - hole.par})

    #     data = {
    #         'course_name': course_name,
    #         'date': date,
    #         'score_vs_par': total_score - par,
    #         'total_putts': total_putts,
    #         'total_score': total_score,
    #         'round_length': round_length,
    #         'hole_data': hole_data
    #     }

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return Round.objects.filter(user=user)
        
    #     return Round.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class HoleScoreViewSet(viewsets.ModelViewSet):
    queryset = HoleScore.objects.all()
    serializer_class = HoleScoreSerializer
    http_method_names = ('get', 'post', 'put', 'patch', 'delete')

