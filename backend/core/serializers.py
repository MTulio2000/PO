from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from core.models import *

def get_label(choices,value):
            for data in choices:
                if value == data[0]:
                    return data[1]

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            'id',
            'description',
            'carbohydrate',
            'cholesterol',
            'fiber',
            'kilocalories',
            'protein',
            'saturated_fat',
            'iron',
            'sodium',
            'price',
            'quantity'
    ]

class RestricaoSerializer(serializers.ModelSerializer):
    
    comparacao = ChoiceField(choices=Restricao.COMPARISON_CHOICES)
    tipo = ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        model = Restricao
        fields = ['id','dieta','comparacao','tipo','valor']

class DietaSerializer(serializers.ModelSerializer):
    variavel = ChoiceField(choices=TYPE_CHOICES)
    objetivo = ChoiceField(choices=Dieta.TARGET_CHOICES)
    restricoes = serializers.SerializerMethodField()

    class Meta:
        model = Dieta
        fields = ['id','nome','objetivo','variavel','restricoes']
    
    def get_restricoes(self,instance):
        restricoes = []

        for restricao in Restricao.objects.filter(dieta=instance.id):
            print(restricao.__dict__)
            restricoes.append({
                "id":restricao.id,
                "comparacao":get_label(Restricao.COMPARISON_CHOICES,restricao.comparacao),
                "tipo":get_label(TYPE_CHOICES,restricao.tipo),
                "valor":restricao.valor
            })
            
        return restricoes

    
