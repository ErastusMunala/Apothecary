from django.db import models

# Create your models here.
class Product:
    def __init__(self, image:str, name: str, cost: int, quantity: int):
        self.image = image
        self.name = name
        self.cost = cost
        self.quantity = quantity