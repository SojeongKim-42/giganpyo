# product/serializers.py
from rest_framework import serializers
from subjectapp.models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth=1


class SubjectProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectProf
        fields = '__all__'


class SubjectTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTime
        fields = '__all__'
