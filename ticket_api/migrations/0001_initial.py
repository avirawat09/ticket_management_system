# Generated by Django 3.2.15 on 2022-09-01 17:35

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('estimated_time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IssueStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='IssueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('password', models.CharField(default='', max_length=50)),
                ('role', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ticket_api.role')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectIssueMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='issue', to='ticket_api.issue')),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='ticket_api.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='ticket_api.user'),
        ),
        migrations.AddField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='ticket_api.user'),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reporter', to='ticket_api.user'),
        ),
        migrations.AddField(
            model_name='issue',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ticket_api.issuestatus'),
        ),
        migrations.AddField(
            model_name='issue',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ticket_api.issuetype'),
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_field', models.CharField(max_length=20)),
                ('previous_value', models.TextField()),
                ('new_value', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('issue_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='issue_id', to='ticket_api.issue')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='ticket_api.user')),
                ('issue_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_issue_id', to='ticket_api.issue')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('email', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('password', models.CharField(default='', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('role', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ticket_api.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
