# product/serializers.py
from rest_framework import serializers
from subjectapp.models import *
from parse import parse


class SubjectSerializer(serializers.ModelSerializer):
    times = serializers.SerializerMethodField(read_only=True)
    professors = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'code', 'credit', 'department', 'location', 'times', 'professors', 'select_person', 'max_person']

    def get_times(self, obj):
        return obj.times.values('day', 'start_h', 'start_m', 'fin_h', 'fin_m')

    def get_professors(self, obj):
        return obj.professors.values('name')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth = 1


# class ProfessorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Professor
#         fields = ['name']


# class TableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Table
#         fields = '__all__'


# class TimeSerializer(serializers.ModelSerializer):
#     start_h = serializers.SerializerMethodField()
#     start_m = serializers.SerializerMethodField()
#     fin_h = serializers.SerializerMethodField()
#     fin_m = serializers.SerializerMethodField()

#     def get_start_h(self, obj):
#         start_time = parse("{}:{}", obj.start_time)
#         return int(start_time[0])

#     def get_start_m(self, obj):
#         start_time = parse("{}:{}", obj.start_time)
#         return int(start_time[1])

#     def get_fin_h(self, obj):
#         fin_time = parse("{}:{}", obj.fin_time)
#         return int(fin_time[0])

#     def get_fin_m(self, obj):
#         fin_time = parse("{}:{}", obj.fin_time)
#         return int(fin_time[1])

#     class Meta:
#         model = Time
#         fields = ['day', 'start_h', 'start_m', 'fin_h', 'fin_m']
