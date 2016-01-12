$(function(){

    $("#add_post").click(function(){
        //修改隐藏域，设定参数为发布
        $("#post_action_flag").val("add");
        $("#post_form").submit();
    });

    $("#post_form").validate({
        debug: true,
        ignore: "",
        rules:{
           title:{
               required: true,
               maxlength: 100
           },
           content:{
               required: true
           },
           catalogue:{
               required: true,
               minlength: 1,
           },
           tag:{
               required: false
           }
        },
        messages:{
           title:{
               required: "请输入标题",
               maxlength: "标题过长，请检查",
           },
           content:{
               required: "请输入博客内容",
           },
           catalogue:{
               required: "请给博客选择一个目录",
               minglength: "请给您的博文选择一个目录"
           }
       }
    });

});