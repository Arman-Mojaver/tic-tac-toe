from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="tictactoe")


@app.get("/health", status_code=200)
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
