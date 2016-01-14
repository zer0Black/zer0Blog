from django import template

register = template.Library()


class NavTagItem(template.Node):
    def __init__(self, nav_path, nav_displaytext, nav_icon):
        self.path = nav_path.strip('"')
        self.text = nav_displaytext.strip('"')
        self.icon = nav_icon.strip('"')

    def render(self, context):
        cur_path = context['request'].path
        if self.path == '/admin/':
            current = cur_path == '/admin/'
        else:
            current = cur_path.startswith(self.path)
        cur_id = ''
        arrow_span = ''
        if current:
            cur_id = ' class="active" '
            arrow_span = '<span class="selected"></span>'
        return '<li %s><a href="%s"><i class="%s"></i><span class="title">%s</span>%s</a></li>' % (cur_id, self.path, self.icon, self.text, arrow_span)


def navtagitem(parser, token):
    try:
        tag_name, nav_path, nav_text, nav_icon = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "%r tag requires exactly three arguments: icon, path and text" % \
            token.split_contents[0]
    return NavTagItem(nav_path, nav_text, nav_icon)

register.tag('nav', navtagitem)