from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.contrib import messages
from apps.clients.models import Client
from apps.portfolios.models import Project, Skill, Experience, Education
from apps.portfolios.forms import ProjectForm, SkillForm, ExperienceForm, EducationForm
from apps.core.views import is_staff_user

def public_portfolio_view(request, slug):
    preview_mode = request.GET.get('preview', 'false').lower() == 'true' and request.user.is_staff
    
    if preview_mode:
        client = get_object_or_404(Client, slug=slug)
    else:
        client = get_object_or_404(Client, slug=slug, is_published=True)
    
    projects = client.projects.filter(is_published=True) if not preview_mode else client.projects.all()
    skills = client.skills.all()
    experiences = client.experiences.all()
    education = client.education.all()
    
    # Public files filter
    public_files = client.files.filter(visibility='public')
    certificates = public_files.filter(category='certificate')
    resumes = public_files.filter(category='resume')
    other_docs = public_files.filter(category__in=['document', 'other'])
    
    # Categorize skills
    skills_by_category = {}
    for skill in skills:
        cat = skill.category or 'General'
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)

    # Contact payload consumed by the public template's "Save Contact" button.
    # Rendered via json_script and used on the client side to build a vCard
    # (.vcf) that the visitor's device imports directly into its Contacts app.
    client_contact = {
        'slug': client.slug,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'profession': client.profession,
        'location': client.location,
        'headline': client.headline,
        'social_links': {
            'github': client.github_url,
            'linkedin': client.linkedin_url,
            'twitter': client.twitter_url,
            'instagram': client.instagram_url,
            'facebook': client.facebook_url,
            'youtube': client.youtube_url,
            'tiktok': client.tiktok_url,
            'website': client.website_url,
        },
    }

    context = {
        'client': client,
        'client_contact': client_contact,
        'projects': projects,
        'skills_by_category': skills_by_category,
        'experiences': experiences,
        'education': education,
        'certificates': certificates,
        'resumes': resumes,
        'other_docs': other_docs,
        'preview_mode': preview_mode,
    }
    return render(request, 'public/portfolio.html', context)


# Project CRUD Views
@login_required
@user_passes_test(is_staff_user)
def project_create_view(request):
    client_id = request.GET.get('client_id')
    initial = {}
    if client_id:
        initial['client'] = client_id

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' created.")
            return redirect('clients:client_detail', pk=project.client.pk)
    else:
        form = ProjectForm(initial=initial)

    return render(request, 'dashboard/portfolios/project_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(is_staff_user)
def project_edit_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, f"Project '{project.title}' updated.")
            return redirect('clients:client_detail', pk=project.client.pk)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/portfolios/project_form.html', {'form': form, 'project': project, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff_user)
def project_delete_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    client_pk = project.client.pk
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' deleted.")
    return redirect('clients:client_detail', pk=client_pk)


# Skill CRUD Views
@login_required
@user_passes_test(is_staff_user)
def skill_create_view(request):
    client_id = request.GET.get('client_id')
    initial = {}
    if client_id:
        initial['client'] = client_id

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Skill '{skill.name}' added.")
            return redirect('clients:client_detail', pk=skill.client.pk)
    else:
        form = SkillForm(initial=initial)

    return render(request, 'dashboard/portfolios/skill_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_staff_user)
def skill_edit_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save()
            messages.success(request, f"Skill '{skill.name}' updated.")
            return redirect('clients:client_detail', pk=skill.client.pk)
    else:
        form = SkillForm(instance=skill)

    return render(request, 'dashboard/portfolios/skill_form.html', {'form': form, 'skill': skill, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff_user)
def skill_delete_view(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    client_pk = skill.client.pk
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        messages.success(request, f"Skill '{name}' deleted.")
    return redirect('clients:client_detail', pk=client_pk)


# Experience CRUD Views
@login_required
@user_passes_test(is_staff_user)
def experience_create_view(request):
    client_id = request.GET.get('client_id')
    initial = {}
    if client_id:
        initial['client'] = client_id

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save()
            messages.success(request, f"Experience at '{exp.company}' added.")
            return redirect('clients:client_detail', pk=exp.client.pk)
    else:
        form = ExperienceForm(initial=initial)

    return render(request, 'dashboard/portfolios/experience_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_staff_user)
def experience_edit_view(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            exp = form.save()
            messages.success(request, f"Experience at '{exp.company}' updated.")
            return redirect('clients:client_detail', pk=exp.client.pk)
    else:
        form = ExperienceForm(instance=exp)

    return render(request, 'dashboard/portfolios/experience_form.html', {'form': form, 'experience': exp, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff_user)
def experience_delete_view(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    client_pk = exp.client.pk
    if request.method == 'POST':
        company = exp.company
        exp.delete()
        messages.success(request, f"Experience at '{company}' deleted.")
    return redirect('clients:client_detail', pk=client_pk)


# Education CRUD Views
@login_required
@user_passes_test(is_staff_user)
def education_create_view(request):
    client_id = request.GET.get('client_id')
    initial = {}
    if client_id:
        initial['client'] = client_id

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save()
            messages.success(request, f"Education at '{edu.institution}' added.")
            return redirect('clients:client_detail', pk=edu.client.pk)
    else:
        form = EducationForm(initial=initial)

    return render(request, 'dashboard/portfolios/education_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_staff_user)
def education_edit_view(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            edu = form.save()
            messages.success(request, f"Education at '{edu.institution}' updated.")
            return redirect('clients:client_detail', pk=edu.client.pk)
    else:
        form = EducationForm(instance=edu)

    return render(request, 'dashboard/portfolios/education_form.html', {'form': form, 'education': edu, 'action': 'Edit'})


@login_required
@user_passes_test(is_staff_user)
def education_delete_view(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    client_pk = edu.client.pk
    if request.method == 'POST':
        inst = edu.institution
        edu.delete()
        messages.success(request, f"Education at '{inst}' deleted.")
    return redirect('clients:client_detail', pk=client_pk)
