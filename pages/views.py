from django.shortcuts import render
from django.http import HttpResponse
from .models import Contact
import requests
from django.contrib import messages
from .models import Post
# Create your views here.

# def home(request):
#     return HttpResponse('Hello Python world')

def get_html_content(request):
    import requests
    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

def home(request):

    result = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        # extract region
        result['region'] = soup.find("span", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text
        # extract temperature now
        result['temp_now'] = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
        # get the day, hour and actual weather
        result['dayhour'], result['weather_now'] = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"}).text.split('\n')
        result['chairt'], result['chairt'] = soup.find("div", attrs={"class": "nawv0d"}).text.format('\n')

        #context = {'result':result}
    return render(request, 'pages/home.html', {'result':result})



def about(request):
    context = {}
    return render(request, 'pages/about.html', context)


def blog(request):
    # obj = blog.objects.get(id=1)
    allPosts= Post.objects.all()
    context={'allPosts': allPosts}
    return render(request, 'pages/blog.html', context)


def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    context = {}
    return render(request, 'pages/contact.html', context)
