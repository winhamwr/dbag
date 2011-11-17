from django.template.defaultfilters import slugify

class MetricManager(object):

    def __init__(self):
        self._registry = {}
        super(MetricManager, self).__init__()

    def register_metric_type(self, label, metric_type):
        self._registry[label] = metric_type

    def unregister_metric_type(self, label):
        self._registry.pop(label)

    def get_metric_type(self, label):
        return self._registry.get(label)

    def get_metric_types(self):
        return self._registry

    def create_metric(
            self, metric_type_label, label, slug=None, description=None,
            unit_label='unit', unit_label_plural='units', do_collect=True, *args,
            **kwargs):
        from dbag.models import Metric # Workaround so __init__ doesnt need a settings file

        if not self.get_metric_type(metric_type_label):
            raise Exception("MetricType doesn't exist with label %s" % metric_type_label)

        if not slug:
            slug = slugify(label)
        metric_properties = kwargs
        if not metric_properties:
            metric_properties = {}

        metric = Metric.objects.create(
            metric_type_label=metric_type_label,
            label=label,
            slug=slug,
            description=description,
            unit_label=unit_label,
            unit_label_plural=unit_label_plural,
            do_collect=do_collect,
            metric_properties=metric_properties,
        )

        return metric

    def collect_metrics(self):
        """
        Collect and create ``DataSample`` objects for all ``Metric``s that have
        collection enabled.
        """
        from dbag.models import Metric # Workaround so __init__ doesnt need a settings file

        data_samples = []
        for metric in Metric.objects.filter(do_collect=True):
            data_samples.append(metric.collect_data_sample(self))

        return data_samples



dbag_manager = MetricManager()
