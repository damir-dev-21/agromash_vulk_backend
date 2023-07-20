from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
import json
from django.utils.safestring import mark_safe


    


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Car(TimeBasedModel):

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорты'

    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=200, verbose_name='Номер машины')
    image = models.ImageField(upload_to='media/cars',default=None)
    created_at = models.DateTimeField(editable=True,
        auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"{self.number}"


class Producer(TimeBasedModel):

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Производитель", max_length=500)
    passenger = models.BooleanField(default=False, verbose_name='Легковой')
    truck = models.BooleanField(default=False, verbose_name='Грузовой')
    condition = models.CharField(default='',
        max_length=500, verbose_name='Условия распознования', blank=True)

    def __str__(self):
        return f"№{self.id} - {self.name}"



class User(AbstractUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    username = models.CharField(max_length=30, unique=False)
    name = models.CharField(unique=True, max_length=100,
                            verbose_name="Имя пользователя")
    fio = models.CharField(max_length=100,verbose_name='ФИО', blank=True)
    password = models.CharField(
        max_length=100, verbose_name="Пароль пользователя")
    latitude = models.CharField(max_length=255, verbose_name="Широта",blank=True)
    longitude = models.CharField(
        max_length=255, verbose_name="Долгота", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    balance = models.FloatField(
        verbose_name='Баланс', default=0.0,  blank=True)
    district = models.CharField(
        max_length=255, verbose_name='Регион', blank=True)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ["username","password"]
    

    def __str__(self):
        return self.name

class Order(TimeBasedModel):
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    id = models.AutoField(primary_key=True)
    carNumber = models.ForeignKey(Car,verbose_name='Номер машины',on_delete=models.SET(0))   
    brand = models.ForeignKey(Producer,verbose_name='Производитель',on_delete=models.SET(0))
    user = models.ForeignKey(User, verbose_name='Пользователь',on_delete=models.SET(0))
    created_at = models.DateTimeField(
        editable=True, auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"№{self.id} - {self.user}"


class Mark(TimeBasedModel):

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.photo.url}" width="150" height="150" />')
        else:
            return '(No image)'

    class Meta:
        verbose_name = 'Уникальный код'
        verbose_name_plural = 'Уникальные коды'

    mark = models.CharField(verbose_name='Код', max_length=500)
    photo = models.ImageField(upload_to='media/marks', verbose_name='Изображение')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='marks')
    created_at = models.DateTimeField(editable=True,
        auto_now_add=True, verbose_name='Дата создания')

class Category(TimeBasedModel):
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    id = models.AutoField(primary_key = True)
    name = models.CharField(verbose_name="Категория", max_length=500)

    def __str__(self):
        return f"№{self.id} - {self.name}" 



class Item(TimeBasedModel):
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    id = models.AutoField(primary_key = True)
    name = models.CharField(verbose_name="Наименование Товара", max_length=500)
    #photo = models.CharField(verbose_name="Изображение", max_length=5000)
    #description = models.TextField(verbose_name="Описание Товара", max_length=5000, null=True)
    price = models.CharField(verbose_name="Цена", max_length=200)
    category = models.ForeignKey(to=Category, verbose_name='Категория',on_delete=models.CASCADE)
    producer = models.ForeignKey(to=Producer,  verbose_name='Производитель', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(verbose_name="Дата создания",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата редактирования",auto_now=True)


    def __str__(self):
        return f"№{self.id} - {self.name}"   


class ItemMark(TimeBasedModel):


    def thumbnail(self):
        return u'<img src="{self.photo.url}" />' % (self.image.url)

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='marks')
    mark = models.CharField(max_length=1000)