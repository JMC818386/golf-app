from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'par']

class HoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hole
        fields = ['id', 'course', 'number', 'par', 'distance']

        

class RoundSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', required=False)
    formatted_date = serializers.SerializerMethodField()
    stroke_total = serializers.SerializerMethodField()
    putt_total = serializers.SerializerMethodField()
    
    class Meta:
        model = Round
        fields = ['id', 'user', 'course', 'course_name', 'date', 'round_length', 'stroke_total', 'putt_total', 'formatted_date']

    def get_course_name(self, obj):
        course_name = obj.name
        return course_name

    def get_formatted_date(self, obj):
        round_datetime = obj.date
        return round_datetime.strftime('%m-%d-%Y')

    def get_putt_total(self, obj):
        scores = HoleScore.objects.filter(hole_round_id=obj.id)
        putt_total = 0
        for score in scores:
            putt_total += score.putts
        return putt_total

    def get_stroke_total(self, obj):
        scores = HoleScore.objects.filter(hole_round_id=obj.id)
        stroke_total = 0
        for score in scores:
            stroke_total += score.strokes
        return stroke_total 

class HoleScoreSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    class Meta:
        model = HoleScore
        fields = ['user', 'hole_round', 'hole', 'strokes', 'swings', 'putts']
