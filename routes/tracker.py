from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal
from tracker.models import NoteInput, HabitInput, TimerCreate, CountdownCreate, TimeInput, TimeStateInput, TaskInput, TaskUpdate, NoteUpdate, CompInput, HabitTemplateInput, HabitFromTemplate
from tracker.functions import create_habit, create_note, get_user_habits
from tracker.functions import create_task, update_task, get_user_tasks, get_habit_tasks, create_habit_template, create_habit_from_template, delete_habit_template
from tracker.functions import get_habit_notes, update_note, delete_note_by_id
from tracker.functions import create_completion, update_completion, get_habit_completions, get_habits_completions
from tracker.timer import create_timer, create_countdown, get_user_countdown, update_countdown_time, finish_countdown
    
db: Session = SessionLocal()

router = APIRouter()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")
        
# ------- Habit API ---------
@router.post("/tracker/habit")
async def post_habit(data: HabitInput):
    db_habit = create_habit(db=db, data=data)
    return db_habit

@router.get("/tracker/habit/user/{user_id}")
async def get_habits(user_id: str):
    habits = get_user_habits(db=db, user=user_id)
    if not habits:
        raise HTTPException(status_code=404, detail="No habits found for this user")
    return habits


# Template routes 
@router.post("/tracker/habit/template")
async def post_habit_template(data: HabitTemplateInput):
    db_habit = create_habit_template(db=db, data=data)
    return db_habit


@router.delete("/tracker/habit/template/{template_id}")
async def delete_habit_template_by_id(template_id: str):
    db_habit = delete_habit_template(db=db, id=template_id)
    BackgroundTasks.add_task(write_log, f"Deleted template {template_id}")
    return db_habit

@router.post("/tracker/habit/from/")
async def post_habit_from_template(data: HabitFromTemplate):
    db_habit = create_habit_from_template(db=db, data=data)
    return db_habit


# ------- Habit Notes API ---------
@router.post("/habit/notes")
async def post_note_by_tracker(data: NoteInput):
    db_note = create_note(db=db, data=data)
    return db_note


@router.get("/habit/notes/habit/{habit_id}")
async def get_notes(habit_id: str):
    notes = get_habit_notes(db=db, habit=habit_id)
    if not notes:
        raise HTTPException(status_code=404, detail="No notes found for this habit")
    return notes

@router.put("/habit/notes/{note_id}")
async def update_note_by_id(note_id: str, data: NoteUpdate):
    db_note = update_note(db=db, id=note_id, data=data)
    return db_note

@router.delete("/habit/notes/{note_id}")
async def delete_note(note_id: str):
    db_note = delete_note_by_id(db=db, id=note_id)
    return db_note

# Tasks -----------------
@router.post("/tracker/task")
async def post_task(data: TaskInput):
    db_task = create_task(db=db, data=data)
    return db_task

@router.put("/tracker/task/{task_id}")
async def update_task_state(task_id: str, data: TaskUpdate):
    db_task = update_task(db=db, id=task_id, data=data)
    return db_task

@router.get("/tracker/task/user/{user_id}")
async def get_tasks_by_user(user_id: str):
    tasks = get_user_tasks(db=db, user=user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks

@router.get("/tracker/task/habit/{habit_id}")
async def get_tasks_by_habit(habit_id: str):
    tasks = get_habit_tasks(db=db, habit=habit_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this habit")
    return tasks

# Countdowns -----------------
@router.post("/tracker/countdown")
async def post_cd(data: CountdownCreate):
    db_timer = create_countdown(db=db, data=data)
    return db_timer

@router.get("/tracker/countdown/user/{user_id}")
async def get_cd_user(user_id: str):
    cds = get_user_countdown(db=db, user_id=user_id)
    if not cds:
        raise HTTPException(status_code=404, detail="No countdown found for this user")
    return cds


@router.put("/tracker/countdown/{countdown_id}")
async def update_cd(countdown_id: str, data: TimeInput):
    db_cd = update_countdown_time(db=db, id=countdown_id, data=data)
    return db_cd    

@router.put("/tracker/countdown/{countdown_id}/finish")
async def finish_cd(countdown_id: str, data: TimeStateInput):
    db_cd = finish_countdown(db=db, id=countdown_id, data=data)
    return db_cd

# Timers -----------------
@router.post("/tracker/timer")
async def post_timer(data: TimerCreate):
    db_timer = create_timer(db=db, data=data)
    return db_timer

# Habit completion -----------------

@router.post("/tracker/completion")
async def post_completion(data: CompInput):
    db_comp = create_completion(db=db, data=data)
    return db_comp

@router.put("/tracker/completion/{completion_id}")
async def update_completion_state(completion_id: str, data: CompInput):
    db_comp = update_completion(db=db, id=completion_id, data=data)
    return db_comp

@router.get("/tracker/completion/habit/{habit_id}")
async def get_completions_by_habit(habit_id: str):    
    comps = get_habit_completions(db=db, habit=habit_id)
    if not comps:
        raise HTTPException(status_code=404, detail="No completions found for this habit")
    return comps

@router.get("/tracker/completion/habits/{habit_ids}")
async def get_completions_by_habits(habit_ids: str):
    comps = get_habits_completions(db=db, habits=habit_ids)
    if not comps:
        raise HTTPException(status_code=404, detail="No completions found for these habits")
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
