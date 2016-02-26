$(function () {

    $('#blog-comment-form').submit(function (event) {
        var url = $(event.target).attr('action');
        var comment_content = $(event.target).find('textarea').val();
        //提交验证
        if (comment_content == null || comment_content == '') {
            var warn_element = $(event.target).find('.warning');
            warn_element.css('display', 'inline-block');
            var warn_text_element = warn_element.find('.warning-text');
            warn_text_element.text('请输入评论内容');
            return false;
        }

        $.ajax({
            type: "post",
            url: url,
            data: {
                "comment": comment_content
            },
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data, textStatus) {
                //$("#comment_content").val("");
                //$(".blog-comment ul").prepend(data);
                var comment_html = '<div class="child-comment" id="comment-"' + data.comment_id + '>';
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });


    $('.delete').on('click', function (event) {
        deleteEvent();
    });

    function deleteEvent() {
        if (confirm("确认删除?")) {
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
                            parent_div.addClass('hidden')
                        }
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    console.log(XMLHttpRequest.responseText);
                }
            });
        }
    }

    $('.reply').on('click', function (event) {
        replyEvent();
    });

    function replyEvent() {
        var current_tag = $(event.target);
        var target_username = current_tag.attr('data-nickname');
        var root_id = current_tag.attr('data-id');
        var parent_id = current_tag.attr('data-id');
        //找出form展示出来
        var form_parent_element = current_tag.parents('.blog-comment-content').find('.child-comment-list');
        form_parent_element.removeClass('hide');
        var form_element = form_parent_element.find('form');
        form_element.css('display', 'block');
        //找到form中的input[name=root_id] 和 input[name=parent_id]项，赋予root_id 和 parent_id给它
        form_element.find('input[name=root_id]').val(root_id);
        form_element.find('input[name=parent_id]').val(parent_id);
        //再找出form中的textarea，把@赋予它
        form_element.find('textarea').val('@' + target_username + ' ').focus();
    }

    $('.child_reply').on('click', function (event) {
        childReplyEvent();
    });

    function childReplyEvent() {
        var current_tag = $(event.target);
        var target_username = current_tag.attr('data-nickname');
        var root_id = current_tag.attr('data-root-id');
        var parent_id = current_tag.attr('data-parent-id');
        //找出form展示出来
        var form_element = current_tag.parents('.child-comment-list').find('form');
        form_element.css('display', 'block');
        //找到form中的input[name=root_id] 和 input[name=parent_id]项，赋予root_id 和 parent_id给它
        form_element.find('input[name=root_id]').val(root_id);
        form_element.find('input[name=parent_id]').val(parent_id);
        //再找出form中的textarea，把@赋予它
        form_element.find('textarea').val('@' + target_username + ' ').focus();
    }

    $('.child-comment-form').submit(function (event) {
        var current_tag = $(event.target)
        var url = current_tag.attr('action');
        var comment_content = current_tag.find('textarea').val();
        var root_id = current_tag.find('input[name=root_id]').val();
        var parent_id = current_tag.find('input[name=parent_id]').val();
        //提交验证
        if (comment_content == null || comment_content == '') {
            var warn_element = $(event.target).find('.warning');
            warn_element.css('display', 'inline-block');
            var warn_text_element = warn_element.find('.warning-text');
            warn_text_element.text('请输入评论内容');
            return false;
        }

        $.ajax({
            type: "post",
            url: url,
            data: {
                "comment": comment_content,
                "root_id": root_id,
                "parent_id": parent_id
            },
            dataType: 'json',
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success: function (data, textStatus) {
                current_tag.css('display', 'none');
                //组装html
                var comment_html = '<div class="child-comment" id="comment-"' + data.comment_id + '>';
                comment_html += '<p><a class="blue-link" href="#">' + data.comment_author + '</a>：' + data.comment_content + '</p>';
                comment_html += '<div class="child-comment-footer text-right clearfix">';
                if (data.user_id == data.author_id) {
                    comment_html += '<a data-id="' + data.comment_id + '" class="delete" href="javascript:void(0)">删除</a> ';
                }
                comment_html += '<a data-parent-id="' + data.comment_id + '" data-root-id="' + root_id + '" data-nickname="' + data.comment_author + '" class="child_reply" href="javascript:void(0)">回复</a>';
                comment_html += '<span class="reply-time pull-left">' + data.comment_publish_time + '</span>';
                comment_html += '</div></div>';

                //判断是否有子评论
                if (current_tag.parent('.child-comment-list').find('.child-comment').length > 0) {
                    var last_comment_element = current_tag.parent('.child-comment-list').find('.child-comment').last();
                    last_comment_element.after(comment_html);
                } else {
                   current_tag.parent('.child-comment-list').prepend(comment_html);
                }

                var new_comment_element = current_tag.parent('.child-comment-list').find('.child-comment').last();
                new_comment_element.on('click', '.delete', function () {
                    deleteEvent();
                });
                new_comment_element.on('click', '.child_reply', function () {
                    childReplyEvent();
                });
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(XMLHttpRequest.responseText);
                console.log(XMLHttpRequest.responseText);
            }
        });
        return false;
    });

});
