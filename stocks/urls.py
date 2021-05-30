from django.urls import path
from . import views


# /api/stoocks/: GET, POST
# /api/stoocks/<id>: GET, PUT, DELETE
urlpatterns = [
    path('', views.index),
    path('api/stocks/', views.allStocks),
    path('api/stocks/<int:id>/', views.stock)
]