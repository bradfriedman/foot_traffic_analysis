# Placer Shopping Analysis Exercise

## Description

This Django app takes in information about daily foot traffic to shopping centers and uses
LLMs to talk about trends and anomalies in the data in natural language.

## Tradeoffs

# LLM Choices
The website offers several different LLMs as engines. Claude 3 Haiku, Anthropic's lightweight
2024 release, does surprisingly well for most inputs, so that is the default. The highest-quality
output is subjective, but it seems that ChatGPT 4.5 Turbo is consistently a step above, but is
quite a bit slower than Haiku.

# Cost
This app does not put too much emphasis on economical token usage. The prompt engineering is
a bit verbose, which comes at a cost of extra API usage and time, but for this toy
application, the differences are quite small. At scale, it would be important to consider
the relative costs of concise prompting compared to output quality.

## Contact

- Brad Friedman - [brad.friedman@gmail.com](mailto:brad.friedman@gmail.com)
- Project Link: [https://github.com/bradfriedman/placer-exercise](https://github.com/bradfriedman/placer-exercise)