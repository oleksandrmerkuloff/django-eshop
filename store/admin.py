from django.contrib import admin

from store.models import Category, Product, ProductImage, Review
from store.models import Wishlist, WishlistItem


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'price',
        'product_code',
        'description',
        'details',
        'in_stock',
        'category',
        'created_at',
        )
    readonly_fields = ('created_at',)
    list_display = ('name', 'product_code', 'price', 'in_stock', 'created_at')
    list_display_links = ('name',)
    list_filter = ('price', 'created_at', 'category', 'in_stock')
    list_per_page = 50
    search_fields = ('name', 'category__name', 'product_code',)
    ordering = ('name', '-created_at', 'in_stock')
    sortable_by = ('name', 'price', 'in_stock', 'category')
    inlines = [
        ProductImageInline,
    ]


class ReviewAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'product',
        'score',
        'content',
        'created_at',
    )
    readonly_fields = ('created_at',)
    list_display = ('user', 'product', 'score')
    list_display_links = ('user', 'product',)
    list_filter = ('user', 'product', 'created_at')
    list_per_page = 50
    search_fields = ('user__email', 'product__name',)
    sortable_by = ('user', 'product', 'score',)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
