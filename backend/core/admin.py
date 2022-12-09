from django.contrib import admin
from core.models import *

class Foods(admin.ModelAdmin):
    fields = (
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
    )
    search_fields = ('id','description')
    list_display = (
        'id',
        'description',
        'carbohydrate',
        'cholesterol',
        'fiber',
        'kilocalories',
        'protein',
        'iron',
        'sodium',
        'price',
        'quantity'
    )

class Restricoes(admin.ModelAdmin):
    fields = ['dieta','tipo','comparacao','valor']
    search_fields = ['id','tipo','dieta','valor']
    list_display = ['id','tipo','dieta','comparacao','valor']

class Dietas(admin.ModelAdmin):
    fields = ['nome','variavel','objetivo']
    search_fields = ['id','nome',]
    list_display = ['id','nome','variavel','objetivo']
    
admin.site.register(Food,Foods)
admin.site.register(Dieta,Dietas)
admin.site.register(Restricao,Restricoes)