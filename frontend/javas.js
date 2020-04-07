function getCountryInfo() {
  var CountryCode = document.getElementById("countryCode").value;
  var div = document.getElementById("div01");
  div.style.display = "block";
  var table = document.getElementById("table1");
  var first = true;
  if(first){
    var row = table.insertRow(1);
    
	// Insert new cells (<td> elements) at the 1st and 2nd position of the "new" <tr> element:
	var cell0 = row.insertCell(0);
	var cell1 = row.insertCell(1);
	var cell2 = row.insertCell(2);
	var cell3 = row.insertCell(3);
	var cell4 = row.insertCell(4);
	var cell5 = row.insertCell(5);
	var cell6 = row.insertCell(6);
	var cell7 = row.insertCell(7);
	var cell8 = row.insertCell(8);
	var cell9 = row.insertCell(9);
	
	
  }
	
  if (CountryCode.length == 3) {
    var xhttp = new XMLHttpRequest();
	var url = "http://35.190.114.222/country/" + CountryCode;
      
	$.ajax({
        type: "GET", 
        url: url,
        timeout: 3000,
        contentType: "application/json; charset=utf-8",
        cache: false,
        beforeSend: function() {
            $("h2").html("Carregando..."); //Carregando
        },
        error: function() {
            $("h2").html("O servidor não conseguiu processar o pedido");
        },
        success: function(resposta) {
                // Interpretando retorno JSON...
                first = false;
                if(resposta[0] != "Nenhum Pais encontrado"){
                cell0.innerHTML = resposta.shortname;
                cell1.innerHTML = resposta.longname;
                cell2.innerHTML = resposta.currencyunit;
                cell3.innerHTML = resposta.region;
                cell4.innerHTML = resposta.incomegroup;
                cell5.innerHTML = resposta.latestpopulationcensus;
                cell6.innerHTML = resposta.latesthouseholdsurvey;
                cell7.innerHTML = resposta.latestagriculturalcensus;
                cell8.innerHTML = resposta.latestindustrialdata;
                cell9.innerHTML = resposta.latesttradedata;
                }
                
        } 
    });    
    }
  

  } 


function addIndicator(){
    var countryName = document.getElementById("countryName").value;
    var countryCode = document.getElementById("countryCode").value;
    var indicatorName = document.getElementById("indicatorName").value;
    var indicatorCode = document.getElementById("indicatorCode").value;
    var year = document.getElementById("year").value;
    var value = document.getElementById("value").value;
    
    var xhttp = new XMLHttpRequest();
    var url = "http://35.190.114.222/indicator/";
    
    var obj = new Object();
    
    obj.countryname = countryName;
    obj.countrycode = countryCode;
    obj.indicatorname = indicatorName;
    obj.indicatorcode = indicatorCode;
    obj.year = year;
    obj.value = value;
    $.post(url, obj);
    
    
}
