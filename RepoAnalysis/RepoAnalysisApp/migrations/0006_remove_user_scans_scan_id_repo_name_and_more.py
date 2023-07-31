from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('RepoAnalysisApp', '0005_remove_user_scans_scan_session_repo_constraint_and_more'),
    ]
    operations = [
        migrations.RemoveConstraint(
            model_name='user_scans',
            name='scan_id_repo_name',
        ),
        migrations.RenameField(
            model_name='user_scans',
            old_name='name',
            new_name='repo_name',
        ),
        migrations.AddConstraint(
            model_name='user_scans',
            constraint=models.UniqueConstraint(fields=('scan_id', 'repo_name'), name='scan_id_repo_name'),
        ),
    ]