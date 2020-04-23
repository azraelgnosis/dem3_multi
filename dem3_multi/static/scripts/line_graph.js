$(document).ready(function() {
    console.log(data_points);
    $("div.line_graph").CanvasJSChart(
        {
            title: {
                text: $("div.line_graph").attr('title')
            },
            axisY: {
                prefix: prefix | "",
                suffix: suffix | ""
            },
            data: [
                {
                    type: "line",
                    dataPoints: data_points.map(x => {return  {y: x} })
                }
            ]

        }
    );
});