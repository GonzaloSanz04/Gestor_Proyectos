from fastapi import FastAPI, status

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
