from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from models import Base
from sqlalchemy.exc import OperationalError
from database import SessionLocal, engine
from langchain.indexes import SQLRecordManager
from dotenv import load_dotenv, find_dotenv
from routes import file, tracker, user
from fastapi.responses import JSONResponse
from exceptions import UnicornException
import logging
import time

#jjLvpAUbWKs7fw1z

import sentry_sdk
sentry_sdk.init(
    dsn="https://f71e49ef94245eda96443ae6fff4040c@o1223284.ingest.sentry.io/4506444979240960",
    traces_sample_rate=1.0,
    send_default_pii=True,
)



load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

CONNECTION_STRING = "postgresql+psycopg2://admin:admin@127.0.0.1:5432/postgres"
COLLECTION_NAME = "vectordb"

# Update namespace to reflect PGVector
namespace = f"pgvector/{COLLECTION_NAME}"
record_manager = SQLRecordManager(
    namespace, db_url=CONNECTION_STRING
)
# Create schema for the record manager
record_manager.create_schema()


try:
    Base.metadata.create_all(bind=engine)
except OperationalError:
    # Handle the case where the database does not exist
    print("Database does not exist")

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3001",
    "http://localhost:3000",
]

class TimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TimeMiddleware)

app.include_router(file.router)
app.include_router(tracker.router)
app.include_router(user.router)
print(tracker.router)

    
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    logger.error(f"UnicornException: {exc.name}", exc_info=True)
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )
    
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."},
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}




# @app.on_event("startup")
# def start_scheduler():
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(process_habits, "interval", minutes=10)
#     scheduler.start()

        
    