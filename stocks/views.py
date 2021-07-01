from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StockSerializer
from .models import Stock


def index(request):
    return render(request, 'index.html')


# API endpoints
@api_view(['GET', 'POST'])
def allStocks(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        stocks_serializer = StockSerializer(stocks, many=True)
        # safe=False allows non-dict objects to be serialized
        return JsonResponse(stocks_serializer.data, safe=False)

    elif request.method == 'POST':
        stock_serializer = StockSerializer(data=request.data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse(stock_serializer.data)
        else:
            return JsonResponse({"message": "Stock already exists in database"}, status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET', 'PUT', 'DELETE'])
def stock(request, id):
    try:
        stock = Stock.objects.get(pk=id)
    except Stock.DoesNotExist:
        msg = {'message': f'The stock with id = {id} does not exist'}
        return JsonResponse(msg, status=status.HTTP_404_NOT_FOUND)    

    if request.method == 'GET':
        stock_serializer = StockSerializer(stock)
        return JsonResponse(stock_serializer.data)
    
    elif request.method == 'PUT':
        stock_serializer = StockSerializer(stock, data=request.data)
        if stock_serializer.is_valid():
            stock_serializer.save()
            return JsonResponse(stock_serializer.data)    
        else:
            return JsonResponse({"message": "Couldn't update stock with provided details"}, status=status.HTTP_400_BAD_REQUEST)    
    
    elif request.method == 'DELETE':
        stock.delete()
        msg = {'message': f'Stock with id = {id} was deleted successfully'}
        return JsonResponse(msg, status=status.HTTP_204_NO_CONTENT)