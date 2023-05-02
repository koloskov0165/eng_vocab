import pandas as pd
import random
from django.shortcuts import render, redirect
from django.core.cache import cache
from . import vocab_work


def index(request):
    return render(request, "index.html")

def vocab(request):
    words = vocab_work.get_words_for_table()
    return render(request, "vocab.html", context={"words": words})

def add_word(request):
    return render(request, "add_word.html")

def send_word(request):
    if request.method == "POST":
        cache.clear()
        # user_name = request.POST.get("name")
        ru_word = request.POST.get("ru_word", "")
        en_word = request.POST.get("en_word", "").replace(";", ",")
        # context = {"user": user_name}
        context = {}
        if len(ru_word) == 0:
            context["success"] = False
            context["comment"] = "Поле для перевода должно быть не пустым"
        elif len(en_word) == 0:
            context["success"] = False
            context["comment"] = "Поле для слова должено быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваше слово принято"
            vocab_work.write_word(en_word, ru_word)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "word_request.html", context)
    else:
        add_word(request)

def start_test(request):
    request.session['en_set'] = list()
    request.session['en_word'] = ""
    request.session['correct'] = 0
    request.session['amount'] = 0
    request.session['started'] = True
    return render(request, "start_test.html")

def test(request):
    if 'started' not in request.session or not request.session['started']:
        return redirect('/start_test')

    df = pd.read_csv("./data/words.csv")

    en_word = random.choice(list(set(df.en.values) - set(request.session['en_set'])))
    request.session['en_word'] = en_word
    # request.session['en_set'].append(en_word)

    context = {}
    context['en_word'] = en_word
    context['volume'] = len(set(df.en.values))
    context['idx'] = len(set(request.session['en_set']))
    return render(request, "test.html", context)

def check_ans(request, finish=False):
    if request.method == "POST":
        cache.clear()
        ru_word = request.POST.get("ru_word", "")
        df = pd.read_csv("./data/words.csv")

        request.session['en_set'].append(request.session['en_word'])

        ans = ru_word in df[df.en == request.session['en_word']].ru.values
        if request.session['started']:
            if ans:
                request.session['correct'] += 1
            request.session['amount'] += 1
        if len(set(request.session['en_set'])) < len(set(df.en.values)) and not finish:
            return redirect("/test")
        else:
            return redirect("/test_result")
    else:
        test(request)

def send_answer(request):
    return check_ans(request, finish=False)

def finish_test(request):
    # request.session['finish'] = True
    return check_ans(request, finish=True)

def test_result(request):
    context = {"correct": request.session['correct'],
               "amount": request.session['amount'],
               "all": pd.read_csv("./data/words.csv").en.nunique(),
               "score": round(request.session['correct'] / request.session['amount'] * 10, 1)}
    request.session['started'] = False
    return render(request, "test_result.html", context)
