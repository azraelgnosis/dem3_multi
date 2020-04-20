$(document).ready(function() {
    var data_points = [];
    for (let i = 0; i < cost_history.length; i++) {
        data_points.push({x:i, y:cost_history[i]});
    }

    var chart = new CanvasJS.Chart("graph", {
        title: {
            text: "Cost History"
        },
        data: [{
            type: "line",
            dataPoints: data_points
        }]
    });

    chart.render();
});