from rest_framework import serializers

from predictor.models import StockPrice

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'