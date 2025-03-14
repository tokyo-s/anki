from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Import the Anki API functions
from anki_api_v2 import add_anki_card, add_multiple_cards

# Load environment variables
load_dotenv()

# Get the authentication cookie from environment variables
DEFAULT_COOKIE = os.getenv(
    "ANKI_COOKIE",
    "has_auth=1; ankiweb=eyJvcCI6ImNrIiwiaWF0IjoxNzM2Nzk4ODI1LCJqdiI6MCwiayI6"
    "InZidTxTQ1EqOVFHb34uaTwiLCJjIjoyLCJ0IjoxNzM2Nzk4ODI1fQ.mwUZf4Fym4BWUbMTQF"
    "lAeHa-3bq9fOIdxsNl2W1bcEs",
)

# Create the FastAPI app
app = FastAPI(
    title="Anki API",
    description="API for adding cards to Anki decks",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define the request models
class CardBase(BaseModel):
    front: str = Field(..., description="Text for the front of the card")
    back: str = Field(..., description="Text for the back of the card")


class CardRequest(CardBase):
    deck_name: str = Field(
        default="default", description="Name of the deck to add the card to"
    )


class MultipleCardsRequest(BaseModel):
    cards: List[CardBase] = Field(..., description="List of cards to add")
    deck_name: str = Field(
        default="default", description="Name of the deck to add the cards to"
    )
    delay: float = Field(default=1.0, description="Delay in seconds between requests")


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


# Define the API endpoints
@app.post("/add-card", response_model=ApiResponse)
async def api_add_card(request: CardRequest):
    """
    Add a single card to an Anki deck
    """
    result = add_anki_card(
        front_text=request.front,
        back_text=request.back,
        deck_name=request.deck_name,
        cookie=DEFAULT_COOKIE,
        verbose=False,
    )

    if result["success"]:
        return {
            "success": True,
            "message": result["message"],
            "data": {"status_code": result["status_code"]},
        }
    else:
        raise HTTPException(
            status_code=result.get("status_code", 500), detail=result["message"]
        )


@app.post("/add-multiple-cards", response_model=ApiResponse)
async def api_add_multiple_cards(request: MultipleCardsRequest):
    """
    Add multiple cards to an Anki deck
    """
    cards = [(card.front, card.back) for card in request.cards]

    summary = add_multiple_cards(
        cards=cards,
        deck_name=request.deck_name,
        cookie=DEFAULT_COOKIE,
        delay=request.delay,
        verbose=False,
    )

    return {
        "success": summary["success"] > 0,
        "message": f"Added {summary['success']} out of {summary['total']} cards",
        "data": {
            "total": summary["total"],
            "success": summary["success"],
            "failed": summary["failed"],
        },
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


@app.get("/decks")
async def list_decks():
    """
    List available decks
    """
    # For now, just return the hardcoded decks we know about
    decks = ["default", "test", "life_tricks"]
    return {"decks": decks}


# Run the server if this file is executed directly
if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))

    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
