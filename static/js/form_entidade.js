/**
 *   Cria lista de pessoas, endereços e processos que serão usados nas funções ####
 */


var list_sei_pendente = [];
var list_pessoas_pendente = [];
var list_enderecos_pendente = [];
var list_vinculacoes_pendente = [];


///**
// * Transformando tabela de processos em array de objetos
// *
// * Essa função é chamada na mudança de tabs.
// */
////https://www.github.developerdan.com/table-to-json/
//getListaProcessos = function(){
//  $('#table-listprocessos').delay( 500 )
//    .promise().done(function() {
//      listsei = $(this).tableToJSON({
//        ignoreColumns: [3]
//      });
//      console.log(listsei);
//    });
//};

/**
 *   NOVO PROCESSO
 *       - Verifica se existe o processo cadastrado na lista(listsei)
 *       - Inclui novo processo na lista de pendentes
 *       - Imprime dados do processo na área de visualização
 */
var cont_sei = 0;
$("#novoprocesso").click(function() {
    var existe = false;
    var nroprocesso = $("#id_nro_processo");

    $.each(list_sei_pendente, function(nro, processo) {
        if (processo.nro === nroprocesso.val()) {
            existe = true;
        }
    });
    if(!existe){
        $('#table-listprocessos tr').each(function() {
            var trprocesso = $(this).find(".sei_nroprocesso").html();
            if(nroprocesso.val() === trprocesso)
                existe = true;
        });
    }

    if (!existe) {
        var id_tipo_processo = $("#id_tipo_processo");
        var tipo_processo = $("#id_tipo_processo option:selected").text();
        var descricao = $("#id_descricao");


        if ($.trim(nroprocesso.val()).length === 0 || $.trim(id_tipo_processo.val()).length === 0 || $.trim(descricao.val()).length === 0) {
            alert("Todos campos deverão ser preenchidos!");
        } else {
            cont_sei++;
            pendente_id = 'processo_pendente_id'+cont_sei;

            var proc = {
                id: pendente_id,
                nro: nroprocesso.val().trim(),
                id_tipo_processo: id_tipo_processo.val(),
                descricao: descricao.val().trim(),
                tipo_processo: tipo_processo,
            };
            list_sei_pendente.push(proc);

            $("#table-addprocessos tbody").append(
                '<tr id="'+pendente_id+'">'+
                    '<td>' + proc.nro + '</td>'+
                    '<td>' + proc.tipo_processo +'</td>'+
                    '<td>' + proc.descricao + '</td>'+
                    '<td><button onclick="exclui_sei_pendente('+cont_sei+')" type="button">X</button></td>'+
                '</tr>');

            $(nroprocesso).val('');
            $(id_tipo_processo).prop('selectedIndex', 0);
            $(descricao).val('');

        }
    } else
        alert("Processo já cadastrado!");
});

/*
* Exclui processo sei pendente
*/
var exclui_sei_pendente = function(id){
    id = 'processo_pendente_id'+id;
    $("#"+id).remove();
    list_sei_pendente = list_sei_pendente.filter(x => x.id !== id);
}

/**
 *  Chama função create_post()
 **/
$('#entidadeForm').on('submit', function(event) {
    event.preventDefault();
    create_post();
});

/**
 *  Verifica se a lista de pessoas, processos e endereços estão preenchidos
 *  Envia todas as listas e os formulários(django) para o back-end e salva na base
 **/
