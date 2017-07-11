from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from member.forms import UserEditForm

User = get_user_model()

__all__ = (
    'profile',
    'profile_edit',
)
def profile(request, user_pk=None):
    # (0628) 유저가 로그인하지 않고, user_pk도 주어지지 안ㅇ흔 경우 my_profile에 접근하려는 경우 로그인 페이지로 리다이렉트
    if not request.user.is_authenticated and not user_pk:
        login_url = reverse('member:login')
        redirect_url = login_url + '?next=' + request.get_full_path()
        return redirect(redirect_url)
    NUM_POST_PER_PAGE = 3
    # 0. urls.py에 연결
    # 1. User_pk에 해당하는 User를 cur_user키로 render
    # 또는 user = get_object_or_404(User, pk=user_pk)

    # 2. member/profile.html작성, 해당 user정보 보여주기
    # 2-1 해당 user의 follwers, following 목록 보여주기


    # 3 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고 있는지 여부 보여주기
    # 3-1 팔로우하고 있다면 '팔로우 해제'버튼, 아니라면 '팔로우'버튼 띄워주기

    # 4. -> def follow_toggle(request) 뷰 생성


    """
    1. GET parameter로 'page'를 받아 처리
    2. page가 1일 경우 Post의 author가 해당 User인 Post 목록을 
        -created_date 순서로 page * 9 만큼의 QuerySet을 생성해서 리턴

        만약, 실제 Post 개수보다 큰 page가 왔을 경우, 최대한의 값을 보여준다.
        int로 변환 불가능한 경우, except처리
        1보다 작은값일 경우 except 처리 
        오지 않을 경우 page=1로 처리
    """

    # 1. GET 파라미터 처리
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    """
        3. def follow_toggle(request, user_pk)
          위 함수기반 뷰를 구현
                login_required
                required POST
            데코레이터를 사용(필요하다면 추가)
            처리 후 next값을 받아 처리하고, 없을 경우 해당 User의 Profile로 이동

        ** extra. 유저 차단기능 만들어보기
            Block여부는 Relation에서 다룸
                1. followers, following에 유저가 나타나면 안됨
                2. block_users로 차단한 유저 목록 QuerySet 리턴
                3. follow, unfollow 기능을 하기전에 block된 유저인지 확인
                4. block처리시 follow상태는 해제되어야 함 (동시적용 불가)
                5. 로그인 시 post_list에서 block_users의 글은 보이지 않도록 함. 

    """
    if user_pk:
        user = get_object_or_404(User, pk=user_pk)

    else:
        user = request.user

    # page * 9만큼의 Post QuerySet을 리턴

    posts = user.post_set.order_by('-created_date')[:page * NUM_POST_PER_PAGE]
    post_count = user.post_set.count()
    # next_page = 현재 page에서 보여주는 Post개수보다 post_count가 클 경우 전달받은 page + 1, 아닐 경우 None 할당
    next_page = page + 1 if post_count > page * NUM_POST_PER_PAGE else None
    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }

    return render(request, 'member/profile.html', context)


    # if request.method == "POST":
    #     print("포스트 :", request.POST)
    #
    # else:
    #     posts = user.post_set.all().order_by('-created_date')
    #     posts_count = posts.count()
    #
    #     paginator = Paginator(posts, 3)
    #
    #     try:
    #         pages = paginator.page(int(page))
    #     except PageNotAnInteger:
    #         pages = paginator(1)
    #     except EmptyPage:
    #         pages = paginator.page(paginator.num_pages)
    #     except CustomException as e:
    #         print("1보다 작은 값 ", e)
    #
    #     index = pages.number - 1
    #     max_index = len(paginator.page_range)
    #     start_index = index - 3 if index >= 3 else 0
    #     end_index = index + 3 if index <= max_index - 3 else max_index
    #     page_range = paginator.page_range[start_index:end_index]

    # context = {
    #     'posts': posts,
    #     'posts_count': posts_count,
    #     'pages': pages,
    #     'page_range': page_range,
    # }


@login_required
def profile_edit(request):
    """
    request.method == "POST"일 때 nickname과 img_profile(필드도 모델에 추가)을 수정할
    UserEditForm을 구성 (ModelForm 상속) 

    1. UserEditForm 구성
    2. 이 view에서 request method가 GET일떄, 해당 Form에서 request.user에 해당하는 User를 이용해
    bound form을 만듬.
    3. POST 요청일 때, 받은 데이터를 이용해 Form에 bind된 User Instance를 업데이트 
    """

    if request.method == "POST":
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('member:profile_edit')

    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context)

