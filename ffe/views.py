from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, CommentForm, ProfileForm, UserUpdateForm, RecipeForm

from .models import Recipe, Comment, Follower

# - Authentication models and functions

from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.db.models import Q

from django.contrib import messages


def homepage(request):
    popular_recipes = Recipe.objects.all()[:12]  # Supponiamo che mostriamo le prime n ricette
    categories = Recipe.CATEGORY_CHOICES
    context = {
        'popular_recipes': popular_recipes,
        'categories': categories,
    }
    return render(request, "ffe/index.html", context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"registerform": form}
    return render(request, "ffe/register.html", context=context)


def login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
            else:
                return redirect("my-login")
    else:
        form = LoginForm()

    context = {"loginform": form}
    return render(request, "ffe/login.html", context=context)


@login_required(login_url="my-login")
def dashboard(request):
    followed_users = Follower.objects.filter(follower=request.user).values_list('user', flat=True)
    followed_users_list = User.objects.filter(id__in=followed_users)
    followed_recipes = Recipe.objects.filter(user__in=followed_users)
    categories = Recipe.CATEGORY_CHOICES

    # Inizializza is_following come False di default
    is_following = False

    # Se l'utente è autenticato, controlla se sta seguendo la ricetta
    if request.user.is_authenticated:
        # Qui puoi mettere la logica per determinare se l'utente segue l'utente della ricetta
        # In questo esempio, sto solo impostando is_following su True se l'utente ha almeno un follower
        is_following = Follower.objects.filter(user=request.user).exists()

    context = {
        'categories': categories,
        'followed_recipes': followed_recipes,
        'is_following': is_following,
        'followed_users': followed_users_list,
    }
    return render(request, "ffe/dashboard.html", context)


def user_logout(request):
    auth.logout(request)
    return redirect("homepage")


def explore():
    pass


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    author_username = recipe.user.username if recipe.user else None  # Ottieni l'username dell'autore della ricetta se presente
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe.id)

    is_following = False
    if request.user.is_authenticated:
        is_following = Follower.objects.filter(user=recipe.user, follower=request.user).exists()

    categories = Recipe.CATEGORY_CHOICES
    context = {
        'recipe': recipe,
        'comment_form': comment_form,
        'categories': categories,
        'is_following': is_following,
        'author_username': author_username,  # Passa l'username dell'autore della ricetta al contesto del template
    }
    return render(request, 'ffe/recipe_detail.html', context)


@login_required(login_url="my-login")
def add_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            # Ritorna una risposta JSON di successo senza includere il messaggio "success: true"
            return JsonResponse({'success': True})
        else:
            # Se il form non è valido, ritorna una risposta JSON con gli errori del form
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CommentForm()
    # Se la richiesta non è una richiesta POST, ritorna una risposta JSON con il messaggio di richiesta non valida
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)


@login_required(login_url="my-login")
def favorites(request):
    user_favorites = Recipe.objects.filter(favorited_by=request.user)
    categories = Recipe.CATEGORY_CHOICES
    context = {
        'user_favorites': user_favorites,
        'categories': categories,
    }
    return render(request, 'ffe/favorites.html', context)


@login_required(login_url="my-login")
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.favorited_by.filter(id=request.user.id).exists():
        recipe.favorited_by.remove(request.user)
    else:
        recipe.favorited_by.add(request.user)
    return redirect('recipe_detail', recipe_id=recipe.id)


@login_required(login_url="my-login")
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.favorited_by.filter(id=request.user.id).exists():
        recipe.favorited_by.remove(request.user)
    else:
        recipe.favorited_by.add(request.user)
    return redirect('favorites')


@login_required(login_url="my-login")
def add_recipe(request):
    categories = Recipe.CATEGORY_CHOICES  # Ottieni le categorie
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  # Imposta l'utente autenticato come autore della ricetta
            recipe.user = request.user  # Imposta l'utente autenticato come utente della ricetta
            recipe.save()
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        initial_data = {'author': request.user, 'user': request.user}
        form = RecipeForm(initial=initial_data)  # Passa i dati iniziali al form per popolare i campi nascosti

    context = {
        'form': form,
        'categories': categories,  # Aggiungi le categorie al contesto
    }
    return render(request, 'ffe/add_recipe.html', context)


def search(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(title__icontains=query)
    else:
        recipes = Recipe.objects.all()
    categories = Recipe.CATEGORY_CHOICES
    context = {
        'recipes': recipes,
        'query': query,
        'categories': categories,
    }
    return render(request, 'ffe/search_results.html', context)


def category_recipes(request, category):
    recipes = Recipe.objects.filter(category=category)
    categories = Recipe.CATEGORY_CHOICES
    context = {
        'recipes': recipes,
        'category': category,
        'categories': categories,
        'query': category  # Utilizziamo 'query' per riutilizzare lo stesso template di ricerca
    }
    return render(request, 'ffe/category_recipes.html', context)


@login_required(login_url="my-login")
def follow_user(request, username):
    # Trova l'utente da seguire
    user_to_follow = get_object_or_404(User, username=username)

    # Verifica se l'utente corrente sta già seguendo l'utente da seguire
    if Follower.objects.filter(user=user_to_follow, follower=request.user).exists():
        # Se già segue, smetti di seguire
        Follower.objects.filter(user=user_to_follow, follower=request.user).delete()
    else:
        # Altrimenti, aggiungi un nuovo follow
        Follower.objects.create(user=user_to_follow, follower=request.user)

    # Redirect alla pagina di dettaglio dell'utente seguito o a una pagina di conferma
    return redirect('user_detail', username=username)


@login_required(login_url="my-login")
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        Follower.objects.filter(user=user_to_unfollow, follower=request.user).delete()
    return redirect('user_detail', username=username)


def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=user)
    is_following = Follower.objects.filter(user=user, follower=request.user).exists() if request.user.is_authenticated else False
    context = {
        'user': user,
        'recipes': recipes.distinct(),
        'num_recipes': recipes.count(),
        'is_following': is_following,
    }
    return render(request, 'ffe/user_detail.html', context)


@login_required
def profile(request):
    categories = Recipe.CATEGORY_CHOICES  # Ottieni le categorie
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'form': form,
        'categories': categories,  # Aggiungi le categorie al contesto
    }
    return render(request, 'ffe/profile.html', context)
