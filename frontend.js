showedCountries = [];
  
$(function() {
  $("#countryForm").submit(function() { 
    getCountryInfo();
    return false; 
    });
});

$(function() {
  $("#indicatorForm").submit(function() { 
    getCountryInfo();
    return false; 
    });
});

$(function() {
  $("#indicatorInfoForm").submit(function() { 
    getCountryInfo();
    return false; 
    });
});

function clearTable(tableId){
$('#' + tableId +' tr:not(:first-child)').remove();
showedCountries = [];
}
  
function getCountryRegression() {
  
  var div = document.getElementById("div05");
  var table = document.getElementById("table5");
    var countryChosen = document.getElementById("countryCode5").value;
    var year = document.getElementById("yearL1").value;
    console.log(countryChosen);
    console.log(caseChosen);

    var xhttp = new XMLHttpRequest();
    var url = "http://35.190.114.222/regression/" + countryChosen "/" + year ;
      
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
                  
                    //div.style.display = "block";

                        var row = table.insertRow(1);

                        var cell0 = row.insertCell(0);
                        var cell1 = row.insertCell(1);
                        var cell2 = row.insertCell(2);
                        var cell3 = row.insertCell(3);
                    var url = "http://35.190.114.222/country/" + resposta.country;
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
                            cell0.innerHTML = resposta.shortname;
                          } 
                      });    
                        
                        cell1.innerHTML = resposta.indicator.replace('-','.');
                        
                        var url = "http://35.190.114.222/serie/" + cell1.innerHTML;
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
                            cell2.innerHTML = resposta.indicatorname;
                          } 
                      });    
                    
                   
                            
                        cell3.innerHTML = resposta.prediction;
                }
           
        }); 
    }
   
  
function getCountryCorrelation() {
  
  var div = document.getElementById("div04");
  var table = document.getElementById("table4");
    var e = document.getElementById("countrydd");
    var countryChosen = e.options[e.selectedIndex].value;
    var e1 = document.getElementById("casedd");
    var caseChosen = e1.options[e1.selectedIndex].value;
    console.log(countryChosen);
    console.log(caseChosen);

    var xhttp = new XMLHttpRequest();
    var url = "http://35.190.114.222/correlation/" +countryChosen "/"+ caseChosen ;
      
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
                  
                    //div.style.display = "block";
                    for (var i=0;i<resposta.length;i++) {
                        var row = table.insertRow(1);

                        var cell0 = row.insertCell(0);
                        var cell1 = row.insertCell(1);
                        var cell2 = row.insertCell(2);
                        var cell3 = row.insertCell(3);

                        cell0.innerHTML = resposta[i].targetcode.replace('-','.');
                        cell1.innerHTML = resposta[i].indicatorcode.replace('-','.');
                        
                        var url = "http://35.190.114.222/serie/" + cell1.innerHTML;
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
                            cell2.innerHTML = resposta.indicatorname;
                          } 
                      });    
                    
                  } 
                            
                        cell3.innerHTML = resposta[i].correlationvalue;
                }
           
      });    
    
  } 
  
