Chart.pluginService.register({
  beforeDraw: function (chart) {
    if (chart.config.options.elements.center) {
      //Get ctx from string
      let ctx = chart.chart.ctx;

      //Get options from the center object in options
      let centerConfig = chart.config.options.elements.center;
      let fontStyle = centerConfig.fontStyle || 'Arial';
      let txt = centerConfig.text;
      let color = centerConfig.color || '#000';
      let fontMaxSize = centerConfig.fontMaxSize || null;
      let sidePadding = centerConfig.sidePadding || 20;
      let sidePaddingCalculated = (sidePadding / 100) * (chart.innerRadius * 2);
      //Start with a base font of 30px
      ctx.font = "30px " + fontStyle;

      //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
      let stringWidth = ctx.measureText(txt).width;
      let elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

      // Find out how much the font can grow in width.
      let widthRatio = elementWidth / stringWidth;
      let newFontSize = Math.floor(30 * widthRatio);
      let elementHeight = (chart.innerRadius * 2);

      // Pick a new font size so it will not be larger than the height of label.
      let fontSizeToUse = Math.min(newFontSize, elementHeight);
      if (fontMaxSize && fontMaxSize < fontSizeToUse) {fontSizeToUse = fontMaxSize}

      //Set font settings to draw it correctly.
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      let centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
      let centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
      ctx.font = fontSizeToUse + "px " + fontStyle;
      ctx.fillStyle = color;

      //Draw text in center
      ctx.fillText(txt, centerX, centerY);
    }
  }
});