import uvicorn
import json
from fastapi import FastAPI
from utils.database import execute_query_json
from controllers.PokeRequestController import insert_pokemon_request, update_pokemon_request, select_pokemon_request, delete_pokemon_to_queue, delete_pokemon_request, get_all_request
from models.PokeRequest import PokeRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


@app.get("/")
async def root():
    query = "select * from pokequeue.MESSAGES"
    result = await execute_query_json(query)
    result_dict = json.loads(result)
    return result_dict


@app.get("/api/version")
async def version():
    return {"version": "0.3.0"}

@app.get("/api/request/{id}")
async def create_request(id: int):
    return await select_pokemon_request(id)

@app.post("/api/request")
async def create_request(poquemon_request: PokeRequest):
    return await insert_pokemon_request(poquemon_request)

@app.put("/api/request")
async def update_request(poquemon_request: PokeRequest):
    return await update_pokemon_request(poquemon_request)

@app.delete("/api/request/{id}")
async def delete_request(id: int):
    return await delete_pokemon_request(id)

@app.post("/api/delete-request")
async def create_request(id: int):
    return await delete_pokemon_to_queue(id)

@app.get("/api/request")
async def select_all_request():
    return await get_all_request()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)