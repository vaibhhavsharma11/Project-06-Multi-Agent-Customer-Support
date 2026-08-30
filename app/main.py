from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.support import router as support_router


app = FastAPI(
    title="Multi-Agent Customer Support AI",
    description=(
        "AI-powered multi-agent customer support system."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(support_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "customer-support",
    }
