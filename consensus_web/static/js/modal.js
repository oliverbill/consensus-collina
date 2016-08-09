jQuery(document).ready(function() {

     $('#modal').on('show.bs.modal', function (e) {
        id = $(e.relatedTarget).data('id');
        $('#num_sugestao').val(id);
     });


    $('#btn_confirmar').on('click', function (event) {
          num_sugestao = $('#num_sugestao').val();
          url = "/aprovar-sugestao/" + num_sugestao + "/"

          $.post( url, function( data ) {
              $(location).attr('href', data)
          });

          $('#modal').modal('hide');
    })
});