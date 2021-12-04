from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from .models import Category
from django.urls import reverse

from .forms import OrderForm

from django.core.paginator import Paginator
from django.views.generic import ListView
import re 



class ContactListView(ListView):
    paginate_by = 2
    model = Product

def index(request):
    contact_list = Product.objects.all()
    paginator = Paginator(contact_list, 8)
    # Show 8 contacts per page.

    page_number = request.GET.get('page')
    context = paginator.get_page(page_number)
    return render(request, 'main/index.html', {'context': context})


def pizza(request):
    context = Product.objects.all()
    category = Category.objects.get(pk = 1)
    return render(request,'main/pizza.html',{'context':context, 'category': category})

def sushi(request):
    context = Product.objects.all()
    category = Category.objects.get(pk = 3)
    return render(request,'main/sushi.html',{'context':context, 'category': category})

def drink(request):
    context = Product.objects.all()
    category = Category.objects.get(pk = 4)
    return render(request,'main/drink.html',{'context':context, 'category': category})
    
def burger(request):
    context = Product.objects.all()
    category = Category.objects.get(pk = 2)
    return render(request,'main/burger.html',{'context':context, 'category': category})

def discount(request):
    contact_list = Product.objects.all()
    paginator = Paginator(contact_list, 8) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    context = paginator.get_page(page_number)
    return render(request,'main/discount.html',{'context':context} )


# def cart (request):
#    context = Product.objects.all()
#    return render(request,'main/cart.html',{'context':context})

#3 Сервер принимает request от страницы со списком товара, 
# создает зависимость товара
def addCart(request):
    if request.method == "GET":
        data = request.GET.dict()
        all_price = 0
        print(data)
        #Перебираем весь заказ
        for key in data:
            #Регулярное выражение на нахождения товара  
            if re.search(r'data\[\d+\]', key):
                #Вывод данных о заказаном продукте
                print("id продукта: ",re.findall('\d+', key)[0])
                print("количество этого продукта: ", data[key])
                prod = Product.objects.get(pk = int(re.findall('\d+', key)[0]))
                all_price += (prod.price * int(data[key]))
        Order.objects.filter(id=data["pk"]).update(price=all_price)




    return HttpResponse()

#1 работа с формой
def cart (request):
    context = Product.objects.all()
    error = ''
    # Получение данных с формы
    if request.method == 'POST':
        form = OrderForm(request.POST)
        # Проверка заполнены ли все данные
        if form.is_valid():
            # form.save()
            pk = form.save().id
            print(form.save().id)
            # переадресация на страницу finish и
            # передача id создоной истории в БД
            return redirect('finish', pk)
        else:
            error = 'Форма была неверной'
    # Отправка шаблона формы на страницу
    form = OrderForm()
    data = {
        'form': form,
        "error": error,
        'context': context
    }
    return render(request, 'main/cart.html', data)

#2 Отправка Id в шаблон на страницу, 
# где отправится запрос со списком товара
def finish(request, pk):
   return render(request, 'main/finish.html', {"pk":pk})












