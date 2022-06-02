
    $("#novoendereco").click(function() {  <!-- NOVO ENDEREÇO -->
        var url = $("#alteraForm").attr("ajax-url");
        console.log("sucesso");
        $.ajax({
            url: url,
            data: {
                action: 'novo_endereco',
                id_entidade: {{ entidade.id }},
            },
            success: function (data) {   // `data` is the return of the `load_cities` view function
                $("#formendereco").html(data);  // replace the contents of the city input with the data that came from the server
            }
        });
    });

    var altera_ende = function(id){ <!-- ALTERA ENDEREÇO-->
       var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'altera_endereco',
                id_entidade_endereco: id,
                id_entidade: {{ entidade.id }},

            },
            success: function (data) {
                $("#formendereco").html(data);
            }
        });
    }

    var exclui_ende = function(id){ <!-- DELETA ENDEREÇO-->
       var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_endereco',
                id_entidade_endereco: id,
                id_entidade: {{ entidade.id }},

            },
             success: function (data) {
                var idtr = "#tr_ee"+id;
                $(idtr).remove();
                <!--                $("#altera_endereco").remove();-->


            }
        });
    }




     $("#novapessoa").click(function() {  <!-- NOVA PESSOA -->
        var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'nova_pessoa',
                id_entidade: {{ entidade.id }},
            },
            success: function (data) {
                $("#formpessoa").html(data);
            }
        });
    });

    var altera_pessoa = function(id){ <!-- ALTERA PESSOA-->
       var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'altera_pessoa',
                id_entidade_pessoa: id,
                id_entidade: {{ entidade.id }},

            },
            success: function (data) {
                $("#formpessoa").html(data);
            }
        });
    }

    var exclui_pessoa = function(id){ <!-- DELETA PESSOA -->
       var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_pessoa',
                id_entidade_pessoa: id,
                id_entidade: {{ entidade.id }},

            },
             success: function (data) {
                var idtr = "#tr_ep"+id;
                $(idtr).remove();
            }
        });
    }


    // $("#novoprocesso").click(function() {  <!-- NOVO PROCESSO -->
    //     var url = $("#alteraForm").attr("ajax-url");
    //     $.ajax({
    //         url: url,
    //         data: {
    //             action: 'novo_processo',
    //         },
    //         success: function (data) {   // `data` is the return of the `load_cities` view function
    //             $("#formprocesso").html(data);  // replace the contents of the city input with the data that came from the server
    //         }
    //     });
    // });

    var exclui_processo = function(id){ <!-- DELETA PROCESSO -->
       var url = $("#alteraForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_processo',
                id_sei: id,
                id_entidade: {{ entidade.id }},
            },
             success: function (data) {
                var idtr = "#tr_s"+id;
                $(idtr).remove();
            }
        });
    }
