from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.clients.models import Client
from apps.clients.forms import ClientForm
from apps.portfolios.models import Project, Skill, Experience, Education
from apps.media_manager.models import PortfolioFile
from apps.core.views import is_staff_user

@login_required
@user_passes_test(is_staff_user)
def client_list_view(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    clients = Client.objects.all()
    if query:
        clients = clients.filter(name__icontains=query) | clients.filter(profession__icontains=query)
    if status_filter == 'published':
        clients = clients.filter(is_published=True)
    elif status_filter == 'draft':
        clients = clients.filter(is_published=False)
        
    return render(request, 'dashboard/clients/list.html', {
        'clients': clients,
        'query': query,
        'status_filter': status_filter
    })

@login_required
@user_passes_test(is_staff_user)
def client_create_view(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client profile for '{client.name}' created successfully.")
            return redirect('clients:client_detail', pk=client.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ClientForm()
        
    return render(request, 'dashboard/clients/form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
@user_passes_test(is_staff_user)
def client_detail_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    projects = client.projects.all()
    skills = client.skills.all()
    experiences = client.experiences.all()
    education = client.education.all()
    files = client.files.all()
    
    context = {
        'client': client,
        'projects': projects,
        'skills': skills,
        'experiences': experiences,
        'education': education,
        'files': files,
    }
    return render(request, 'dashboard/clients/detail.html', context)

@login_required
@user_passes_test(is_staff_user)
def client_edit_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client profile for '{client.name}' updated.")
            return redirect('clients:client_detail', pk=client.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ClientForm(instance=client)
        
    return render(request, 'dashboard/clients/form.html', {
        'form': form,
        'client': client,
        'action': 'Edit'
    })

@login_required
@user_passes_test(is_staff_user)
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client_name = client.name
        client.delete()
        messages.success(request, f"Client '{client_name}' and all associated portfolio data have been deleted.")
        return redirect('clients:client_list')
    return redirect('clients:client_detail', pk=pk)

@login_required
@user_passes_test(is_staff_user)
def client_toggle_publish_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.is_published = not client.is_published
        client.save()
        status_str = "published" if client.is_published else "unpublished"
        messages.success(request, f"Portfolio for {client.name} is now {status_str}.")
    return redirect(request.META.get('HTTP_REFERER', 'clients:client_list'))
