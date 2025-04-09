from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, NoteForm  # Updated to use our custom forms
from .models import Note, User  # Added User import
from django.contrib.auth import logout 


def signup_login(request):
    # Initialize our custom forms instead of Django's default ones
    signup_form = SignUpForm()
    login_form = LoginForm()
    login_error = None

    if request.method == 'POST':
        # Handling signup
        if 'signup' in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, 'Account created and logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Error creating account')
                # Show signup form with errors and hide login form
                return render(request, 'notes/signup_login.html', {
                    'signup_form': signup_form,
                    'login_form': LoginForm(),  # Fresh login form
                    'show_signup': True  # Add this to control which form is visible
                })

        # Handling login
        elif 'login' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('your_notes')
            else:
                login_error = "Invalid username or password"
                # Show login form with errors and hide signup form
                return render(request, 'notes/signup_login.html', {
                    'login_form': login_form,
                    'signup_form': SignUpForm(),  # Fresh signup form
                    'login_error': login_error,
                    'show_signup': False  # Add this to control which form is visible
                })

    # Default GET request handling
    return render(request, 'notes/signup_login.html', {
        'signup_form': signup_form,
        'login_form': login_form,
        'show_signup': False  # By default, show login form first
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('signup_login')  # Redirecting to combined signin/signup page


# All your existing note-related views remain exactly the same
@login_required
def home(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('home')
    else:
        form = NoteForm()
    notes = Note.objects.filter(user=request.user)
    return render(request, 'notes/home.html', {'form': form, 'notes': notes})


@login_required
def your_notes(request):
    form = NoteForm()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('saved_notes')

    query = request.GET.get('q', '')
    if query:
        notes = Note.objects.filter(user=request.user, title__icontains=query)
    else:
        notes = Note.objects.filter(user=request.user)

    return render(request, 'notes/home.html', {'form': form, 'notes': notes})


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('saved_notes')  # Redirecting to saved_notes page after deletion


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('saved_notes')  # Redirecting to saved_notes page after update
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/edit_note.html', {'form': form, 'note': note})


@login_required
@login_required
def saved_notes(request):
    query = request.GET.get("q", "")
    sort_by = request.GET.get('sort', 'recent')  # Ensure it's always defined

    notes = Note.objects.filter(user=request.user)

    # Search logic
    if query:
        if len(query) == 1:
            notes = notes.filter(title__istartswith=query)
        else:
            notes = notes.filter(title__icontains=query)

        if not notes.exists():
            messages.info(request, "Word not found")  # Feedback when no match
            notes = Note.objects.none()  # Return empty queryset

    # Sorting logic
    if sort_by == 'recent':
        notes = notes.order_by('-created_at')
    elif sort_by == 'last_written':
        notes = notes.order_by('created_at')

    return render(request, 'notes/saved_notes.html', {'notes': notes})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
            else:
                return render(request, 'auth.html', {
                    'login_form': form,
                    'login_error': 'Invalid username or password',
                    'signup_form': UserCreationForm()
                })
        else:
            return render(request, 'auth.html', {
                'login_form': form,
                'login_error': 'Please correct the errors below',
                'signup_form': UserCreationForm()
            })
    else:
        return render(request, 'auth.html', {
            'login_form': AuthenticationForm(),
            'signup_form': UserCreationForm()
        }) 


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login?signup_success=true')
        else:
            return render(request, 'auth.html', {
                'signup_form': form,
                'login_form': AuthenticationForm()
            })
    else:
        return redirect('login')
