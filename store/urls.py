from django.urls import path


urlpatterns = [
    path('', HomePageView, name='home'),
    path('products/', ProductsView, name='products-list'),
    path('products/<uuid:product_id>/', ProductsDetailView, name='product-detail'),
    path('<int:user_id>/wishlist/', WishlistView, name='wishlist')
]
