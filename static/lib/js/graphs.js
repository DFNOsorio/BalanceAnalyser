var temp

$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/_get_cache_data', {}, function(data){
        $('#Frequency').text(data);
    });
    $.getJSON($SCRIPT_ROOT + '/_make_graph', {}, function(data){
        temp = data
        //Bokeh.embed.add_document_static()
    });
});
