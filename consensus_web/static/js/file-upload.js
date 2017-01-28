$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: '/sugerir-item-pauta/upload',
        disableImageResize: /Android(?!.*Chrome)|Opera/.test(window.navigator.userAgent),
        maxFileSize: 5000000,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png|pdf|doc|docx|xls|xlsx|png|bmp|txt)$/i
    });

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

// nao mostra os arquivos presentes no diretorio

//    $('#fileupload').addClass('fileupload-processing');
//    $.ajax({
//        // Uncomment the following to send cross-domain cookies:
//        //xhrFields: {withCredentials: true},
//        url: $('#fileupload').fileupload('option', 'url'),
//        dataType: 'json',
//        context: $('#fileupload')[0]
//    }).always(function () {
//        $(this).removeClass('fileupload-processing');
//    }).done(function (result) {
//        $(this).fileupload('option', 'done')
//            .call(this, $.Event('done'), {result: result});
//    });

});
