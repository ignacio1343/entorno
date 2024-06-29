$(document).ready(function () {

    console.log("Esperando datos......");

    $.getJSON('https://mindicador.cl/api', function() {
        
        //console.log([data]);
        

}).fail(function() {
    console.log('Error al consumir la API!');
    $("#dolar").text("No se pudo obtener");
    $("#dolar").addClass("h6");
}).done(function(data)
{
    $(".spinner-grow").hide();
    $(".textloader").hide();
    /*$("#loader").hide();
    $("#textloader").hide();*/
    $("#dolar").text('$' + data.dolar.valor);
    $("#uf").text("$" + data.uf.valor);
    $("#bitcoin").text("$" + data.bitcoin.valor);
    
});
});