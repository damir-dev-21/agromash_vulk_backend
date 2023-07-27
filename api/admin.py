from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from .models import User, Item, ItemMark, Producer, Category, Car, Order, Mark
from django.utils.html import format_html
from django.db import models


# class AdminImageWidget(AdminFileWidget):
#     def render(self, name, value, attrs=None):
#         output = []
#         if value and getattr(value, "url", None):
#             image_url = value.url
#             file_name = str(value)
#             output.append(
#                 f' <a href="{image_url}" target="_blank"><img src="{image_url}" alt="${file_name}" width="150" height="150"  style="object-fit: cover;"/></a>  ')
#         output.append(super(AdminFileWidget, self).render(name, value, attrs))
#         return mark_safe(u''.join(output))

class CustomAdminFileWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        if hasattr(value, "url"):
            result.append(
                f'''<a href="{value.url}" target="_blank">
                      <img 
                        src="{value.url}" alt="{value}" 
                        width="100" height="100"
                        style="object-fit: cover;"
                      />
                    </a>'''
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))

class MarkInlineAdmin(admin.TabularInline):

    #readonly_fields = ['image_tag']
    model = ItemMark
    extra = 0

    # formfield_overrides = {
    #     models.ImageField: {'widget': AdminImageWidget}
    # }


class MarksInlineAdmin(admin.TabularInline):

    model = Mark
    extra = 0
    #readonly_fields = ('image_preview',)
    formfield_overrides = {
        models.ImageField: {'widget': CustomAdminFileWidget}
    }


class OrderInlineAdmin(admin.TabularInline):
    model = Order
    extra = 0


@admin.register(Category)
class Categories(admin.ModelAdmin):
    fieldsets = (
        ('Информация о категориях', {
            'fields': ('name',)
        }),
    )
    list_display = ('id', 'name')


@admin.register(Producer)
class Producers(admin.ModelAdmin):
    fieldsets = (
        ('Информация о бренде', {
            'fields': ('name', 'passenger', 'truck', 'condition','summa')
        }),
    )
    list_display = ('id', 'name', 'passenger', 'truck')


@admin.register(Car)
class Cars(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="max-width:200px; max-height:200px"/>')

    fieldsets = (
        ('Информация о машинах', {
            'fields': ('number', 'image_tag')
        }),
    )
    readonly_fields = ['image_tag', 'created_at']
    list_display = ('id', 'number', 'image_tag')


@admin.register(Mark)
class Marks(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.photo.url}" style="max-width:200px; max-height:200px"/>')

    fieldsets = (
        ('Информация о машинах', {
            'fields': ('mark', 'image_tag', 'order', )
        }),
    )
    readonly_fields = ['image_tag', 'created_at']

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
            'fields': ('name', 'email', 'fio', 'password', 'district', 'latitude', 'longitude', 'balance', 'is_superuser')
        }),
    )
    list_display = ('id', 'name', 'is_superuser')
    inlines = [OrderInlineAdmin]


@admin.register(Item)
class Items(admin.ModelAdmin):

    inlines = [MarkInlineAdmin]

    fieldsets = (
        ('Информация о товаре', {
            'fields': ('name',  'category', 'producer', 'price')
        }),
    )
    list_display = ('id', 'name')
