jQuery(document).ready(function() {

    btn_classes = ['btn btn-primary','btn btn-warning','btn btn-danger'];

    /* guarda o TEXTO de cada label, sem repetí-lo  */
    var textosLabels = new Set();
    $('.btn-group > label').each(function(index) {
        textosLabels.add($(this).text().trim());
    });

    /*  mapeia cada classe para um label */
    var mapaLabelsClasses = new Map();
    var i = 0;
    textosLabels.forEach(function (label) {
        mapaLabelsClasses.set(label,btn_classes[i++]);
    });

    /* atribui uma classe para cada label */
    mapaLabelsClasses.forEach(function (value,key) {
        $(".btn-group > label:contains('"+ key +"')").attr('class', value);
    });

});