from django.conf import settings

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .enums import LLMChoice


def get_llm(llm_choice: LLMChoice) -> BaseChatModel:
  '''
  Get the language model based on the user's choice.

  Args:
    llm_choice: The user's choice of language model.
  '''
  if llm_choice == LLMChoice.CLAUDE3_OPUS:
    llm = ChatAnthropic(
        model='claude-3-opus-20240229',
        temperature=settings.LLM_TEMP,
    )
  elif llm_choice == LLMChoice.CLAUDE3_SONNET:
    llm = ChatAnthropic(
        model='claude-3-sonnet-20240229',
        temperature=settings.LLM_TEMP,
    )
  elif llm_choice == LLMChoice.CLAUDE3_HAIKU:
    llm = ChatAnthropic(
        model='claude-3-haiku-20240307',
        temperature=settings.LLM_TEMP,
    )
  elif llm_choice == LLMChoice.CLAUDE2:
    llm = ChatAnthropic(
        model='claude-2.1',
        temperature=settings.LLM_TEMP,
    )
  elif llm_choice == LLMChoice.CHATGPT35:
    llm = ChatOpenAI(
        model='gpt-3.5-turbo-0125',
        temperature=settings.LLM_TEMP,
    )
  else:  # default to ChatGPT-4
    llm = ChatOpenAI(
        model='gpt-4-0125-preview',
        temperature=settings.LLM_TEMP,
    )
  return llm
