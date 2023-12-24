TEMPLATE_SKILL = """
Based on the following tasks I have completed as a developer specializing in {skill}, I am seeking recommendations to further enhance my proficiency. Please suggest exactly three new, progressively advanced tasks. These should build upon my existing knowledge and guide me towards mastering React development.
Give tasks with small granularity, so it could be completed in a few hours.
Limit the length of each task description to 30 characters. Avoid using words "Learn how to" or "Understand how to" to keep the description short.

Completed Tasks: {input}

Please provide the recommendations in a structured format, with each task clearly labeled as 'taskOne', 'taskTwo', and 'taskThree'. The tasks should be well-defined and actionable, helping me to delve deeper into {skill} development.
Output always must be an array with three strings.

Output example:
  ["Description of the first","Description of the second","Description of the third"]
"""

TEMPLATE_HEALTH = """
Given my current exercise routine, I am seeking suggestions to enhance it for better overall performance and health. The recommendations should be specific, manageable, and aimed at advancing my current fitness level. Please consider the balance of strength, endurance, and flexibility in your suggestions.

Current Routine: {input}

Please provide three detailed improvements or additions to my routine in a JSON format. Each suggestion should be a JSON object with 'name', 'description', and 'rationale' as keys. These should be feasible, build upon my existing exercises, and include brief explanations for each recommendation, outlining how they contribute to my overall fitness goals.
Format improvements into an array with JSON objects as elements. Limit the length of each `name` to 30 characters.
Output always must be an array with three objects.

JSON Output format:
    "name": "Name of first improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"

    "name": "Name of second improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"

    "name": "Name of third improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"

"""