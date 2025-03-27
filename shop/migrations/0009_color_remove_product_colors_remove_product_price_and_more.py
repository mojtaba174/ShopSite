# Generated by Django 4.2.20 on 2025-03-27 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('hex_code', models.CharField(max_length=7, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(default=0)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shop.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shop.product')),
            ],
            options={
                'unique_together': {('product', 'color')},
            },
        ),
    ]
