Dbag- Easy time-series metrics and dashboarding 
===============================================

Dbag is a simple Django app to help you remember, graph and create dashboards
for arbitrary metrics that change over time. 

It's best used to graph things like: 

* number of active user accounts
* % of users who have logged in today
* number of new blog comments
  
These are things that are easy to run a query or a quick bit of python to
determine the answer to the question *right now* but that are hard or fuzzy to
calculate for periods in the past. You want to figure out your number every day
and then remember it so you can display fancy graphs and trending (and you want
these graphs to just work and be pretty). You also want to reduce complexity by
using your existing Django database backend to hold all of the data.

Why Dbag?
---------

Dbag fills a niche not currently well-covered by existing solutions. Dbag is
simpler than existing tools because it does less. If you meet the following 
conditions, it might be right for you:

* You want to collect a small to moderate amount of data and daily resolution
  is good enough.
* You have many different ways of getting the data, but you want to collect it
  from one place.
* You want the simplicity of builtin metric types to get commonly-needed Django
  metrics, but you also want the flexibility to define arbitrary python
  functions to collect data.
* You want simple dashboarding that you can use internally and expose to your
  users without a lot of work (and it should be pretty).
* You want to be able to interact with your metrics via Django's ORM if necessary.
* You want the option to tie a metric to a specific object in your database. If
  you have a `Customer` object, you might want the number of active accounts on
  each specific customer.

What you should use instead
---------------------------

If that's not what you're looking for, then one of the following is probably a
better option.

Operations and SysAdmin Graphing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There several great system information graphing applications like
, `munin <http://munin-monitoring.org/>`_
and `cacti <http://www.cacti.net/>`_ if you want to see CPU usage over time.
These are better if you want to know how disk usage is trending across 30
different nodes.

Capture Events
~~~~~~~~~~~~~~

`Mixpanel <http://mixpanel.com/>`_, `statsd <https://github.com/etsy/statsd>`_,
`Google Analytics <http://www.google.com/analytics/>`_, etc are all better at
capturing events and high-frequency data. Use them if that's all you need. Dbag
would fit in to that equation if you want to regularly slice off or corelate
data from those sources and display the changes over time on a dashboard.

Graph Anything
~~~~~~~~~~~~~~

If you just want to dump any kind of data at any volume in to one system and
then graph it a thousand different ways, you should use
`graphite <http://graphite.wikidot.com/>`_. You'll want to put it on a different
server and you'll need to figure it out, but you'll get as much scalability and
flexibility as you need. `dbag` actually works well in combination with
graphite if you'd like to display simple dashboards of summarized date to your
users.

Other Django Dashboards
~~~~~~~~~~~~~~~~~~~~~~~

There are some other Django dashboarding-ish apps around.

* This one isn't meant to be general-purpose, but is used specifically for
  grabbing metrics for the `Django project
  dashboard <https://github.com/jacobian/django-dev-dashboard>`_. It has very
  attractive panels with a optional sparklines and a nice master/default
  layout. Visual inspiration was taken heavily from this project and `dbag` can
  be used to effectively recreate the Django project dashboard..
* This sub-project in
  `djutils <http://charlesleifer.com/docs/djutils/django-utils/dashboard/panels.html>`_
  effectively re-creates Munin using Django. It allows you to collect and
  aggregate very granular data using whatever python code you'd like. It does
  not however let you create parameterized panels and metrics (meaning that if
  you wanted to create separate panels for every ``Customer`` in your database,
  you'd need to write python code registering a panel for each customer.
* These exist but `aren't <http://code.google.com/p/django-dashboard/>`_
  `documented <https://github.com/stefanw/django-dashboard>`_ or
  `maintained <https://github.com/ojii/django-dashboard>`_.

Installation
------------

1. Get the project source and install it::

    $ pip install dbag

2. Add `dbag` to your tuple of ``INSTALLED_APPS``.
3. Add the dbag urls to your ``urls.py``. Eg::

        urlpatterns = patterns('',
            url('^dbag/', include('dbag.urls'),
        )

    If you're not using `Nexus <https://github.com/dcramer/nexus>`_ then you
    also need to add this to ``urls.py`` for automatic ``MetricType``
    discovery::

        import dbag
        dbag.autodiscover()

3. Create the database schema::
  

        $ ./manage.py syncdb

    or if you're using `South <http://south.aeracode.org/>`_ ::
    
        $ ./manage.py syncdb --migrate

4. Configure some initial metrics::

    $ ./manage.py dbag_init

5. If you're already using `Celery <http://celeryproject.org/>`_ then
    ensure that
    `celerybeat <http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html#starting-celerybeat>`_
    is running. Otherwise, you can run:: 
    
        $ ./manage.py dbag_output_cronjob > /etc/cron.d/dbag_collect_metrics 
    
    to set up a cron job to collect your metrics every day. You'll need to
   edit the resulting file to use the correct paths and the correct user. 

6. If you want to force collection of your first days worth of metrics, you can also run::

       $ ./manage.py dbag_collect_metrics

   Alternatively, you can generate some random fake data to demo with using::

       $ ./manage.py dbag_fake_metrics

7. Now start up your devserver, login and visit 
   `http://localhost:8000/dbag/ <http://localhost:8000/dbag/>`_
   (or wherever you told your ``urls.py`` to point for dbag).

Add a New Metric
----------------

You can add new metrics to start collecting either through the `Nexus
<https://github.com/dcramer/nexus>`_ frontend or via the API in python. Either
way you'll be choosing 5 things to define your metric.

**metric_type_label** 
    The label for the type of metric we're collecting. These python subclasses
    of ``dbag.metric_types.MetricType`` are registered with dbag (with a unique
    label) and define how a metric is gathered and what options are required to
    gather it. Included examples are an ``ActiveUsersCount`` type that optionally
    takes an ORM filter to define a subset of users and a ``MixpanelEvent`` type
    that takes an event name and optional properties to slice and records the
    value for the day.

**label** 
    The human-readable name of this metric.

**slug** 
    A unique slug identifying this metric.

**description** 
    An optional long-form description of this metric.

**do_collect** 
    Whether or not to collect new values for this metric (default to False).

**kwargs** 
    Some MetricTypes take required or optional keyword configuration arguments.
    In the following example, ``mp_property`` is an optional keyword argument.


An example API call to create a metric might be::

    from dbag import dbag_manager
    dbag_manager.create_metric(
        'MixpanelEvent', 
        label='superuser comments', 
        slug='superuser_comments', 
        description="number of comments made by superusers", 
        unit_label="comment",
        unit_label_plural="comments",
        mp_property="is_superuser=true")


Create a New MetricType
-----------------------

You can add a new MetricType whenever you need to gather/summarize data from a
new source. An example would be a MetricType that used github's API to count
the number of open tickets on a specific project. Subclass
``dbag.metric_types.MetricType`` with your object, put it in a
``dbag_metric_types`` module in one of your ``INSTALLED_APPS`` and then call::

    from dbag import dbag_manager
    dbag_manager.register_metric_type(<your label>, <your class>)

For now, check the builtin types located at ``dbag.metric_types`` for details.

Dbag? Really?
-------------

A defensible rationalization is that the name is short for "data bag."

Is it Awesome?
--------------

Yes. Increasingly so.

TODO- maybe?
------------

* Add support for Flask and Pyramid (or others?)
* Provide a REST API for accessing metrics data
