from tracker.models import Habit, Completed
from tracker.functions import get_user_habits, get_habits_completions
from datetime import datetime, timedelta

from sqlalchemy.orm import Session


async def process_habits(db: Session):
    # Get habits for specific user -> Get all habits
    user_habits = get_user_habits(db)
    # TBD test connection between dbs
    habit_ids = [habit.id for habit in user_habits]
    # Retrieve all completions for all habits
    completions = get_habits_completions(db, habit_ids)
    # Define period for the report
    one_week_ago = datetime.now() - timedelta(days=7)
    # Get all completions for the last week
    completions_last_week = [comp for comp in completions if comp.day >= one_week_ago and comp.completed]
    # TBD count total completions for each habit
    # Prepare data structure for notifications + Recommendation API
    # Expand this function to operate with new data stucture
    # Separate jobs to a new microservice
    # Handle error scenarios  
    # Process habits for all the users one by one - Log the progres somehow
    return len(completions_last_week)