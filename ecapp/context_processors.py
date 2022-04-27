from.models import Category, Products


def menu_link(request):
    link = Category.objects.all()
    return dict(link=link)