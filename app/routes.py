from fastapi import APIRouter, HTTPException, Request
import httpx

router = APIRouter()

BASE_URL = "https://jsonplaceholder.typicode.com"

@router.get("/proxy/{resource}")
async def proxy_get(resource: str, request: Request):
    """
    Proxy dinámico que reenvía la petición GET a JSONPlaceholder.
    """

    # --- Seguridad básica ---
    # ✅ Validar que el recurso es "seguro" (evitamos SSRF o rutas maliciosas)
    allowed_resources = {"posts", "comments", "users", "albums", "photos", "todos"}
    if resource not in allowed_resources:
        raise HTTPException(status_code=400, detail="Recurso no permitido")

    # --- Query params ---
    query_params = dict(request.query_params)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/{resource}", params=query_params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error al contactar con servicio externo: {str(e)}")
