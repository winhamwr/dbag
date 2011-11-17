if (typeof DBAG_BASE_URL === 'undefined') {
    DBAG_BASE_URL = "/dbag/";
}
$(function () {
    $("div.metric div.sparkline").each(function (index, elem) {
        var e = $(elem),
            value_element = e.parent().find('p.value a'),
            timestamp_element = e.parent().find('span.timestamp'),
            original_value = value_element.html(),
            i;

        var url = DBAG_BASE_URL + 'metric/' + e.data('metric') + ".json";
        $.getJSON(url, function (response) {
            // flot time series data needs to be in time/value pairs and the
            // time needs to be in *milliseconds*, not seconds.  fixing this in
            // Python would be easier but would limit reuse.
            var js_data = [];
            for (i = 0; i < response.data.length; i++) {
                var datapoint = [];
                datapoint[0] = response.data[i].utc_timestamp * 1000;
                datapoint[1] = response.data[i].value;
                js_data.push(datapoint);
            }
            var options = {
                xaxis: {show: false, mode: "time"},
                yaxis: {show: false, min: 0},
                grid: {borderWidth: 0, hoverable: true},
                colors: ["yellow"]
            };
            $.plot(e, [js_data], options);

            e.bind('plothover', function (event, pos, item) {
                if (item) {
                    var d = new Date(item.datapoint[0]);
                    timestamp_element.html(
                        $.plot.formatDate(d, "%b %d, %h:%M%p")
                    );
                    value_element.html(item.datapoint[1]);
                } else {
                    value_element.html(original_value);
                    timestamp_element.html('&nbsp;');
                }
            });
        });

        e.click(function () {
            window.location = DBAG_BASE_URL + "metric/" + e.data('metric') + '/';
        });
    });
});
