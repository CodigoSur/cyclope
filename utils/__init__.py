import cyclope

def layout_for_request(request):
    """
    Returns the layout corresponding to the MenuItem matching the request
    or the default site layout if no matching MenuItem is found
    """
    from cyclope.models import MenuItem

    req_url= request.META['PATH_INFO']

    #ToDo: this check is just to make the URL: /cyclope/ work (correct later)
    if req_url[1:] != cyclope.settings.CYCLOPE_PREFIX:
        req_url = req_url[len(cyclope.settings.CYCLOPE_PREFIX)+1:]

    try:
        menu_item = MenuItem.objects.select_related().get(url=req_url)
    except:
        menu_item = None
    if menu_item and menu_item.layout:
        layout = menu_item.layout
    else:
        layout = cyclope.settings.CYCLOPE_DEFAULT_LAYOUT

    return layout


def template_for_request(request):
    """
    Returns the layout corresponding to the MenuItem matching the request
    or the default site template if no matching MenuItem is found
    """
    layout = layout_for_request(request)
    template = '%sthemes/%s/%s' % (
                cyclope.settings.CYCLOPE_PREFIX,
                cyclope.settings.CYCLOPE_CURRENT_THEME,
                layout.template
                )
    return template
