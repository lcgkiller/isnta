from django.db import models

__all__ = (
    'Video',
)
class VideoManager(models.Manager):
    def create_from_search_result(self, result):
        """
        :param result: Youtube Search API 사용후, 검색 결과에서
        :return: Video object
        """
        youtube_id = result['id']['videoId']
        title = result['snippet']['title']
        thumbnails = result['snippet']['thumbnails']['high']['url']
        description = result['snippet']['description']
        created_date = result['snippet']['publishedAt'].split('T')[0]
        # get_or_create를 이용해 youtube_id에 해당하는 데이터가 있으면 넘어가고, 없으면 생성
        video, video_created = self.get_or_create(
            youtube_id=youtube_id,
            defaults={
                'title': title,
                'description': description,
                'thumbnails': thumbnails,
                # 'created_date': created_date,
            }
        )
        print('Video({}) is {}'.format(
            video.title,
            'created' if video_created else 'already exist'
        ))

        return video


class Video(models.Model):
    youtube_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    thumbnails = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(blank=True, null=True)

    objects = VideoManager()

    def __str__(self):
        return self.title
