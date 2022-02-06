from django.utils.text import slugify


def get_upload_path(instance, filename):
    """slugify filenames and put them in a directory named 'class_name'"""
    filename, dot, extension = filename.rpartition('.')
    return '{}/{}.{}'.format(
        instance.__class__.__name__.lower(),
        slugify(filename), extension)
