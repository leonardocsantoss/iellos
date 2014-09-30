# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename
from django.template.defaultfilters import slugify

from PIL import Image
import os, shutil


class SpecialCharFileSystemStorage(FileSystemStorage):
    """
    Remove Special Char filesystem storage
    """
    
    def get_valid_name(self, name):
        filename = slugify(get_valid_filename("".join(name.split('.')[:-1])))
        extension = name.split('.')[-1]
        return u"%s.%s" % (filename, extension)

    def _save(self, name, content):
        name = super(SpecialCharFileSystemStorage, self)._save(name, content)
        extension = name.split('.')[-1].lower()
        full_path = self.path(name)
        if extension == 'pdf':
            temp_path = u'%s~' % full_path
            shutil.copyfile(full_path, temp_path)
            os.popen("gs -dPDFSETTINGS=/prepress -dSAFER -dCompatibilityLevel=1.5 -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dGrayImageResolution=300 -dMonoImageResolution=600 -dColorImageResolution=150 -sOutputFile=%(full_path)s -c .setpdfwrite -f %(temp_path)s" % {'full_path': full_path, 'temp_path': temp_path, })
            os.remove(temp_path)
        elif extension in ('png', 'jpg', 'jpeg'):
            img = Image.open(full_path)
            width = 1024
            if img.size[1] > width:
                height = int((float(img.size[1])*float((width/float(img.size[0])))))
                img = img.resize((width,height), Image.ANTIALIAS)
                img.save(full_path)
        return name