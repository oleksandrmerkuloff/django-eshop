from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'address',
        'status',
        'notes',
        'create_at',
    )
    list_display = ('user', 'status', 'created_at')
    list_display_links = ('user',)
    ordering = ('-created_at', 'status')
    readonly_fields = ('create_at')
    list_per_page = 20
    list_filter = ('created_at', 'status')
    search_fields = ('user__name', 'status', 'address')
    inlines = [
        OrderItemInline
    ]

# I will think about OrderItemInline


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
