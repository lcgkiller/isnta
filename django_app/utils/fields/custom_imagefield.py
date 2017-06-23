# FieldFile을 오버라이드 (이미지가 없을 때를 대비)
from django.db.models.fields.files import ImageFieldFile, ImageField


class CustomImageFieldFile(ImageFieldFile):
    @property
    def url(self):
        try:
            return super().url
        except ValueError:
            # ValueError가 일어날 때만 staticfiles_storage를 불러온다.
            from django.contrib.staticfiles.storage import staticfiles_storage
            return staticfiles_storage.url(self.field.static_image_path)

            # return '/static/images/unknown.jpg' # 이렇게 쓰는 법은 좋지 않다.


class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile #

    def __init__(self, *args, **kwargs):

        # 키워드 인자를 pop을 통해 없애버린다.
        self.static_image_path = kwargs.pop('default_static_image', 'images/no_image.png')
        super().__init__(*args, **kwargs)
