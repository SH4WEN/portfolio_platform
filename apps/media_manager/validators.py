import io
import os
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_DOC_EXTENSIONS = {'.pdf', '.doc', '.docx'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS.union(ALLOWED_DOC_EXTENSIONS)

MAX_IMAGE_SIZE_BYTES = getattr(settings, 'MAX_IMAGE_SIZE_MB', 5) * 1024 * 1024
MAX_DOC_SIZE_BYTES = getattr(settings, 'MAX_DOC_SIZE_MB', 10) * 1024 * 1024


def validate_file_upload(file):
    """
    Validates file extension, size, header magic bytes, and content.
    Returns dictionary with verified content_type, category, resource_type, and file_format.
    """
    if not file or file.size == 0:
        raise ValidationError("Uploaded file is empty.")

    filename = file.name or ''
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"File format '{ext}' is not supported. Allowed formats: JPG, JPEG, PNG, WebP, PDF, DOC, DOCX."
        )

    is_image = ext in ALLOWED_IMAGE_EXTENSIONS
    max_size = MAX_IMAGE_SIZE_BYTES if is_image else MAX_DOC_SIZE_BYTES

    if file.size > max_size:
        max_mb = getattr(settings, 'MAX_IMAGE_SIZE_MB', 5) if is_image else getattr(settings, 'MAX_DOC_SIZE_MB', 10)
        raise ValidationError(f"File size exceeds the {max_mb} MB limit.")

    # Read initial magic bytes safely
    file.seek(0)
    header = file.read(2048)
    file.seek(0)

    verified_type = None
    resource_type = 'image' if is_image else 'raw'

    if is_image:
        try:
            img = Image.open(file)
            img.verify()
            file.seek(0)
            
            # Re-open image after verify() to inspect format
            img = Image.open(file)
            fmt = (img.format or '').lower()
            file.seek(0)
            
            mime_map = {
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'png': 'image/png',
                'webp': 'image/webp',
            }
            verified_type = mime_map.get(fmt, f"image/{fmt}")
        except Exception as e:
            file.seek(0)
            raise ValidationError("File failed image verification or is corrupted.")
    else:
        # Document verification
        if ext == '.pdf':
            if not header.startswith(b'%PDF'):
                raise ValidationError("Invalid PDF file signature.")
            verified_type = 'application/pdf'
        elif ext == '.doc':
            # OLECF magic bytes for MS Office binary doc
            if not header.startswith(b'\xd0\xcf\x11\xe0'):
                raise ValidationError("Invalid Word document (.doc) structure.")
            verified_type = 'application/msword'
        elif ext == '.docx':
            # ZIP magic bytes PK\x03\x04
            if not header.startswith(b'PK\x03\x04'):
                raise ValidationError("Invalid Office OpenXML document (.docx) structure.")
            verified_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    file_format = ext.lstrip('.')
    
    return {
        'verified_content_type': verified_type,
        'resource_type': resource_type,
        'file_format': file_format,
        'is_image': is_image,
    }
