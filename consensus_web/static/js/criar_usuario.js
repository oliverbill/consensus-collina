jQuery(document).ready(function() {

    $("#criar").prop("disabled",true);

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

    var isSenhaConfirmada = false;
    var isSenhaValidada = false;

   $('#confirma_senha').blur(function() {
        if ($(this).val() == $('#senha').val()){
            isSenhaConfirmada = true;
        }

        if (isSenhaValidada && isSenhaConfirmada)
        {
            $("#criar").prop("disabled",false);
        }
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

        var isLengthValidated = false;
        var isLetterValidated = false;
        var isSpecialCharValidated = false;
        var isNumberValidated = false;

        //validate the length
        if ( pswd.length < 8 | pswd.length > 10) {
            $('#length').removeClass('valid').addClass('invalid');
        } else {
            $('#length').removeClass('invalid').addClass('valid');
            isLengthValidated = true;
        }

        //validate letter
        if ( pswd.match(/[A-z]/) ) {
            $('#letter').removeClass('invalid').addClass('valid');
            isLetterValidated = true;
        } else {
            $('#letter').removeClass('valid').addClass('invalid');
        }

        //validate caracteres especiais
        if ( pswd.match(/[@#$%^&+=]/) ) {
            $('#special_char').removeClass('invalid').addClass('valid');
            isSpecialCharValidated = true;
        } else {
            $('#special_char').removeClass('valid').addClass('invalid');
        }

        //validate number
        if ( pswd.match(/\d/) ) {
            $('#number').removeClass('invalid').addClass('valid');
            isNumberValidated = true;
        } else {
            $('#number').removeClass('valid').addClass('invalid');
        }

        if(isLengthValidated && isLetterValidated && isSpecialCharValidated && isNumberValidated)
        {
            isSenhaValidada = true;
        }
    }

});