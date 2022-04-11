import jsonData from './final_results.json' assert { type: "json" };
console.log(jsonData['journals'].slice(0, 10));
    
let chart = am4core.create("journal-pie-chart", am4charts.PieChart);

var series = chart.series.push(new am4charts.PieSeries());
series.dataFields.value = "data";
series.dataFields.category = "key";

// Add data
chart.data = jsonData['self_cit_area'];

// And, for a good measure, let's add a legend
chart.legend = new am4charts.Legend();

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
    