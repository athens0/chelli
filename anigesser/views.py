import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from .models import Title, Suggestion


class TitleCover:
    def __init__(self, title: Title):
        self.id = title.pk
        self.original_name = title.original_name
        self.description = title.description
        self.image_url = title.image_url
        self.studios = list()
        for i in title.studios.all():
            self.studios.append(str(i))
        self.genres = list()
        for i in title.genres.all():
            self.genres.append(str(i))
        self.themes = list()
        for i in title.themes.all():
            self.themes.append(str(i))
        self.source = str(title.source)
        self.title_type = str(title.title_type)
        self.release_date = str(title.release_date)
        self.rating = title.rating
        self.members = title.members


def index(request):
    return render(request, 'anigesser/index.html')


def home(request):
    data = {
        'home_active': 'active',
        'home_aria': 'page'
    }
    return render(request, 'anigesser/index.html', data)


def ratings(request):
    data = {
        'ratings_active': 'active',
        'ratings_aria': 'page'
    }
    return render(request, 'anigesser/index.html', data)


def calendar(request):
    data = {
        'calendar_active': 'active',
        'calendar_aria': 'page'
    }
    return render(request, 'anigesser/index.html', data)


def news(request):
    data = {
        'news_active': 'active',
        'news_aria': 'page'
    }
    return render(request, 'anigesser/index.html', data)


def register(request):
    MAIL_COOLDOWN = 60
    ATTEMPTS = 3
    if request.user.is_authenticated:
        return redirect('anigesser:home')

    data = {}
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        last_email_sent = request.session.get("last_email_sent", 0)
        if time.time() - last_email_sent < MAIL_COOLDOWN:
            data["error"] = "Пожалуйста, подождите перед повторной отправкой кода."
            return render(request, 'anigesser/register.html', data)

        if not User.objects.filter(email=email).exists():
            code = str(random.randint(0, 999999))
            request.session["verification_code"] = code.rjust(6, '0')
            request.session["email"] = email
            request.session["username"] = username
            request.session["password"] = password
            request.session["attempts"] = ATTEMPTS
            request.session["last_email_sent"] = time.time()

            send_mail(
                "Код подтверждения",
                f"Ваш код подтверждения на Анигессер: {code}",
                "info@chelli.ru",
                [email],
                fail_silently=False,
            )
            return redirect('anigesser:verify')
        
        data["error"] = "Пользователь с такой почтой уже существует!"

    return render(request, 'anigesser/register.html', data)


def verify(request):
    if request.user.is_authenticated:
        return redirect('anigesser:home')

    if request.method == "POST":
        entered_code = request.POST["code"]
        saved_code = request.session.get("verification_code")
        email = request.session.get("email")
        username = request.session.get("username")
        password = request.session.get("password")
        attempts = request.session.get("attempts", 0)

        if attempts <= 0:
            request.session.flush()
            return redirect("anigesser:register")

        if str(entered_code) == str(saved_code):
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            request.session.flush()
            return redirect('anigesser:home')
        else:
            request.session["attempts"] = attempts - 1
            return render(request, "verify_code.html", {"error": f"Неверный код! Осталось попыток: {attempts - 1}"})

    return redirect('anigesser:home')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('anigesser:home')

    data = {}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('anigesser:home')
        else:
            data["error"] = "Неверная почта или пароль!"

    return render(request, 'anigesser/login.html', data)


def about(request):
    return render(request, 'anigesser/about.html')


def licence(request):
    return render(request, 'anigesser/licence.html')


def titles(request, page=1):
    titles_per_page = 20
    data = {
        'titles': list(),
    }
    title_count = Title.objects.count()
    if (page - 1) * titles_per_page < title_count:
        counter = titles_per_page * (page - 1) + 1
        for i in Title.objects.all()[titles_per_page * (page - 1):titles_per_page * page]:
            data['titles'].append((counter, TitleCover(i)))
            print(i.studios.all())
            counter += 1
        data['results'] = (titles_per_page * (page - 1) + 1, counter - 1, title_count)
        data['page'] = page
        if page > 1:
            data['prev_page'] = page - 1
            if page > 2:
                if page != 3:
                    data['first_page_skip'] = True
                data['first_page'] = 1
        if page * titles_per_page < title_count:
            data['next_page'] = page + 1
            if (page + 1) * titles_per_page < title_count:
                if title_count // titles_per_page != page + 2:
                    data['last_page_skip'] = True
                data['last_page'] = title_count // titles_per_page

    return render(request, 'anigesser/titles.html', data)


def title(request, id):
    title = None
    try:
        title = Title.objects.get(pk=id)
    except Exception as e:
        return render(request, 'anigesser/title.html')

    data = dict()
    data['title'] = TitleCover(title)

    return render(request, 'anigesser/title.html', data)


def suggest(request):
    data = dict()

    if request.method == 'POST':
        title_url = request.POST.get('title_url')
        extra_info = request.POST.get('extra_info', '')

        try:
            Suggestion.objects.create(url=title_url, data=extra_info)
            data['success'] = True
        except Exception as e:
            data['success'] = False

    return render(request, "anigesser/suggest.html", data)
    

def contacts(request):
    return render(request, 'anigesser/contacts.html')


def profile(request):
    return redirect('anigesser:home')
