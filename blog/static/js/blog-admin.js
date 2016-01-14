$(function () {

    $('#save_editor').click(function () {
        $('#editor_form').submit();
    });

    $("#editor_form").validate({
        ignore: "",
        rules: {
            editor: {
                required: true,
            },
        },
        messages: {
            editor: {
                required: "请选择您要使用的编辑器",
            }
        },
    });

});