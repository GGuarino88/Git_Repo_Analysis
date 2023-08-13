from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('scan_created_at', models.DateTimeField(auto_now_add=True)),
                ('scan_updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_semester',
            },
        ),
        migrations.CreateModel(
            name='SemesterProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('repo_name', models.CharField(max_length=200)),
                ('url_name', models.URLField()),
                ('user_scan_created_at', models.DateTimeField(auto_now_add=True)),
                ('user_scan_updated_at', models.DateTimeField(auto_now=True)),
                ('semester_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RepoAnalysisApp.semester')),
            ],
            options={
                'db_table': 'user_semester_projects',
            },
        ),
        migrations.AddConstraint(
            model_name='semesterproject',
            constraint=models.UniqueConstraint(fields=('semester_id', 'team_name'), name='semester_id_team_name'),
        ),
        migrations.AddConstraint(
            model_name='semesterproject',
            constraint=models.UniqueConstraint(fields=('semester_id', 'repo_name'), name='semester_id_repo_name'),
        ),
        migrations.AddConstraint(
            model_name='semesterproject',
            constraint=models.UniqueConstraint(fields=('semester_id', 'url_name'), name='semester_id_url_name'),
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='author title constraint'),
        ),
    ]