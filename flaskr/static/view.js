import('https://code.jquery.com/jquery-3.4.1.min.js');


function resetAllFields() {
    $("#city-error").hide(0);
    $("#service-error").hide(0);
    $("#station-error").hide(0);

    $("p#temp").text('');
    $("p#hum").text('');
    $("p#precip").text('');
    $("p#wind").text('');
    $("p#icon").text('');
    $("p#forecast").text('');
    $("p#recom").text('');
}


function updateInfo(resp) {
    resetAllFields();
    var pm = '\u00B1';

    if(resp.status !== 'ok') {
        if(resp.status === 'C') {
            $("#city-error").css("display", "block");
        }

        if(resp.status === 'N') {
            $("#station-error").css("display", "block");
        }

        return
    }

    $("p#temp").text(resp.forecast['temp'][0] + pm + resp.forecast['temp'][1] + 'C' + '\u00B0');
    $("p#hum").text(resp.forecast['humidity'][0] + pm + resp.forecast['humidity'][1] + '%');
    $("p#precip").text(resp.forecast['precip'] + '%');
    $("p#wind").text(resp.forecast['wind'] + 'м/с');

    $("p#forecast").text(resp.forecast['description']);
    $("p#recom").text(resp.recom);

    $('#icon').html('<img src="../static/images/' + resp.forecast.icon +'.png">')
}


function getForecast() {
    var request = $.ajax({
        method: "POST",
        url: "/forecast",
        data: {city: $("#city")[0].value}
    })
    .done(function(msg) {
        updateInfo(msg);
    });

    request.fail(function(jqXHR, status) {
        $("#service-error-error").css("display", "block");
        console.log(status);
    });

    return false;
}
