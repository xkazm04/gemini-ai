# Look into Postgres, find through API User habit and tasks completed/incompleted - tools: openapi, postgres, fastapi
# https://python.langchain.com/docs/integrations/toolkits/postgres
# Prompt suggestion in specific format 
# Save into suggestions db schema - tools: fastapi, postgres

# Use llama over Langchain probably
from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain 
from tracker.models import Habit, Task, TaskSuggestionInput
from exceptions import UnicornException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import List
from agent.templates import TEMPLATE_SKILL, TEMPLATE_HEALTH

import datetime

llm = ChatOpenAI()

db: Session = SessionLocal()


# Enhance function - Get all habits with unprocessed goals  
# Mock: 
habit = "Morning routine"
tasks = ["Do 20 pushups", "Do 20 situps", "Run 1km", "Shower"]
tasks_skill = ["Nested React components", "Use React hooks", "Use React context", "Use React router"]
skill = "React"
output = "Try to do 5 more pushups than last time."

prompt_template = ChatPromptTemplate.from_template(TEMPLATE_SKILL)
habit_template = ChatPromptTemplate.from_template(TEMPLATE_HEALTH)


chain = LLMChain(llm=llm, prompt=prompt_template)
habit_chain = LLMChain(llm=llm, prompt=habit_template)
print(chain.run(input=tasks_skill, skill=skill))
# print(habit_chain.run(input=tasks))

def recommend_tasks(habit: Habit):
    tasksDescriptions = get_ai_habit_task(db=db,habit=habit)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    habit_chain = LLMChain(llm=llm, prompt=habit_template)
    # category dospecifikovat
    create_task_suggestion(db=db, tasks=chain.run(input=tasksDescriptions, skill=habit.category), habit=habit.id)
    
    
def get_ai_habit_task(db: Session, habit: Habit):
    try:
        today = datetime.date.today()
        if habit.specific_days[today.weekday()] == False:    
            return []
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
    scheduler.add_job(update_habits, 'cron', hour=12, minute=0, timezone=timezone('UTC'))  # runs every day at 12:00 UTC
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
    
    






