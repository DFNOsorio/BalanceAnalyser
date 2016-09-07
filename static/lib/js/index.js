var folder_names;
$(document).ready(function () {
    var current_folder;
    $.getJSON($SCRIPT_ROOT + '/_display_folders', {}, function (data) {
        folder_names = data;
        list_folders(folder_names);
    });

    $('#button').click(function(){window.location.href = $GraphPageLocation});
});

function list_folders(data) {
    $('#button').attr('disabled', 'true')
    var toAppend = "<div align='center'><select id='folderSelection'>";
    folder_names = folder_names.sort()
    for (i = 0; i < folder_names.length; i++) {
        if (folder_names[i] == '.DS_Store') {}
        else {
            toAppend = toAppend + "<option value='" + folder_names[i] + "'>" + folder_names[i] + "</option>";
        }
    }
    $('#FolderList').append(toAppend = toAppend + "</select></div>");
    current_folder = $('#folderSelection').val();
    load_data(current_folder)
    $('#folderSelection').change(function () {
        current_folder = $('#folderSelection').val();
        $('#button').attr('disabled', 'true')
        load_data(current_folder)
            // LOAD THE CORRECT DATA AND FOLDER
    });
};

function load_data(current_folder_name) {
    $('#LoadingStatus').text("Opening files")
    $.getJSON($SCRIPT_ROOT + '/_set_folder_name', {
        folder_name: current_folder_name
    }).done(function (data) {
        var source = new EventSource("/_load_data");
        setProgress(0)
        source.onmessage = function (event) {
            if (event.data == 'End') {
                $('#LoadingStatus').text('Loaded')

            }
            else if (event.data == 'Close') {
                $.getJSON($SCRIPT_ROOT + '/_cache_data');
                source.close();
                $.getJSON($SCRIPT_ROOT + '/graph');
                $('#button').attr('disabled', false);

            }
            else {
                tempJSON = JSON.parse(event.data)
                $('#LoadingStatus').text(tempJSON.data);
                setProgress((tempJSON.counter / tempJSON.total))
            };
        };
    });
}

function setProgress(progress)
{
    var progressBarWidth =progress*$(".container").width();
    $(".progressbar").width(progressBarWidth);
}
