import datetime

from django.db import models

from jsonfield import JSONField

class Metric(models.Model):
    """
    A specific combination of a ``MetricType`` and configuration that is then
    related to one ``DatumSample`` per day to define a trend. This generally matches
    to one panel on a Dashboard.

    ``metric_type``
        The string under which a specific ``MetricType`` class was
        registered. The ``MetricType`` defines how the ``DatumSample`` is actually
        retrieved.

    ``metric_properties``
        This is a JSON representation of all properties that
        the ``MetricType`` requires in order to retrieve a specific
        ``DatumSample``. For example, a ``MetricType`` for retrieving the results
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
    metric_type = models.CharField(max_length=200)
    metric_properties = JSONField(default="{}")

    slug = models.CharField(max_length=75, unique=True)
    label = models.CharField(max_length=75)
    description = models.CharField(max_length=500, null=True, blank=True)

    unit_label = models.CharField(max_length=75)
    unit_label_plural = models.CharField(max_length=75)

    do_collect = models.BooleanField(default=True)

class DatumSample(models.Model):
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
        get_latest_by = 'timestamp'
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


