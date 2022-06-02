var url = $("#analise-ocorrencia").attr("ajax-url");

var oco_labels = {
	"oco_num": "Núremo da ocorrência",
	"responsavel_registro": "Responsável pelo registro",
	"cpf_responsavel_registro": "CPF do responsável pelo registro",
	"data_cadastro": "Data cadastro",
	"data_oco": "Data ocorrência",
	"tipo_certificado": "Tipo do certificado",
	"tipo_ocorrencia": "Tipo da ocorrência",
	"serial_number": "Serial Number",
	"descricao_oco": "Descrição da ocorrência",
	"justificativa_marcador": "Justificativa do marcador",
	"codinome": "Codinome",
	"autoridade_certificadora": "Autoridade Certificadora",
	"autoridade_registro": "Autoridade de Registro",
	"usuario": "Usuário",
	"marcador": "Marcador",
	"marcador_atribuido": "Marcador Atribuído por",
	"nome": "Nome",
	"cpf": "CPF",
	"email": "Email",
	"telefone": "Telefone",
	"representa_pj": "Representa PJ",
	"municipio": "Município",
	"uf": "UF",
	"caracteristicas": "Caracteristicas",
	"formas_deteccao": "Formas de detecção",
	"outras": {
	    "tipo": "Tipo",
	    "observado": "Observado",
	    "pyt": "Formas de detecção de fraude",
	    "resultado": "Resultado"
	},
}

$("#pesquisa-ocorrencia").click(function () {
	var oco_num = $("#oco_num").val()
    $('#ocorrencia_dados_form').addClass('d-none')
    $('#ocorrencia_dados').addClass('d-none')
    $('#checks').addClass('d-none')

    destroyTableCertificates('#table-certificates')
    destroyTableCertificates('#table-certificates-email')

    if(searchOcoScaff(oco_num) === false){
        searchOcoApi(oco_num)
    }

});
function searchOcoScaff(oco_num){
    var sucesso;
    $.ajax({
		url: url,
		data: {
			action: 'get_ocorrencia_scaff',
			oco_num: oco_num,
		},
		success: function (data) {
		    buildSearchResult(data);
		    sucesso = true;
		},
		error: function (data) {
			cleanOco()
			sucesso = false;
		}

	});
	return false;
}

function searchOcoApi(oco_num){
    $.ajax({
		url: url,
		data: {
			action: 'get_ocorrencia_saf',
			oco_num: oco_num,
		},
		success: function (data) {
		    buildSearchResult(data);
		},
		error: function (data) {
			cleanOco()
		}

	});
};

function buildSearchResult(data) {
    if (data.length == 0) {
        cleanOco();
        buildTableForm({})
        if ($('#ocorrencia_dados_form').hasClass('d-none')) {
            $('#ocorrencia_dados_form').removeClass('d-none')
            $('#ocorrencia_dados').addClass('d-none')
        }
        $('#certificados-email').addClass('d-none')
        $('#edita-ocorrencia').addClass('d-none')
    } else {
        $('#ocorrencia_dados').empty();
        data = data[0];
        populateOccurrence(data, '#ocorrencia_dados')

        search_certificate_cpf(data['cpf']);
        search_size_certificates_email(data['email']);
        $("#edita-ocorrencia").removeClass('d-none');
        $("#salva-edicao").addClass('d-none');

        if ($('#ocorrencia_dados').hasClass('d-none')) {
            $('#ocorrencia_dados').removeClass('d-none')
            $('#ocorrencia_dados_form').addClass('d-none')
        }
        $('#certificados-email').removeClass('d-none')
        $('#checks').removeClass('d-none')

    }
};


$("#edita-ocorrencia").click(function () {
	var oco_data = {};
	var obj = {};
	$('#ocorrencia_dados table tr td').each(function () {
		var key = $(this).attr('id');
		var value = $(this).text();
		eval('obj = { ' + key + ' : value}');

		Object.assign(oco_data, obj);
	});
	buildTableForm(oco_data)

	$("#ocorrencia_dados_form").removeClass('d-none');
	$("#ocorrencia_dados").addClass('d-none');
	$("#salva-edicao").removeClass('d-none');
	$("#edita-ocorrencia").addClass('d-none');
});

$("#salva-edicao").click(function(){
    var oco_data = {};
	var obj = {};

	$('#ocorrencia_dados').empty();

	$('#ocorrencia_dados_form div').each(function () {
        var key = $(this).find('input').attr('id');
		var value = $(this).find('input').val();

		key = key.replace("form_", "");

		eval('obj = { ' + key + ': value}');

		Object.assign(oco_data, obj);
	});

    populateOccurrence(oco_data, '#ocorrencia_dados');

    $("#ocorrencia_dados").removeClass('d-none');
    $("#ocorrencia_dados_form").addClass('d-none');
    $("#salva-edicao").addClass('d-none');
    $("#edita-ocorrencia").removeClass('d-none');

    search_certificate_cpf(oco_data['cpf']);
	search_size_certificates_email(oco_data['email']);

});


function search_certificate_cpf(cpf) {
	$.ajax({
		url: url,
		data: {
			action: 'get_certificates_cpf',
			cpf: cpf,
		},
		success: function (data) {
		    var quantidade = data.length == null ? 0 : data.length
		    if(quantidade === 0)
		        destroyTableCertificates('#table-certificates')
			else
			    createTable(data, '#table-certificates');
		},
		error: function (data) {
			destroyTableCertificates('#table-certificates')
		}
	});

};

