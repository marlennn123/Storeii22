from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'username', 'email', 'age', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_image', 'category_name']



class SubCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'sub_category_name']


class CategoryDetailSerializers(serializers.ModelSerializer):
    category_sub = SubCategoryListSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'category_sub']


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']



class ProductListSerializers(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    product_images = ProductImageSerializers(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_images', 'price', "product_type",
                  'get_avg_rating', 'get_count_people', 'created_date']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class SubCategoryDetailSerializers(serializers.ModelSerializer):
    products = ProductListSerializers(read_only=True, many=True)

    class Meta:
        model = SubCategory
        fields = ['sub_category_name', 'products']


class ReviewSerializers(serializers.ModelSerializer):
    created_date = serializers.DateField(format('%d-%m-%Y'))
    user = UserProfileReviewSerializers()

    class Meta:
        model = Review
        fields = ['user', "text", "stars", "created_date"]


class ProductDetailSerializers(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    product_images = ProductImageSerializers(read_only=True, many=True)
    subcategory = SubCategoryListSerializers()
    product_reviews = ReviewSerializers(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product_name', 'subcategory', 'price', 'article_number', "product_type",
                  'video', 'product_images', 'description', 'created_date',
                  'get_avg_rating', 'get_count_people', 'product_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
