from fastapi import FastAPI

app = FastAPI()

@app.get("/miapp")
def hola_mundo():
    return {"message": "hola mundo"}