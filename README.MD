# Store all domain directories inside src folder
- src/ - highest level of an app, contains common models, configs, and constants, etc.
- src/main.py - root of the project, which inits the FastAPI app
# Each package has its own router, schemas, models, etc.
- router.py - is a core of each module with all the endpoints
- schemas.py - for pydantic models
- models.py - for db models
- service.py - module specific business logic
- dependencies.py - router dependencies
- constants.py - module specific constants and error codes
- config.py - e.g. env vars
- utils.py - non-business logic functions, e.g. response normalization, data enrichment, etc.
- exceptions.py - module specific exceptions, e.g. PostNotFound, InvalidUserData
  # Best practices 
  https://github.com/zhanymkanov/fastapi-best-practices