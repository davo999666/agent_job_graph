import json

from fastapi import FastAPI, HTTPException
from time import perf_counter

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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


from time import perf_counter




@app.post("/job")
def receive_job(job: Job):
    def generate():
        start = perf_counter()
        result = None
        try:
            input_state = {
                "job_url": job.url,
                "job_title": job.title,
                "job_description": job.description,
            }
            for stream_mode, data in graph.stream(
                input_state,
                stream_mode=["messages", "updates"],
            ):
                if stream_mode == "messages":
                    message_chunk, metadata = data

                    if metadata.get("langgraph_node") != "match":
                        continue

                    if message_chunk.content:
                        token = message_chunk.content

                        yield (
                            "event: token\n"
                            f"data: {json.dumps(token, ensure_ascii=False)}\n\n"
                        )

                elif stream_mode == "updates":
                    if "match" in data:
                        result = data["match"]

            if result is None:
                raise RuntimeError(
                    "The match node did not return a result."
                )
            done_data = {
                "processing_time_sec": round(perf_counter() - start,2)
            }
            yield (
                "event: done\n"
                f"data: {json.dumps(done_data)}\n\n"
            )
        except Exception as error:
            print(
                f"\nStreaming error: {error}",
                flush=True,
            )

            yield (
                "event: error\n"
                f"data: {json.dumps(str(error), ensure_ascii=False)}\n\n"
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)



#     python -m uvicorn main:app --reload