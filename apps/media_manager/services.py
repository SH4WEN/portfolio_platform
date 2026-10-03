import uuid
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Try importing cloudinary SDK
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.utils
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False


def is_cloudinary_configured():
    return (
        CLOUDINARY_AVAILABLE and
        bool(settings.CLOUDINARY_CLOUD_NAME) and
        bool(settings.CLOUDINARY_API_KEY) and
        bool(settings.CLOUDINARY_API_SECRET)
    )


def configure_cloudinary():
    if is_cloudinary_configured():
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )


def upload_to_cloudinary(file_obj, resource_type='image', visibility='private', client_slug='client'):
    """
    Uploads a file to Cloudinary with unpredictable public IDs and returns upload metadata.
    Falls back to mock/demo URL if Cloudinary is not configured (e.g. in test environment).
    """
    unique_id = uuid.uuid4().hex
    public_id = f"portfolios/{client_slug}/{unique_id}"
    
    # Determine Cloudinary delivery type based on visibility
    # For private files, delivery type can be 'authenticated' or 'private'
    delivery_type = 'upload' if visibility == 'public' else 'authenticated'

    if is_cloudinary_configured():
        configure_cloudinary()
        file_obj.seek(0)
        options = {
            'public_id': public_id,
            'resource_type': resource_type,
            'type': delivery_type,
            'overwrite': True,
        }
        
        # Perform Cloudinary upload
        res = cloudinary.uploader.upload(file_obj, **options)
        file_obj.seek(0)
        
        return {
            'public_id': res.get('public_id', public_id),
            'url': res.get('secure_url') or res.get('url', ''),
            'resource_type': res.get('resource_type', resource_type),
            'delivery_type': res.get('type', delivery_type),
            'format': res.get('format', ''),
        }
    else:
        # Fallback for testing / dev without Cloudinary API credentials
        file_obj.seek(0)
        ext = os.path.splitext(file_obj.name)[1].lstrip('.').lower()
        mock_url = f"https://res.cloudinary.com/demo/{resource_type}/{delivery_type}/{public_id}.{ext}"
        return {
            'public_id': public_id,
            'url': mock_url,
            'resource_type': resource_type,
            'delivery_type': delivery_type,
            'format': ext,
        }


def delete_from_cloudinary(public_id, resource_type='image', delivery_type='upload'):
    """
    Safely deletes a file from Cloudinary.
    """
    if not public_id:
        return True
        
    if is_cloudinary_configured():
        try:
            configure_cloudinary()
            res = cloudinary.uploader.destroy(
                public_id,
                resource_type=resource_type,
                type=delivery_type,
                invalidate=True
            )
            return res.get('result') == 'ok'
        except Exception as e:
            logger.error(f"Failed to delete Cloudinary asset {public_id}: {e}")
            return False
    return True


def generate_private_download_url(file_obj, expires_in_seconds=300):
    """
    Generates a short-lived signed Cloudinary URL for authorized private file access.
    """
    if is_cloudinary_configured():
        configure_cloudinary()
        try:
            # Cloudinary signed URL generation for private/authenticated asset
            url, options = cloudinary.utils.cloudinary_url(
                file_obj.cloudinary_public_id,
                resource_type=file_obj.cloudinary_resource_type,
                type=file_obj.delivery_type,
                format=file_obj.file_format,
                sign_url=True,
                expires_at=int(cloudinary.utils.now()) + expires_in_seconds,
                flags="attachment" # Force download behavior
            )
            return url
        except Exception as e:
            logger.error(f"Failed to generate signed URL for {file_obj.cloudinary_public_id}: {e}")
            return file_obj.cloudinary_url
    return file_obj.cloudinary_url
