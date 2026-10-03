from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.clients.models import Client
from apps.portfolios.models import Project
from apps.media_manager.models import PortfolioFile

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('core:dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', 'core:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Access restricted to administrators.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'dashboard/login.html', {'form': form})

@login_required
@user_passes_test(is_staff_user)
def admin_logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('core:login')

@login_required
@user_passes_test(is_staff_user)
def dashboard_overview(request):
    total_clients = Client.objects.count()
    published_clients = Client.objects.filter(is_published=True).count()
    total_projects = Project.objects.count()
    total_files = PortfolioFile.objects.count()
    
    recent_clients = Client.objects.order_by('-created_at')[:5]
    recent_files = PortfolioFile.objects.select_related('client').order_by('-uploaded_at')[:5]
    
    context = {
        'total_clients': total_clients,
        'published_clients': published_clients,
        'total_projects': total_projects,
        'total_files': total_files,
        'recent_clients': recent_clients,
        'recent_files': recent_files,
    }
    return render(request, 'dashboard/overview.html', context)
