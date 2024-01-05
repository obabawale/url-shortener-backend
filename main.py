from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import secrets

app = FastAPI()

class URLItem(BaseModel):
    original_url: str

url_database = {}

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten/")
def shorten_url(url_item: URLItem):
    # Generate a short URL using secrets module
    short_url = secrets.token_urlsafe(6)

    # Store the mapping between short URL and original URL in the database
    url_database[short_url] = url_item.original_url

    # Return the short URL in the response
    return {"short_url": short_url}

@app.get("/{short_url}")
def redirect_to_original(short_url: str):
    # Retrieve the original URL from the database
    original_url = url_database.get(short_url)

    # If the original URL exists, redirect to it
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        # If the short URL is not found in the database, return an error response
        return {"error": "URL not found"}