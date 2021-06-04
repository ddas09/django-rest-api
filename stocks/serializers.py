from rest_framework import serializers
from .models import Stock

# Serializer class to convert the model to json
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'