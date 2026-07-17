from http.client import HTTPException
from time import perf_counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.graph import graph

app = FastAPI()

# Allow requests from your browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Job(BaseModel):
    url: str
    title: str
    description: str


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.post("/job")
def receive_job(job: Job):
    start = perf_counter()

    try:
        result = graph.invoke(
            {
                "job_url": job.url,
                "job_title": job.title,
                "job_description": job.description,
            }
        )

        return {
            "status": "success",
            "analysis": result["analysis"],
            "processing_time_sec": round(
                perf_counter() - start,
                2,
            ),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)



#     python -m uvicorn main:app --reload