function create_post() {
    var formData = $("#entidadeForm").serializeArray();
    var url = $("#entidadeForm").attr("submit-url");

    var form_data = new FormData();
    for (var key of formData.entries()) {
        form_data.append(key[1].name, key[1].value);
    }
//    if (list_sei_pendente.length == 0) {
//        alert("Adicione um processo");
//    } else {
        form_data.append("processos", JSON.stringify(list_sei_pendente));
        form_data.append("pessoas", JSON.stringify(list_pessoas_pendente));
        form_data.append("enderecos", JSON.stringify(list_enderecos_pendente));
        form_data.append("vinculacoes",JSON.stringify(list_vinculacoes_pendente));

        $.ajax({
            url: url,
            type: "POST",
            contentType: false,
            processData: false,
            data: form_data,

            success: function(data) {
                console.log("sucesso");
            },
            error: function(data) {
                console.log("erro");
            }
        });
//    }
};
//
///**
// *   Esconde e mostra tab de AGR
// **/
//$("#id_tipo_entidade").change(function() {
//    console.log("Oi");
//    var id_tipo_entidade = $("#id_tipo_entidade").val();
//    if (id_tipo_entidade == 0 || id_tipo_entidade == 1 || id_tipo_entidade == 2 || id_tipo_entidade == 7){
//        $("#agrs").css('display','none');
//        $("#tab_agrs").css('display','none');
////        $("#tab_agrs").attr('hidden',true);
//    }
//    else{
//        $("#tab_agrs").css('display','block');
//        $("#agrs").css('display','block');
//    }
//});


/**
 *  Traz os dados do processo a partir da número do processo
 **/
$("#id_nro_processo").change(function() {
    var nroprocesso = $(this).val();
    var url = $("#entidadeForm").attr("ajax-url");

    $.ajax({
        url: url,
        data: {
            'processo': nroprocesso,
            action: 'get_processo',
        },
        dataType: 'json',
        success: function(response) {
            //console.log(response);

            $("#id_descricao").val(response.descricao_processo);
            select_default("id_tipo_processo");
            $("#id_tipo_processo option[value=" + response.id_tipo_processo + "]").attr('selected', 'selected');


        }
    });
});

/**
 *  Pega o cpf e traz os dados daquela pessoa caso exista na base
 **/
$("#id_cpf").change(function() {
    var cpfpessoa = $(this).val();
    var url = $("#entidadeForm").attr("ajax-url");

    $.ajax({
        url: url,
        data: {
            'cpfpessoa': cpfpessoa,
            action: 'get_pessoa',
        },
        dataType: 'json',
        success: function(response) {
            $("#id_nome_pessoa").val(response.nome_pessoa);
        }
    });
});

/**
 *  Pega o id do estado no momento que é selecionado e chama a função get_municipios
 **/
$("#id_estado_ibge").change(function() {
    var estadoId = $(this).val(); // get the selected country ID from the HTML input
    get_municipios(estadoId, function(){

    });

});
/*
* Pega os munícípios a partir do id do estado
*/
function get_municipios(estado_ibge_id, callback){
    var url = $("#entidadeForm").attr("ajax-url");
    $.ajax({
        url: url,
        data: {
            'estado_ibge': estado_ibge_id,
             action: 'load_mun'
         },
         success: function(data) {
            $("#id_municipio_ibge").html(data);
            console.log("get_mun");
            callback();
            console.log("get_mun2");
         }
    });
}
/**
 *  Pega cep digitado e traz as informações do endereço(viacep.com.br/)
 **/
$("#id_cep").change(function() {
    var cep = $(this).val();
    var url = $("#entidadeForm").attr("ajax-url");

    $.ajax({
        url: url,
        data: {
            'cep': cep,
            action: 'get_endereco',
        },
        dataType: 'json',
        success: function(response) {
            $("#id_logradouro").val(response.logradouro);
            $("#id_complemento").val(response.complemento);
            $("#id_bairro").val(response.bairro);
            select_default("id_estado_ibge");
            select_default("id_municipio_ibge");
            $("#id_estado_ibge option[value=" + response.ibge[0] + response.ibge[1] + "]").attr('selected', 'selected');
            $("#id_estado_ibge option[value=" + response.ibge[0] + response.ibge[1] + "]").prop('selected', 'selected');
            get_municipios(response.ibge[0] + response.ibge[1], function(){
                $("#id_municipio_ibge option[value=" + response.ibge + "]").attr('selected', 'selected');
            });
        },
        error: function(response) {
            console.log("erro");
            console.log(response);
        }
    });
});

