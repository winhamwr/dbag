import datetime

from django.db import models

from jsonfield import JSONField

class MetricCollectionDisabled(Exception):
    """
    Thrown when we attempt to collect a new ``DataSample`` for a ``Metric`` that
    currently has ``do_collect`` toggled off.
    """
    pass


class Metric(models.Model):
    """
    A specific combination of a ``MetricType`` and configuration that is then
    related to one ``DataSample`` per day to define a trend. This generally matches
    to one panel on a Dashboard.

    ``metric_type``
        The string under which a specific ``MetricType`` class was
        registered. The ``MetricType`` defines how the ``DataSample`` is actually
        retrieved.

    ``metric_properties``
        This is a JSON representation of all properties that
        the ``MetricType`` requires in order to retrieve a specific
        ``DataSample``. For example, a ``MetricType`` for retrieving the results
        of a query against the ORM might require a Model name and a specific ORM
        query.

    ``slug``
        The unique slug for identifying this specific metric.

    ``label``
        A human-readable short string summarizing what this metric defines. By
        default, this is used as the header when this metric is displayed in a
        panel.

    ``description``
        A longer-form description of what exactly this metric defines. An
        explanation of how this metric is gathered or how to interpret the data
        would go here.

    ``unit_label``
        The singular label for the unit of this measurement. eg. ``user account``

    ``unit_label_plural``
        The plural label for the unit of this measurement. eg. ``user accounts``

    ``do_collect``
        Should this metric be collected the next time the daily metric
        collection operation occurs. This field can be used to permanently or
        temporarily pause collection of metric if you'd like to retain data
        that's already collected.

    """
    metric_type_label = models.CharField(max_length=200)
    metric_properties = JSONField(default="{}")

    slug = models.CharField(max_length=75, unique=True)
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=500, null=True, blank=True)

    unit_label = models.CharField(max_length=75)
    unit_label_plural = models.CharField(max_length=75)

    do_collect = models.BooleanField(default=True)

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return self.label

    @models.permalink
    def get_absolute_url(self):
        return ("dbag-metric-detail", [self.slug])

    def get_latest_sample(self):
        try:
            return DataSample.objects.filter(metric=self)[0]
        except IndexError:
            return None

    def get_sample_for_day(self, utc_datetime):
        """
        Get the ``DataSample`` collected on the day matching the given ``utc_datetime``.

        ``utc_datetime``
        """
        day_start = utc_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + datetime.timedelta(days=1)

        samples = DataSample.objects.filter(
            utc_timestamp__gte=day_start, utc_timestamp__lt=day_end, metric=self)
        if len(samples) > 0:
            return samples[0]

        return None

    def get_samples_since(self, utc_datetime):
        """
        Get the all ``DataSample``s since the given time.

        ``utc_datetime``
        """
        return DataSample.objects.filter(
            utc_timestamp__gte=utc_datetime, metric=self)

    def collect_data_sample(self, manager, override_do_collect=False):
        """
        Use the appropriate ``MetricType`` corresponding to our
        ``metric_type_label`` to ollect a new data sample and create a new
        corresponding ``DataSample`` object with the current (utc-adjusted)
        timestamp.

        ``override_do_collect`` If ``do_collect`` is ``False``, then ``override_do_collect`` must be true or an
        """
        if not override_do_collect and not self.do_collect:
            # Don't allow collection of a toggled-off Metric without an explicit override
            raise MetricCollectionDisabled(
                "Metric collection is disabled for Metric %s and "
                "override_do_collect was not True" % self)
        metric_type_cls = manager.get_metric_type(self.metric_type_label)
        if metric_type_cls is None:
            raise Exception(
                "No metric type for this metric: %s" % self.metric_type_label)
        metric_type = metric_type_cls()
        data_value = metric_type.collect_data_sample(self)

        data_sample = DataSample.objects.create(
            metric=self, utc_timestamp=datetime.datetime.utcnow(), value=data_value)

        return data_sample

class DataSample(models.Model):
    """
    One sample of a given metric representing a daily summary.

    ``metric``
        The ``dbag.models.Metric`` object for which this is a single sample.

    ``utc_timestamp``
        The UTC-timezoned timestamp when this sample was collected.

    ``value``
        The numerical value retrieved for this sample at the time represented
        by the ``utc_timestamp``

    """
    metric = models.ForeignKey(Metric)
    utc_timestamp = models.DateTimeField(default=datetime.datetime.utcnow)
    value = models.BigIntegerField()

    class Meta:
        ordering = ['-utc_timestamp']
        get_latest_by = 'utc_timestamp'
        verbose_name_plural = 'data sample'

class Dashboard(models.Model):
    slug = models.CharField(max_length=75, unique=True)
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=500, null=True, blank=True)
    panels = models.ManyToManyField(Metric, through='DashboardPanel')

class DashboardPanel(models.Model):
    """
    An individual panel displaying a ``Metric`` for a specific
    ``Dashboard``. This allows the same set of data to be displayed in
    different ways on different screens.

    ``do_display``
        Should this metric be displayed on this dashboard. Toggle to hide
        temporarily.

    """
    metric = models.ForeignKey(Metric)
    dashboard = models.ForeignKey(Dashboard)
    do_display = models.BooleanField(default=True)
    show_sparkline = models.BooleanField(default=True)

    class Meta:
        unique_together = ('metric', 'dashboard')

