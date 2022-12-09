from core.serializers import *
from django.http import JsonResponse

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class RestricaoViewSet(viewsets.ModelViewSet):
    queryset = Restricao.objects.all()
    serializer_class = RestricaoSerializer

class DietaViewSet(viewsets.ModelViewSet):
    queryset = Dieta.objects.all()
    serializer_class = DietaSerializer


from scipy.optimize import linprog
import numpy as np
import json
def get_cardapios(request,id,quantity):
    cardapios = []

    dieta = Dieta.objects.filter(id=id)[0]
    operation = dieta.objetivo
    variavel = get_label(TRADUCTION_CHOICES,dieta.variavel)

    objetivo = []
    

    # fields = {
    #     "A_ub":np.matrix(),
    #     "B_ub"
    # }

    
    restricoes = Restricao.objects.filter(dieta=id)

    answers = {
        "Ingredientes":[],
        "Pratos" : [],
        "Values":[],
    }
    for _ in range(quantity):
        foods = Food.objects.exclude(quantity=0)
        A_ub = [[] for _ in range(restricoes.count()+foods.count())]
        b_ub = []
        c = []
        r=0
        for restricao in restricoes:
            signal = 1 if restricao.comparacao < 2 else -1
            for food in foods:
                A_ub[r].append(signal*food.__dict__[get_label(TRADUCTION_CHOICES,restricao.tipo)])
            r+=1
            b_ub.append(signal*restricao.valor)
        f = 0
        for _ in range(foods.count()):
            for i in range(foods.count()):
                A_ub[r+f].append(1 if i == f else 0)
            b_ub.append(foods[f].quantity)
            f+=1
        ids = []
        signal = 1 if dieta.objetivo else -1
        for food in foods:
            ids.append(food.id)
            c.append(food.__dict__[variavel]*signal)

        result = linprog(np.array(c),A_ub=np.array(A_ub),b_ub=np.array(b_ub))
        answer = {}
        values = {
            "Carboidratos":0,
            "Colesterol":0,
            "Fibras":0,
            "Kilocalorias":0,
            "Proteínas":0,
            "Ferro":0,
            "Sódio":0,
            "Gordura Saturada":0,
            "Preço":0,
        }
        for res,i in zip(result["x"],range(foods.count())):
            if res:
                
                answer[foods[i].description] = res
                values["Carboidratos"] = foods[i].carbohydrate
                values["Colesterol"] += foods[i].cholesterol
                values["Fibras"] += foods[i].fiber
                values["Kilocalorias"] += foods[i].kilocalories
                values["Proteínas"] += foods[i].protein
                values["Ferro"] += foods[i].iron
                values["Sódio"] += foods[i].sodium
                values["Gordura Saturada"] += foods[i].saturated_fat
                values["Preço"] += foods[i].price
                foods[i].quantity -= res
                foods[i].save()

        if len(answers["Pratos"])==0 or answer != answers["Ingredientes"][-1]:
            answers["Pratos"].append(1)
            answers["Ingredientes"].append(answer)
            answers["Values"].append(values)
        else:
            answers["Pratos"][-1]+=1
    
    return JsonResponse(answers)
