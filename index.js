import jsonData from './results/final_results.json' assert { type: "json" };

console.log(jsonData);

// self citation pie by area
let self_cit_area_chart = am4core.create("self-cit-pie", am4charts.PieChart);

var series = self_cit_area_chart.series.push(new am4charts.PieSeries());
series.dataFields.value = "data";
series.dataFields.category = "key";

// Add data
self_cit_area_chart.data = jsonData['self_cit_area'];


// bar chart //

am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create chart instance
    var bar_chart_journals = am4core.create("top-journals", am4charts.XYChart);
    
    // Add data
    bar_chart_journals.data = jsonData['journals'].slice(0, 10);
    
    // Create axes
    
    var categoryAxis = bar_chart_journals.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "key";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 30;
    categoryAxis.renderer.labels.template.fontSize = 11;
    
    categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
      if (target.dataItem && target.dataItem.index & 2 == 2) {
        return dy + 25;
      }
      return dy;
    });

    // fix labels
    categoryAxis.renderer.labels.template.truncate = true;

    categoryAxis.renderer.labels.template.maxWidth = 180;

    var valueAxis = bar_chart_journals.yAxes.push(new am4charts.ValueAxis());
    
    // Create series
    var series = bar_chart_journals.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = "data";
    series.dataFields.categoryX = "key";
    series.name = "Visits";
    series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
    series.columns.template.fillOpacity = .8;
    
    var columnTemplate = series.columns.template;
    columnTemplate.strokeWidth = 2;
    columnTemplate.strokeOpacity = 1;
    
    }); // end am4core.ready()


// bar chart fields//

am4core.ready(function() {

  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  
  // Create chart instance
  var bar_chart_journals = am4core.create("top-fields", am4charts.XYChart);
  
  // Add data
  bar_chart_journals.data = jsonData['areas_fields'].slice(0, 10);
  
  // Create axes
  
  var categoryAxis = bar_chart_journals.xAxes.push(new am4charts.CategoryAxis());
  categoryAxis.dataFields.category = "key";
  categoryAxis.renderer.grid.template.location = 0;
  categoryAxis.renderer.minGridDistance = 30;
  
//fix labels
categoryAxis.renderer.labels.template.truncate = true;
categoryAxis.renderer.labels.template.maxWidth = 180;
categoryAxis.renderer.labels.template.fontSize = 11;

  categoryAxis.renderer.labels.template.adapter.add("dy", function(dy, target) {
    if (target.dataItem && target.dataItem.index & 2 == 2) {
      return dy + 25;
    }
    return dy;
  });
  
  var valueAxis = bar_chart_journals.yAxes.push(new am4charts.ValueAxis());
  
  // Create series
  var series = bar_chart_journals.series.push(new am4charts.ColumnSeries());
  series.dataFields.valueY = "data";
  series.dataFields.categoryX = "key";
  series.name = "Visits";
  series.columns.template.tooltipText = "{categoryX}: [bold]{valueY}[/]";
  series.columns.template.fillOpacity = .8;
  
  var columnTemplate = series.columns.template;
  columnTemplate.strokeWidth = 2;
  columnTemplate.strokeOpacity = 1;
  
  }); // end am4core.ready()

// nested pie cart **Bisogna settare manualmente il numero di sottocategorie, va normalizzato in qualche modo

