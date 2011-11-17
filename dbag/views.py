import datetime
import time

from django import http
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.utils import simplejson

from dbag.models import Metric

def index(request):
    metrics = Metric.objects.all().order_by('label')

    data = []
    for metric in metrics:
        latest = metric.get_latest_sample()
        data.append({'metric': metric, 'latest': latest})

    return render(request, 'dbag/index.html', {'data': data})

def metric_detail(request, metric_slug):
    metric = get_object_or_404(Metric, slug=metric_slug)

    return render(
        request,
        'dbag/detail.html',
        {
            'metric': metric,
            'latest': metric.get_latest_sample(),
        }
    )

def metric_json(request, metric_slug):
    metric = get_object_or_404(Metric, slug=metric_slug)

    try:
        daysback = int(request.GET['days'])
    except (TypeError, KeyError):
        daysback = 30

    start_date = datetime.datetime.utcnow() - datetime.timedelta(days=daysback)

    metric_dict = model_to_dict(metric)
    metric_dict['data'] = []
    for sample in metric.get_samples_since(utc_datetime=start_date):
        metric_dict['data'].append(
            {
                'value': sample.value,
                'utc_timestamp': time.mktime(sample.utc_timestamp.timetuple()),
            }
        )

    return http.HttpResponse(
        simplejson.dumps(metric_dict, indent=2),
        content_type="application/json")




