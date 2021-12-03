# Generated by Django 2.2.10 on 2021-12-03 10:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import vote_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('created_at', models.DateField(default=django.utils.timezone.now)),
                ('ended_at', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('type', models.CharField(max_length=20, validators=[vote_app.models.questionTypeValidator])),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.Poll')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_id', models.PositiveIntegerField()),
                ('text', models.CharField(max_length=100)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(db_index=True)),
                ('question_type', models.CharField(max_length=20, validators=[vote_app.models.questionTypeValidator])),
                ('question_text', models.CharField(max_length=150)),
                ('text_answer', models.CharField(max_length=150)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.Poll')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote_app.Question')),
            ],
        ),
    ]
