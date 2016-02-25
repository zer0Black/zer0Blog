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
        if(confirm("确定删除?")) {
            var comment_id = $(event.target).attr('data-id');
            $.ajax({
                type: "post",
                url: "/comment/delete/" + comment_id,
                data: {},
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
                },
                success: function (data) {
                    var delete_comment_id = 'comment-' + data.comment_id;
                    var delete_element = $('#' + delete_comment_id);
                    var parent_div = delete_element.parent();
                    delete_element.remove();
                    /*
                     * 查看父节点是否为Div，若为Div，则证明删除元素为楼中楼评论，
                     * 在查看父Div下是否有其他Div元素，若没有，则证明再无楼中楼评论
                     * 可直接删除父Div
                     */
                    if (parent_div.is('div')) {
                        var has_children = parent_div.has('div').length > 0;
                        if (!has_children) {
                            parent_div.remove();
                        }
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    console.log(XMLHttpRequest.responseText);
                }
            });
        }
    });

});
