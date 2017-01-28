jQuery(document).ready(function() {

    $('#combo_votacao').on('change', function(){
        mostrarOuEsconderDivOutrasOpcoesVoto();
    });

// acionado antes de terminar de carregar a pagina
    window.onload = function(){
        mostrarOuEsconderDivOutrasOpcoesVoto();
    };

// se o usuario selecionar outros, mostra o div com as 2 textbox para informar outras opções de voto
    function mostrarOuEsconderDivOutrasOpcoesVoto(){
        var option = $('#combo_votacao').find("option:selected").text();

        if (option.indexOf('outras') > -1){
            $('#div_votacao_outros').show();
            addRequired();
        }else{
            $('#div_votacao_outros').hide();
            addNoValidate();
        }
    };

    function addNoValidate(){
        $('div:hidden').find('#combo_votacao_outros').find('ul:hidden').children().find('input:hidden')
            .each(function()
            {
                $(this).attr("novalidate","");
                $(this).removeAttr("required");
                $('div:hidden').find('#combo_votacao_outros').find('ul:hidden').attr("novalidate","");
                $('div:hidden').find('#combo_votacao_outros').find('ul:hidden').removeAttr("required");
            });
    };

    function addRequired(){
        $('#combo_votacao_outros').find('ul').children().find('input')
            .each(function()
            {
                $(this).attr("required","");
                $(this).removeAttr("novalidate");
                $(this).parent().parent().attr("required","");
                $(this).parent().parent().removeAttr("novalidate");
            });
    };

// adiciona mais uma textbox de opção de voto (além das 2 acima) para cada click no botão
    $('#add_opcao_voto').on('click',function(e)  {
        e.preventDefault();

        var name = $('#outra_opcao_voto').children().last().find('input').attr("name");
        var idx_fim = name.indexOf("-") + 1;
        var num = name.substring(idx_fim).trim();
        var numNovo = parseInt(num) + 1;
        var nameNovo = name.replace(num,numNovo).trim();

        $('#outra_opcao_voto').append( $('<li><label for=' + nameNovo + '> </label><input name=' + nameNovo + ' required="True"/></li>') );

        $.ajax({
            type: 'POST',
            url: ' /add-opcao-voto/',
            async: false, // para poder retornar o resultado
            success: function(data) {
                console.log('Sucesso !');
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('#csrf_token').val());
            }
        });
     });

    $(function () {
      $('[data-toggle="popover"]').popover()
    });

    setInterval(function(){
        if( $('#count_char').is(":visible") ){
            var max = $('#descricao').attr("maxlength");
            var len = $('#descricao').val().length;
            var char = max - len;

            if (len >= max) {
                $('#count_char').text('Você atingiu o número máximo de carácteres.');
            }else if ( (max - len) == 1) {
                $('#count_char').text('carácteres restantes: ' + char);
            }else{
                $('#count_char').text('carácteres restantes: ' + char);
            }
        }
    }, 500);

});

