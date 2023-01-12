# product/serializers.py
from rest_framework import serializers
from subjectapp.models import *
from parse import parse


class TimeSerializer(serializers.ModelSerializer):
    start_h = serializers.SerializerMethodField()
    start_m = serializers.SerializerMethodField()    
    fin_h = serializers.SerializerMethodField()
    fin_m = serializers.SerializerMethodField()

    def get_start_h(self, obj):
        start_time = parse("{}:{}", obj.start_time)
        return int(start_time[0])

    def get_start_m(self, obj):
        start_time = parse("{}:{}", obj.start_time)
        return int(start_time[1])

    def get_fin_h(self, obj):
        fin_time = parse("{}:{}", obj.fin_time)
        return int(fin_time[0])

    def get_fin_m(self, obj):
        fin_time = parse("{}:{}", obj.fin_time)
        return int(fin_time[1])

    class Meta:
        model = Time
        fields = ['day', 'start_h', 'start_m', 'fin_h', 'fin_m']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['name']


class SubjectProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectProf
        fields = ['professor']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        prof = Professor.objects.get(id=instance.professor_id)
        response['professor'] = ProfessorSerializer(prof).data
        return response



class SubjectTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTime
        fields = ['time']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        time= Time.objects.get(id=instance.time_id)
        response['time'] = TimeSerializer(time).data
        return response



class SubjectSerializer(serializers.ModelSerializer):
    sub_prof_subject = SubjectProfSerializer(many=True, read_only=True)
    sub_time_subject = SubjectTimeSerializer(many=True, read_only=True)
    class Meta:
        model = Subject
        fields = ['name', 'code', 'credit', 'department', 'is_required',
                  'is_major', 'sub_prof_subject', 'sub_time_subject', 'select_person']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth=1

