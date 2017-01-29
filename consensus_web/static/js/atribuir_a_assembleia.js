jQuery(document).ready(function() {

    var op_sugestao_sel = "";
    var op_assembleia_sel = "";

  $('#btn_add_itempauta').click(function(e) {
    e.preventDefault();

    val_assembleia_sel = $("#assembleias_combo").find('option:selected').val();
    op_assembleia_sel = $("#assembleias_combo").find('option:selected');

    val_sugestao_sel = $("#sugestoes").find('option:selected').val();
    op_sugestao_sel = $("#sugestoes").find('option:selected');

    sugestao = getSugestaoById(val_sugestao_sel);

    divSugestoes = $("#div-sugestoes" + val_assembleia_sel);

    // cria alert com sugestao dentro
    alert = "";
    alert = $("<div class='alert alert-info' role='alert'>"
                +"<strong>Sugestão #"+sugestao.num+"</strong> => "
                +sugestao.titulo
                +" (sugerido por "+(sugestao.autor == null?"[autor excluído]":sugestao.autor)+")</div>");

    if (divSugestoes.find("div").length == 0){
        $("<br>").insertBefore(alert);
    }

    alert.appendTo(divSugestoes);

    btn_excluir = $("<button type='button' class='close' data-dismiss='alert' aria-label='Close'>"
        +"<span aria-hidden='true'>&times;</span></button>");

    btn_excluir.appendTo(alert);

    // move a tela para o div no qual o alert foi incluído
    $('html, body').stop().animate({
        'scrollTop': divSugestoes.offset().top
    }, 900, 'swing');

    op_sugestao_sel.remove();

    // evento de fechamento dos alerts
    $('.close').click(function(e) {
        /*
            reinclui o alert fechado no combo sugestoes
         */
        num = numSugestaoFromAlert($(this).closest('.alert'));
        titulo = tituloSugestaoFromAlert($(this).closest('.alert'));
        // verifica se o option já foi incluído (previne contra dupla execução do evento .click)
        if (num.length > 0 && titulo.length > 0){
            optionAindaNaoIncluido = $("#sugestoes option[value='"+num+"']").length == 0;
            if (optionAindaNaoIncluido){
                optionFromAlert = $("<option value='"+num+"'>"+titulo+"</option>")
                $("#sugestoes").append(optionFromAlert);
            }
        }
        // remove o alert do div-sugestoes (depois de fechado)
        $(this).closest('.alert').remove();
    });


    });

    function numSugestaoFromAlert(alert){
        if (alert.length){
            textoAlert = alert.text();
            idx_inicio = textoAlert.indexOf("#");
            idx_fim = textoAlert.indexOf("=>");
            num = textoAlert.substring(idx_inicio+1,idx_fim).trim();

            return num;
        }
    }

    function tituloSugestaoFromAlert(alert){
        if (alert.length){
            textoAlert = alert.text();
            idx_inicio = textoAlert.indexOf(" ' ")+1;
            idx_fim = textoAlert.indexOf("(")-1;
            sem_aspas_pattern = /['']+/g
            titulo = textoAlert.substring(idx_inicio,idx_fim).replace(sem_aspas_pattern, '').trim();

            return titulo;
        }
    }

    function numAssembleiaFromPanelHeading(tituloPanel){
        idx_inicio = tituloPanel.trim().indexOf(" ");
        idx_fim = tituloPanel.indexOf(" -");
        num_assembleia = tituloPanel.substring(idx_inicio+2,idx_fim).trim();

        return num_assembleia;
    }

    function getSugestaoById(vl_selecionado) {
        result = "";
        $.ajax({
            type: 'post',
            data: 'sugestao_num='+vl_selecionado,
            url: '/add-itempauta-a-assembleia/',
            async: false, // para poder retornar o resultado
            success: function(data) {
                console.log('Sucesso !');
                result = data;
            },
            beforeSend: function(xhr) {
                //$('#csrf_token').val() nao estava funcionando
                xhr.setRequestHeader("X-CSRFToken", $('input:hidden:first').val());
            }
        });
        return result;
    }

    $('#confirmar').click(function(e) {
        e.preventDefault();

        divs = $("[id*=div-sugestoes]");
        var mapaAssembleiaSugestoes = {};
        divs.each(function() {
            strongFromPanelHeading = $(this).closest(".panel-body").prev(".panel-heading").find("strong").text();
            num_assembleia = numAssembleiaFromPanelHeading(strongFromPanelHeading);
            if (num_assembleia.length > 0){
                alertsDesseDiv = $( this ).find(".alert");
                nums_sugestoes = [];
                alertsDesseDiv.each(function() {
                    nums_sugestoes.push(numSugestaoFromAlert($( this )));
                });
                mapaAssembleiaSugestoes[num_assembleia] = nums_sugestoes;
            }
        });

        if (mapaAssembleiaSugestoes){
            $.ajax({
                type: 'post',
                data: { mapa:JSON.stringify(mapaAssembleiaSugestoes)},
                url: '/atribuir-a-assembleia/',
                async: false, // para poder retornar o resultado
                success: function(data) {
                    console.log('Sucesso !');
                    $(location).attr('href', data)
                },
                beforeSend: function(xhr) {
                    //$('#csrf_token').val() nao estava funcionando
                    xhr.setRequestHeader("X-CSRFToken", $('input:hidden:first').val());
                }
            });
        }
    });

});