# Generated by Django 4.2.3 on 2023-07-19 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.CharField(max_length=200, verbose_name='Номер машины')),
                ('image', models.ImageField(default=None, upload_to='media/cars')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Транспорт',
                'verbose_name_plural': 'Транспорты',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, verbose_name='Наименование Товара')),
                ('price', models.CharField(max_length=200, verbose_name='Цена')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, verbose_name='Производитель')),
                ('passenger', models.BooleanField(default=False, verbose_name='Легковой')),
                ('truck', models.BooleanField(default=False, verbose_name='Грузовой')),
                ('condition', models.CharField(blank=True, default='', max_length=500, verbose_name='Условия распознования')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='fio',
            field=models.CharField(default='admin', max_length=100, verbose_name='ФИО'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='user',
            name='district',
            field=models.CharField(blank=True, max_length=255, verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.CharField(blank=True, max_length=255, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.CharField(blank=True, max_length=255, verbose_name='Долгота'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('brand', models.ForeignKey(on_delete=models.SET(0), to='api.producer', verbose_name='Производитель')),
                ('carNumber', models.ForeignKey(on_delete=models.SET(0), to='api.car', verbose_name='Номер машины')),
                ('user', models.ForeignKey(on_delete=models.SET(0), to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mark', models.CharField(max_length=500, verbose_name='Код')),
                ('photo', models.CharField(max_length=1000, verbose_name='Код фотки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='api.order')),
            ],
            options={
                'verbose_name': 'Уникальный код',
                'verbose_name_plural': 'Уникальные коды',
            },
        ),
        migrations.CreateModel(
            name='ItemMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mark', models.CharField(max_length=1000)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='api.item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.producer', verbose_name='Производитель'),
        ),
    ]