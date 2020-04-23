from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from main.models import Post

posts = Index('posts')


@registry.register_document
class PostDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'posts'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
    class Django:
        model = Post

        fields = [
            'text',
        ]
