from django.db.models import *
from users.models import CustomUser


class TimeStampMixin(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Memory(TimeStampMixin):
    title = CharField(max_length=100)
    date = DateField(null=True, blank=True)
    feeling = CharField(max_length=5, null=True, blank=True)
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='owner')
    locked = BooleanField(blank=True, null=True, default=False)
    body = TextField(null=True, blank=True)
    members = ManyToManyField(CustomUser, blank=True)

    class Meta:
        verbose_name_plural = 'memories'

    # def first_three_comments(self):
    #     return self.comments.all().order_by('-created_at')[:3]

    def get_number_of_comments(self):
        return 5

    def __str__(self):
        return self.title


class Image(Model):
    memory = ForeignKey(Memory, on_delete=CASCADE, related_name='images')
    src = ImageField(upload_to='memories/', )

    def __str__(self):
        return self.src.name


class Comment(TimeStampMixin):
    memory = ForeignKey(Memory, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='comments')
    image = ImageField(upload_to='memories/comments/', blank=True, null=True)
    gif = URLField(blank=True, null=True)
    body = TextField(blank=True, null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author.username)
