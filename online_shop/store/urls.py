from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileViewSet, CategoryListAPIView,
                    SubCategoryListAPIView, SubCategoryDetailAPIView, ProductListAPIView,
                    ProductDetailAPIView, CategoryDetailAPIView,ReviewViewSet,
                    CartViewSet, CartItemViewSet, RegisterView, LoginView, LogoutView)

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cart_item', CartItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>/', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]