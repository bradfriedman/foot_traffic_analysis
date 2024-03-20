from django import forms

from analysis.utils.enums import LLMChoice


class UserQueryForm(forms.Form):
  query = forms.CharField(label='Enter your query', widget=forms.TextInput(
      attrs={'style': 'width: 850px;'}), initial='Tell me about Skyview Plaza in Satellite Beach')
  llm_choices = [
      (LLMChoice.CHATGPT45.value, 'ChatGPT 4.5 Turbo'),
      (LLMChoice.CHATGPT35.value, 'ChatGPT 3.5 Turbo'),
      (LLMChoice.CLAUDE3_OPUS.value, 'Claude 3 Opus'),
      (LLMChoice.CLAUDE3_SONNET.value, 'Claude 3 Sonnet'),
      (LLMChoice.CLAUDE3_HAIKU.value, 'Claude 3 Haiku'),
  ]
  llm_choice = forms.ChoiceField(
      label='LLM', choices=llm_choices, initial=LLMChoice.CLAUDE3_HAIKU.value)
