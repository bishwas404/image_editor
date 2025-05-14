from django.shortcuts import render, redirect
import uuid,os
from django.core.files.base import ContentFile
from .models import CroppedImage
from django.http import JsonResponse,HttpResponseForbidden,FileResponse
from rembg import remove
from PIL import Image
import io
import base64


def upload_view(request):
  return render(request,'croppe_remover/upload.html')

def crop_image_view(request):
    if request.method == "POST":
        blob = request.FILES.get('cropped_image')
        if blob:
            original_name = blob.name
            unique_id = uuid.uuid4()

            filename = f'{unique_id}.png'
            image = CroppedImage.objects.create(
                original_name=original_name,
                image=ContentFile(blob.read(), name=filename),
                unique_id=unique_id
            )

            return JsonResponse({'redirect_url': f'/result/{image.id}/{unique_id}/'})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def remove_background_view(request):
    if request.method=="POST":
        data=request.FILES.get('cropped_image')
        image_bytes = data.read()
        input_image=Image.open(io.BytesIO(image_bytes)).convert("RGBA")

        output_image=remove(input_image)

        image_io=io.BytesIO()
        output_image.save(image_io,format='PNG')
        image_io.seek(0)
        original_name = data.name
        image_uuid=uuid.uuid4()
        filename=f'{image_uuid}.png'

        image=CroppedImage.objects.create(
            original_name=original_name,
            image=ContentFile(image_io.read(),name=filename),
            unique_id=image_uuid
        )
        return JsonResponse({'redirect_url': f'/result/{image.id}/{image.unique_id}/'})

    return JsonResponse({'error':'Invalid request'},status=400)


def result_view(request, image_id, unique_id):
    try:
        image_obj = CroppedImage.objects.get(id=image_id, unique_id=unique_id)
    except CroppedImage.DoesNotExist:
        return HttpResponseForbidden("Unauthorized access")

    return render(request, 'croppe_remover/result.html', {'image': image_obj})

def download_image(request,image_id,unique_id):
    try:
        image_obj = CroppedImage.objects.get(id=image_id, unique_id=unique_id)
    except CroppedImage.DoesNotExist:
        return HttpResponseForbidden("Unauthorized access")

    file_path = image_obj.image.path
    filename = os.path.basename(file_path)

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)


