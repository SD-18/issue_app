from fastapi import FastAPI
from database import Base, engine
from routes import auth, user, issue
from middlewares.auth_middleware import AuthMiddleware
from middlewares.role_middleware import RoleMiddleware
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.performance_middleware import PerformanceMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# ✅ Initialize FastAPI app
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
app = FastAPI(
    title="Issue Reporting API",
    debug=debug_mode,
    description="API for managing issue reporting and tracking."
)

# ✅ Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ✅ Conditional Database Table Creation (Development Only)
if os.getenv("ENV", "development") == "development":
    try:
        logging.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created successfully!")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")

# ✅ Register Middlewares (Execution Order Matters)
app.add_middleware(AuthMiddleware)
app.add_middleware(RoleMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(PerformanceMiddleware)

# ✅ Enable CORS for Frontend Communication
allow_origins = ["*"]
#allow_origins = ["http://localhost:3000"] if os.getenv("ENV") == "development" else ["https://your-production-frontend.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include Routers
try:
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(issue.router)
except Exception as e:
    logging.error(f"Error including routers: {e}")

# ✅ Root Endpoint to Verify API is Running
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Issue Reporting App API is running successfully!"}

# ✅ Health Check Endpoint
@app.get("/health", tags=["Health"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy"}
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        env = os.getenv("ENV", "development")
        return {"status": "unhealthy", "details": str(e) if env == "development" else "Error details hidden"}