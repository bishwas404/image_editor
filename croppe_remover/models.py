from django.db import models
import uuid

class CroppedImage(models.Model):
  original_name=models.CharField(max_length=50)
  image=models.ImageField(upload_to='cropped/')
  unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  uploaded_at=models.DateTimeField(auto_now_add=True)
