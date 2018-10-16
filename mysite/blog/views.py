from io import BytesIO
import uuid

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import reverse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET,require_http_methods, require_POST,require_safe
from django.forms.models import model_to_dict
from django.core.serializers import serialize

from . import models
from . import utils
from . import cacheUtils


# 博客首页
def index(request):
    articles = cacheUtils.getAllArticle()
    return render(request, "blog/index.html", {"articles": articles})

# 添加用户
def add_user(request):
    return render(request, "blog/add_user.html", {})

# 删除用户
def delete_user(request, user_id):
    # u_id = request.GET["id"]
    user = models.User.objects.get(pk=user_id)
    user.delete()
    # return render(request, "blog/list_user.html", {})
    # return HttpResponseRedirect("/blog/list_user/")
    return redirect("/blog/list_user/")

# 查看所有用户列表
def list_user(request):
    users = models.User.objects.all()
    return render(request, "blog/list_user.html", {"users": users})


# 用户注册
def reg(request):
    if request.method == "GET":
        return render(request, "blog/add_user.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        # 接受参数
        try:
            username = request.POST["username"].strip()
            password = request.POST.get("password").strip()  # .getlist()
            confirmpwd = request.POST.get("confirmpwd").strip()
            nickname = request.POST.get("nickname", None)
            code = request.POST['code']
            avatar = request.FILES.get("avatar", 'static/img/headers/default.png')

            mycode = request.session['code']
            if code.upper() != mycode.upper():
                return render(request, "blog/add_user.html", {"msg": "验证码错误，请重新输入！"})
            # 删除session中的验证码
            del request.session['code']

            # 数据校验
            if len(username) < 1:
                return render(request, "blog/add_user.html", {"msg": "用户名称不能为空！！"})
            if len(password) < 6:
                return render(request, "blog/add_user.html", {"msg": "密码长度不能小于6位！！"})
            if password != confirmpwd:
                return render(request, "blog/add_user.html", {"msg": "两次密码不一致！！"})
            # 用户名称是否重复
            try:
                user = models.User.objects.get(name=username)
                return render(request, "blog/add_user.html", {"msg": "该用户名称已经存在，请重新填写！！"})
            except:
                # 保存数据
                password = utils.hmac_by_md5(password)

                user = models.User(name=username, password=password, nickname=nickname, header=avatar)
                user.save()
                return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})
        except:
            return render(request, "blog/add_user.html", {"msg": "对不起，用户名称不能为空！！"})


# 展示单个用户信息
def show(request, u_id):
    user =  models.User.objects.get(pk=u_id)
    return render(request, "blog/show.html", {"user": user})


# 修改用户信息
def update(request, u_id):
    if request.method == "GET":
        user = models.User.objects.filter(id=u_id).first()
        return render(request, "blog/update.html", {"user": user})
    else:
        nickname = request.POST["nickname"]
        age = request.POST["age"]

        # 数据校验
        if int(age) < 0:
            return render(request, "blog/update.html", {"msg": "好好在娘胎里待着，不要作妖"})
        if int(age) > 100:
            return render(request, "blog/update.html", {"msg": "年龄太大就安静一点吧"})

        # 修改数据
        # 获取用户
        user = models.User.objects.get(pk=u_id)
        # 修改数值
        user.age = age
        user.nickname = nickname
        # 保存
        user.save()

        return redirect("/blog/show/" + str(u_id) + "/")
        # return redirect("/blog/show", args(u_id, ))
        # return redirect(reverse("blog:show",args=(u_id,)))


# 修改用户密码
def update_pwd(request):
    if request.method == "GET":
        # 获取用户
        user = request.session['loginUser']
        return render(request, "blog/update_pwd.html", {"msg": "请正确填写修改信息！"}, {"user": user})
    elif request.method == "POST":
        # 获取输入信息
        oldpassword = request.POST["oldpassword"]
        oldpassword = utils.hmac_by_md5(oldpassword)
        password = request.POST['password'].strip()
        confirmpwd = request.POST['confirmpwd']

        # 获取用户
        user = request.session['loginUser']
        # 判断输入信息
        if oldpassword != user.password:
            return render(request, "blog/update_pwd.html", {"msg": "原密码输入错误，请重新输入！"})
        elif password != confirmpwd:
            return render(request, "blog/update_pwd.html", {"msg": "两次输入的密码不一致，请重新输入！"})
        else:
            # 密码加密并覆盖原密码
            password = utils.hmac_by_md5(password)
            user.password = password

            # 保存
            user.save()
            return redirect(reverse("blog:logout"))


