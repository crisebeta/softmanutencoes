from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Primeiro salva o perfil
        super().save(*args, **kwargs)
        
        # Depois trata a imagem
        try:
            if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
        except Exception as e:
            # Se houver erro com a imagem, definir uma imagem padrão válida
            self.image = 'default.jpg'
            if not kwargs.get('update_fields'):
                super().save(update_fields=['image'])

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # Verifica se já existe um perfil
            Profile.objects.get(user=instance)
        except Profile.DoesNotExist:
            # Se não existe, cria um novo
            Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Se o perfil não existe, cria um novo
        Profile.objects.create(user=instance)
