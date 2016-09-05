var folder_names;

$(document).ready(function () {
    var current_folder;
    $.getJSON($SCRIPT_ROOT + '/_display_folders', {},
              function(data){folder_names = data;
                             present_folders(folder_names);});
});

function present_folders(data){
    var toAppend = "<div align='center'><select id='folderSelection'>";
    for (i = 1; i < folder_names.length; i++) {
        toAppend  = toAppend + "<option value='"+folder_names[i]+"'>"+folder_names[i]+"</option>";
    }
    $('#FolderList').append(toAppend  = toAppend + "</select></div>");
    current_folder = $('#folderSelection').val();
    $('#folderSelection').change(function(){
        current_folder = $('#folderSelection').val();
        // LOAD THE CORRECT DATA AND FOLDER
    });
}
