from django.db import models


class UserManager(models.Manager):
    def get_by_name(self, name):
        return self.get(name=name)


class User(models.Model):
    id = models.UUIDField
    email = models.EmailField
    # name = models.CharField(max_length=50, unique=True, error_messages={
    #     'unique': "This value is not unique, please try a different one."
    # })

    objects = UserManager()

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["name"],
    #             name="unique_name",
    #         ),
    #     ]


class Comments(models.Model):
    """
    A ForeignObject, is a more flexible way of defining a foreign key relationship.
    It allows you to customize the way the foreign key relationship is handled.
    For example, you can use a ForeignObject to define a relationship where the
    foreign key is not on the primary key of the target model.
    You can also use it to define a relationship with a non-integer primary key.
    """

    title = models.CharField(max_length=240)
    content = models.CharField(max_length=500)
    author_name = models.CharField(max_length=50)

    # ERROR
    #     if name.startswith('"') and name.endswith('"'):
    # AttributeError: 'NoneType' object has no attribute 'startswith'

    # author = models.ForeignObject(
    #     User,
    #     on_delete=models.CASCADE,
    #     from_fields=['author_name'],
    #     to_fields=['name']
    # )


class Tag(models.Model):
    name = models.CharField(max_length=50)


# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=50)
    subTitle = models.CharField(max_length=50)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
    )
    subscribed = models.DateTimeField()
    Notifications = models.BooleanField()


