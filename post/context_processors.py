def select_parent_template(request):
    """Check if it's ajax, if so no need parent template."""
    print(1)
    parent_template = 'dummy_parent.html' if request.is_ajax() else 'base.html'
    return {'parent_template': parent_template}
