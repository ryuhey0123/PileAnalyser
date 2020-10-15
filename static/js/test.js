function file_upload() {

    var form_data = new FormData($('#upload-file').get(0));

    $.ajax({
        type: 'POST',
        url: '/upload_ajax',
        data: form_data,
        contentType: false,
        processData: false,
        success: function(data) {
            console.log('Success!');
        },
    });
};
