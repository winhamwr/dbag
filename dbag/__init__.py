"""
Dbag- Easy time-series metrics and dashboarding
"""
__version__ = '0.0.1dev'
__author__ = 'Wes Winham'
__contact__ = 'winhamwr@gmail.com'
__homepage__ = 'http://github.com/winhamwr/dbag'

__all__ = ('dbag', 'autodiscover')

from dbag.manager import dbag

def autodiscover():
    """
    Auto-discover all ``MetricTypes`` inside ``dbag_metric_types`` modules on
    all ``INSTALLED_APPS``.
    """
    import copy
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        # Attempt to import the dbag_metric_types module
        before_import_registry = copy.copy(dbag._registry)
        try:
            import_module('%s.dbag_metric_types' % app)
        except:
            # Reset the model registry to the state before the last import as
            # this import will have to reoccur on the next request and this
            # could raise NotRegistered and AlreadyRegistered exceptions
            dbag._registry = before_import_registry

