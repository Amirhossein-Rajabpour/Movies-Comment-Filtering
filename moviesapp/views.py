from django.shortcuts import render
from moviesapp.models import Movie, Comment
from django.core.files.storage import default_storage
from moviesapp.services import *
from django.http import HttpResponse


def movies_view(request):
    # should pass list of movies with their details
    all_movies = Movie.objects.all()
    context = {"movies": all_movies}
    return render(request, 'main2.html', context=context)


def ask_language(request, movie_id):
    context = {"movie_id": movie_id}
    return render(request, 'ask_lang.html', context=context)


def view_comments(request, movie_id):
    # should pass id of the movie and its comments and the selected language
    comments = Comment.objects.filter(movie=movie_id)   # is it correct?
    movie = Movie.objects.get(pk=movie_id)
    lang = request.GET['lang']

    context = {"movie": movie, "language": lang, "comments": comments}
    return render(request, 'view_comments.html', context=context)


def add_comment(request, movie_id):
    # a form with 'username' and a button for uploading voice
    if request.method == "GET":
        context = {"movie_id": movie_id}
        return render(request, 'upload_voice.html', context=context)

    elif request.method == "POST":
        username = request.POST['uname']
        voice_file = request.FILES['voice_file']
        print('username: ', username)
        print('voice content', voice_file)

        file_name = default_storage.save(voice_file.name, voice_file)

        all_movies = Movie.objects.all()
        context = {"movies": all_movies}
        run_IBM_services(username, voice_file, movie_id)
        return render(request, 'main2.html', context=context)


def say_hello(request):
    return HttpResponse("hello")




