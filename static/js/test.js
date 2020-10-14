function test_ajax() {
    $.ajax({
        type: 'POST',
        url: '/test_ajax',
        data: '',
        contentType: 'application/json',
        success: function(data) {
            console.log(data)
            const message = data.message
            document.getElementById('ajax_test').innerHTML = message
        }
    })
}
