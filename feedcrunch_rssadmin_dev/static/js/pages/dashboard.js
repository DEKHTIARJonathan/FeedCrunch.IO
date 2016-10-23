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

	function create_flotchart(divName){

		var flotdiv = $(divName);
		var api_route = flotdiv.data("api-route");
		var legend = flotdiv.data("legend");
		var username = window.location.pathname.substr(1).split("/")[0].slice(1)+"/";
		var api_url = api_route + username;

		var flotchart_generator = function (data_flot, ticks_flot) {

			var dataset =  [
				{
					data: data_flot,
					color: "#3d5afe",
					lines: {
						show: true,
						fill: 0.4,
					},
					shadowSize: 0,
				},
				{
					data: data_flot,
					color: "#3d5afe",
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

			var plot1 = $.plot(divName, dataset, {
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
					ticks: ticks_flot,
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
					content: "%y " + legend,
					defaultTheme: false
				}
			});

		};

		$.ajax({
			url: api_url,
			type: 'get',
			dataType: 'json',
			timeout: 5000,

			success:function(rslt)
			{

				var data_flot = rslt.data;
				var ticks_flot = rslt.ticks;

				flotchart_generator(data_flot, ticks_flot);
			}
		});

	}

	create_flotchart("#flotchart1");
	create_flotchart("#flotchart2");
});
