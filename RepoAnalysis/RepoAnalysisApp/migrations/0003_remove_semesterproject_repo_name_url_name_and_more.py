from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('RepoAnalysisApp', '0002_semester_semesterproject_remove_user_scans_scan_id_and_more'),
    ]
    operations = [
        migrations.RemoveConstraint(
            model_name='semesterproject',
            name='repo_name_url_name',
        ),
        migrations.AddConstraint(
            model_name='semesterproject',
            constraint=models.UniqueConstraint(fields=('scan_id', 'team_name'), name='scan_id_team_name'),
        ),
        migrations.AddConstraint(
            model_name='semesterproject',
            constraint=models.UniqueConstraint(fields=('scan_id', 'url_name'), name='scan_id_url_name'),
        ),
    ]