function getCountryInfo() {
  var countryCode = document.getElementById("countryCodeSearchCode").value;
  var div = document.getElementById("div01");
  var table = document.getElementById("table1");

  console.log(countryCode);

  if (!showedCountries.includes(countryCode)) {
    showedCountries.push(countryCode);

    var xhttp = new XMLHttpRequest();
    var url = "http://35.190.114.222/country/" + countryCode;
      
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
                  if(resposta[0] != "Nenhum Pais encontrado"){
                    div.style.display = "block";

                    var row = table.insertRow(1);

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

function getAllCountriesInfo() {
  var div = document.getElementById("div01");
  div.style.display = "block";
  var table = document.getElementById("table1");
  var xhttp = new XMLHttpRequest();
  var url = "http://35.190.114.222/country/ALL";

  
    
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
                for (var i=0;i<resposta.length;i++) {
                  if (!showedCountries.includes(resposta[i].countrycode) && resposta[i].currencyunit != null) {
                    showedCountries.push(resposta[i].countryCode);

                    var row = table.insertRow(1);
  
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

                    cell0.innerHTML = resposta[i].shortname;
                    cell1.innerHTML = resposta[i].longname;
                    cell2.innerHTML = resposta[i].currencyunit;
                    cell3.innerHTML = resposta[i].region;
                    cell4.innerHTML = resposta[i].incomegroup;
                    cell5.innerHTML = resposta[i].latestpopulationcensus;
                    cell6.innerHTML = resposta[i].latesthouseholdsurvey;
                    cell7.innerHTML = resposta[i].latestagriculturalcensus;
                    cell8.innerHTML = resposta[i].latestindustrialdata;
                    cell9.innerHTML = resposta[i].latesttradedata;
                  }
                }  
        } 
    });    
  
  } 


function getCountryIndicators() {
  var div = document.getElementById("div02");
clearTable("table2");
var country = document.getElementById("countryCode1").value;
var year = document.getElementById("yearL").value;
  div.style.display = "block";
  var table = document.getElementById("table2");
  var xhttp = new XMLHttpRequest();
  var url = "http://35.190.114.222/indicator/" + country;

  
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
                for (var i=0;i<resposta.length;i++) {
        if(parseInt(resposta[i].year)== year){
                    var row = table.insertRow(1);
  
                    var cell0 = row.insertCell(0);
                    var cell1 = row.insertCell(1);
                    var cell2 = row.insertCell(2);
                    var cell3 = row.insertCell(3);
                    var cell4 = row.insertCell(4);

                    cell0.innerHTML = resposta[i].countryname;
                    cell1.innerHTML = resposta[i].indicatorname;
                    cell2.innerHTML = resposta[i].indicatorcode;
                    cell3.innerHTML = resposta[i].value;
                    cell4.innerHTML = resposta[i].year;
        }
                  
                }  
        } 
    });    
  
  } 
function addIndicator(){
    var countryName = document.getElementById("countryName").value;
    var countryCode = document.getElementById("countryCode").value;
    var indicatorName = document.getElementById("indicatorName").value;
    var indicatorCode = document.getElementById("indicatorCode").value;
    var year = document.getElementById("year").value;
    var value = document.getElementById("value").value;
    
    var xhttp = new XMLHttpRequest();
    var url = "http://35.190.114.222/indicator";
    if(countryName.length > 0 && countryCode.length == 3 && indicatorName.length > 0 && indicatorCode.length > 0){
    var obj = new Object();
    
    obj.countryname = countryName;
    obj.countrycode = countryCode;
    obj.indicatorname = indicatorName;
    obj.indicatorcode = indicatorCode;
    obj.year = year;
    obj.value = value;
    $.post(url, obj);
  }
}

function getSerieInfo() {
  var indicatorCode = document.getElementById("indicatorCodePlace").value;
  var div = document.getElementById("div03");
  div.style.display = "block";
  var table = document.getElementById("table3");

  var xhttp = new XMLHttpRequest();
  var url = "http://35.190.114.222/serie/" + indicatorCode;
  console.log(indicatorCode);
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
                var row = table.insertRow(1);

                var cell0 = row.insertCell(0);
                var cell1 = row.insertCell(1);
                var cell2 = row.insertCell(2);
                var cell3 = row.insertCell(3);
                var cell4 = row.insertCell(4);
                var cell5 = row.insertCell(5);

                cell0.innerHTML = resposta.indicatorname;
                cell1.innerHTML = resposta.longdefinition;
                cell2.innerHTML = resposta.seriescode;
                cell3.innerHTML = resposta.source;
                cell4.innerHTML = resposta.topic;
                cell5.innerHTML = resposta.unitofmeasure;  
        } 
    });    
}
  $(document).ready(function() {
$('.mdb-select').materialSelect();
});