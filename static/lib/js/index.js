var folder_names;

$(document).ready(function () {
    $.getJSON($SCRIPT_ROOT + '/_display_folders', {},
              function(data){folder_names = data;
                             present_folders(data);});
});

function present_folders(data){
    console.log(data);
    console.log(folder_names);
}
