# Generated by Django 5.1 on 2024-09-01 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('about_id', models.AutoField(primary_key=True, serialize=False)),
                ('about_title', models.CharField(max_length=100)),
                ('about_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('contact_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailSubscription',
            fields=[
                ('subscription_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('faq_id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=100)),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('partner_id', models.AutoField(primary_key=True, serialize=False)),
                ('partner_name', models.CharField(max_length=50)),
                ('partner_image', models.ImageField(default='default.jpg', upload_to='partner_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('pricing_id', models.AutoField(primary_key=True, serialize=False)),
                ('pricing_name', models.CharField(max_length=50)),
                ('pricing_price', models.FloatField()),
                ('pricing_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('privacy_policy_id', models.AutoField(primary_key=True, serialize=False)),
                ('privacy_policy_title', models.CharField(max_length=100)),
                ('privacy_policy_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=50)),
                ('service_description', models.TextField()),
                ('service_price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=50)),
                ('team_designation', models.CharField(max_length=50)),
                ('team_image', models.ImageField(default='default.jpg', upload_to='team_images')),
                ('team_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('terms_and_conditions_id', models.AutoField(primary_key=True, serialize=False)),
                ('terms_and_conditions_title', models.CharField(max_length=100)),
                ('terms_and_conditions_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('testimonial_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('user_image', models.ImageField(default='default.jpg', upload_to='testmonial_images')),
                ('testimonial', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('feature_id', models.AutoField(primary_key=True, serialize=False)),
                ('feature_name', models.CharField(max_length=50)),
                ('feature_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.service')),
            ],
        ),
    ]