am5.ready(function() {

  // Create root element
  // https://www.amcharts.com/docs/v5/getting-started/#Root_element
  var root = am5.Root.new("nested-piechart");
  
  // Set themes
  // https://www.amcharts.com/docs/v5/concepts/themes/
  root.setThemes([am5themes_Animated.new(root)]);
  
  var container = root.container.children.push(
    am5.Container.new(root, {
      width: am5.p100,
      height: am5.p100,
      layout: root.horizontalLayout
    })
  );
  
  // Create main chart
  // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
  var chart = container.children.push(
    am5percent.PieChart.new(root, {
      tooltip: am5.Tooltip.new(root, {})
    })
  );
  
  // Create series
  // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
  var series = chart.series.push(
    am5percent.PieSeries.new(root, {
      valueField: "value",
      categoryField: "category",
      alignLabels: false
    })
  );
  
  series.labels.template.setAll({
    textType: "circular",
    radius: 4
  });
  series.ticks.template.set("visible", false);
  series.slices.template.set("toggleKey", "none");
  
  // add events
  series.slices.template.events.on("click", function(e) {
    selectSlice(e.target);
  });
  
  // Create sub chart
  // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/
  var subChart = container.children.push(
    am5percent.PieChart.new(root, {
      radius: am5.percent(50),
      tooltip: am5.Tooltip.new(root, {})
    })
  );
  
  // Create sub series
  // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Series
  var subSeries = subChart.series.push(
    am5percent.PieSeries.new(root, {
      valueField: "value",
      categoryField: "category"
    })
  );
  
  subSeries.data.setAll([
    { category: "A", value: 0 },
    { category: "B", value: 0 },
    { category: "C", value: 0 },
    { category: "D", value: 0 },
    { category: "E", value: 0 },
    
  ]);
  subSeries.slices.template.set("toggleKey", "none");
  
  var selectedSlice;
  
  series.on("startAngle", function() {
    updateLines();
  });
  
  container.events.on("boundschanged", function() {
    root.events.on("frameended", function(){
      updateLines();
     })
  })
  
  function updateLines() {
    if (selectedSlice) {
      var startAngle = selectedSlice.get("startAngle");
      var arc = selectedSlice.get("arc");
      var radius = selectedSlice.get("radius");
  
      var x00 = radius * am5.math.cos(startAngle);
      var y00 = radius * am5.math.sin(startAngle);
  
      var x10 = radius * am5.math.cos(startAngle + arc);
      var y10 = radius * am5.math.sin(startAngle + arc);
  
      var subRadius = subSeries.slices.getIndex(0).get("radius");
      var x01 = 0;
      var y01 = -subRadius;
  
      var x11 = 0;
      var y11 = subRadius;
  
      var point00 = series.toGlobal({ x: x00, y: y00 });
      var point10 = series.toGlobal({ x: x10, y: y10 });
  
      var point01 = subSeries.toGlobal({ x: x01, y: y01 });
      var point11 = subSeries.toGlobal({ x: x11, y: y11 });
  
      line0.set("points", [point00, point01]);
      line1.set("points", [point10, point11]);
    }
  }
  
  // lines
  var line0 = container.children.push(
    am5.Line.new(root, {
      position: "absolute",
      stroke: root.interfaceColors.get("text"),
      strokeDasharray: [2, 2]
    })
  );
  var line1 = container.children.push(
    am5.Line.new(root, {
      position: "absolute",
      stroke: root.interfaceColors.get("text"),
      strokeDasharray: [2, 2]
    })
  );
  
  // Set data
  // https://www.amcharts.com/docs/v5/charts/percent-charts/pie-chart/#Setting_data
  series.data.setAll(jsonData['areas_GroupsAndSuper']);
  
  function selectSlice(slice) {
    selectedSlice = slice;
    var dataItem = slice.dataItem;
    var dataContext = dataItem.dataContext;
  
    if (dataContext) {
      var i = 0;
      subSeries.data.each(function(dataObject) {
        subSeries.data.setIndex(i, dataContext.subData[i]);
        i++;
      });
    }
  
    var middleAngle = slice.get("startAngle") + slice.get("arc") / 2;
    var firstAngle = series.dataItems[0].get("slice").get("startAngle");
  
    series.animate({
      key: "startAngle",
      to: firstAngle - middleAngle,
      duration: 1000,
      easing: am5.ease.out(am5.ease.cubic)
    });
    series.animate({
      key: "endAngle",
      to: firstAngle - middleAngle + 360,
      duration: 1000,
      easing: am5.ease.out(am5.ease.cubic)
    });
  }
  
  container.appear(1000, 10);
  
  series.events.on("datavalidated", function() {
    selectSlice(series.slices.getIndex(0));
  });
  
  }); // end am5.ready()

  // chord diagram

  am5.ready(function() {

    // Create root element
    var root = am5.Root.new("chord-diagram");
    
    
    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/
    root.setThemes([
      am5themes_Animated.new(root)
    ]);
    
    
    // Create series
    // https://www.amcharts.com/docs/v5/charts/flow-charts/
    var series = root.container.children.push(am5flow.ChordDirected.new(root, {
      startAngle: 80,
      padAngle: 1,
      linkHeadRadius: undefined,
      sourceIdField: "from",
      targetIdField: "to",
      valueField: "value"
    }));
    
    series.nodes.labels.template.setAll({
      textType: "radial",
      centerX: 0,
      fontSize: 9
    });
    
    series.links.template.set("fillStyle", "source");
    
    
    // Set data
    // https://www.amcharts.com/docs/v5/charts/flow-charts/#Setting_data
    series.data.setAll(jsonData['net']);
    
    
    // Make stuff animate on load
    series.appear(1000, 100);}); // end am5.ready()


//inserting text

$("#articles-counter").html('<p style="margin: 0; position: absolute; font-weight: 600; top: 30%;transform: translateY(-50%);"> <span class="oc-violet">' + jsonData['init']['journals'] + '</span> Different Journals </p> <p style="margin: 0; position: absolute; top: 60%;transform: translateY(-50%); font-weight: 600;"><span class="oc-violet">' + String(jsonData['init']['citing'] + jsonData['init']['cited']) + '</span> Citations Between Articles </p>')