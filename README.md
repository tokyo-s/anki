# Anki API

A FastAPI application that provides an API for adding cards to Anki decks.

## Setup

1. Clone this repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on the `.env.example` template:
   ```
   cp .env.example .env
   ```
4. Update the `.env` file with your actual Anki cookie (you can get this from your browser's developer tools when logged into AnkiWeb)

## Running the API

Start the API server:

```
python anki_fastapi.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Add a Single Card

```
POST /add-card
```

Request body:
```json
{
  "front": "Front text",
  "back": "Back text",
  "deck_name": "default"
}
```

### Add Multiple Cards

```
POST /add-multiple-cards
```

Request body:
```json
{
  "cards": [
    {
      "front": "Front text 1",
      "back": "Back text 1"
    },
    {
      "front": "Front text 2",
      "back": "Back text 2"
    }
  ],
  "deck_name": "default",
  "delay": 1.0
}
```

### List Available Decks

```
GET /decks
```

### Health Check

```
GET /health
```

## Connecting to a Custom GPT

To connect this API to a Custom GPT:

1. Deploy this API to a server with a public URL
2. In your Custom GPT configuration, add an "API Action" with the following details:
   - API URL: Your server URL (e.g., https://your-server.com)
   - Authentication: None (or add appropriate authentication if you implement it)
   - OpenAPI Schema: Copy the schema from http://your-server.com/openapi.json

## Supported Decks

Currently, the API supports the following decks:
- default
- test
- life_tricks

To add support for more decks, modify the `add_anki_card` function in `anki_api.py`. 