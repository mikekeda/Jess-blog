def select_parent_template(request):
    """Check if it's ajax, if so no need parent template."""
    parent_template = "base.html"
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        parent_template = "dummy_parent.html"

    return {"parent_template": parent_template}
