jQuery(document).ready(function() {

    $("#criar").prop("disabled",true);

    $('#criar').click(function(e) {
        e.preventDefault();

        if (validarNumApBloco()){
            $("form").submit();
        }
    });

    $('#num_ap').keyup(function(){
        limparErros();
    });

    $('#bloco').keyup(function(){
        limparErros();
    });

    function limparErros(){
        if (isBlocoValido()){
            $('#erro_bloco').text("");
        }
        if (isNumApValido()){
            $('#erro_num_ap').text("");
        }
    }

    $('#data_nascimento').datetimepicker({
        useCurrent: false,
        viewMode: 'years',
        format: 'DD/MM/YYYY',
        useStrict: true
    });

    $('#roles').change(function() {
        $('#erro_bloco').text("");
        $('#erro_num_ap').text("");

        $.ajax({
            type: 'POST',
            //data: JSON.stringify({ "role_id" : $(this).val()}),
            data: "role_id=" + $(this).val(),
            url: '/get-permissoes/',
            async: false, // para poder retornar o resultado
            success: function(data) {
                console.log('Sucesso !');
                var listaLI = new Array();
                data.split(',').forEach(function(privilegio){
                    listaLI.push($('<li>').append(privilegio));
                });
                console.log(listaLI);
                $('#privilegios').empty();
                $('#privilegios').append(listaLI);
                if (data != null){
                    $('#role_info').show();
                }
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('input:hidden:first').val());
            }
        });

        validarNumApBloco();
    });

    function validarNumApBloco(){
        var out = false;
        if (!isNumApValido()){
            $('#erro_num_ap').text("[campo obrigatório]");
            out = false;
        }else{
            out = true;
        }
        if (!isBlocoValido()){
            $('#erro_bloco').text("[campo obrigatório]");
            out = false;
        }else{
            out = true;
        }
        return out;
    }

    // validacao cruzada: exige preenchimento de num ap e bloco se a role selecionada for MORADORES
    function isNumApValido(){
        // jquery vlidation nao funcionou
        if ($('#num_ap').val() == "" && $("#roles").find('option:selected').val() == 2){
            return false;
        }
        return true;
    }

    // validacao cruzada: exige preenchimento de num ap e bloco se a role selecionada for MORADORES
    function isBlocoValido(){
        // jquery vlidation nao funcionou
        if ($('#bloco').val() == "" && $("#roles").find('option:selected').val() == 2){
            return false;
        }
        return true;
    }

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