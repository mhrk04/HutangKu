"""
FastAPI main application - HutangKu - Debt Management Backend
Runs on port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import debt_router, company_router
from core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for managing personal debt records with BNPL tracking"
)

# CORS configuration - allows frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (no trailing slash in prefix, routes will be /debts, not /debts/)
app.include_router(debt_router.router, prefix="/debts", tags=["debts"])
app.include_router(company_router.router)  # prefix already set in router

@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint - API status check"""
    return {
    "message": "Welcome to the HutangKu - Debt Management API!",
        "version": settings.APP_VERSION,
        "status": "online"
    }

@app.get("/health", tags=["root"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=True
    )