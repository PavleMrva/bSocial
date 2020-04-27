from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from main.models import Post, User, Comment
from elasticsearch_dsl import analyzer, tokenizer

posts = Index('posts')

@registry.register_document
class PostDocument(Document):
    # user = fields.ObjectField(properties={
    #     'first_name': fields.TextField(),
    #     'last_name': fields.TextField(),
    #     'username': fields.TextField(),
    #     'email': fields.TextField(),
    # })
    # comment = fields.NestedField(properties={
    #     'text': fields.TextField(),
    # })

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
            'created_at',
        ]
    #     related_models = [User, Comment]
    #
    # def get_queryset(self):
    #     return super().get_queryset().select_related(
    #         'user'
    #     )
    #
    # def get_instances_from_related(self, related_instance):
    #     if isinstance(related_instance, User):
    #         return related_instance..all()
    #     elif isinstance(related_instance, Comment):
    #         return related_instance.post