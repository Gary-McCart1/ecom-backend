
from django.urls import path
from .views import Register, Login, Logout, VerifyToken
from . import views

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('verify/', VerifyToken.as_view(), name='verify-token'),

    path('products/', views.ProductList.as_view()),
    path('products/<int:productId>/', views.ProductView.as_view()),

    path('messages/', views.MessageList.as_view()),
    path('messages/<int:messageId>/', views.MessageView.as_view()),

    path('orders/', views.OrderList.as_view()),
    path('orders/<int:orderId>/', views.OrderView.as_view()),

    path('orderitems/', views.OrderItemList.as_view()),
    path('orderitems/<int:orderId>/', views.OrderItemView.as_view()),

    path('images/', views.ImageList.as_view()),

    path('cumulative-monthly-stats/', views.cumulative_monthly_stats)
]