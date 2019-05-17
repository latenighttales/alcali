// Register plugin to always show tooltip
// ref: https://github.com/chartjs/Chart.js/issues/4045
Chart.plugins.register({
	beforeRender: function(chart) {
		if (chart.config.options.showAllTooltips) {
			// create an array of tooltips
			// we can't use the chart tooltip because there is only one tooltip per chart
			chart.pluginTooltips = [];
			chart.config.data.datasets.forEach(function(dataset, i) {
				chart.getDatasetMeta(i).data.forEach(function(sector, j) {
					chart.pluginTooltips.push(
						new Chart.Tooltip(
							{
								_chart: chart.chart,
								_chartInstance: chart,
								_data: chart.data,
								_options: chart.options.tooltips,
								_active: [sector]
							},
							chart
						)
					);
				});
			});

			// turn off normal tooltips
			chart.options.tooltips.enabled = false;
		}
	},
	afterDraw: function(chart, easing) {
		if (chart.config.options.showAllTooltips) {
			// we don't want the permanent tooltips to animate, so don't do anything till the animation runs at least once
			if (!chart.allTooltipsOnce) {
				if (easing !== 1) return;
				chart.allTooltipsOnce = true;
			}

			// turn on tooltips
			chart.options.tooltips.enabled = true;
			Chart.helpers.each(chart.pluginTooltips, function(tooltip) {
				tooltip.initialize();
				tooltip._options.bodyFontFamily = "Roboto";
				tooltip._options.displayColors = false;
				tooltip._options.bodyFontSize = tooltip._chart.height * 0.10;
				tooltip._options.yPadding = 0;
				tooltip._options.xPadding = 0;
				tooltip._options.backgroundColor = '#FFF';
				tooltip._options.bodyFontColor = '#555';
				// tooltip._options.position = 'average';
				tooltip._options.caretSize = tooltip._options.bodyFontSize * 0.6;
				tooltip._options.caretPadding = 5;
				tooltip._options.cornerRadius = 0;
				// tooltip._options.borderColor = '#555';
				// tooltip._options.borderWidth = 1;
				tooltip.update();
				// we don't actually need this since we are not animating tooltips
				tooltip.pivot();
				tooltip.transition(easing).draw();
			});
			chart.options.tooltips.enabled = false;
		}
	}
});