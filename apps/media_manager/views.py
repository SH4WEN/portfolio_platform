from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from apps.media_manager.models import PortfolioFile
from apps.media_manager.forms import PortfolioFileUploadForm, PortfolioFileReplaceForm
from apps.media_manager.validators import validate_file_upload
from apps.media_manager.services import upload_to_cloudinary, delete_from_cloudinary, generate_private_download_url
from apps.clients.models import Client
from apps.portfolios.models import Project
from apps.core.views import is_staff_user


@login_required
@user_passes_test(is_staff_user)
def file_list_view(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    visibility_filter = request.GET.get('visibility', '').strip()
    client_filter = request.GET.get('client_id', '').strip()

    files = PortfolioFile.objects.select_related('client', 'project').all()

    if query:
        files = files.filter(display_title__icontains=query) | files.filter(original_filename__icontains=query)
    if category_filter:
        files = files.filter(category=category_filter)
    if visibility_filter:
        files = files.filter(visibility=visibility_filter)
    if client_filter and client_filter.isdigit():
        files = files.filter(client_id=int(client_filter))

    clients = Client.objects.all()

    context = {
        'files': files,
        'clients': clients,
        'query': query,
        'category_filter': category_filter,
        'visibility_filter': visibility_filter,
        'client_filter': client_filter,
    }
    return render(request, 'dashboard/files/list.html', context)


@login_required
@user_passes_test(is_staff_user)
def file_upload_view(request):
    client_id = request.GET.get('client_id')
    initial = {}
    if client_id:
        initial['client'] = client_id

    if request.method == 'POST':
        form = PortfolioFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # Step 1: Server-side file validation
            try:
                validation_info = validate_file_upload(uploaded_file)
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'dashboard/files/upload.html', {'form': form})

            client = form.cleaned_data['client']
            project = form.cleaned_data.get('project')
            display_title = form.cleaned_data['display_title']
            category = form.cleaned_data['category']
            visibility = form.cleaned_data['visibility']

            # Step 2: Upload to Cloudinary
            try:
                cloudinary_res = upload_to_cloudinary(
                    file_obj=uploaded_file,
                    resource_type=validation_info['resource_type'],
                    visibility=visibility,
                    client_slug=client.slug
                )
            except Exception as e:
                messages.error(request, f"Cloudinary upload failed: {e}")
                return render(request, 'dashboard/files/upload.html', {'form': form})

            # Step 3: Atomic database record save & reference update
            try:
                with transaction.atomic():
                    file_record = PortfolioFile.objects.create(
                        client=client,
                        project=project,
                        display_title=display_title,
                        original_filename=uploaded_file.name,
                        category=category,
                        cloudinary_public_id=cloudinary_res['public_id'],
                        cloudinary_url=cloudinary_res['url'],
                        cloudinary_resource_type=cloudinary_res['resource_type'],
                        delivery_type=cloudinary_res['delivery_type'],
                        file_format=validation_info['file_format'],
                        verified_content_type=validation_info['verified_content_type'],
                        file_size=uploaded_file.size,
                        visibility=visibility
                    )

                    # Update Client profile image if category is profile_image
                    if category == 'profile_image':
                        client.profile_image_url = cloudinary_res['url']
                        client.save(update_fields=['profile_image_url'])

                    # Update Project featured image if project is selected & category is project_image
                    if category == 'project_image' and project:
                        project.featured_image_url = cloudinary_res['url']
                        project.save(update_fields=['featured_image_url'])

                messages.success(request, f"File '{display_title}' uploaded successfully.")
                return redirect('media_manager:file_list')

            except Exception as e:
                # Rollback Cloudinary asset if DB fails
                delete_from_cloudinary(
                    cloudinary_res['public_id'],
                    resource_type=cloudinary_res['resource_type'],
                    delivery_type=cloudinary_res['delivery_type']
                )
                messages.error(request, f"Database transaction failed: {e}")
                return render(request, 'dashboard/files/upload.html', {'form': form})
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = PortfolioFileUploadForm(initial=initial)

    return render(request, 'dashboard/files/upload.html', {'form': form})


