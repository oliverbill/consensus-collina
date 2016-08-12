jQuery(document).ready(function() {

// se o usuario selecionar outros, mostra o div com as 2 textbox para informar outras opções de voto
    $('#combo_votacao').on('change', function()  {
        var option = $(this).find("option:selected").text();

        if (option.indexOf('outras') > -1){
            $('#div_votacao_outros').show()
        }else{
            $('#div_votacao_outros').hide()
        }
      }
     );

// adiciona mais uma textbox de opção de voto (além das 2 acima) para cada click no botão
    $('#add_opcao_voto').on('click',function(e)  {
        e.preventDefault();
          $('#combo_votacao_outros').append( $('<br><input name="txt_outra_opcao" class="form-control" style="width:50%"/>') );
     });

    $(function () {
      $('[data-toggle="popover"]').popover()
    })

});