/*
* Adiciona endereço na tabela endereço pendente
*/
var cont_endereco = 0;
$("#novoendereco").click(function(){
    var cep = $("#id_cep").val();
    var id_mun = $("#id_municipio_ibge").val();
    var municipio = $("#id_municipio_ibge option:selected").text();
    var uf = $("#id_estado_ibge option:selected").text();
    var logradouro = $("#id_logradouro").val();
    var bairro = $("#id_bairro").val();
    var numero = $("#id_numero").val();
    var complemento = $("#id_complemento").val();
    var latitude = $("#id_latitude").val();
    var longitude = $("#id_longitude").val();
    var tipo_endereco = $("#id_tipo_endereco").val();


    cont_endereco+=1;
    var pendenteid = 'endereco_pendente'+cont_endereco;
    var endereco = {
        id: pendenteid,
        cep: cep,
        id_mun: id_mun,
        municipio: municipio,
        uf: uf,
        logradouro: logradouro,
        bairro:bairro,
        numero: numero,
        complemento: complemento,
        latitude: latitude,
        longitude: longitude,
        tipo_endereco: tipo_endereco,
    };

    list_enderecos_pendente.push(endereco);

    $("#table-addenderecos tbody").append(
        '<tr id="'+pendenteid+'">'+
            '<td>' + endereco.cep + '</td>'+
            '<td>' + endereco.logradouro + '</td>'+
            '<td>' + endereco.bairro + '</td>'+
            '<td>' + endereco.numero + '</td>'+
            '<td>' + endereco.complemento + '</td>'+
            '<td>' + endereco.latitude + '</td>'+
            '<td>' + endereco.longitude + '</td>'+
            '<td>' + endereco.municipio + '</td>'+
            '<td>' + endereco.uf + '</td>'+
            '<td>' + endereco.tipo_endereco + '</td>'+
            '<td><button onclick="exclui_ende_pendente('+cont_endereco+')" type="button">X</button></td>'+
        '</tr>');

    limpa_endereco();
});

/*
* Exclui endereço pendente
*/
var exclui_ende_pendente = function(id){
    var pendente_id = 'endereco_pendente'+id;
    $("#"+pendente_id).remove();

    list_enderecos_pendente = list_enderecos_pendente.filter(x => x.id !== pendente_id)
}

/*
* Adiciona pessoa na tabela pessoa pendente
*/
var cont_pessoa = 0;
$("#novapessoa").click(function(){
    var cpf = $("#id_cpf").val();
    var nome = $("#id_nome_pessoa").val();
    var id_tipo_pessoa = $("#id_tipo_pessoa").val();
    var tipo_pessoa = $("#id_tipo_pessoa option:selected").text();
    var telefone = $("#id_telefone_pessoa").val();
    var email = $("#id_email_pessoa").val();

    var existe = false;

    $.each(list_pessoas_pendente, function(cpf1, pessoa) {
        if (pessoa.cpf === cpf && pessoa.id_tipo_pessoa === id_tipo_pessoa)  {
            existe = true;
        }
    });

    if(!existe){
        $('#table-listpessoas tr').each(function() {
            var tr_cpf = $(this).find(".pessoa-cpf").html();
            var tr_idtipopessoa = $(this).find(".pessoa-tipo_pessoa").prop('id');

            if(cpf === tr_cpf && tr_idtipopessoa === id_tipo_pessoa)
                existe = true;
        });
    }

    if (existe) {
        alert("Pessoa já cadastrada!");
    }else{
        cont_pessoa++;
        var pendenteid = 'pessoa_pendente'+cont_pessoa;
        var pessoa = {
            id: pendenteid,
            cpf: cpf,
            nome: nome,
            id_tipo_pessoa: id_tipo_pessoa,
            tipo_pessoa: tipo_pessoa,
            telefone: telefone,
            email: email,
        };

        list_pessoas_pendente.push(pessoa);

         $("#table-addpessoas tbody").append(
            '<tr id="'+pendenteid+'">'+
                '<td>' + pessoa.tipo_pessoa + '</td>'+
                '<td>' + pessoa.nome + '</td>'+
                '<td>' + pessoa.cpf + '</td>'+
                '<td>' + pessoa.telefone + '</td>'+
                '<td>' + pessoa.email + '</td>'+
                '<td><button onclick="exclui_pessoa_pendente('+cont_pessoa+')" type="button">X</button></td>'+
            '</tr>');
         limpa_pessoa();
        }

});

