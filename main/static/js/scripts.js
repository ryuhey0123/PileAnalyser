window.addEventListener('DOMContentLoaded', function() {
    login();
    update_selectable_projects();
});

const saveForm = document.getElementById("saveForm");
saveForm.project.onchange = () => update_selectable_contents();

const loadForm = document.getElementById("loadForm");

const inputForm = document.getElementById("inputForm");

const loading_spiner = document.getElementById("loading-spiner");


function add_options(node, titles) {
    for (let i = 0; i < titles.length; i++) {
        let option = document.createElement("option");
        option.text = titles[i];
        node.appendChild(option);
    }
}

function delete_options(node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
}

function update_selectable_projects() {
    $.ajax({
        type: 'POST',
        url: '/get_projects',
        data: '',
        contentType: false,
        beforeSend: function() {
            delete_options(saveForm.project);
        }
    }).done(function(data) {
        add_options(saveForm.project, data.titles);
    });
}

function update_selectable_contents() {
    $.ajax({
        type: 'POST',
        url: '/get_contents_name',
        data: JSON.stringify({'project': saveForm.project.value}),
        contentType: 'application/json',
        beforeSend: function() {
            delete_options(loadForm.contents);
        }
    }).done(function(data) {
        if (data.titles != '') {
            add_options(loadForm.contents, data.titles);
        }
    });
}


function login() {
    const userData = JSON.stringify({
        'name': 'admin',
        'password': 'admin'
    });

    $.ajax({
        type: 'POST',
        url: '/login',
        data: userData,
        contentType: 'application/json'
    });
}


function init() {
    solve_button();

    $.ajax({
        type: 'POST',
        url: '/init_upload_ajax',
        data: "",
        contentType: false,
        processData: false,
        beforeSend: function() {
            loading_spiner.style.display = "block";
        },
    }).done(function(data) {
        $("#soil-table").html(data);
        loading_spiner.style.display = "none";
    }).complete(function(data) {
        loading_spiner.style.display = "none";
    });
}


function save_button() {
    const inputData = JSON.stringify({
        "inputs": {
            "mode": inputForm.mode.value,
            "condition": inputForm.condition_value.value,
            "bottom_condition": inputForm.bottom_condition.value,
            "material": inputForm.material.value,
            "diameter": inputForm.diameter.value,
            "length": inputForm.pile_length.value,
            "level": inputForm.level.value,
            "force": inputForm.force.value
        },
        "contents": {
            "project": saveForm.project.value,
            "title": saveForm.title.value
        }
    });

    $.ajax({
        type: 'POST',
        url: '/save',
        data: inputData,
        contentType: 'application/json',
    }).done(function() {
        update_selectable_contents();
        saveForm.title.value = '';
    });
}


function solve_button() {
    const inputForm = document.getElementById("inputForm");
    const inputData = JSON.stringify({
        "mode": inputForm.mode.value,
        "condition": inputForm.condition_value.value,
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
        beforeSend: function() {
            loading_spiner.style.display = "block";
        },

    }).done(function(data) {
        var result = JSON.parse(data);
        update_summary(result.results);
        plot_graph(result.results);
        document.getElementById("time").innerText = result.time;
        document.getElementById("soil-data-details").open = false;
        loading_spiner.style.display = "none";

    }).complete(function(data) {
        loading_spiner.style.display = "none";
    });
}


function file_upload() {

    const form_data = new FormData($('#upload-file').get(0));

    $.ajax({
        type: 'POST',
        url: '/upload_ajax',
        data: form_data,
        contentType: false,
        processData: false,

    }).done(function(data) {
        $("#soil-table").html(data);
        document.getElementById("soil-data-details").open = true;

    }).complete(function(data) {
        loading_spiner.style.display = "none";
    });
}


function update_summary(results) {

    function max_and_min_values_by(key, fixed=1) {

        const aryMax = function (a, b) {return Math.max(a, b);};
        const aryMin = function (a, b) {return Math.min(a, b);};

        const ary = results[key];
        const maximum = ary.reduce(aryMax);
        const minimum = ary.reduce(aryMin);

        return [maximum.toFixed(fixed), minimum.toFixed(fixed)];
    }

    const summary = {
        kh: max_and_min_values_by('kh0s'),
        deformation: max_and_min_values_by('y', field='2'),
        degree: max_and_min_values_by('t', field='3'),
        moment: max_and_min_values_by('m'),
        shear: max_and_min_values_by('q'),
    };

    document.getElementById("kh_max").innerText = summary.kh[0];
    document.getElementById("kh_min").innerText = summary.kh[1];
    document.getElementById("deformation_max").innerText = summary.deformation[0];
    document.getElementById("deformation_min").innerText = summary.deformation[1];
    document.getElementById("degree_max").innerText = summary.degree[0];
    document.getElementById("degree_min").innerText = summary.degree[1];
    document.getElementById("moment_max").innerText = summary.moment[0];
    document.getElementById("moment_min").innerText = summary.moment[1];
    document.getElementById("shear_max").innerText = summary.shear[0];
    document.getElementById("shear_min").innerText = summary.shear[1];
}


function plot_graph(results) {

    const trace_dec = {x: results.dec, y: results.x, fill: 'tozerox', type: 'scatter'};
    const trace_kh0s = {x: results.kh0s, y: results.x, xaxis: 'x2', yaxis: 'y2', fill: 'tozerox', type: 'scatter'};
    const trace_y = {x: results.y, y: results.x, xaxis: 'x3', yaxis: 'y3', fill: 'tozerox', type: 'scatter'};
    const trace_t = {x: results.t, y: results.x, xaxis: 'x4', yaxis: 'y4', fill: 'tozerox', type: 'scatter'};
    const trace_m = {x: results.m, y: results.x, xaxis: 'x5', yaxis: 'y5', fill: 'tozerox', type: 'scatter'};
    const trace_q = {x: results.q, y: results.x, xaxis: 'x6', yaxis: 'y6', fill: 'tozerox', type: 'scatter'};

    const data = [trace_dec, trace_kh0s, trace_y, trace_t, trace_m, trace_q];

    const layout = {
        grid: {
            rows: 1,
            columns: 6,
            subplots: ['xy', 'x2y', 'x3y', 'x4y', 'x5y', 'x6y']
        },

        yaxis:  {autorange: 'reversed'},
        yaxis2: {autorange: 'reversed'},
        yaxis3: {autorange: 'reversed'},
        yaxis4: {autorange: 'reversed'},
        yaxis5: {autorange: 'reversed'},
        yaxis6: {autorange: 'reversed'},

        xaxis:  {hoverformat: '.3f'},
        xaxis2: {hoverformat: '.1f'},
        xaxis3: {hoverformat: '.2f'},
        xaxis4: {hoverformat: '.3f'},
        xaxis5: {hoverformat: '.1f'},
        xaxis6: {hoverformat: '.1f'},

        showlegend: false,
        autosize: true,
        margin: {l: 20, r: 20, b: 50, t: 70},

        colorway: ["#795548", "#9C27B0", "#2196F3", "#FFC107", "#E91E63", "#4CAF50"],
        plot_bgcolor: "#FFFFFF",

        hovermode: 'closest',

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
        ],
    };

    Plotly.newPlot('figure', data, layout);
}