# 修改用户头像
def update_header(request):
    # 获取用户
    user = request.session['loginUser']
    if request.method == "GET":
        return render(request, "blog/update_pwd.html", {"msg": "请正确填写修改信息！"}, {"user": user})
    elif request.method == "POST":
        avatar = request.FILES.get("avatar")

        # 覆盖原头像并保存
        user.header = avatar
        user.save()
        return render(request, "blog/show.html", {"msg": "对不起，用户名称不能为空！！"})


# 用户登录
def login(request):
    if request.method == "GET":
        return render(request, "blog/login.html", {"msg": "欢迎登录"})
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        code = request.POST['code']

        mycode = request.session['code']
        if code.upper() != mycode.upper():
            return render(request, "blog/login.html", {"msg": "验证码错误，请重新输入！"})
        # 删除session中的验证码
        del request.session['code']

        try:
            password = utils.hmac_by_md5(password)
            user = models.User.objects.get(name=username, password=password)
            # 使用session来记录用户的登录信息
            request.session["loginUser"] = user
            # 使用cookie记住用户名称
            response = redirect(reverse("blog:index"))
            # cookie不能存储中文
            response.set_cookie("username", user.name, max_age=3600 * 24 * 14)
            return response
        except:
            return render(request, "blog/login.html", {"msg": "账号密码错误，请重新输入！"})


# 用户退出
def logout(request):
    try:
        del request.session["loginUser"]
    finally:
        return redirect(reverse("blog:index"))


# 添加文章
def add_article(request):
    if request.method == "GET":
        return render(request, "blog/add_article.html", {"msg": "请开始你的表演"})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"]
        author = request.session["loginUser"]

        article = models.Article(title=title, content=content, author=author)
        article.save()

        # 将缓存重新更新
        cacheUtils.getAllArticle(ischange=True)
        return redirect(reverse("blog:show_article", kwargs={"a_id": article.id}))


# 删除文章
def delete_article(request, a_id):
    article = models.Article.objects.get(pk=a_id)
    article.delete()
    # 更新缓存
    cacheUtils.getAllArticle(ischange=True)
    return redirect(reverse("blog:index"))

# 修改文章
def update_article(request, a_id):
    article = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "blog/update_article.html", {"article": article})
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"]
        article.title = title
        article.content = content
        article.save()

        return redirect(reverse("blog:show_article", kwargs={"a_id": a_id}))

# 查看文章
def show_article(request, a_id):
    article = models.Article.objects.get(pk=a_id)
    return render(request, "blog/show_article.html", {"article": article})


#展示单个用户所有的文章
def show_all_articles(request):
    articles = models.Article.objects.all()
    return render(request, "blog/show_all_articles.html", {"articles": articles})


def code(request):
    image, code = utils.create_code()
    # 首先需要将我们的code保存到我们的session中
    request.session['code'] = code
    # 返回图片
    file = BytesIO()
    image.save(file, 'PNG')

    return HttpResponse(file.getvalue(), "image/png")

@require_POST
@csrf_exempt # 这个装饰器，表示装饰者的函数忽略csrf验证
# @require_http_methods("GET", "POST")
def ajax_hello(request):
    # id = request.POST['id']
    # article = models.Article.objects.get(pk=id)
    # msg = {
    #     "id": user.id,
    #     "uname": user.name,
    #     "unickname": user.nickname,
    #     "uage": user.age,
    # }
    # JsonResponse 返回一个字段对象，会自动完成dict --> json的转换
    # return JsonResponse(model_to_dict(article))
    # HttpResponse返回的是一个字符串
    # return HttpResponse(msg)

    # jqueryset django考虑到大家需要传输，提供了一个序列化
    ats = models.Article.objects.all()

    return HttpResponse(serialize("json", ats))