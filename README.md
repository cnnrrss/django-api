# Django API

A forum-like app to dive deeper into Django


### Mess around in development

```python
from django.db import models
from forum_api.models import User, Topic, Post
from forum_api.serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

u = User(id=1)
u.save()

t = Topic(title="AI")
t.save()

post = Post(title="What about ChatGPT?", 
            content="...", 
            topic=t, 
            user=u)
post.save()

serializer = PostSerializer(post)
serializer.data
# TODO: should print but doesn't 
# # {'id': 1, 'title': 'What about...'}

content = JSONRenderer().render(serializer.data)
content
# b'{"id": 1, ...}'

# Deserialization is similar. First we parse a stream into Python native datatypes...
import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = PostSerializer(data=data)
serializer.is_valid()
# True

serializer.validated_data
# OrderedDict([('title', '...')])

serializer.save()
# <Snippet: Snippet object>
```

#### Notes:
Function based views, class based views, mixins, 