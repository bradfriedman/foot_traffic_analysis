from django import template
import markdown as md
from django.utils.safestring import SafeText, mark_safe

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text) -> SafeText:
  return mark_safe(
      md.markdown(
          text,
          extensions=['mdx_truly_sane_lists', 'prependnewline']
      )
  )
