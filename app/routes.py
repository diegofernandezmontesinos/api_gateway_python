from fastapi import APIRouter, Request, HTTPException, Depends
import httpx

router = APIRouter()

ALLOWED_RESOURCES = {"posts", "comments", "users"}
BASE_URL = "https://jsonplaceholder.typicode.com"

# API Key fija para pruebas (luego se guarda en variables de entorno)
API_KEY = "mi-super-api-key"

# --- Middleware de autenticación ---
async def verify_api_key(request: Request):
    key = request.headers.get("X-API-KEY")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")
    return True

@router.api_route("/proxy/{resource}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(resource: str, request: Request, _: bool = Depends(verify_api_key)):
    if resource not in ALLOWED_RESOURCES:
        raise HTTPException(status_code=400, detail="Recurso no permitido")

    url = f"{BASE_URL}/{resource}"

    # Limitar tamaño del body a 1MB
    if request.method in ("POST", "PUT"):
        body = await request.body()
        if len(body) > 1024 * 1024:
            raise HTTPException(status_code=413, detail="Payload demasiado grande")
        json_body = await request.json()
    else:
        json_body = None

    try:
        async with httpx.AsyncClient() as client:
            if request.method == "GET":
                response = await client.get(url)
            elif request.method == "POST":
                response = await client.post(url, json=json_body)
            elif request.method == "PUT":
                response = await client.put(url, json=json_body)
            elif request.method == "DELETE":
                response = await client.delete(url)

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error al contactar con servicio externo: {str(e)}")
