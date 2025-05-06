from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ProductSerializer, MessageSerializer, OrderSerializer, OrderItemSerializer, ImageSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, filters
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.generics import ListCreateAPIView
from django.db.models import Q
from .models import Product, Message, Order, OrderItem, Image
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F
import jwt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings

# Create your views here.
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'detail': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)


# Login View - Authenticate user and provide JWT
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Missing username or password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        response = Response({'message': 'Login successful'})

        # Set JWT as a cookie with proper flags for security
        response.set_cookie(
            'jwt', str(access_token),
            httponly=True,
            secure=settings.SECURE_COOKIE,  # Use the SECURE_COOKIE setting
            samesite='Lax',  # This is generally good for security
            max_age=settings.JWT_EXPIRATION_TIME  # Set expiration time if desired
        )

        return response



# Logout View - Invalidate JWT (delete from cookies)
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt', path='/')  # Specify path and domain as needed
        return response


# Token Verification - Check if the provided token is valid
class VerifyToken(APIView):
    permission_classes = []

    def get(self, request):
        try:
            token = request.COOKIES.get("jwt")
            if not token:
                return Response({"detail": "No access token"}, status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get("user_id")

            if not user_id:
                return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"detail": "Token is valid", "user_id": user_id}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"detail": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Products
class ProductList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'category', 'price', 'stock', 'rating']  # fields users can order by
    ordering = ['id']

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        queryset = Product.objects.all()

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset
    
    def perform_create(self, serializer):
        if not self.request.user.is_superuser:  # or use is_superuser
            raise PermissionDenied("Only admins can create products.")
        serializer.save()

class ProductView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, productId):
        product = get_object_or_404(Product, id=productId)
        serializer = ProductSerializer(instance=product, many=False)
        return Response(serializer.data)

    def put(self, request, productId):
        product = get_object_or_404(Product, id=productId)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Product successfully updated'}, status=status.HTTP_202_ACCEPTED)
        return Response({"Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, productId):
        product = get_object_or_404(Product, id=productId)
        product.delete()
        return Response({'Product Succesfully Deleted'}, status=status.HTTP_204_NO_CONTENT)


# Messages
class MessageList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MessageSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        if search_query:
            return Message.objects.filter(Q(title__icontains=search_query) | Q(sender__icontains=search_query))
        return Message.objects.all().order_by("id")
    
    def perform_create(self, serializer):
        serializer.save()

class MessageView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, messageId):
        message = get_object_or_404(Message, id=messageId)
        serializer = MessageSerializer(message, many=False)
        return Response(serializer.data)

    def put(self, request, messageId):
        message = get_object_or_404(Message, id=messageId)
        serializer = MessageSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message successfully updated'}, status=status.HTTP_202_ACCEPTED)
        return Response({'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, messageId):
        message = get_object_or_404(Message, id=messageId)
        message.delete()
        return Response({'Message Succesfully Deleted'}, status=status.HTTP_204_NO_CONTENT)


# Orders
class OrderList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'total', 'name', 'status', 'date']  # fields users can order by
    ordering = ['-date']

    def get_queryset(self):
        # Get the status filter from query params
        status_filter = self.request.query_params.get('status', '')
        queryset = Order.objects.all()

        # Apply the status filter if it is provided
        if status_filter:
            queryset = queryset.filter(status__icontains=status_filter)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

class OrderView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, orderId):
        order = get_object_or_404(Order, id=orderId)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

    def put(self, request, orderId):
        order = get_object_or_404(Order, id=orderId)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Order successfully updated'}, status=status.HTTP_202_ACCEPTED)
        return Response({'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, orderId):
        order = get_object_or_404(Order, id=orderId)
        order.delete()
        return Response({'Order Succesfully Deleted'}, status=status.HTTP_204_NO_CONTENT)

class OrderItemList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search', '')
        if search_query:
            return OrderItem.objects.filter(Q(name__icontains=search_query))
        return OrderItem.objects.all().order_by("id")
    
    def perform_create(self, serializer):
        serializer.save()

class OrderItemView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, requst, orderId):
        orderItem = OrderItem.objects.filter(order=orderId)
        serializer = OrderItemSerializer(orderItem, many=True)
        return Response(serializer.data)


# Images -- NOT REQUIRED WITH CREATE AND UPDATE IMAGE FUNCTIONALITY IN PRODUCT SERIALIZER
class ImageList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()

class ImageView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, imageId):
        image = get_object_or_404(Image, id=imageId)
        serializer = ImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Image successfully updated'}, status=status.HTTP_202_ACCEPTED)
        return Response({'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, imageId):
        image = get_object_or_404(Image, id=imageId)
        image.delete()
        return Response({'Image Succesfully Deleted'}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def cumulative_monthly_stats(request):
    monthly_data = (
        OrderItem.objects
        .annotate(month=TruncMonth('order__date'))
        .values('month')
        .annotate(
            revenue=Sum(F('quantity') * F('product__price')),
            cost=Sum(F('quantity') * F('product__cogs')),
        )
        .order_by('month')
    )

    # Compute cumulative values
    cumulative_revenue = 0
    cumulative_cost = 0
    cumulative_data = []
    for item in monthly_data:
        cumulative_revenue += item['revenue']
        cumulative_cost += item['cost']
        cumulative_data.append({
            "month": item['month'].strftime("%Y-%m"),  # Format as "2025-05"
            "revenue": cumulative_revenue,
            "cost": cumulative_cost,
            "profit": cumulative_revenue - cumulative_cost
        })

    return Response(cumulative_data)

    



