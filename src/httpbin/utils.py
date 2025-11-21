import base64
from typing import Any, Dict
from fastapi import Request, UploadFile
from fastapi.datastructures import FormData


async def get_request_data(request: Request) -> Dict[str, Any]:
    """Extract comprehensive request data"""

    # Get query parameters
    args = dict(request.query_params)

    # Get headers
    headers = dict(request.headers)

    # Get client IP
    origin = request.client.host if request.client else "unknown"

    # Get URL
    url = str(request.url)

    # Get method
    method = request.method

    # Initialize data containers
    data = ""
    json_data = None
    form_data = {}
    files = {}

    # Try to parse body based on content type
    content_type = headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            json_data = await request.json()
        except Exception:
            pass
    elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            for key, value in form.items():
                if isinstance(value, UploadFile):
                    files[key] = {
                        "filename": value.filename,
                        "content_type": value.content_type,
                    }
                else:
                    form_data[key] = value
        except Exception:
            pass
    else:
        # Read raw body
        try:
            body_bytes = await request.body()
            data = body_bytes.decode("utf-8") if body_bytes else ""
        except Exception:
            pass

    return {
        "args": args,
        "data": data,
        "files": files,
        "form": form_data,
        "headers": headers,
        "json": json_data,
        "method": method,
        "origin": origin,
        "url": url,
    }


def decode_base64(value: str) -> str:
    """Decode base64 string"""
    try:
        decoded_bytes = base64.b64decode(value)
        return decoded_bytes.decode("utf-8")
    except Exception as e:
        return f"Error decoding base64: {str(e)}"


def encode_base64(value: str) -> str:
    """Encode string to base64"""
    try:
        encoded_bytes = base64.b64encode(value.encode("utf-8"))
        return encoded_bytes.decode("utf-8")
    except Exception as e:
        return f"Error encoding base64: {str(e)}"
