
imgExt= ['.JPG','.PNG','.GIF','.WEBP','.TIFF','.PSD','.RAW','.BMP','.HEIF','.INDD','SVG']
vidExt= ['.WEBM','.MPG','.MP2','.MPEG','.MPE','.MPV','.OGG','.MP4','.M4P','.M4V','.AVI','.WMV','.MOV','.QT','.FLV','.SWF','.AVCHD']

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = imgExt+vidExt
    if not ext.upper() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def media_type(ext)
    if ext.upper() in imgExt:
        return 'image'
    else if ext.upper() in vidExt: 
        return 'video'
    else:
        return 'unknown'
