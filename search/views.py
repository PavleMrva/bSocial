from django.shortcuts import render
from elasticsearch_dsl.query import MultiMatch

from search.documents import PostDocument


def search(request):
    q = request.GET.get('q')

    if q:
        query = MultiMatch(query=q,  fields=['text'])
        posts = PostDocument.search().query(query)
    else:
        posts = ''
    return render(request, 'search/search.html', {'posts': posts})
