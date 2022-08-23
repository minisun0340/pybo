from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question
from ..forms import QuestionForm

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) #commit=False는 임시저장을 의미
            question.author = request.user #추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() #request.method가 get인 경우 호출

    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: #로그인한 사용자와 수정하려는 글쓴이가 다르면 수정권한없음 오류
        messages.error(request, '수정권한이 없습니다')
        return  redirect('pybo:detail', question_id=question_id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question) #조회한 질문question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now() #수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id = question_id)
    else:
        form = QuestionForm(instance=question) #instance매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있다.
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, "삭제권한이 없습니다.")
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')

