$(document).ready(function () {
    $getJSON("../countries.json", function (data) {
        $.each(data, function (index, item) {
            $('#country').append(
                '<option value="' + item.code + '">' + item.name + '</option>');
        });
    });
});

    
    