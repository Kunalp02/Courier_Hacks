from .models import Category

# Takes request as an argument and returns dictionary as an argument
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)