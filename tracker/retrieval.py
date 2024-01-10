# Look into Postgres, find through API User habit and tasks completed/incompleted - tools: openapi, postgres, fastapi
# https://python.langchain.com/docs/integrations/toolkits/postgres
# Prompt suggestion in specific format 
# Save into suggestions db schema - tools: fastapi, postgres

# Use llama over Langchain probably
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from tracker.templates import TEMPLATE_SKILL, TEMPLATE_HEALTH, TEMPLATE_HABIT
from tracker.models import Habit, Task, TaskSuggestionInput, Completed, Stats, Categories
from datetime import datetime

llm = ChatOpenAI()
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import db connection from env
import os


SQLALCHEMY_DATABASE_URL = os.getenv("DBCONN") or "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
db: Session = SessionLocal()

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name
    

# Enhance function - Get all habits with unprocessed goals  
# Mock: 
habit = "Morning routine"
tasks = ["Do 20 pushups", "Do 20 situps", "Run 1km", "Shower"]
tasks_skill = ["Nested React components", "Use React hooks", "Use React context", "Use React router"]
skill = "React"
output = "Try to do 5 more pushups than last time."

prompt_template = ChatPromptTemplate.from_template(TEMPLATE_SKILL)
habit_template = ChatPromptTemplate.from_template(TEMPLATE_HEALTH)
h_template = ChatPromptTemplate.from_template(TEMPLATE_HABIT)	


chain = LLMChain(llm=llm, prompt=prompt_template)
habit_chain = LLMChain(llm=llm, prompt=habit_template)
# print(chain.run(input=tasks_skill, skill=skill))
# print(habit_chain.run(input=tasks))

# Online recommendation
def recommend_tasks(habit_id: str):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    tasksDescriptions = get_ai_habit_task(db=db,habit=habit)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    # habit_chain = LLMChain(llm=llm, prompt=habit_template)
    # return "[\"React Hooks\", \"Context API\", \"Server-side rendering (SSR)\"]"
    return chain.run(input=tasksDescriptions, skill="React development")
    # return create_task_suggestion(db=db, tasks=chain.run(input=tasksDescriptions, skill=habit.category), habit=habit.id)
    
    
def get_ai_habit_task(db: Session, habit: Habit):
    try:
        # today = datetime.date.today()
        # if habit.specific_days[today.weekday()] == False:    
            # return []
        if not habit:
            return []
        tasks = db.query(Task).filter(Task.habit_id == habit.id).all()
        if not tasks:
            return []
        tasksDescriptions = []
        for task in tasks:
            tasksDescriptions.append(task.name)
        return tasksDescriptions
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
def update_habits(db: Session):
    while True:
        habits = db.query(Habit).filter(Habit.ai == False).all()
        if not habits:
            break
        for habit in habits:
            recommend_tasks(habit)
            habit.ai = False
            db.commit()
            db.refresh(habit)
            
def start_ai_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_habits(db=db), 'cron', hour=12, minute=0, timezone=timezone('UTC'))  # runs every day at 12:00 UTC
    scheduler.start()



def create_task_suggestion(db: Session, tasks: List[str], habit: str):
    try:
        for task in tasks:
            suggestion = TaskSuggestionInput(habit=habit, name=task)
            db.add(suggestion)
            db.commit()
            db.refresh(suggestion)
    except SQLAlchemyError as e:
        db.rollback()
        raise UnicornException(name=str(e))
    
# offline recommendation
def get_stats(db: Session, habit_id: str):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    completed_volume = db.query(func.sum(Completed.volume_actual)).filter(Completed.completed == True).scalar()
    cat = db.query(Categories).filter(Habit.category == Categories.id).first()
    total_instances = 0
    # Parse habit.date_from into a datetime object
    date = habit.date_from
    today = datetime.today()
    while date <= today:
        if habit.specific_days[date.weekday()]:
            total_instances += 1
        date += timedelta(days=1)

    # Get number of completed instances
    completed_instances = db.query(Completed).filter(
        Completed.habit_id == habit.id,
        Completed.completed == True
    ).count()
    
    # Calculate number of weeks
    elapsed_time = today - habit.date_from
    weeks_elapsed = elapsed_time.days 

    # Inputs to the AI model
    return {
        "habit_id": habit_id,
        "category": cat.label,
        "habit_name": habit.name,
        "total_instances": total_instances,
        "completed_instances": completed_instances,
        "completed_volume": completed_volume,
        "volume_units": habit.volume_units,
        "weeks_elapsed": weeks_elapsed
    }


def generate_recommendation(db: Session, habit_id: str):
    # Get stats
    stats:Stats = get_stats(db=db, habit_id=habit_id)
    habit_name = stats["habit_name"]
    total_instances = stats["total_instances"]
    completed_instances = stats["completed_instances"]
    weeks_elapsed = stats["weeks_elapsed"]
    category = stats["category"]
    volume_units = stats["volume_units"]
    volume = stats["completed_volume"]
    tasks = db.query(Task).filter(Task.habit_id == habit_id).filter(Task.completed == True).all()
    task_names = []
    for task in tasks:
        task_names.append(task.name)
    # Get recommendation
    chain = LLMChain(llm=llm, prompt=h_template)
    recommendation = chain.run(
        habit_name=habit_name, 
        total_instances=total_instances,
        completed_instances=completed_instances,
        weeks_elapsed=weeks_elapsed,
        category=category,
        volume_units=volume_units,
        volume=volume,
        task_names=task_names
    )

    return recommendation



