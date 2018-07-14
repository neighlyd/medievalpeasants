from django.apps import AppConfig


class PeasantlegaldbConfig(AppConfig):
    name = 'peasantlegaldb'

    def ready(self):
        import peasantlegaldb.signals