/*
* Exclui pessoa pendente
*/
var exclui_pessoa_pendente = function(id){
    var pendente_id = 'pessoa_pendente'+id;
    $("#"+pendente_id).remove();
    list_pessoas_pendente = list_pessoas_pendente.filter(x => x.id !== pendente_id);
}

/*
* Formata campo select para pesquisa (remover o script e link da entidade.html)
* https://harvesthq.github.io/chosen/
*/
$("#id_entidade_propria").chosen({
    inherit_select_classes: false,
    no_results_text: "Entidade não encontrada!",
    width: "100%",
});

/*
* Preenche os inputs do endereço para ser alterado
*/
preenche_campos_endereco = function(id){
    if(!$("#novoendereco").hasClass("d-none"))
        $("#novoendereco").addClass("d-none");

    if($("#alteraendereco").hasClass("d-none"))
        $("#alteraendereco").removeClass("d-none");

    var endereco = "#tr_ee"+id;

    $("#id_cep").val($(endereco+" .ende-cep").text());
    $("#id_logradouro").val($(endereco+" .ende-logradouro").text());
    $("#id_bairro").val($(endereco+" .ende-bairro").text());
    $("#id_numero").val($(endereco+" .ende-numero").text());
    $("#id_complemento").val($(endereco+" .ende-complemento").text());
    $("#id_latitude").val($(endereco+" .ende-latitude").text());
    $("#id_longitude").val($(endereco+" .ende-longitude").text());
    $("#id_tipo_endereco").val($(endereco+" .ende-tipo_endereco").text());
    $("#id_entidade_endereco").val(id);

    var id_estado_ibge = $(endereco+" .ende-estado_ibge").prop('id');
    var id_mun_ibge = $(endereco+" .ende-mun_ibge").prop('id');

    select_default("id_estado_ibge");
    select_default("id_municipio_ibge");
    $("#id_estado_ibge #"+id_estado_ibge).attr('selected', 'selected');
    $("#id_estado_ibge #"+id_estado_ibge).prop('selected', 'selected');

    get_municipios(id_estado_ibge, function(){
        $("#id_municipio_ibge option[value=" + id_mun_ibge + "]").attr('selected', 'selected');
    });

    console.log(id_mun_ibge);



}

/*
* Troca os botões da aba endereço
*/
$("#buttoncancelarendereco").click(function(){
    if($("#novoendereco").hasClass("d-none"))
        $("#novoendereco").removeClass("d-none");

    if(!$("#alteraendereco").hasClass("d-none"))
        $("#alteraendereco").addClass("d-none");

    limpa_endereco();


});

/*
* Limpa os campos do endereço
*/
function limpa_endereco(){
    $("#id_cep").val("");
    select_default("id_estado_ibge");
    select_default("id_municipio_ibge");
    $("#id_logradouro").val("");
    $("#id_bairro").val("");
    $("#id_numero").val("");
    $("#id_complemento").val("");
    $("#id_latitude").val("");
    $("#id_longitude").val("");
    $("#id_tipo_endereco").val("");
    $("#id_entidade_endereco").val("");
};

/*
* Remove todas seleções do select
*/
function select_default(id){
    $("#"+id+" option").removeAttr('selected');
    $("#"+id+" option").removeProp('selected');
    $("#"+id).prop('selectedIndex', 0);
};

