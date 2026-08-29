from fastapi import FastAPI

from app.api.support import router as support_router


app = FastAPI(
    title="Multi-Agent Customer Support AI",
    description=(
        "AI-powered multi-agent customer support system."
    ),
)

app.include_router(support_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "customer-support",
    }