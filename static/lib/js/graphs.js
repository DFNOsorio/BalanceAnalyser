$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/_get_cache_data', {}, function(data){
        $('#Frequency').text(data);
    });
    $.getJSON($SCRIPT_ROOT + '/_make_graph', {}, function(data){
        console.log(data.script);
        appendHtml(document.getElementById('Graphs'), data.div + data.script)
    });

});

function appendHtml(el, str) {
    var div = document.createElement('div');
    div.innerHTML = str;
    while (div.children.length > 0) {
        el.appendChild(div.children[0]);
    }
}
