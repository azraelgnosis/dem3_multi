$(document).ready(function() {
    function line_graph() {
        var elem = $(this);
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
    }

    $("div.line_graph").each(function() {
        var data_points = $(this).attr("data").split(',')//.map(x=>+x);
        
        console.log(data_points);

        var options = {
            data: [{
                type: "line",
                dataPoints: []
            }]
        }

    });

    $("div.line_graph").CanvasJSChart({
        data: [{
            type: "line",
            dataPoints: [
                { x: 10, y: 10 },
                { x: 20, y: 14 },
                { x: 30, y: 18 },
                { x: 40, y: 22 },
                { x: 50, y: 18 },
                { x: 60, y: 28 }
            ]
        }]
    })
});