/*
* Altera os dados do endereço
*/
$("#alteraendereco").click(function(){
    var id_entidade_endereco = $("#id_entidade_endereco").val();
    var url = $("#entidadeForm").attr("ajax-url");
    var cep = $("#id_cep").val();
    var id_mun = $("#id_municipio_ibge").val();
    var municipio = $("#id_municipio_ibge option:selected").text();
    var uf = $("#id_estado_ibge option:selected").text();
    var logradouro = $("#id_logradouro").val();
    var bairro = $("#id_bairro").val();
    var numero = $("#id_numero").val();
    var complemento = $("#id_complemento").val();
    var latitude = $("#id_latitude").val();
    var longitude = $("#id_longitude").val();
    var tipo_endereco = $("#id_tipo_endereco").val();


    $.ajax({
        url: url,
        data: {
            action: 'altera_endereco',
            id_entidade_endereco: id_entidade_endereco,
            cep: cep,
            municipio: id_mun,
            logradouro: logradouro,
            bairro: bairro,
            numero: numero,
            complemento: complemento,
            latitude: latitude,
            longitude: longitude,
            tipo_endereco: tipo_endereco,
         },
         success: function (data) {
            $("#tr_ee"+id_entidade_endereco+" .ende-cep").html(cep);
            $("#tr_ee"+id_entidade_endereco+" .ende-logradouro").html(logradouro);
            $("#tr_ee"+id_entidade_endereco+" .ende-bairro").html(bairro);
            $("#tr_ee"+id_entidade_endereco+" .ende-complemento").html(complemento);
            $("#tr_ee"+id_entidade_endereco+" .ende-latitude").html(latitude);
            $("#tr_ee"+id_entidade_endereco+" .ende-longitude").html(longitude);
            $("#tr_ee"+id_entidade_endereco+" .ende-tipo_enderecop").html(tipo_endereco);
            $("#tr_ee"+id_entidade_endereco+" .ende-numero").html(numero);
            $("#tr_ee"+id_entidade_endereco+" .ende-estado_ibge").html(uf);
            $("#tr_ee"+id_entidade_endereco+" .ende-mun_ibge").html(municipio);
            $("#tr_ee"+id_entidade_endereco+" .ende-mun_ibge").prop('id',id_mun);
            $("#tr_ee"+id_entidade_endereco+" .ende-estado_ibge").prop('id',id_mun[0]+id_mun[1]);
            $("#buttoncancelarendereco").trigger('click')
         }

    });

});
/*
*Exclui endereço direto na base (muda dt extinção)
*/
var exclui_ende = function(id) {
    var url = $("#entidadeForm").attr("ajax-url");
    $.ajax({
        url: url,
        data: {
            action: 'exclui_endereco',
            id_entidade_endereco: id,
        },
        success: function(data) {
            var idtr = "#tr_ee" + id;
            $(idtr).remove();
        }
    });
}

/*
*Exclui sei direto na base (vinculação)
*/
var exclui_processo = function(idsei, identidade){
    var url = $("#entidadeForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_processo',
                id_sei: idsei,
                id_entidade: identidade,
            },
             success: function (data) {
                var idtr = "#tr_s"+idsei;
                $(idtr).remove();
            }
        });
}
/*
*Exclui pessoa direto na base (muda dt extinção)
*/
var exclui_pessoa = function(id){
       var url = $("#entidadeForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_pessoa',
                id_entidade_pessoa: id,

            },
             success: function (data) {
                var idtr = "#tr_ep"+id;
                $(idtr).remove();
            }
        });
    }

