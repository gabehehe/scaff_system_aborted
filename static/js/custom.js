/**
 * Pesquisa global na tabela
 */
function filterGlobal() {
  $('#datatable-entity').DataTable().search(
    $('#dataTable-search').val()
  ).draw();
}

/**
 * Muda situação da tab de acordo com a validação
 */



$(document).ready(function() {

  // Mostrar/alterar passo ativo no momento quando clicado no círculo
  $('#form-cadastro-steps .nav-item').on('click', function(e) {
    e.preventDefault();
    $(this).tab('show');
    $('#form-cadastro-steps .nav-item').removeClass('active');
    $(this).addClass('active');
//    getListaProcessos();
  });


  // Mostrar/alterar passo ativo no momento quando clicado no botão Avançar
  $('#form-cadastro-content .tab-next').on('click', function(e) {
    e.preventDefault();

    if ($('#form-cadastro-content .is-invalid')) {
      $('#form-cadastro-content .tab-pane.active.show').removeClass('active show').next().addClass('active show');
      $('#form-cadastro-steps .nav-item.active').removeClass('active').addClass('danger').next().addClass('active');
    } else {
      $('#form-cadastro-content .tab-pane.active.show').removeClass('active show').next().addClass('active show');
      $('#form-cadastro-steps .nav-item.active').removeClass('active').next().addClass('active');
    }
    // TODO: Verificar se essa chamada está funcionando
//    getListaProcessos();
  });

  // Mostrar/alterar passo ativo no momento quando clicado no botão Voltar
  $('#form-cadastro-content .tab-prev').on('click', function(e) {
    e.preventDefault();
    $('#form-cadastro-content .tab-pane.active.show').removeClass('active show').prev().addClass('active show');
    $('#form-cadastro-steps .nav-item.active').removeClass('active').prev().addClass('active');
  });

  // $('.form-table').DataTable({
  //   "dom": 'rt<"bottom"ip><"clear">',
  //   "pageLength": 10
  // });

  $('#datatable-entity').DataTable({
    "dom": 'rt<"bottom"ipl><"clear">',
    "pageLength": 20,
    "order": [[ 5, "desc" ]]
  });

  /**
   #table-vinc-pai
   #table-vinc-filhos
   #table-pessoas
   #table-processos
   */
   var tables = ['#table-vinc-pai', '#table-vinc-filhos', '#table-pessoas', '#table-processos'];
   var tb_vinc_pai = $('#table-vinc-pai tr').length;
   var tb_vinc_filhos = $('#table-vinc-filhos tr').length;
   var tb_pessoas = $('#table-pessoas tr').length;
   var tb_processos = $('#table-processos tr').length;
   // console.log(vinc_pai);
   for (var tb of tables) {
     var key = tb + ' tr';
     var value = $(key).length;
     // console.log(key, value);
     //
     if (value > 10) {
       // console.log("No IF: ", key);
       $(tb).DataTable({
         "dom": 'rt<"bottom"ip><"clear">',
         "pageLength": 10
       });
       if (tb == '#table-vinc-pai' || tb == '#table-vinc-filhos') {
         console.log('mudando o datatables');
        //  $(tb).DataTable({
        //    "columns": [
        //   null,
        //   null,
        //   null,
        //   null,
        //   { "width": "20%" }
        // ]
        //  });
       }
     }
     else{
       // console.log("Fora do IF: ", key);
     }
   }


  // $('.table-default-format').DataTable({
  //   "dom": 'rt<"bottom"ipl><"clear">',
  //   "pageLength": 10
  // });

  // $('.table-default-format')

  $('input#dataTable-search').on('keyup click', function() {
    filterGlobal();
  });

  // Adicionando Mascaras
  $('.mask-cnpj').mask('00.000.000/0000-00', {
    reverse: true
  });
  $('.mask-cpf').mask('000.000.000-00', {
    reverse: true
  });
  $('.mask-sei').mask('00000.000000/0000-00', {
    reverse: true
  });
  $('.mask-cep').mask('00.000-000', {
    reverse: true
  });



  $('.user-picture').each(function(){
    var symbols, color;
    symbols = '0123456789ABCDEF';
    color = '#';
    for (var i = 0; i < 6; i++) {
      color += symbols[Math.floor(Math.random() * 16)];
    }
    $(this).css("background-color", color);
  });

});


/**
 * Validação dos dados do formulário
 */
var formCadastro = {
  "entidade": {
    "id_tipo_entidade": null,
    "id_nome_entidade": null,
    "id_razao_social": null,
    "id_cnpj_entidade": null,
    "id_telefone_entidade": null,
    "id_email_entidade": null,
    "id_dt_credenciamento": null
  },
  "enderecos": {
    "id_municipio_ibge": null,
    "id_cep": null,
    "id_logradouro": null,
    "id_bairro": null,
    "id_numero": null,
    "id_complemento": null,
    "id_latitude": null,
    "id_longitude": null
  }
};

bootstrapValidate('#id_cnpj_entidade', 'numeric:Apenas números são permitidos', function(isValid) {
  if (isValid) {
    formCadastro.entidade.id_cnpj_entidade = true;
  } else {
    formCadastro.entidade.id_cnpj_entidade = false;
  }
});

bootstrapValidate(['#id_tipo_entidade', '#id_nome_entidade', '#id_razao_social'], 'required:Esses campos são obrigatórios', function(isValid) {
  if (isValid) {
    console.log("true");
  } else {
    console.log("false");
  }
});
