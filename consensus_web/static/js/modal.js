jQuery(document).ready(function() {

     $('#modal').on('show.bs.modal', function (e) {
        id = $(e.relatedTarget).data('id');
        user_id = $(e.relatedTarget).data('user-id');
        $('#num_sugestao').val(id);
     });


      $('#btn_confirmar').on('click', function (event) {
        num_sugestao = $('#num_sugestao').val();
        var url_var = null;
        if (num_sugestao != null){
            url_var = "/aprovar-sugestao/" + num_sugestao + "/"
        }else{
            url_var = "/admin/remove-user/" + user_id + "/"
        }
        $.ajax({
            type: 'POST',
            url: url_var,
            success: function( data ) {
                    $(location).attr('href', data);
                  },
            async: false, // para poder retornar o resultado
            beforeSend: function(xhr) {
                //$('#csrf_token').val() nao estava funcionando
                xhr.setRequestHeader("X-CSRFToken", $('input:hidden:first').val());
            }
        });

        $('#modal').modal('hide');
    })

});