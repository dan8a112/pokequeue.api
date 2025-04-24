import json
import logging

from fastapi import HTTPException
from models.PokeRequest import PokeRequest
from utils.database import execute_query_json
from utils.AQueue import AQueue


# configurar el logging
logging.basicConfig(level=logging.INFO)
loggerr = logging.getLogger(__name__)

async def select_pokemon_request(id: int) -> dict:
    try:
        query = " select * from pokequeue.requests where id = ? "
        params = (id,)
        result = await execute_query_json( query, params )
        result_dict = json.loads( result )

        return result_dict
    except Exception as e:
        loggerr.error(f"Error selecting pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def insert_pokemon_request(pokemon_request: PokeRequest) -> dict:
    try:
        query = " exec pokequeue.create_poke_request ? "
        params = (pokemon_request.pokemon_type,)
        result = await execute_query_json( query, params, True )
        result_dict = json.loads( result )

        await AQueue('AZURE_SAK', 'AZURE_NAME').insert_message_on_queue( result )

        return result_dict
    except Exception as e:
        loggerr.error(f"Error inserting pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
async def update_pokemon_request(pokemon_request: PokeRequest) -> dict:
    try:
        query = " exec pokequeue.update_poke_request ?, ?, ? "

        if not pokemon_request.url:
            pokemon_request.url = ""
        
        params = (pokemon_request.id, pokemon_request.status, pokemon_request.url)
        result = await execute_query_json( query, params, True )
        result_dict = json.loads( result )
        return result_dict
    except Exception as e:
        loggerr.error(f"Error inserting pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
async def delete_pokemon_request(id: int) -> dict:
    try:
        query = " exec pokequeue.delete_poke_request ? "
        params = (id,)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)

        # Manejo de error esperado: reporte no encontrado
        if result_dict[0]['completed'] == 0:
            raise HTTPException(status_code=404, detail="El reporte a eliminar no se ha encontrado")

        return result_dict

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        loggerr.error(f"Error inesperado al eliminar el reporte de Pokémon: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error interno. Por favor, intente más tarde.")
    
async def delete_pokemon_to_queue(id: int) -> dict:
    try:
        query = " select id from pokequeue.requests where id = ? "
        params = (id,)
        result = await execute_query_json( query, params )
        result_dict = json.loads( result )

        if not result_dict:
            raise HTTPException(status_code=404, detail="El reporte a eliminar no se ha encontrado")

        await AQueue('AZURE_SAK', 'AZURE_NAME_DELETE').insert_message_on_queue( result )

        return result_dict
    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        loggerr.error(f"Error inserting pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")