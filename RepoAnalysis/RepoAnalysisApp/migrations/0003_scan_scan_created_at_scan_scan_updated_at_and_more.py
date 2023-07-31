from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):
    dependencies = [
        ('RepoAnalysisApp', '0002_remove_scan_description_alter_scan_title'),
    ]
    operations = [
        migrations.AddField(
            model_name='scan',
            name='scan_created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scan',
            name='scan_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='user_scans',
            name='user_scan_created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_scans',
            name='user_scan_updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='scan',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]