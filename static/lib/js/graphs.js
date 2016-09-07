$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/_get_cache_data', {}, function(data){
        $('#Frequency').text(data);
    });
});
