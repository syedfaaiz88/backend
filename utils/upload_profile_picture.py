import os
from django.conf import settings
from django.core.files.storage import default_storage

def upload_profile_picture(user, profile_picture):
    try:
        # Define the folder path for storing the user's profile picture
        user_folder = f"user_{user.id}/profile_picture/"
        folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)

        # Ensure the directory exists
        os.makedirs(folder_path, exist_ok=True)

        # Define the file path and save the image
        image_name = f"profile_{user.id}.jpg"  # You can modify the naming convention as needed
        image_path = os.path.join(folder_path, image_name)

        # Save the image using Django's default storage system
        with default_storage.open(image_path, 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)

        # Return the relative media path for the image
        return f"{user_folder}{image_name}"
    except Exception as e:
        raise Exception(f"Error while uploading the image: {str(e)}")
