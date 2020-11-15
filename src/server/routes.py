from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

html_content = """
    <html>
        <head>
            <title>TestPage</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """

@router.get("/info")
async def sendInfo():
    return HTMLResponse(content=html_content, status_code=200)
