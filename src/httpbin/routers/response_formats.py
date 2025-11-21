from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, Response

router = APIRouter(tags=["Response Formats"])


@router.get("/json")
async def get_json():
    """Returns a sample JSON response"""
    return JSONResponse({
        "slideshow": {
            "author": "Yours Truly",
            "date": "date of publication",
            "slides": [
                {"title": "Wake up to WonderWidgets!", "type": "all"},
                {
                    "items": [
                        "Why <em>WonderWidgets</em> are great",
                        "Who <em>buys</em> WonderWidgets"
                    ],
                    "title": "Overview",
                    "type": "all"
                }
            ],
            "title": "Sample Slide Show"
        }
    })


@router.get("/html", response_class=HTMLResponse)
async def get_html():
    """Returns a simple HTML page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>httpbin - HTML Response</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            p {
                line-height: 1.6;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>Herman Melville - Moby-Dick</h1>
        <p>
            Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse,
            and nothing particular to interest me on shore, I thought I would sail about a little and see the watery
            part of the world. It is a way I have of driving off the spleen and regulating the circulation.
        </p>
    </body>
    </html>
    """


@router.get("/xml")
async def get_xml():
    """Returns a sample XML response"""
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<slideshow>
    <title>Sample Slide Show</title>
    <author>Yours Truly</author>
    <date>date of publication</date>
    <slide type="all">
        <title>Wake up to WonderWidgets!</title>
    </slide>
    <slide type="all">
        <title>Overview</title>
        <item>Why <em>WonderWidgets</em> are great</item>
        <item>Who <em>buys</em> WonderWidgets</item>
    </slide>
</slideshow>"""

    return Response(content=xml_content, media_type="application/xml")


@router.get("/robots.txt")
async def get_robots_txt():
    """Returns a robots.txt file"""
    robots_content = """User-agent: *
Disallow: /deny
"""
    return Response(content=robots_content, media_type="text/plain")
