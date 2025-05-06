from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import Product, Message, Order, OrderItem, Image

## LOGIN SERIALIZERS

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "password_confirm"]
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('Passwords do not match')
        return attrs

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
                if not user:
                    raise serializers.ValidationError("No user found")
            except ValidationError as e:
                raise serializers.ValidationError(e.messages)
        else:
            raise serializers.ValidationError("Username and password are both required")
        attrs['user'] = user
        return attrs

# MODEL SERIALIZERS
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["url"]
    
    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.product = validated_data.get('product', instance.product)

class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ["id", "name", "category", "price", "originalPrice", "stock", "rating", "cogs", "description", "images"]
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            Image.objects.create(product=product, **image_data)

        return product
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        if images_data is not None:
            current_images = set(instance.images.values_list('id', flat=True))
            new_images = set(image['id'] for image in images_data if 'id' in image)
            images_to_delete = current_images - new_images
            instance.images.filter(id__in=images_to_delete).delete()

            # Loop through new images and either update or create them
            for image_data in images_data:
                if 'id' in image_data:
                    # Update existing image
                    image = instance.images.get(id=image_data['id'])
                    image.url = image_data.get('url', image.url)
                    image.save()
                else:
                    # Create new image if no 'id' is present
                    Image.objects.create(product=instance, **image_data)
        return instance

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
    
    def update(self, instance, validated_data):
        instance.sender = validated_data.get('sender', instance.sender)
        instance.email = validated_data.get('email', instance.email)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.body = validated_data.get('body', instance.body)
        instance.date = validated_data.get('date', instance.date)
        instance.read = validated_data.get('read', instance.read)

        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "name", "email", "address", "phone", "date", "status", "shippingMethod", "trackingNumber", "total", "products"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.date = validated_data.get('date', instance.date)
        instance.status = validated_data.get('status', instance.status)
        instance.shippingMethod = validated_data.get('shippingMethod', instance.shippingMethod)
        instance.trackingNumber = validated_data.get('trackingNumber', instance.trackingNumber)
        instance.total = validated_data.get('total', instance.total)

        instance.save()
        return instance
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "order", "product"]


