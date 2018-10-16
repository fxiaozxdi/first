from django.conf.urls import url

from . import views

urlpatterns = [
    # 关于用户操作的路由
    url(r"^$", views.index),
    url(r"^index/$", views.index, name="index"),
    url(r"^add_user/$", views.add_user, name="add_user"),
    # url(r"^delete_user/$", views.delete_user, name="delete_user"),
    # url(r"^(\d+)delete_user/$", views.delete_user, name="delete_user"),
    #\d代表匹配任意一个字符，/d无意义
    url(r"^delete_user/(?P<user_id>\d+)/$", views.delete_user, name="delete_user"),
    url(r"^list_user/$", views.list_user, name="list_user"),
    url(r"^reg/$", views.reg, name="reg"),
    url(r"^show/(\d+)/$", views.show, name="show"),
    # url(r"^(?P<u_id>\d+)/show/$", views.show, name="show"),
    url(r"^(?P<u_id>\d+)/update/$", views.update, name="update"),
    url(r"^update_pwd/$", views.update_pwd, name="update_pwd"),
    # url(r"^update_header/$", views.update_header, name="update_header"),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),

    # 文章操作的路由
    url(r"^add_article/$", views.add_article, name="add_article"),
    url(r"^(?P<a_id>\d+)/delete_article/$", views.delete_article, name="delete_article"),
    url(r"^(?P<a_id>\d+)/update_article/$", views.update_article, name="update_article"),
    url(r"^(?P<a_id>\d+)/show_article/$", views.show_article, name="show_article"),
    url(r"^show_all_articles/$", views.show_all_articles, name="show_all_articles"),

    url(r"^code/$", views.code, name="code"),
    url(r"^ajax_hello/$", views.ajax_hello, name="ajax_hello"),
]