/*
* Troca os botões da aba pessoa
*/
$("#buttoncancelarpessoa").click(function(){
    if($("#novapessoa").hasClass("d-none"))
        $("#novapessoa").removeClass("d-none");

    if(!$("#alterapessoa").hasClass("d-none"))
        $("#alterapessoa").addClass("d-none");

    limpa_pessoa();



});
/*
* Preenche os inputs da pessoa para ser alterado
*/
preenche_campos_pessoa = function(id){
    if(!$("#novapessoa").hasClass("d-none"))
        $("#novapessoa").addClass("d-none");

    if($("#alterapessoa").hasClass("d-none"))
        $("#alterapessoa").removeClass("d-none");

    var pessoa = "#tr_ep"+id;

    $("#id_cpf").val($(pessoa+" .pessoa-cpf").text());
    $("#id_telefone_pessoa").val($(pessoa+" .pessoa-telefone").text());
    $("#id_email_pessoa").val($(pessoa+" .pessoa-email").text());
    $("#id_nome_pessoa").val($(pessoa+" .pessoa-nome").text());
    $("#id_entidade_pessoa").val(id);

    var id_tipo_pessoa = $(pessoa+" .pessoa-tipo_pessoa").prop('id');


    select_default("id_tipo_pessoa");
    $("#id_tipo_pessoa #"+id_tipo_pessoa).attr('selected', 'selected');
    $("#id_tipo_pessoa #"+id_tipo_pessoa).prop('selected', 'selected');
}
/*
* Altera os dados da pessoa
*/
$("#alterapessoa").click(function(){
    var url = $("#entidadeForm").attr("ajax-url");
    var cpf = $("#id_cpf").val();
    var nome = $("#id_nome_pessoa").val();
    var telefone = $("#id_telefone_pessoa").val();
    var email = $("#id_email_pessoa").val();
    var tipo_pessoa = $("#id_tipo_pessoa option:selected").text();
    var id_tipo_pessoa = $("#id_tipo_pessoa").val();
    var id_entidade_pessoa = $("#id_entidade_pessoa").val();


    $.ajax({
        url: url,
        data: {
            action: 'altera_pessoa',
            id_entidade_pessoa: id_entidade_pessoa,
            cpf: cpf,
            nome: nome,
            telefone: telefone,
            email: email,
            id_tipo_pessoa: id_tipo_pessoa,
         },
         success: function (data) {
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-cpf").html(cpf);
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-nome").html(nome);
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-telefone").html(telefone);
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-email").html(email);
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-tipo_pessoa").html(tipo_pessoa);
            $("#tr_ep"+id_entidade_pessoa+" .pessoa-tipo_pessoa").prop('id',id_tipo_pessoa);
            $("#buttoncancelarpessoa").trigger('click');

         }

    });

});

/*
*Limpa os campos do formulário da pessoa
*/
limpa_pessoa = function(){
    $("#id_cpf").val("");
    select_default("id_tipo_pessoa");
    $("#id_nome_pessoa").val("");
    $("#id_telefone_pessoa").val("");
    $("#id_email_pessoa").val("");
}
/*
* Troca os botões da aba vinculação
*/
$("#buttoncancelarvinculacao").click(function(){
    if($("#novavinculacao").hasClass("d-none"))
        $("#novavinculacao").removeClass("d-none");

    if(!$("#alteravinculacao").hasClass("d-none"))
        $("#alteravinculacao").addClass("d-none");

    limpa_vinculacao();
});
/*
*Limpa os campos do formulário das vinculações
*/
limpa_vinculacao = function(){
    $("#id_dt_vinculacao").val("");
    select_default("id_situacoes");
    select_default("id_entidades_pai");
    $("#id_entidades_pai").removeAttr('disabled');
}
/**
 *Adiciona vinculação na tabela vinculação pendente
 */
var cont_vinculacao = 0;
$("#novavinculacao").click(function() {
    var existe = false;
    var id_entidade = $("#id_entidades_pai option:selected").attr("id");

    $.each(list_vinculacoes_pendente, function(vin, entidade) {
        if (entidade.id === id_entidade) {
            existe = true;
        }
    });

    if(!existe){
        $('#table-listvinculacoes tr').each(function() {
            var tr_identidade = $(this).find(".entidadevin_nome").prop('id');
            if(id_entidade === tr_identidade)
                existe = true;
        });
    }

    if (!existe) {
        var cnpj = $("#id_entidades_pai option:selected").val();
        var entidade_nome = $("#id_entidades_pai option:selected").text();
        var id_situacao = $("#id_situacoes").val();
        var situacao = $("#id_situacoes option:selected").text();
        var dt_vinculacao = $("#id_dt_vinculacao").val();



            cont_vinculacao++;

            var vincul = {
                id: id_entidade,
                cnpj: cnpj,
                entidade_nome: entidade_nome,
                situacao: situacao,
                id_situacao: id_situacao,
                dt_vinculacao: dt_vinculacao,
            };
            list_vinculacoes_pendente.push(vincul);

            $("#table-addvinculacao tbody").append(
                '<tr id="'+id_entidade+'">'+
                    '<td>' + entidade_nome + '</td>'+
                    '<td>' + cnpj +'</td>'+
                    '<td>' + dt_vinculacao + '</td>'+
                    '<td>' + situacao + '</td>'+
                    '<td><button onclick="exclui_vinculacao_pendente('+id_entidade+')" type="button">X</button></td>'+
                '</tr>');

            limpa_vinculacao();


    } else
        alert("Entidade já cadastrada!");
});
/*
* Exclui vinculação pendente
*/
var exclui_vinculacao_pendente = function(id){
    $("#table-addvinculacao #"+id).remove();
    list_vinculacoes_pendente = list_vinculacoes_pendente.filter(x => x.id !== ""+id);
}

