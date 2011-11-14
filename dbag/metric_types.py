
class Field(object):
    default_help_text = None

    def __init__(self, label=None, help_text=None):
        self.label = label
        self.help_text = help_text or self.default_help_text
        self.set_values(None)

    def set_values(self, name):
        self.name = name
        if name and not self.label:
            self.label = name

    def validate(self, data):
        value = data.get(self.name)
        if value:
            value = self.clean(value)
            assert isinstance(value, basestring), 'clean methods must return strings'
        return value

    def clean(self, value):
        return value

    def render(self, value):
        return mark_safe(
            '<input type="text" value="%s" name="%s" />' % (escape(value or ''), escape(self.name)))

    def display(self, value):
        return value

class String(Field):
    pass

class QueryFilter(Field):
    """
    A field with a key and value that filters an orm query. eg::

        Foo.objects.filter(key=value)
    """
    def validate(self, data):
        key = data.get(self.name + '-key')
        value = data.get(self.name + '-value')

        return self.clean((key, value))

    def clean(self, value):
        return '='.join(value)

    def render(self, value):
        if not value:
            value = ['', '']

        key_input = '<input type="text" value="%s" placeholder="field" name="%s-key" />' % escape(value[0])
        value_input = '<input type="text" value="%s" placeholder="value" name="%s-value" />' % escape(value[1])
        return mark_safe('%s = %s' % (key_input, value_input))

    def display(self, value):
        value = value.split('=')
        return '%s: %s=%s' % (self.label, value[0], value[1])


class MetricTypeBase(type):
    def __new__(cls, name, bases, attrs):
        attrs['fields'] = {}

        # Inherit any fields from parent(s).
        parents = [b for b in bases if isinstance(b, MetricTypeBase)]

        for p in parents:
            fields = getattr(p, 'fields', None)

            if fields:
                attrs['fields'].update(fields)

        for field_name, obj in attrs.items():
            if isinstance(obj, Field):
                field = attrs.pop(field_name)
                field.set_values(field_name)
                attrs['fields'][field_name] = field

        instance = super(MetricTypeBase, cls).__new__(cls, name, bases, attrs)

        return instance

class MetricType(object):
    __metaclass__ = MetricTypeBase

    def collect_data_sample(self, metric):
        pass

class QueryMetric(MetricType):
    query_model = None
    default_query_filter = None

    def build_queryset(self, metric):
        # Build the queryset object. This is the most common thing to overwrite
        return self.query_model.objects.all()

    def filter_queryset(self, queryset, query_filter):
        if query_filter:
            return queryset.filter(
                **{query_filter['key']: query_filter['value']})
        elif self.default_query_filter:
            return queryset.filter(
                **{self.default_query_filter['key']: self.default_query_filter['value']})

        return queryset

    def collect_data_sample(self, metric):
        queryset = self.build_queryset(metric)
        queryset = self.filter_queryset(queryset, metric.metric_properties.get('query_filter'))

        return queryset.count()

