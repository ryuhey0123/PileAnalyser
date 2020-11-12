// DOMs

const saveForm = document.getElementById("saveForm");

const loadForm = document.getElementById("loadForm");
loadForm.project.onchange = () => update_selectable_contents(loadForm);

const inputForm = document.getElementById("inputForm");
const loading_spiner = document.getElementById("loading-spiner");

const inputData = () => { return {
    "mode": inputForm.mode.value,
    "condition": inputForm.condition_value.value,
    "bottom_condition": inputForm.bottom_condition.value,
    "div_num": 100,
    "material": inputForm.material.value,
    "diameter": inputForm.diameter.value,
    "length": inputForm.pile_length.value,
    "level": inputForm.level.value,
    "force": inputForm.force.value
};};

$("switch.ios-toggle").click((e)=>{$(e.target).toggleClass("on");});

// jQuery

var $body = $('body');

$('.menu-open-btn').on('click', function(){
  $body.addClass('is-menu-open');
  return false;
});

$('.menu-close-btn').on('click', function(){
  $body.removeClass('is-menu-open');
  return false;
});

// Functions

window.addEventListener('DOMContentLoaded', function() {
    loading_spiner.style.display = "block";

    $("switch.ios-toggle").toggleClass("on");

    login();

    (async() => {
        await update_selectable_projects(saveForm);
        await update_selectable_projects(loadForm);
        await update_selectable_contents(loadForm);
    })();

    solve_button();

    $.post('/upload', NaN, function(data) {
        $("#soil-table").html(data);
    });

    loading_spiner.style.display = "none";
});

function add_options(select_node, titles) {
    for (let i = 0; i < titles.length; i++) {
        let option = document.createElement("option");
        option.text = titles[i];
        select_node.appendChild(option);
    }
}

function delete_options(node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
}

async function update_selectable_projects(node) {
    delete_options(node.project);
    await $.ajax({
        type: 'GET',
        url: '/database/projects',
    }).done(function(data) {
        add_options(node.project, data.titles);
    });
}

async function update_selectable_contents(node) {
    delete_options(node.contents);
    await $.ajax({
        type: 'GET',
        url: '/database/contents/' + node.project.value,
    }).done(function(data) {
        if (data.titles != '') {
            add_options(node.contents, data.titles);
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

function save_button() {
    const data = JSON.stringify({
        "inputs": inputData(),
        "contents": {
            "project": saveForm.project.value,
            "title": saveForm.title.value
        }
    });

    $.ajax({
        type: 'POST',
        url: '/database/save',
        data: data,
        contentType: 'application/json',
    }).done(function() {
        update_selectable_contents();
        saveForm.title.value = '';
    });
}

function load_button() {
    $.ajax({
        type: 'POST',
        url: '/database/load',
        data: JSON.stringify({'content': loadForm.contents.value, 'project': loadForm.project.value}),
        contentType: 'application/json',
        beforeSend: function() {
            loading_spiner.style.display = "block";
        },
    }).done(function(data) {
        const result = JSON.parse(data);
        const input = result.input;
        const soil_data = result.soil_data;

        inputForm.mode.value = input.mode;
        inputForm.condition_value.value = input.condition;
        inputForm.bottom_condition.value = input.bottom_condition;
        inputForm.material.value = input.material;
        inputForm.diameter.value = input.diameter;
        inputForm.pile_length.value = input.length;
        inputForm.level.value = input.level;
        inputForm.force.value = input.force;

        $("#soil-table").html(soil_data);

        solve_button();

        loading_spiner.style.display = "none";
    }).complete(function(data) {
        loading_spiner.style.display = "none";
    });
}

function solve_button() {
    loading_spiner.style.display = "block";

    $.ajax({
        type: 'POST',
        url: '/solve',
        data: JSON.stringify(inputData()),
        contentType: 'application/json',
    }).done(function(data) {
        const result = JSON.parse(data);

        update_summary(result.results);
        plot_graph(result.results);

        document.getElementById("time").innerText = result.time;
        document.getElementById("soil-data-details").open = false;
        loading_spiner.style.display = "none";
    });
}

async function file_upload() {
    const form_data = new FormData($('#upload-file').get(0));

    await $.ajax({
        type: 'POST',
        url: '/upload',
        data: form_data,
        contentType: false,
        processData: false,
    }).done(function(data) {
        $("#soil-table").html(data);
        document.getElementById("soil-data-details").open = true;
    });
}

async function update_summary(results) {

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

async function plot_graph(results) {

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
