from django.contrib import admin
from .models import User,Item, ItemMark,Producer,Category,Car,Order,Mark


class MarkInlineAdmin(admin.TabularInline):
    model = ItemMark
    extra = 0

class MarksInlineAdmin(admin.TabularInline):
    model = Mark
    extra=0    

class OrderInlineAdmin(admin.TabularInline):
    model = Order
    extra = 0    

@admin.register(Category)
class Categories(admin.ModelAdmin):
    fieldsets = (
        ('Информация о категориях', {
            'fields' : ('name',)
        }),
    )
    list_display = ('id', 'name')

@admin.register(Producer)
class Producers(admin.ModelAdmin):
    fieldsets = (
        ('Информация о бренде', {
            'fields': ('name', 'passenger', 'truck', 'condition')
        }),
    )
    list_display = ('id','name', 'passenger', 'truck')


@admin.register(Car)
class Cars(admin.ModelAdmin):
    fieldsets = (
        ('Информация о машинах', {
            'fields': ('number' , 'created_at')
        }),
    )
    readonly_fields = ['created_at']
    list_display = ('id', 'number')


@admin.register(Mark)
class Marks(admin.ModelAdmin):
    fieldsets = (
        ('Информация о машинах', {
            'fields': ('mark', 'photo', 'order', 'created_at')
        }),
    )
    readonly_fields = ['created_at']
    list_display = ('id', 'mark')


@admin.register(Order)
class Orders(admin.ModelAdmin):
    fieldsets = (
        ('Информация о машинах', {
            'fields': ('carNumber', 'brand', 'user', 'created_at')
        }),
    )
    readonly_fields = ['created_at']
    list_display = ('id', 'carNumber', 'brand')
    inlines = [MarksInlineAdmin]


@admin.register(User)
class Users(admin.ModelAdmin):
    fieldsets = (
        ('Информация о пользователе', {
            'fields': ('name', 'email', 'fio', 'password', 'district','latitude', 'longitude', 'balance', 'is_superuser')
        }),
    )
    list_display = ('id', 'name', 'is_superuser')
    inlines = [OrderInlineAdmin]


@admin.register(Item)
class Items(admin.ModelAdmin):

    inlines = [MarkInlineAdmin]

    fieldsets = (
        ('Информация о товаре', {
            'fields': ('name',  'category', 'producer','price')
        }),
    )
    list_display = ('id', 'name')


