from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('buy/', views.buy_lotto, name='buy_lotto'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/draw/', views.admin_draw, name='admin_draw'),
    path('charge/', views.charge_money, name='charge_money'), # 자산 충전 주소 추가
]
