from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('RepoAnalysisApp', '0004_scan_author_title_constraint_and_more'),
    ]
    operations = [
        migrations.RemoveConstraint(
            model_name='user_scans',
            name='scan session repo constraint',
        ),
        migrations.AddConstraint(
            model_name='user_scans',
            constraint=models.UniqueConstraint(fields=('scan_id', 'name'), name='scan_id_repo_name'),
        ),
        migrations.AddConstraint(
            model_name='user_scans',
            constraint=models.UniqueConstraint(fields=('scan_id', 'url_name'), name='repo_name_url_name'),
        ),
    ]