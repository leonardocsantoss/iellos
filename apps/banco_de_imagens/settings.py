from django.conf import settings

BANCO_IMAGE_UPLOAD_DIR = getattr(settings, 'BANCO_IMAGE_UPLOAD_DIR', 'banco_de_imagem/')
