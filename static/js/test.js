function init() {
    solve_button()

    $.ajax({
        type: 'POST',
        url: '/init_upload_ajax',
        data: "",
        contentType: false,
        processData: false,
        success: function(data) {
            $("#soil-table").html(data)
        },
    });
}


function solve_button() {
    var inputForm = document.getElementById("inputForm");
    var inputData = JSON.stringify({
        "mode": inputForm.mode.value,
        "condition": inputForm.condition.value,
        "bottom_condition": inputForm.bottom_condition.value,
        "material": inputForm.material.value,
        "diameter": inputForm.diameter.value,
        "length": inputForm.pile_length.value,
        "level": inputForm.level.value,
        "force": inputForm.force.value
    });

    $.ajax({
        type: 'POST',
        url: '/solve',
        data: inputData,
        contentType: 'application/json',
        success: function(data) {
            var result = JSON.parse(data);

            document.getElementById("time").innerText = result.time;

            document.getElementById("kh_max").innerText = result.summary.kh[0];
            document.getElementById("kh_min").innerText = result.summary.kh[1];
            document.getElementById("deformation_max").innerText = result.summary.deformation[0];
            document.getElementById("deformation_min").innerText = result.summary.deformation[1];
            document.getElementById("degree_max").innerText = result.summary.degree[0];
            document.getElementById("degree_min").innerText = result.summary.degree[1];
            document.getElementById("moment_max").innerText = result.summary.moment[0];
            document.getElementById("moment_min").innerText = result.summary.moment[1];
            document.getElementById("shear_max").innerText = result.summary.shear[0];
            document.getElementById("shear_min").innerText = result.summary.shear[1];

            plot_glaph(result.results)

            // var figure = document.getElementById("figure-iframe");
            // figure.contentWindow.document.open();
            // figure.contentWindow.document.write(result.fig);
            // figure.contentWindow.document.close();
            // plot_glaph();

            document.getElementById("soil-data-details").open = false;
        }
    })
}


function file_upload() {

    var form_data = new FormData($('#upload-file').get(0));

    $.ajax({
        type: 'POST',
        url: '/upload_ajax',
        data: form_data,
        contentType: false,
        processData: false,
        success: function(data) {
            $("#soil-table").html(data)
            document.getElementById("soil-data-details").open = true;
        },
    });
};

function plot_glaph(results) {

    var trace_dec = {x: results['dec'], y: results['x'], fill: 'tozerox', type: 'scatter'};
    var trace_kh0s = {x: results['kh0s'], y: results['x'], xaxis: 'x2', yaxis: 'y2', fill: 'tozerox', type: 'scatter'};
    var trace_y = {x: results['y'], y: results['x'], xaxis: 'x3', yaxis: 'y3', fill: 'tozerox', type: 'scatter'};
    var trace_t = {x: results['t'], y: results['x'], xaxis: 'x4', yaxis: 'y4', fill: 'tozerox', type: 'scatter'};
    var trace_m = {x: results['m'], y: results['x'], xaxis: 'x5', yaxis: 'y5', fill: 'tozerox', type: 'scatter'};
    var trace_q = {x: results['q'], y: results['x'], xaxis: 'x6', yaxis: 'y6', fill: 'tozerox', type: 'scatter'};

    var data = [trace_dec, trace_kh0s, trace_y, trace_t, trace_m, trace_q];

    var layout = {
        grid: {
            rows: 1,
            columns: 6,
            subplots: ['xy', 'x2y', 'x3y', 'x4y', 'x5y', 'x6y']
        },

        yaxis: {autorange: 'reversed'},
        yaxis2: {autorange: 'reversed'},
        yaxis3: {autorange: 'reversed'},
        yaxis4: {autorange: 'reversed'},
        yaxis5: {autorange: 'reversed'},
        yaxis6: {autorange: 'reversed'},

        showlegend: false,
        autosize: true,
        margin: {l: 20, r: 20, b: 10, t: 50},

        annotations: [
            {
                text: "Decrease",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.03,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },
            {
                text: "kh0s",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.2,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },
            {
                text: "Deformation",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.42,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },
            {
                text: "Degree",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.60,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },
            {
                text: "Moment",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.82,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },
            {
                text: "Shear",
                font: {size: 14},
                showarrow: false,
                align: 'center',
                x: 0.95,
                y: 1.10,
                xref: 'paper',
                yref: 'paper',
            },

        ]
    };

    Plotly.newPlot('figure', data, layout);
}
