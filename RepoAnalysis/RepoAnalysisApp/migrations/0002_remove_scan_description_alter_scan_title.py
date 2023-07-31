from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('RepoAnalysisApp', '0001_initial'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='scan',
            name='description',
        ),
        migrations.AlterField(
            model_name='scan',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]