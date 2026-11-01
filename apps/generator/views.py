import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .services import generate_ui_code
from .models import Generation, Component
from .models import Generation, Component, Folder

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def workspace_view(request):
    return render(request, 'workspace.html')

@login_required
def generate_endpoint(request):
    """Generates UI and saves it to the Version History."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_prompt = data.get('prompt', '')
            
            if not user_prompt:
                return JsonResponse({'error': 'Please provide a prompt.'}, status=400)
                
            generated_html = generate_ui_code(user_prompt)
            
            # Save to history database
            Generation.objects.create(
                user=request.user,
                prompt=user_prompt,
                html_code=generated_html
            )
            
            return JsonResponse({'success': True, 'html_code': generated_html})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@login_required
def get_history(request):
    """Fetches the user's latest 10 generations."""
    history = Generation.objects.filter(user=request.user)[:10]
    data = [{'id': h.id, 'prompt': h.prompt, 'code': h.html_code, 'date': h.created_at.strftime("%b %d, %H:%M")} for h in history]
    return JsonResponse({'history': data})

@login_required
def save_component(request):
    """Saves a generated code block to the Library."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Component.objects.create(
                user=request.user,
                name=data.get('name', 'Untitled Component'),
                html_code=data.get('code', ''),
                category="Generated UI"
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=405)

@login_required
def get_library(request):
    """Fetches the user's saved components."""
    components = Component.objects.filter(user=request.user)
    data = [{'id': c.id, 'name': c.name, 'category': c.category, 'code': c.html_code} for c in components]
    return JsonResponse({'components': data})
@login_required
def create_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            folder_name = data.get('name', 'New Folder')
            Folder.objects.create(user=request.user, name=folder_name)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=405)
@login_required
def get_library(request):
    folders = Folder.objects.filter(user=request.user)
    components = Component.objects.filter(user=request.user, folder__isnull=True)

    folder_data = [{'id': f.id, 'name': f.name} for f in folders]
    comp_data = [{'id': c.id, 'name': c.name, 'category': c.category, 'code': c.html_code} for c in components]

    return JsonResponse({'folders': folder_data, 'components': comp_data})