function search_size_certificates_email(email) {

	$.ajax({
		url: url,
		data: {
			action: 'get_certificates_email',
			email: email,
		},
		success: function (data) {
		    var quantidade =  (data.length == null ? '0' : data.length)
			$('#qtd-certificados-email').empty().append("Quantidade de certificados encontrados pelo e-mail: "+quantidade)
			if(quantidade == 0)
			    $('#list-certificates-email').addClass('d-none')
			else
			    $('#list-certificates-email').removeClass('d-none')
		},
		error: function (data) {
		}
	});

};

function search_certificates_email() {
	var email = $('#email').text()
	$.ajax({
		url: url,
		data: {
			action: 'get_certificates_email',
			email: email,
		},
		success: function (data) {
			tableId = '#table-certificates-email'
			createTable(data, tableId);
		},
		error: function (data) {
			$(tableId).DataTable().destroy()
			$(tableId).addClass('d-none')
			$(tableId + '_wrapper').addClass('d-none')
		}
	});

};

function displayInput(input) {
	var inputId = '#' + input.id
	if ($(inputId).hasClass('d-none'))
		$(inputId).removeClass('d-none')
	else {
		$(inputId).addClass('d-none')
		$(inputId).val('')
	}
};

function cleanOco() {
	$('#ocorrencia_dados input').val('')
};

function createTable(json, tableId) {
	if ($(tableId).hasClass('dataTable')) {
		$(tableId).DataTable().destroy()
	}
	if ($(tableId).hasClass('d-none')) {
		$(tableId).removeClass('d-none')
		$(tableId + '_wrapper').removeClass('d-none')
	}
	$(tableId).DataTable({
		"data": json,
		"columns": [{
				"data": "serial_number"
			},
			{
				"data": "cpf"
			},
			{
				"data": "responsavel"
			},
			{
				"data": "email"
			},
			{
				"data": "cnpj"
			},
			{
				"data": "razao_social"
			},
			{
				"data": "not_before"
			},
			{
				"data": "not_after"
			},
		],
		"dom": 'tp',
		"pageLength": 10

	});
}

function populateOccurrence(data, tableId){
    var content = '';
    for (var prop in oco_labels) {
        if( prop != 'outras' ){

		content += '<tr><th>' + oco_labels[prop] + '</th><td id=' + prop + '>';
		if (Array.isArray(data[prop])){
		    var inner_table = '<table class="table">';
		    var inner_content = '<tbody>';
		    var inner_thead = '<thead class="thead-light">';
		    var inner_thead_data = [];
		    for (var p in data[prop]){
		        inner_content += '<tr>'
		        for(var p2 in data[prop][p]){
                    if (inner_thead_data.indexOf(p2) == -1) {
                        inner_thead_data.push(p2);
                    }
		            inner_content += '<td id=' + p2+p + '>'+data[prop][p][p2]+'</td>'
		        }
		        inner_content += '</tr>'
		    }
		    for(var p in inner_thead_data){
		        inner_thead += "<th>"+ inner_thead_data[p] + "</th>";
		    }
		    inner_thead += '</thead>';
		    inner_table += inner_thead;
		    inner_content += '</tbody></table>';
		    inner_table += inner_content;
		    content += inner_table;
//		    console.log(inner_table + inner_content + '</table>');

		}else
		    content +=  data[prop];
		content += '</td></tr>';

        }
    }

    $('<table/>', {
		'class': 'table bg-white',
		'html': content
	}).appendTo(tableId);

	if ($('#table-certificates').hasClass('dataTable')) {
		$('#table-certificates').DataTable().destroy()
		$('#table-certificates').addClass('d-none')
		$('#table-certificates_wrapper').addClass('d-none')
	}
}

function buildTableForm(data){
    var content = '';
    for (var prop in oco_labels)
        content += '<div class="form-group"><label>' + oco_labels[prop] + '</label><input class="form-control" id="form_'
            + prop +'" type="text" value = "' + (data[prop] == null ? '' : data[prop]) + '"/></div>'

    $("#ocorrencia_dados_form").html(content);

}

function destroyTableCertificates(tableId){
    $(tableId).DataTable().destroy()
	$(tableId).addClass('d-none')
	$(tableId+'_wrapper').addClass('d-none')
}


function getValues(){
    var oco_data = {};
	var obj = {};
	$('#ocorrencia_dados > table > tr > td').each(function () {
	    var element = $(this).html();
	    if(element.startsWith('<table')){
	        var inner_table = [];
	        $('tbody tr', this).each(function () {
	            var inner_obj = {};
                $('td', this).each(function () {
                    var key = $(this).attr('id');
                    var value = $(this).text();
                    key = key.replace(/[0-9]/g, '');
                    inner_obj[key] = value;
                });
                inner_table.push(inner_obj);
            });
            var key = $(this).attr('id');
            var value = inner_table;
            eval('obj = { ' + key + ' : value}');
	    }else{
	        var key = $(this).attr('id');
            var value = $(this).text();
            eval('obj = { ' + key + ' : value}');
	    }


		Object.assign(oco_data, obj);
	});
	$('#checks input:text').each(function () {
		var key = $(this).attr('id');
		var value = $(this).val();
		eval('obj = { ' + key + ' : value}');

		Object.assign(oco_data, obj);
	});

	console.log(oco_data)

	saveBase(JSON.stringify(oco_data))
}

function saveBase(json){
    $.ajax({
		url: url,
		data: {
			action: 'save_oco_base',
			json: json,
		},
		contentType: "application/json; charset=utf-8",
		dataType: "json",

		success: function (data) {
			console.log('suc')
		},
		error: function (data) {
		    console.log('err')
		}
	});

}
