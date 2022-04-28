from django.shortcuts import render
from .models import TypeLosses


# Create your views here.
def main(request):
    results = TypeLosses.objects.order_by()
    return render(request, 'infoboard/index.html', {'results': results})


def create_type(request):
    message = None
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        tl = TypeLosses(name=name, description=description)
        tl.save()
        message = f'Створено тип втрат {name}. Опис: {description}'
    return render(request, 'infoboard/info.html', {'message': message})

