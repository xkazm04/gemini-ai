from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, ARRAY, DateTime, ForeignKey
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime



class Habit(Base):
    __tablename__ = "habits"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    day_type = Column(ARRAY(Boolean))
    active = Column(Boolean, default=True)
    name = Column(String)
    category = Column(Integer)
    date_from = Column(String)
    date_to = Column(String, default="")
    is_recurring = Column(Boolean, default=False)
    recurrence_type = Column(String, default="Week")
    recurrence_interval = Column(Integer)
    specific_days = Column(ARRAY(Boolean))
    type = Column(String, default="Habit", nullable=True)
    volume_start = Column(Integer, nullable=True)
    volume_units = Column(String, nullable=True)
    volume_target = Column(Integer, nullable=True)
    volume_actual = Column(Integer, nullable=True)
    subscribed = Column(Integer, default=0, nullable=True)	
    ai = Column(Boolean, default=False)
    
class HabitInput(BaseModel):
    userId: str
    dayType: List[bool]
    name: str
    category: int
    dateFrom: Optional[str]
    dateTo: Optional[str]
    isRecurring: Optional[bool]
    recurrenceType: Optional[str]
    recurrenceInterval: Optional[int]
    specificDays: Optional[List[bool]]
    volume_start: Optional[int]  = None
    volume_units: Optional[str]  = None
    
    
class HabitTemplate(Base):
    __tablename__ = "habit_templates"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    day_type = Column(ARRAY(Boolean))
    active = Column(Boolean, default=True)
    category = Column(Integer)
    date_from = Column(String)
    date_to = Column(String, default="")
    is_recurring = Column(Boolean, default=False)
    recurrence_type = Column(String, default="Week")
    recurrence_interval = Column(Integer)
    specific_days = Column(ARRAY(Boolean))
    type = Column(String, default="Habit", nullable=True)
    volume_start = Column(Integer, nullable=True)
    volume_units = Column(String, nullable=True)
    volume_target = Column(Integer, nullable=True)
    volume_actual = Column(Integer, nullable=True)
    creator = Column(UUID(as_uuid=True), nullable=True)
    ai = Column(Boolean, default=False)
    
class HabitTemplateInput(BaseModel):
    name: str
    description: str
    dayType: List[bool]
    category: int
    dateFrom: Optional[str]
    dateTo: Optional[str]
    isRecurring: Optional[bool]
    recurrenceType: Optional[str]
    recurrenceInterval: Optional[int]
    specificDays: Optional[List[bool]]
    type: Optional[str]
    volumeStart: Optional[int]
    volumeUnits: Optional[str]
    volumeTarget: Optional[int]
    volumeActual: Optional[int]
    creator: Optional[str]
    
class Challenge(Base):
    __tablename__ = "habit_challenges"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    type = Column(String, default="Challenge", nullable=True)
    creator = Column(UUID(as_uuid=True))
    active = Column(Boolean, default=True)
    
class HabitSuggestion(Base):
    __tablename__ = "habit_suggestions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    rationale = Column(String)
    category = Column(Integer)
    user = Column(UUID(as_uuid=True))
    accepted = Column(Boolean, default=False)
    
class TaskSuggestion(Base):
    __tablename__ = "task_suggestions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    habit = Column(UUID(as_uuid=True))
    removed = Column(Boolean, default=False)
    
class TaskSuggestionInput(BaseModel):
    name: str
    habit: str
    
class HabitFromTemplate(BaseModel):
    template_id: str
    user_id: str
    

    
class Task(Base):
    __tablename__ = "tracker_tasks"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    habit_id = Column(UUID(as_uuid=True))
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed = Column(Boolean, default=False)
    
class TaskInput(BaseModel):
    user_id: str
    habit_id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class TaskUpdate(BaseModel):
    completed: Optional[bool] = None
    name: Optional[str] = None
    
class Completed(Base):
    __tablename__ = "tracker_completed"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    habit_id = Column(UUID(as_uuid=True))
    day = Column(String)
    completed = Column(Boolean, default=True)
    volume_actual = Column(Integer, nullable=True)
    volume_units = Column(String, nullable=True)

class CompInput(BaseModel):
    habit_id: str
    day: str
    completed: Optional[bool]
    volume_actual: Optional[int] = None
    volume_units: Optional[str] = None

    
class NoteInput(BaseModel):
    tracker_id: int
    note_created: str
    note: str

class Stats(BaseModel):
    habit_id: str
    category: int
    habit_name: str
    total_instances: int
    completed_instances: int
    weeks_elapsed: int
    volume_units: Optional[str]
    completed_volume: Optional[int]
    
class CountdownCreate(BaseModel):
    user_id: str
    countdown: int = Field(..., gt=0)
    # state: str = Field(..., regex="^(running|stopped|completed)$")

class Countdown(Base):
    __tablename__ = "tracker_countdowns"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    countdown = Column(Integer)
    elapsed = Column(Integer, nullable=True)
    state = Column(String)
    created_at = Column(String, default=datetime.now())
    
class Timer(Base):
    __tablename__ = "tracker_timers"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    tracker_id = Column(UUID(as_uuid=True))
    time = Column(Integer)
    
class TimerCreate(BaseModel):
    user_id: str
    tracker_id: str
    time: int
    
class TimeStateInput(BaseModel):
    state: str
    
class TimeInput(BaseModel):
    elapsed: int

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, nullable=True)
    email = Column(String)
    role = Column(String, nullable=True)

class UserInput (BaseModel):
    username: Optional[str]
    email: str  
    
class NoteInput(BaseModel):
    habitId: Optional[str]
    created: str
    text: str
    ai: Optional[bool]
    
class NoteUpdate(BaseModel):
    text: str

class Note(Base):
    __tablename__ = "habit_notes"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True))
    note_created = Column(String)
    text = Column(String)
    ai = Column(Boolean, default=False)
    
class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String)
    description = Column(String)
    examples = Column(String)
