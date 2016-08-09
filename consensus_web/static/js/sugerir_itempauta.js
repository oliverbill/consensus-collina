jQuery(document).ready(function() {

    $('#combo_votacao').on('change', function()  {

        var option = $(this).find("option:selected").text();

        if (option.indexOf('outras') > -1){
            $('#div_votacao_outros').show()
        }else{
            $('#div_votacao_outros').hide()
        }


      }
     );

    $('#add_opcao_voto').on('click',function(e)  {
        e.preventDefault();
        index = $('#combo_votacao_outros').last().index();
        nomeIncrementado = "votacao_outros-" + index
        $('#form_sugerir_itempauta')
            .append(
                $(
                    '<br><input name="'+nomeIncrementado+'"/>')
                 );
        index++
      }
    );

    $(function() {
    $('#upload-file-btn').click(function(e) {
        e.preventDefault();
        var form_data = new FormData($('#form_sugerir_itempauta')[0]);
        $.ajax({
                type: 'POST',
                url: '/sugerir-item-pauta/upload',
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                async: false,
                success: function(data) {
                    console.log('Sucesso !');
                },
            });
        });
    });

});

