import inject
from config import Config
from config_service import ConfigService

def _do_configure_di(binder: inject.Binder):
    binder.bind_to_provider(Config, lambda: inject.instance(ConfigService).config)

class DIConfigurer:
    def configure(self):
        inject.configure_once(_do_configure_di)
