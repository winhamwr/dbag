if (typeof DBAG_BASE_URL === 'undefined') {
    DBAG_BASE_URL = "/dbag/";
}

$(function () {
    var e = $("#graph");
    var url = DBAG_BASE_URL + "metric/" + e.data('metric') + ".json?days=365";
    var hover = {
        show: function (x, y, message) {
            $('<div id="hover">').html(message)
                .css({top: y, left: x})
                .appendTo('body')
                .show();
        },
        hide: function () {
            $("#hover").remove();
        }
    };

    $.getJSON(url, function (response) {
        var i;
        var js_data = [];
        // flot time series data needs to be in time/value pairs and the
        // time needs to be in *milliseconds*, not seconds.  fixing this in
        // Python would be easier but would limit reuse.
        for (i = 0; i < response.data.length; i++) {
            var datapoint = [];
            datapoint[0] = response.data[i].utc_timestamp * 1000;
            datapoint[1] = response.data[i].value;
            js_data.push(datapoint);
        }
        var options = {
            xaxis: {
                mode: "time",
                tickColor: "rgba(0,0,0,0)",
                minTickSize: [1, "day"]
            },
            yaxis: {min: 0, ticks: 4},
            grid: {borderWidth: 0, hoverable: true, color: "white"},
            colors: ["yellow"]
        };
        options.bars = {
            show: true,
            barWidth: 22 * 60 * 60 * 1000,
            align: "center"
        };
        var plot = $.plot(e, [js_data], options);

        var format_message = function (timestamp, measurement) {
            var unit_label = measurement === 1 ? response.unit_label : response.unit_label_plural;
            var d = new Date(timestamp);
            return $.plot.formatDate(d, "%b %d, %h:%M%p") + '<br>' + measurement + ' ' + unit_label;
        };

        var previousPoint = null;
        e.bind("plothover", function (event, pos, item) {
            var x,
                message;
            if (item) {
                if (previousPoint !== item.dataIndex) {
                    previousPoint = item.dataIndex;
                    hover.hide();
                    message = format_message.apply(null, item.datapoint);
                    // I'd like this hover to be centered over the bar. This
                    // simple math sorta works, but it assumes a *lot* about
                    // the plot and basically won't scale. Grr.
                    x = item.pageX - 40;
                    y = item.pageY - 50;
                    hover.show(x, y, message);
                }
            } else {
                hover.hide();
                previousPoint = null;
            }
        });
    });
});
