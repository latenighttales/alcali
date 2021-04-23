let gradientLinePlugin = {
  // Called at start of update.
  afterLayout: function (chartInstance) {
    if (chartInstance.options.linearGradientLine) {
      // The context, needed for the creation of the linear gradient.
      let ctx = chartInstance.chart.ctx;
      chartInstance.data.datasets.forEach((dataset) => {
        // Calculate min and max values of the dataset.
        let minValue = Number.MAX_VALUE;
        let maxValue = Number.MIN_VALUE;
        for (let i = 0; i < dataset.data.length; ++i) {
          if (minValue > dataset.data[i])
            minValue = dataset.data[i];
          if (maxValue < dataset.data[i])
            maxValue = dataset.data[i];
        }
        let yAxis = chartInstance.scales['y-axis-0'];
        let minValueYPixel = yAxis.getPixelForValue(minValue) || 0;
        let maxValueYPixel = yAxis.getPixelForValue(maxValue) || 0;
        // Create the gradient.
        let gradient = ctx.createLinearGradient(0, minValueYPixel, 0, maxValueYPixel);
        // A kind of red for min.
        gradient.addColorStop(0, dataset.colorStart);
        // A kind of blue for max.
        gradient.addColorStop(1, dataset.colorEnd);
        // Assign the gradient to the dataset's border color.
        dataset.borderColor = gradient;
      })
    } else if (chartInstance.options.radialGradientDonut) {
      // The context, needed for the creation of the linear gradient.
      let ctx = chartInstance.chart.ctx;

      chartInstance.data.datasets.forEach((dataset) => {
        let centerX = ((chartInstance.chartArea.left + chartInstance.chartArea.right) / 2);
        let centerY = ((chartInstance.chartArea.top + chartInstance.chartArea.bottom) / 2);

        // Create the gradient.
        let gradient = ctx.createRadialGradient(centerX, centerY, (chartInstance.innerRadius * 2) * (20 / 100), centerX, centerY, (chartInstance.innerRadius * 2));
        // A kind of red for min.
        gradient.addColorStop(0, dataset.colorStart);
        // A kind of blue for max.
        gradient.addColorStop(1, dataset.colorEnd);
        // Assign the gradient to the dataset's border color.
        dataset.backgroundColor = gradient;
      })

    }
  }
};

export default gradientLinePlugin;
