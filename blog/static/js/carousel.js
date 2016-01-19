$(function () {

    $('#carousel_image').on('change', function () {
        var image = this.files[0];
        var reader = new FileReader();
        //把image专为base64字符串
        reader.readAsDataURL(image);
        //加载完成后，绘制图片
        reader.onload = function (readerEvent) {
            $('#carousel_thumbnail').attr('src',readerEvent.target.result);
            //上传图片，则把链接置为空，并禁止输入
            $('#image_link').val('');
            $('#image_link').attr('disabled', 'disabled');
        }
    });

     //发布
    $("#add_carousel").click(function () {
        $("#carousel_form").submit();
    });

    //更新
    $("#update_carousel").click(function () {
        $("#carousel_form").submit();
    });

    $("#carousel_form").validate({
        ignore: "",
        rules: {
            title: {
                required: true,
                maxlength: 100
            },
            post: {
                required: true,
            },
        },
        messages: {
            title: {
                required: "请输入标题",
                maxlength: "标题过长，请检查",
            },
            post: {
                required: "请选择轮播的博客",
            },
        }
    });

});
