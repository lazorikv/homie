# Generated by Django 4.0.5 on 2022-06-08 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('house_number', models.CharField(max_length=20)),
                ('apartment_number', models.CharField(max_length=10)),
            ],
            options={
                'unique_together': {('city', 'district', 'street', 'house_number', 'apartment_number')},
            },
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.IntegerField()),
                ('room_count', models.IntegerField()),
                ('area', models.FloatField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo', models.URLField(unique=True)),
                ('hidden_photo', models.URLField(unique=True)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='apartment_address', to='system.address')),
            ],
        ),
        migrations.CreateModel(
            name='UtilityBills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas_supply', models.DecimalField(decimal_places=4, max_digits=10)),
                ('water_supply', models.DecimalField(decimal_places=4, max_digits=10)),
                ('electricity', models.DecimalField(decimal_places=4, max_digits=10)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='utility_bills', to='system.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('UNDEFINED', 'Undefined')], default='Undefined', max_length=10)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('middle_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('UNDEFINED', 'Undefined')], default='Undefined', max_length=10)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='landlord', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Landlord',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_file', models.URLField(unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='system.apartment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_contract', to='system.landlord')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_contract', to='system.tenant')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_apartment', to='system.landlord'),
        ),
        migrations.AddField(
            model_name='apartment',
            name='tenant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rent_apartment', to='system.tenant'),
        ),
    ]
