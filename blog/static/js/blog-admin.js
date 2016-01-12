$(function () {

    $('#save_editor').submit(function () {
        $.ajax({
            type: "post",
            url: "/admin/update/editor",
            data: {
                "editor": $("#editor_form input[type='radio']:checked").val()
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data, textStatus) {
                alert("修改成功");
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
            }

        });
        return false;
    });

});