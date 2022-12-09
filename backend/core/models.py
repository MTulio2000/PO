from django.db import models

TRADUCTION_CHOICES = (
    (0,"carbohydrate"),
    (1,"cholesterol"),
    (2,"fiber"),
    (3,"kilocalories"),
    (4,"protein"),
    (5,"iron"),
    (6,"sodium"),
    (7,"saturated_fat"),
    (8,"price")
)

TYPE_CHOICES = (
    (0,"Carboidratos"),
    (1,"Colesterol"),
    (2,"Fibras"),
    (3,"Kilocalorias"),
    (4,"Proteínas"),
    (5,"Ferro"),
    (6,"Sódio"),
    (7,"Gordura Saturada"),
    (8,"Preço")
)

class Food(models.Model):
    class Meta:
        verbose_name_plural = "Comidas"
    description = models.CharField(max_length = 2048)
    carbohydrate = models.FloatField()
    cholesterol = models.FloatField()
    fiber = models.FloatField()
    kilocalories = models.FloatField()
    protein = models.FloatField()
    saturated_fat = models.FloatField()
    iron = models.FloatField()
    sodium = models.FloatField()
    quantity = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return self.description
    

class Dieta(models.Model):
    nome = models.CharField(max_length=250)
    variavel = models.IntegerField(choices=TYPE_CHOICES)

    TARGET_CHOICES = (
        (0,"Maximizar"),
        (1,"Minimizar")
    )

    objetivo = models.IntegerField(choices=TARGET_CHOICES)
    
    def __str__(self):
        return self.nome

class Restricao(models.Model):
    class Meta:
        verbose_name_plural = "Restrições"
        verbose_name = "Restrição"
    COMPARISON_CHOICES = (
        (0,"Menor"),
        (1,"Menor ou igual"),
        (2,"Igual"),
        (3,"Maior ou igual"),
        (4,"Maior")
    )
    
    dieta = models.ForeignKey(Dieta,on_delete=models.CASCADE)
    comparacao = models.IntegerField(choices=COMPARISON_CHOICES)
    tipo = models.IntegerField(choices = TYPE_CHOICES)
    valor = models.FloatField(default=0)
