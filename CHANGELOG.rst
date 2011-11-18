Changelog
=========

TODO from readme
----------------

* Things in the readme that don't yet exist

  * Using ``Celery`` and ``CeleryBeat`` to collect metrics.
  * More example metrics created via ``dbag_init``
  * A Mixpanel ``MetricType``
  * Using data to define and organize arbitrary dashboards and customizations
    to the way specific metrics are displayed.

0.1.1
-----

* Fixed a crash when viewing the index page when no data had yet been collected
* This changelog

0.1.0
-----

* Initial stable-ish release!
* Django-dev-dashboard inspired templates and media for attractive data display
* Easy creation and registration of custom MetricTypes via autodiscovery
* Metric collection via a management command
* Management command to generate a cron template
* Initial ``ActiveUsersCount`` metric created via ``dbag_init`` management
  command for easy batteries-included usage.
* ``dbag_fake_metrics`` command to fake 60 days worth data using a random
  normal distribution to make it easy to see how your templates look with some
  semi-reasonable data.
* Parameterized ``MetricType`` based on filtering a queryset to make it easy to
  create a ``MetricType`` that performs a query on a custom ``Model``.
