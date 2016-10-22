$( document ).ready(function() {

    // CounterUp Plugin
    $('.counter').each(function () {
        $(this).prop('Counter',0).animate({
            Counter: $(this).text()
        }, {
            duration: 3500,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
                $(this).text($(this).text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
            }
        });
    });

    // Peity Chart
    $.fn.peity.defaults.pie = {
        delimiter: null,
        fill: ["#26A69A", "#e0e0e0", "#b2dfdb"],
        height: null,
        radius: 8,
        width: null
    };
    $("span.pie").peity("pie")

    var DrawSparkline = function() {

        var linePoints = [0, 1, 3, 2, 1, 1, 4, 1, 2, 0, 3, 1, 3, 4, 1, 0, 2, 3, 6, 3, 4, 2, 7, 5, 2, 4, 1, 2, 6, 13, 4, 2];
        $('#sparkline-line').sparkline(linePoints, {
            type: 'line',
            width: 'calc(100% + 4px)',
            height: '45',
            chartRangeMax: 13,
            lineColor: '#ffb74d',
            fillColor: 'rgba(255,183,77,0.3)',
            highlightLineColor: 'rgba(0,0,0,0)',
            highlightSpotColor: 'rgba(0,0,0,.2)',
            tooltip: false
        });

        var barParent = $('#sparkline-bar').closest('.card');
        var barPoints = [0, 1, 3, 2, 1, 1, 4, 1, 2, 0, 3, 1, 3, 4, 1, 0, 2, 3, 6, 3, 4, 2, 7, 5, 2, 4, 1, 2, 6, 13, 4, 2];
        var barWidth = 6;
        $('#sparkline-bar').sparkline(barPoints, {
            type: 'bar',
            height: $('#sparkline-bar').height() + 'px',
            width: '100%',
            barWidth: barWidth,
            barSpacing: (barParent.width() - (barPoints.length * barWidth)) / barPoints.length,
            barColor: 'rgba(0,0,0,.07)',
            tooltipFormat: ' <span style="color: #ccc">&#9679;</span> {{value}}</span>'
        });

    };

    DrawSparkline();

    var resizeChart;

    $(window).resize(function(e) {
        clearTimeout(resizeChart);
        resizeChart = setTimeout(function() {
            DrawSparkline();
        }, 300);
    });

	var flot1 = function () {

		var data_flot1 = [];
		var ticks_flot1 = [];
		var username = window.location.pathname.substr(1).split("/")[0].slice(1)+"/";

		$.ajax({
			url: '/api/1.0/authenticated/get/user/publications_stats/' + username,
			type: 'get',
			dataType: 'json',
			async: false,
			timeout: 5000,
			success:function(rslt)
			{
				data_flot1 = rslt.data;
				ticks_flot1 = rslt.ticks;
			}
		});

		var dataset =  [
            {
                data: data_flot1,
                color: "#26A69A",
                lines: {
                    show: true,
                    fill: 0.4,
                },
                shadowSize: 0,
            },
			{
                data: data_flot1,
                color: "#26A69A",
                lines: {
                    show: false,
                },
                curvedLines: {
                    apply: false,
                },
                points: {
                    show: true,
                    fill: true,
                    radius: 4,
                    fillColor: "#fff",
                    lineWidth: 2
                },
                shadowSize: 0
            }
        ];

        var plot1 = $.plot("#flotchart1", dataset, {
            series: {
                color: "#14D1BD",
                lines: {
                    show: true,
                    fill: 0.2
                },
                shadowSize: 0,
                curvedLines: {
                    apply: true,
                    active: true,
					monotonicFit: true
                }
            },
            xaxis: {
                ticks: ticks_flot1,
            },
            legend: {
                show: false
            },
            grid: {
                color: "#AFAFAF",
                hoverable: true,
                borderWidth: 0,
                backgroundColor: '#FFF'
            },
            tooltip: true,
            tooltipOpts: {
                content: "%y Publication(s)",
                defaultTheme: false
            }
        });

    };

    flot1();

    var flotchart2 = function () {

		var data_flot1 = [];
		var ticks_flot1 = [];
		var username = window.location.pathname.substr(1).split("/")[0].slice(1)+"/";

		$.ajax({
			url: '/api/1.0/authenticated/get/user/subscribers_stats/' + username,
			type: 'get',
			dataType: 'json',
			async: false,
			timeout: 5000,
			success:function(rslt)
			{
				data_flot1 = rslt.data;
				ticks_flot1 = rslt.ticks;
			}
		});

		var dataset =  [
            {
                data: data_flot1,
                color: "#26A69A",
                lines: {
                    show: true,
                    fill: 0.4,
                },
                shadowSize: 0,
            },
			{
                data: data_flot1,
                color: "#26A69A",
                lines: {
                    show: false,
                },
                curvedLines: {
                    apply: false,
                },
                points: {
                    show: true,
                    fill: true,
                    radius: 4,
                    fillColor: "#fff",
                    lineWidth: 2
                },
                shadowSize: 0
            }
        ];

        var plot1 = $.plot("#flotchart2", dataset, {
            series: {
                color: "#14D1BD",
                lines: {
                    show: true,
                    fill: 0.2
                },
                shadowSize: 0,
                curvedLines: {
                    apply: true,
                    active: true,
					monotonicFit: true
                }
            },
            xaxis: {
                ticks: ticks_flot1,
            },
            legend: {
                show: false
            },
            grid: {
                color: "#AFAFAF",
                hoverable: true,
                borderWidth: 0,
                backgroundColor: '#FFF'
            },
            tooltip: true,
            tooltipOpts: {
                content: "%y Subscribers(s)",
                defaultTheme: false
            }
        });

    };

    flotchart2();


    $(document).on("fixedSidebarClick", function() {
        clearTimeout(resizeChart);
        resizeChart = setTimeout(function() {
            DrawSparkline();
        }, 300);
    });
});
