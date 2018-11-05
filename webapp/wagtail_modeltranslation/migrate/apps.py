from django.apps import AppConfig


class MigrateConfig(AppConfig):
    name = 'webapp.wagtail_modeltranslation.migrate'
    label = 'webapp.wagtail_modeltranslation_migrate'
    verbose_name = "Wagtail Modeltranslation migrate"
