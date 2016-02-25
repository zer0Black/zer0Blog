$(function () {

    $('#blog-comment-form').submit(function (event) {
        var url = $(event.target).attr('action');
        $.ajax({
            type: "post",
            url: url,
            data: {
                "comment": $("#comment").val()
            },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data, textStatus) {
                $("#comment").val("");
                $(".blog-comment ul").prepend(data);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

    $('.delete').on('click', function(event){
        var comment_id = $(event.target).attr('data-id');
        $.ajax({
            type: "post",
            url: "/comment/delete/" + comment_id,
            data: {
            },
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data) {
                var delete_comment_id = 'comment-' + data.comment_id;
                $('#'+ delete_comment_id).remove();
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest.responseText);
            }
        });
    });

});
