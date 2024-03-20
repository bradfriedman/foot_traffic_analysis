from enum import Enum


class LLMChoice(Enum):
  CHATGPT35 = "chatgpt3.5"
  CHATGPT45 = "chatgpt4.5"
  CLAUDE2 = "claude2"
  CLAUDE3_OPUS = "claude3_opus"
  CLAUDE3_SONNET = "claude3_sonnet"
  CLAUDE3_HAIKU = "claude3_haiku"


class DayOfWeek(Enum):
  Mon = 0
  Tue = 1
  Wed = 2
  Thu = 3
  Fri = 4
  Sat = 5
  Sun = 6
