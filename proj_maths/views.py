from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")

def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")

def check_term(request):
    if request.method == "POST":
        cache.clear()
        new_term1 = request.POST.get("new_term1", "")
        new_term3 = request.POST.get("new_term3", "")
        print(new_term1,new_term3)
        return render(request, "term_add.html")

def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term1 = request.POST.get("new_term1", "")
        new_term2 = request.POST.get("new_term2", "")
        new_term3 = request.POST.get("new_term3", "")
        new_term4 = request.POST.get("new_term4", "")
        context = {"user": user_name}
        if len(new_term1) == 0:
            context["success"] = False
            context["comment"] = "Слово на русском языке должно быть не пустым"
        elif len(new_term2) == 0:
            context["success"] = False
            context["comment"] = "Слово на английском должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term1, new_term2, new_term3, new_term4)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)

def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

def show_addition(request):
    return render(request, "addition.html")

def show_registration(request):
    return render(request, "registration.html")

def show_success_reg(request):
    if request.method == "POST":
        cache.clear()
        username = request.POST.get("name")
        email = request.POST.get("email")
        context = {"user": username}
        if len(username) == 0:
            context["success"] = False
            context["comment"] = "Поле имя пользователя не может быть пустым"
        elif len(email) == 0:
            context["success"] = False
            context["comment"] = "Поле email не должно быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Вы успешно зарегистрировались"
        if context["success"]:
            context["success-title"] = ""
        return render(request, "success_reg.html", context)
def show_test(request):
    random_terms_list = terms_work.randomizer_for_test()
    request.session['random_terms'] = random_terms_list
    return render(request, "test.html", random_terms_list)

def show_success_word(request):
    if request.method == "POST":
        cache.clear()
        word = request.POST.get("word").lower()
        context = {"word": word}
        random_terms = request.session.get("random_terms")
        if len(word) == 0:
            context["success"] = False
            context["comment"] = "Поле для слова не может быть пустым"
        elif word != random_terms['term2'].lower():
            context["success"] = False
            context["comment"] = "Поле для слова не может быть пустым"
        else:
            context["success"] = True
            context["comment"] = "Вы правильно написали слово"
        if context["success"]:
            context["success-title"] = ""
        return render(request, "success_word.html", context)