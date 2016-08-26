jQuery(document).ready(function() {

    $('#data_nascimento').datetimepicker({
        useCurrent: false,
        viewMode: 'years',
        format: 'DD/MM/YYYY'
    });


    $('#roles').change(function() {
        $.ajax({
            type: 'post',
            data: 'role_id=' + $(this).val(),
            url: '/get-permissoes/',
            async: false, // para poder retornar o resultado
            success: function(data) {
                console.log('Sucesso !');
                var listaLI = new Array();
                data.split(',').forEach(function(e){
                    listaLI.push($('<li>').append(e));
                });
                console.log(listaLI);
                $('#privilegios').append(listaLI);
                if (data != null){
                    $('#role_info').show();
                }
            }
        });
    });

/* validacao de senha */

    $('#senha').keyup(function() {
        validarSenha($('#senha'));
    }).focus(function() {
        $('#pswd_info').show();
    }).blur(function() {
        $('#pswd_info').hide();
    });

    function validarSenha(txtSenha)
    {
        // set password variable
        var pswd = txtSenha.val();

        //validate the length
        if ( pswd.length < 8 | pswd.length > 10) {
            $('#length').removeClass('valid').addClass('invalid');
        } else {
            $('#length').removeClass('invalid').addClass('valid');
        }

        //validate letter
        if ( pswd.match(/[A-z]/) ) {
            $('#letter').removeClass('invalid').addClass('valid');
        } else {
            $('#letter').removeClass('valid').addClass('invalid');
        }

        //validate caracteres especiais
        if ( pswd.match(/[@#$%^&+=]/) ) {
            $('#special_char').removeClass('invalid').addClass('valid');
        } else {
            $('#special_char').removeClass('valid').addClass('invalid');
        }

        //validate number
        if ( pswd.match(/\d/) ) {
            $('#number').removeClass('invalid').addClass('valid');
        } else {
            $('#number').removeClass('valid').addClass('invalid');
        }
    }

});