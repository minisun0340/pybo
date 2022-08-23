from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Answer, Question
from ..forms import AnswerForm


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # 추가한 속성 author 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id)) # #answer_2와 같은 앵커를 추가하기 위해 format과 resolve_url함수 사용, resolve_url은 실제 호출되는 url을 문자열로 반환하는 장고 함수이다.
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    pybo 답변 수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('{}#answer_{}'.format(
            resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id),answer.id))

    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    pybo 답변 삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')

    else:
        answer.delete()

    return redirect('pybo:detail', question_id=answer.question.id)

