# Generated by Django 5.1 on 2024-09-02 13:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstreamform', '0045_delete_requestfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to='media/Auth/')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='upstreamform.upstreamform')),
            ],
            options={
                'db_table': 'requestfile',
            },
        ),
    ]