@login_required
@user_passes_test(is_staff_user)
def file_replace_view(request, pk):
    file_record = get_object_or_404(PortfolioFile, pk=pk)

    if request.method == 'POST':
        form = PortfolioFileReplaceForm(request.POST, request.FILES)
        if form.is_valid():
            new_title = form.cleaned_data.get('display_title')
            new_visibility = form.cleaned_data.get('visibility')
            new_file = request.FILES.get('file')

            if new_title:
                file_record.display_title = new_title
            
            if new_visibility and new_visibility != file_record.visibility:
                file_record.visibility = new_visibility

            if new_file:
                # Validate & upload new file
                try:
                    validation_info = validate_file_upload(new_file)
                    cloudinary_res = upload_to_cloudinary(
                        file_obj=new_file,
                        resource_type=validation_info['resource_type'],
                        visibility=file_record.visibility,
                        client_slug=file_record.client.slug
                    )
                except Exception as e:
                    messages.error(request, f"Upload error: {e}")
                    return render(request, 'dashboard/files/replace.html', {'form': form, 'file_record': file_record})

                # Delete old Cloudinary asset
                old_public_id = file_record.cloudinary_public_id
                old_resource_type = file_record.cloudinary_resource_type
                old_delivery_type = file_record.delivery_type

                file_record.original_filename = new_file.name
                file_record.cloudinary_public_id = cloudinary_res['public_id']
                file_record.cloudinary_url = cloudinary_res['url']
                file_record.cloudinary_resource_type = cloudinary_res['resource_type']
                file_record.delivery_type = cloudinary_res['delivery_type']
                file_record.file_format = validation_info['file_format']
                file_record.verified_content_type = validation_info['verified_content_type']
                file_record.file_size = new_file.size

                file_record.save()
                delete_from_cloudinary(old_public_id, resource_type=old_resource_type, delivery_type=old_delivery_type)
            else:
                file_record.save()

            messages.success(request, f"File '{file_record.display_title}' updated.")
            return redirect('media_manager:file_list')
    else:
        form = PortfolioFileReplaceForm(initial={
            'display_title': file_record.display_title,
            'visibility': file_record.visibility,
        })

    return render(request, 'dashboard/files/replace.html', {'form': form, 'file_record': file_record})


@login_required
@user_passes_test(is_staff_user)
def file_toggle_visibility_view(request, pk):
    file_record = get_object_or_404(PortfolioFile, pk=pk)
    if request.method == 'POST':
        file_record.visibility = 'public' if file_record.visibility == 'private' else 'private'
        file_record.save(update_fields=['visibility'])
        messages.success(request, f"File '{file_record.display_title}' visibility changed to '{file_record.visibility}'.")
    return redirect(request.META.get('HTTP_REFERER', 'media_manager:file_list'))


@login_required
@user_passes_test(is_staff_user)
def file_delete_view(request, pk):
    file_record = get_object_or_404(PortfolioFile, pk=pk)
    if request.method == 'POST':
        public_id = file_record.cloudinary_public_id
        res_type = file_record.cloudinary_resource_type
        del_type = file_record.delivery_type
        title = file_record.display_title
        url = file_record.cloudinary_url

        # Check references & clean up client/project image URLs
        if file_record.client and file_record.client.profile_image_url == url:
            file_record.client.profile_image_url = ''
            file_record.client.save(update_fields=['profile_image_url'])

        if file_record.project and file_record.project.featured_image_url == url:
            file_record.project.featured_image_url = ''
            file_record.project.save(update_fields=['featured_image_url'])

        file_record.delete()
        delete_from_cloudinary(public_id, resource_type=res_type, delivery_type=del_type)

        messages.success(request, f"File '{title}' deleted safely.")
    return redirect('media_manager:file_list')


@login_required
@user_passes_test(is_staff_user)
def private_file_download_view(request, pk):
    file_record = get_object_or_404(PortfolioFile, pk=pk)

    # Security check: verify staff user authentication
    if not request.user.is_staff:
        raise Http404("Unauthorized")

    signed_url = generate_private_download_url(file_record)
    return redirect(signed_url)
