# Generated by Django 4.1.5 on 2023-05-25 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_conference_payment_status_delete_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='payment_status',
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cvv', models.IntegerField()),
                ('card_number', models.IntegerField()),
                ('starting_time', models.CharField(max_length=100, null=True)),
                ('ending_time', models.CharField(max_length=100, null=True)),
                ('date', models.DateField(null=True)),
                ('conference', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.conference')),
            ],
        ),
    ]