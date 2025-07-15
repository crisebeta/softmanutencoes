from django.core.management.base import BaseCommand
from django.conf import settings
import shutil
import os

class Command(BaseCommand):
    help = 'Configura a imagem padrão do perfil'

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        default_image_path = os.path.join(media_root, 'default.jpg')
        
        # Certifique-se de que o diretório media existe
        os.makedirs(media_root, exist_ok=True)
        
        # Copie a imagem padrão do diretório de recursos estáticos
        source_image = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'default.jpg')
        
        if os.path.exists(source_image):
            shutil.copy(source_image, default_image_path)
            self.stdout.write(self.style.SUCCESS('Imagem padrão configurada com sucesso'))
        else:
            self.stdout.write(self.style.ERROR('Arquivo de imagem padrão não encontrado')) 