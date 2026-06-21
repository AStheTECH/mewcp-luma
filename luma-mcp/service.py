import requests
from fastmcp_credentials import get_credentials
from config import LUMA_API_BASE, LUMA_API_VERSION, API_TIMEOUT


def _get_headers() -> dict[str, str]:
    cred = get_credentials()
    api_key = cred.fields.get("api_key")
    print("creds", cred)
    print("api_key", api_key)
    if not api_key:
        raise ValueError("Missing api_key in credentials")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def make_luma_request(
    method: str,
    endpoint: str,
    body: dict | None = None,
    params: dict | None = None,
) -> dict:
    url = f"{LUMA_API_BASE}/{LUMA_API_VERSION}/{endpoint.lstrip('/')}"
    try:
        resp = requests.request(
            method,
            url,
            headers=_get_headers(),
            json=body,
            params=params,
            timeout=API_TIMEOUT,
        )
        if resp.status_code == 204:
            return {"success": True}
        data = resp.json()
        if not resp.ok:
            error_msg = (
                data.get("message")
                or data.get("error")
                or data.get("detail")
                or data.get("msg")
                or f"HTTP {resp.status_code}"
            )
            return {"error": error_msg, "status_code": resp.status_code, "raw": data}
        return data
    except requests.RequestException as e:
        return {"error": str(e)}
