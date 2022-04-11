import jsonData from './final_results.json' assert { type: "json" };
console.log(jsonData['self_cit_area']);
    
let chart = am4core.create("chartdiv", am4charts.PieChart);

var series = chart.series.push(new am4charts.PieSeries());
series.dataFields.value = "data";
series.dataFields.category = "key";

// Add data
chart.data = jsonData['self_cit_area'];

// And, for a good measure, let's add a legend
chart.legend = new am4charts.Legend();