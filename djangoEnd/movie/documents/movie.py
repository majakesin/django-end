from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

from ..models import Movie

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="whitespace",
    filter=[ "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class MovieDocument(Document):
    id = fields.IntegerField(attr='id')

    title = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(),
        }
    )

    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(),
        }
    )

    class Django(object):
        model = Movie
