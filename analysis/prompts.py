FILTERING_PROMPT = '''
Extract the shopping center name and city from the following user query:
{query}

{format_instructions}
If the city is not present, respond with an empty <City> tag.
Output only the XML, with no preamble or postamble.
'''

TREND_ANALYSIS_PROMPT = '''
Please analyze the following foot traffic data and identify
trends over time. Give a summary of your trend analysis. It should
be quite general, like an executive summary. More details will be
filled in at a later time. For example, a great response would be:

<example>
Between June and November 2023, Dolphin Mall in Florida experienced
a steady rise in foot traffic. The summer months, particularly June
and July, saw a significant increase due to the summer sales and
vacation period. The foot traffic slightly dipped in August but picked
up again in September, maintaining a consistent flow through
November.
</example>

Think step-by-step in determining your answer. Think especially 
carefully about the overall trend from the earliest data point to the
latest. If the trend line is generally up, down, or flat, say so. You
can also comment on the severity of the trend, if it's consistent or
fluctuating, and if there are any significant peaks or troughs.

The mean foot traffic for this data is {ft_mean}, the median is
{ft_median}, the standard deviation is {ft_stddev}, and the variance
is {ft_variance}.

The daily averages of foot traffic by month, in ascending order of date, are:
{monthly_averages}
Use this information to help you analyze the overall trend.

The data to analyze is here:
<data>
{data_str}
</data>
'''

ANOMALY_DETECTION_PROMPT = '''
Please analyze the following foot traffic data and identify any
anomalies or outliers. Consider anomalies at the daily, weekly, or monthly
level, as well as seasonal. Respond with the relevant days, weeks, months,
and/or seasons, along with a brief explanation of why they are considered
anomalies. To help your analysis, the mean foot traffic over this dataset is
{ft_mean}, the median is {ft_median}, the standard deviation is {ft_stddev},
and the variance is {ft_variance}.

Be specific with your anomaly explanations, including qualitative and
quantitative analyses. Consider reasons why the anomalies might have
occurred. For example, if there is a sudden drop in foot traffic, consider if
there was a natural disaster, a holiday, or a special event that might have
caused it. Also consider the location. For example, if the shopping center is
in Florida, you might consider the impact of hurricane season or peak tourism
season on foot traffic. Don't guess at a generic reason, like local events or
bad weather, without evidence. Promotional events or sales are also not valid
explanations. Definitely feel free to attribute anomalies to
holidays, high/low seasons, or other known events.

The data to analyze is here:

<data>
{data_str}
</data>

To help with your analysis, here are some days that have Z-scores with high
absolute values. Ignore individual days that are not listed here.

<anomalies>
{daily_anomalies}
</anomalies>
'''

INSIGHTS_GENERATION_PROMPT = '''
Based on the following trend analysis and anomaly detection results,
please generate a concise and human-friendly summary of the key
insights and findings. Use Markdown to format your response nicely.

You should simply provide the information, commenting only with working
theories or hypotheses. Do not give any preamble about what you are
or are not capable of inferring given the data. DO NOT mention what you
would need to know to make a better analysis. Just provide the insights.

Be sure to mention the earliest and latest date in the data, so we have
context of the time range in question. The earliest date is {earliest_date}
and the latest date is {latest_date}.

Be specific with your anomaly explanations, including qualitative and
quantitative analyses. Consider reasons why the anomalies might have
occurred. For example, if there is a sudden drop in foot traffic, consider if
there was a natural disaster, a holiday, or a special event that might have
caused it. Also consider the location. For example, if the shopping center is
in Florida, you might consider the impact of hurricane season or peak tourism
season on foot traffic. Don't guess at a generic reason, like local events or
bad weather, without evidence. Definitely feel free to attribute anomalies to
holidays, high/low seasons, or other known events. Note that certain holidays
can lead to increased traffic (like Veterans Day due to big sales) or decreased
traffic (like Thanksgiving Day).
  
A good example of your output is as follows, enclosed in <example> tags:

<example>
# Summary
Between June and November 2023, Dolphin Mall in Florida
experienced a steady rise in foot traffic. The summer months,
particularly June and July, saw a significant increase due to the
summer sales and vacation period. The foot traffic slightly
dipped in August but picked up again in September, maintaining a
consistent flow through November.

# Anomalies
There were a couple of anomalies during this period. In late
August, there was an unexpected drop in foot traffic, possibly
due to a tropical storm warning that deterred visitors. In
contrast, there was a sudden surge in foot traffic in the second
week of November, likely due to the early holiday shoppers and
the Veterans Day sales.

In conclusion, Dolphin Mall continues to attract a significant
number of visitors, with notable increases during sale periods
and holidays. The management should continue to monitor these
trends and anomalies to optimize their operations and marketing
strategies.
</example>

It's important that you DO NOT guess at the reasons for anomalous
data. For example, special events and promotions are NOT valid
explanations.

Imitating the overall style and level of detail in the above example,
please generate your insights from this data:

Trend Analysis Summary:
<trend_summary>
{trend_summary}
</trend_summary>

Anomalies Data:
<anomalies_summary>
{anomalies_summary}
</anomalies_summary>
'''
