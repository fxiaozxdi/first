from django.core.cache import cache

from . import models


def getAllArticle(ischange=False):
    '''
    缓存查询首页所有文章
    :return:
    '''
    print("开始查询缓存中的数据")
    articles = cache.get("allArticle")
    if articles is None or ischange:
        print("缓存中没有数据，开始查询数据库……")
        articles = models.Article.objects.all()
        print("数据库中查询到数据，同步到缓存中")
        cache.set("allArticle", articles)
    print("缓存中存在数据，不进行查询")
    return articles