/*
* Altera os dados da vinculação
*/
$("#alteravinculacao").click(function(){
    var url = $("#entidadeForm").attr("ajax-url");

    var id_entidade_vinculada = $("#id_entidade_vinculada").val();
    var entidade_pai = $("#id_entidades_pai option:selected").text();
    var id_entidade_pai = $("#id_entidades_pai option:selected").prop('id');
    var situacao = $("#id_situacoes option:selected").text();
    var id_situacao = $("#id_situacoes").val();
    var dt_vinculacao = $("#id_dt_vinculacao").val();

    $.ajax({
        url: url,
        data: {
            action: 'altera_vinculacao',
            id_entidade_vinculada: id_entidade_vinculada,
            id_entidade_pai: id_entidade_pai,
            id_situacao: id_situacao,
            dt_vinculacao: dt_vinculacao,
         },
         success: function (data) {

            $("#tr_ev"+id_entidade_vinculada+" .entidadevin_dt_vinculacao").html(dt_vinculacao);
            $("#tr_ev"+id_entidade_vinculada+" .situacao").html(situacao);
            $("#tr_ev"+id_entidade_vinculada+" .situacao").prop('id',id_situacao);
            $("#buttoncancelarvinculacao").trigger('click')
         }

    });

});
/*
* Preenche os inputs da pessoa para ser alterado
*/
preenche_campos_vinculacao = function(id){
        if(!$("#novavinculacao").hasClass("d-none"))
            $("#novavinculacao").addClass("d-none");

        if($("#alteravinculacao").hasClass("d-none"))
            $("#alteravinculacao").removeClass("d-none");

        var id_tr_entidade = "#tr_ev"+id;
        var id_entidade = $(id_tr_entidade+" .entidadevin_nome").prop('id');
        var id_situacao = $(id_tr_entidade+" .situacao").prop('id');
        var dt_vinculacao = $(id_tr_entidade+" .entidadevin_dt_vinculacao").text();

        select_default("id_situacoes");
        select_default("id_entidades_pai");

        $("#id_entidades_pai #"+id_entidade).attr('selected', 'selected');
        $("#id_entidades_pai #"+id_entidade).prop('selected', 'selected');
        $("#id_situacoes #"+id_situacao).attr('selected', 'selected');
        $("#id_situacoes #"+id_situacao).prop('selected', 'selected');
        $("#id_dt_vinculacao").val(dt_vinculacao);
        $("#id_entidade_vinculada").val(id);

        $("#id_entidades_pai").prop('disabled', 'disabled');
}
/*
*Exclui vinculação direto na base (muda dt extinção)
*/
var excluivinculacao = function(id){
    var url = $("#entidadeForm").attr("ajax-url");
        $.ajax({
            url: url,
            data: {
                action: 'exclui_vinculacao',
                id_entidade_vinculada: id,
            },
             success: function (data) {
                var idtr = "#tr_ev"+id;
                $(idtr).remove();
            }
        });
    }
/*
* Limpa os campos da aba processos
*/
$("#buttoncancelarprocessos").click(function(){
    $('#id_nro_processo').val('');
    $('#id_descricao').val('');
    select_default('id_tipo_processo');
});
