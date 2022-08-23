from django import template
import markdown
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

# mark함수는 markdown 모듈과 mark_safe 함수를 이용하여 문자열을 HTML코드로 변환하여 반환한다.
# 이 과정을 거치면 말크다운 문법에 맞도록 HTML이 만들어진다.
# markdown모듈에 "nl2br", "fenced_code" 확장 도구를 설정했다.
# "nl2br" : 줄바꿈 문자를 <br>태그로 바꿔주므로 enter를 한 번만 눌러도 줄바꿈으로 인식한다.
# "fenced_code" : 마크다운의 소스 코드 표현
# 마크다운 확장 기능 문서 : python-markdown.github.io/extensions