from fastapi import APIRouter, Request, HTTPException
import httpx

router = APIRouter()

ALLOWED_RESOURCES = {"posts", "comments", "users"}

BASE_URL = "https://jsonplaceholder.typicode.com"

@router.api_route("/proxy/{resource}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(resource: str, request: Request):
    if resource not in ALLOWED_RESOURCES:
        raise HTTPException(status_code=400, detail="Recurso no permitido")

    # Construir la URL destino
    url = f"{BASE_URL}/{resource}"

    try:
        async with httpx.AsyncClient() as client:
            if request.method == "GET":
                response = await client.get(url)
            elif request.method == "POST":
                body = await request.json()
                response = await client.post(url, json=body)
            elif request.method == "PUT":
                body = await request.json()
                response = await client.put(url, json=body)
            elif request.method == "DELETE":
                response = await client.delete(url)

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error al contactar con servicio externo: {str(e)}")
