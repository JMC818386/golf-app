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
    hole_scores = serializers.SerializerMethodField()
    
    class Meta:
        model = Round
        fields = ['id', 'user', 'course', 'course_name', 'date', 'round_length', 'stroke_total', 'putt_total', 'formatted_date', 'hole_scores']

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

    def get_hole_scores(self, obj):
        hole_scores = []
        scores = HoleScore.objects.filter(hole_round_id=obj.id).order_by('hole__number')
        holes = Hole.objects.filter(course=obj.course).order_by('number')

        for score, hole in zip(scores, holes):
            par = hole.par
            strokes = score.strokes
            difference = strokes - par
            classification = None

            if difference == -2:
                classification = 'eagle'
            elif difference == -1:
                classification = 'birdie'
            elif difference == 0:
                classification = 'par'
            elif difference == 1:
                classification = 'bogey'
            else:
                classification = 'bogey+'

            hole_score_data = {
                'hole_number': hole.number,
                'strokes': strokes,
                'par': par,
                'difference': difference,
                'classification': classification
            }

            hole_scores.append(hole_score_data)

        # calculate total eagles, birdies, pars, bogeys, and bogeys+
        eagle_count = sum(score['classification'] == 'eagle' for score in hole_scores)
        birdie_count = sum(score['classification'] == 'birdie' for score in hole_scores)
        par_count = sum(score['classification'] == 'par' for score in hole_scores)
        bogey_count = sum(score['classification'] == 'bogey' for score in hole_scores)
        bogeyplus_count = sum(score['classification'] == 'bogey+' for score in hole_scores)

        # create dictionary with total counts
        counts = {
            'eagles': eagle_count,
            'birdies': birdie_count,
            'pars': par_count,
            'bogeys': bogey_count,
            'bogeys+': bogeyplus_count
        }

        return {'scores': hole_scores, 'counts': counts}

class HoleScoreSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)
    class Meta:
        model = HoleScore
        fields = ['user', 'hole_round', 'hole', 'strokes', 'swings', 'putts']
