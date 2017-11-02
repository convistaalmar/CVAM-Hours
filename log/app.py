from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class LogConfig(AppConfig):
    name = 'log'
    verbose_name = _('Hours log')

    def ready(self):
        import log.signals