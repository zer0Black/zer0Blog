$(function () {

    //发布
    $("#add_post").click(function () {
        //修改隐藏域，设定参数为发布，0为草稿，1为发布
        $("#post_action_flag").val("1");
        tinymce.triggerSave();
        removeExtForm();
        $("#post_form").submit();
    });

    //存为草稿
    $("#draft_post").click(function () {
        //修改隐藏域，设定参数为发布，0为草稿，1为发布
        $("#post_action_flag").val("0");
        tinymce.triggerSave();
        removeExtForm();
        $("#post_form").submit();
    });

    //发布草稿
    $("#add_draft").click(function () {
        $("#post_action_flag").val("1");
        tinymce.triggerSave();
        removeExtForm();
        $("#post_form").submit();
    });

    //保存草稿
    $("#update_draft").click(function () {
        $("#post_action_flag").val("0");
        tinymce.triggerSave();
        removeExtForm();
        $("#post_form").submit();
    });

    //保存修改
    $("#update_post").click(function () {
        tinymce.triggerSave();
        removeExtForm();
        $("#post_form").submit();
    });

    $("#cancel").click(function () {
        if (confirm("确认取消吗？")) {
            window.location.href = '/admin/'
        } else {
            return false;
        }
    });

    function removeExtForm(){
        $("#post_form").find("form").remove();
    }

    $("#post_form").validate({
        ignore: "",
        rules: {
            title: {
                required: true,
                maxlength: 100
            },
            content: {
                required: true,
            },
            catalogue: {
                required: true,
            },
            tag: {
                required: false,
            }
        },
        messages: {
            title: {
                required: "请输入标题",
                maxlength: "标题过长，请检查",
            },
            content: {
                required: "请输入博客内容",
            },
            catalogue: {
                required: "请给博客选择一个目录",
            }
        }
    });

    $("#tags").tagsInput({
        width: 464,
        height: 35,
        defaultText: '添加标签',
        maxChars: 10,
    });

});