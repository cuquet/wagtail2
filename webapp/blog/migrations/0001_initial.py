# Generated by Django 2.0.9 on 2018-11-01 18:42

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.core.fields
import webapp.blog.routes


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('wagtailcore', '0040_page_draft_title'),
        ('wagtailimages', '0021_image_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('excerpt', wagtail.core.fields.RichTextField(blank=True, help_text='The page description that will appear under the title.On Entry list, excerpt to be displayed.If this field is not filled, a truncate version of body text will be used.', verbose_name='Excerpt')),
                ('parallax_filter', models.CharField(blank=True, choices=[('filter filter-black', 'filter-black'), ('filter filter-white', 'filter-white'), ('filter filter-blue', 'filter-blue'), ('filter filter-azure', 'filter-azure'), ('filter filter-green', 'filter-green'), ('filter filter-orange', 'filter-orange'), ('filter filter-red', 'filter-red'), ('filter filter-white', 'filter-white'), ('', 'No filter')], default='filter-black', help_text='Filter effect', max_length=30, null=True, verbose_name='Image Filter')),
                ('parallax_size', models.CharField(blank=True, choices=[('parallax-small', 'Small'), ('parallax-medium', 'Medium'), ('parallax-large', 'Large')], default='parallax-small', help_text='Size effect', max_length=30, null=True, verbose_name='Image Size')),
                ('show_search', models.BooleanField(default=False, help_text='Whether a search form will appear in automatically generated menus', verbose_name='Show search in menus')),
                ('menu_icon', models.CharField(blank=True, max_length=60, null=True, verbose_name='Icon Class')),
                ('twitter_consumer_secret', models.TextField(blank=True, verbose_name='Twitter Consumer Secret')),
                ('twitter_consumer_key', models.TextField(blank=True, verbose_name='Twitter Consumer Key')),
                ('twitter_api_secret', models.TextField(blank=True, verbose_name='Twitter Api Secret')),
                ('twitter_api_key', models.TextField(blank=True, verbose_name='Twitter Api Key')),
                ('twitter_owner', models.TextField(blank=True, verbose_name='Twitter Owner')),
                ('twitter_owner_id', models.TextField(blank=True, verbose_name='Twitter Owner Id')),
                ('twitter_enable_publish', models.BooleanField(default=False, help_text='It will publish entry on twitter account as soon as is saved.', verbose_name='Enable Twitter Publish')),
                ('display_comments', models.BooleanField(default=False, verbose_name='Display comments')),
                ('display_categories', models.BooleanField(default=True, verbose_name='Display categories')),
                ('display_tags', models.BooleanField(default=True, verbose_name='Display tags')),
                ('display_popular_entries', models.BooleanField(default=True, verbose_name='Display popular entries')),
                ('display_last_entries', models.BooleanField(default=True, verbose_name='Display last entries')),
                ('display_archive', models.BooleanField(default=True, verbose_name='Display archive')),
                ('disqus_api_secret', models.TextField(blank=True)),
                ('disqus_shortname', models.CharField(blank=True, max_length=128)),
                ('num_entries_page', models.IntegerField(default=5, verbose_name='Entries per page')),
                ('num_last_entries', models.IntegerField(default=3, verbose_name='Last entries limit')),
                ('num_popular_entries', models.IntegerField(default=3, verbose_name='Popular entries limit')),
                ('num_tags_entry_header', models.IntegerField(default=5, verbose_name='Tags limit entry header')),
                ('num_tags_size_in_cloud', models.IntegerField(default=8, verbose_name='Tags sizes in tag cloud')),
                ('short_feed_description', models.BooleanField(default=True, verbose_name='Use short description in feeds')),
                ('header_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(webapp.blog.routes.BlogRoutes, 'wagtailcore.page', models.Model),
            managers=[
                ('extra', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category name')),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('description', models.CharField(blank=True, max_length=500, verbose_name='Description')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='blog.Category', verbose_name='Parent category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CategoryEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Category', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='EntryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('excerpt', wagtail.core.fields.RichTextField(blank=True, help_text='The page description that will appear under the title.On Entry list, excerpt to be displayed.If this field is not filled, a truncate version of body text will be used.', verbose_name='Excerpt')),
                ('parallax_filter', models.CharField(blank=True, choices=[('filter filter-black', 'filter-black'), ('filter filter-white', 'filter-white'), ('filter filter-blue', 'filter-blue'), ('filter filter-azure', 'filter-azure'), ('filter filter-green', 'filter-green'), ('filter filter-orange', 'filter-orange'), ('filter filter-red', 'filter-red'), ('filter filter-white', 'filter-white'), ('', 'No filter')], default='filter-black', help_text='Filter effect', max_length=30, null=True, verbose_name='Image Filter')),
                ('parallax_size', models.CharField(blank=True, choices=[('parallax-small', 'Small'), ('parallax-medium', 'Medium'), ('parallax-large', 'Large')], default='parallax-small', help_text='Size effect', max_length=30, null=True, verbose_name='Image Size')),
                ('show_search', models.BooleanField(default=False, help_text='Whether a search form will appear in automatically generated menus', verbose_name='Show search in menus')),
                ('menu_icon', models.CharField(blank=True, max_length=60, null=True, verbose_name='Icon Class')),
                ('body', wagtail.core.fields.RichTextField(verbose_name='Content')),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Post date')),
                ('num_comments', models.IntegerField(default=0, editable=False)),
                ('categories', models.ManyToManyField(blank=True, through='blog.CategoryEntryPage', to='blog.Category')),
                ('header_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
            bases=('wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='EntryPageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrypage_from', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_entrypage_from', to='blog.EntryPage', verbose_name='Entry')),
                ('entrypage_to', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_entrypage_to', to='blog.EntryPage', verbose_name='Entry')),
            ],
        ),
        migrations.CreateModel(
            name='TagEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_tags', to='blog.EntryPage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.AddField(
            model_name='tagentrypage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_tagentrypage_items', to='taggit.Tag'),
        ),
        migrations.AddField(
            model_name='entrypage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.TagEntryPage', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='categoryentrypage',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_categories', to='blog.EntryPage'),
        ),
    ]
