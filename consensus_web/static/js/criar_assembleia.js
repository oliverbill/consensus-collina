jQuery(document).ready(function() {

/*
     amanha = moment().add(1, 'days');
     amanha_as_nove = moment(amanha).hour("09").minute("00")
     $("#data_inicio_text").val(amanha_as_nove.format('YYYY-MM-DD HH:mm').toString());
*/

      $("#help").hide()

      $('#data_inicio').datetimepicker({
        daysOfWeekDisabled: [0, 6],
        minDate: moment(),
        useCurrent: false,
        sideBySide: true,
        useStrict: true
      });

      $('#data_fim').datetimepicker({
        daysOfWeekDisabled: [0, 6],
        minDate: moment().add(1,'days'),
        useCurrent: false,
        sideBySide: true,
        useStrict: true
      });


      $("#data_inicio_text").blur(function() {
        data_inicio = $("#data_inicio_text").val()
        if (data_inicio != "")
        {
            data_fim = moment(data_inicio, "DD/MM/YYYY HH:mm").add(7, 'days').format('DD/MM/YYYY HH:mm').toString();
            $("#data_fim_text").val(data_fim);

            $("#help").show()
        }
      });

});

