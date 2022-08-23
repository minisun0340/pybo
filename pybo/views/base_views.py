from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        # annotate함수는 Question모델의 기존 필드인
        # author, subject, content, create_date, modify_date, voter에 질문의 추천 수에 해당하는 num_voter필드를 임시로 추가해 주는 함수
        # Count('voter') : 해당 질문의 추천 수
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer',
                                                 '-create_date')  # order_by함수에 두 개 이상의 인자가 전달되는 경우 1번째 항목부터 우선순위를 매긴다. 추천수->최신순순    else: #recent
    else:
        question_list = Question.objects.order_by('create_date')

    # 조회

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색 : 제목에 kw문자열이 포함되었는지 의미
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색 : 답변을 작성한 사람의 이름에 포함되는지 의미
        ).distinct()
        # filter함수에서 모델필드에 접근하려면 '__' 를 이용하면 된다.
        # subject__contains=kw 대신 subject__icontains=kw를 사용하면 대소문자를 가리지 않고 찾아 준다.

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
