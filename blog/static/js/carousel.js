$(function () {

    $('#carousel_image').on('change', function () {
        var image = this.files[0];
        var reader = new FileReader();
        //把image专为base64字符串
        reader.readAsDataURL(image);
        //加载完成后，绘制图片
        reader.onload = function (readerEvent) {
           $('#carousel_thumbnail').attr('src',readerEvent.target.result);
        }
    });

});
