from rest_framework import serializers
from .models import *

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
"""
este es un ejemplo de como hacerlas mas personalizadas, arreglar todo eso asi
fields = ['id', 
            'name', 
            'description', 
            'created_at',
            'updated_at',
            'deleted_at',  ]

ademas, se debe colocar validacion de cada uno de los modelos (ver que no se repitan los nombres,
que sean unicos), ademas seguriad.

"""