from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from tracker.models import NoteInput, HabitInput, TimerCreate, CountdownCreate, TimeInput, TaskInput, TaskUpdate, NoteUpdate, CompInput, HabitTemplateInput, HabitFromTemplate
from tracker.functions import create_habit, create_note, get_user_habits, delete_habit, get_user_daily_habits
from tracker.functions import create_task, update_task, get_user_tasks, get_habit_tasks, create_habit_template, create_habit_from_template, delete_habit_template
from tracker.functions import get_habit_notes, update_note, delete_note_by_id, get_user_notes, get_categories
from tracker.functions import create_completion, update_completion, get_habit_completions, get_habits_completions, get_week_completions, get_day_completions
from tracker.timer import create_timer, create_countdown, get_user_countdown, pause_countdown, finish_countdown
from tracker.retrieval import recommend_tasks, get_stats, generate_recommendation

from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import os
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )

db: Session = SessionLocal()

router = APIRouter()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")
        
# ------- Habit API ---------
# Protected example to implement further after API key is implemented
@router.get("/tracker/habit/protected",dependencies=[Depends(get_api_key)])
async def post_protected_habit(data: HabitInput):
    res = create_habit(db=db, data=data)
    return res

@router.post("/tracker/habit")
async def post_habit(data: HabitInput):
    res = create_habit(db=db, data=data)
    return res

@router.get("/tracker/habit/user/{user_id}")
async def get_habits(user_id: str):
    habits = get_user_habits(db=db, user=user_id)
    return habits

@router.get("/tracker/habit/user/{user_id}/daily/{day}")
async def get_daily_habits(user_id: str, day: str):
    habits = get_user_daily_habits(db=db, user=user_id, day=day)
    return habits    

@router.delete("/tracker/habit/{habit_id}")
async def remove_habit(habit_id: str):
    res = delete_habit(db=db, habit_id=habit_id)
    return res

# Template routes 
@router.post("/tracker/habit/template")
async def post_habit_template(data: HabitTemplateInput):
    res = create_habit_template(db=db, data=data)
    return res

@router.delete("/tracker/habit/template/{template_id}")
async def delete_habit_template_by_id(template_id: str):
    res = delete_habit_template(db=db, temp=template_id)
    return res

@router.post("/tracker/habit/template/{temp}")
async def post_habit_from_template(temp: str):
    res = create_habit_from_template(db=db, temp=temp)
    return res

# ------- Habit Notes API ---------
@router.post("/tracker/notes")
async def post_note_by_tracker(data: NoteInput):
    res = create_note(db=db, data=data)
    return res


@router.get("/tracker/notes/habit/{habit_id}")
async def get_notes(habit_id: str):
    notes = get_habit_notes(db=db, habit=habit_id)
    return notes

@router.get("/tracker/notes/user/{user_id}")
async def get_notes_by_user(user_id: str):
    notes = get_user_notes(db=db, user=user_id)
    return notes

@router.put("/tracker/notes/{note_id}")
async def update_note_by_id(note_id: str, data: NoteUpdate):
    res = update_note(db=db, id=note_id, data=data)
    return res

@router.delete("/tracker/notes/{note_id}")
async def delete_note(note_id: str):
    res = delete_note_by_id(db=db, id=note_id)
    return res

# Tasks -----------------
@router.post("/tracker/task")
async def post_task(data: TaskInput):
    res = create_task(db=db, data=data)
    return res

@router.put("/tracker/task/{task_id}")
async def update_task_state(task_id: str, data: TaskUpdate):
    res = update_task(db=db, id=task_id, data=data)
    return res

@router.get("/tracker/task/user/{user_id}")
async def get_tasks_by_user(user_id: str):
    tasks = get_user_tasks(db=db, user=user_id)
    return tasks

@router.get("/tracker/task/habit/{habit_id}")
async def get_tasks_by_habit(habit_id: str):
    tasks = get_habit_tasks(db=db, habit=habit_id)
    return tasks

# Countdowns -----------------
@router.post("/tracker/countdown")
async def post_cd(data: CountdownCreate):
    res = create_countdown(db=db, data=data)
    return res

@router.get("/tracker/countdown/user/{user_id}")
async def get_cd_user(user_id: str):
    cds = get_user_countdown(db=db, user_id=user_id)
    return cds


@router.put("/tracker/countdown/{countdown_id}/pause")
async def update_cd(countdown_id: str, data: TimeInput):
    res = pause_countdown(db=db, id=countdown_id, data=data)
    return res    

@router.put("/tracker/countdown/{countdown_id}/finish")
async def finish_cd(countdown_id: str):
    res = finish_countdown(db=db, id=countdown_id)
    return res

# Timers -----------------
@router.post("/tracker/timer")
async def post_timer(data: TimerCreate):
    res = create_timer(db=db, data=data)
    return res

# Habit completion -----------------

@router.post("/tracker/completion")
async def post_completion(data: CompInput):
    res = update_completion(db=db, data=data)
    return res

@router.get("/tracker/completion/habit/{habit_id}")
async def get_completions_by_habit(habit_id: str):    
    comps = get_habit_completions(db=db, habit_id=habit_id)
    return comps

@router.get("/tracker/completion/habits/{habit_ids}")
async def get_completions_by_habits(habit_ids: str):
    comps = get_habits_completions(db=db, habits=habit_ids)
    return comps

@router.get("/tracker/completion/habit/{habit_id}/week")
async def get_week_completions_by_habit(habit_id: str):
    comps = get_week_completions(db=db, habit_id=habit_id)
    return comps

@router.get("/tracker/completion/habit/{habit_id}/day/{day}")
async def get_day_completions_by_habit(habit_id: str, day: str):
    comps = get_day_completions(db=db, habit_id=habit_id, day=day)
    return comps


# Others -----------------
@router.delete("/tracker/user/{user_id}")
async def delete_user(user_id: int):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")



@router.delete("/tracker/{tracker_id}")
async def delete_tracker(tracker_id: int):
    for tracker in db:
        if tracker.id == tracker_id:
            db.remove(tracker)
            return {"message": "Tracker deleted"}
    raise HTTPException(status_code=404, detail="Tracker not found")

# AI -----------------
@router.get("/tracker/ai/{habit_id}")
async def get_recommendations(habit_id: str):
    res = recommend_tasks(habit_id)
    return res

@router.get("/tracker/stats/{habit_id}")
async def get_habit_stats(habit_id: str):
    res = get_stats(db=db, habit_id=habit_id)
    return res

@router.get("/tracker/aihabit/{habit_id}")
async def get_recommendation(habit_id: str):
    res = generate_recommendation(db=db, habit_id=habit_id)
    return res

# Others
@router.get("/categories")
async def get_cats():
    res = get_categories(db=db)
    return res