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

            var figure = document.getElementById("figure-iframe");
            figure.contentWindow.document.open();
            figure.contentWindow.document.write(result.fig);
            figure.contentWindow.document.close();

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
