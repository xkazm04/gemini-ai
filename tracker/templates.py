TEMPLATE_SKILL = """
Based on the following tasks I have completed as a developer specializing in {skill}, I am seeking recommendations to further enhance my proficiency. Please suggest exactly five new, progressively advanced tasks. These should build upon my existing knowledge and guide me towards mastering React development.
Give tasks with small granularity, so it could be completed in a few hours.
Limit the length of each task description to 30 characters. Avoid using words "Learn how to" or "Understand how to" to keep the description short.

Completed Tasks: {input}

Please provide five detailed improvements or additions to my routine in a JSON format. Each suggestion should be a JSON object with 'name', 'description', and 'rationale' as keys. These should be feasible, build upon my existing exercises, and include brief explanations for each recommendation, outlining how they contribute to my overall fitness goals.
Format improvements into an array with JSON objects as elements. Limit the length of each `name` to 30 characters.
Output always must be an array with five objects.
  
JSON Output format:
[
    "name": "Name of first improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
,
    "name": "Name of second improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
,
    "name": "Name of third improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
,
    "name": "Name of fourth improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
.
    "name": "Name of fifth improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
]
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

TEMPLATE_HABIT = """
I have set a goal to {habit_name} in area of {category}. I have completed this goal {completed_instances} times in the past {weeks_elapsed} from target {total_instances} times.
One instance meant activity of time {volume} {volume_units}. I am seeking suggestions to help me achieve this goal. 

List of tasks I have completed: {task_names}

Consistency is the key to success. If I am consistent enough, please provide a recommendation to help me improve my performance or skill.
If I am not consistent enough, please provide a recommendation to help me improve my consistency.

Be as specific as you could be. Do not hesitate to criticize my performance. I am seeking to improve myself and need also explain what I lack.

Please provide a recommendation in a JSON format. The recommendation should be a JSON object with 'name', 'description', and 'rationale' as keys.
  
JSON Output format:
[
    "name": "Name of first improvement",
    "description": "Brief description of what the improvement entails",
    "rationale": "Explanation of how this improvement contributes to overall fitness goals"
]
"""
