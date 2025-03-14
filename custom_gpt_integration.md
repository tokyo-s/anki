# Integrating Anki API with a Custom GPT

This guide explains how to connect your Anki API to a Custom GPT, allowing the GPT to add cards to your Anki decks.

## Prerequisites

1. Your Anki API server is deployed and accessible via a public URL
2. You have access to create or modify a Custom GPT in ChatGPT

## Step 1: Get the OpenAPI Schema

When your FastAPI server is running, you can access the OpenAPI schema at:

```
https://your-server.com/openapi.json
```

This JSON file describes all the endpoints and data models of your API.

## Step 2: Create a Custom GPT

1. Go to ChatGPT: https://chat.openai.com/
2. Click on "Explore GPTs" or "Create a GPT"
3. In the GPT editor, click on "Configure"
4. Give your GPT a name, description, and instructions

## Step 3: Add the API to Your Custom GPT

1. In the GPT editor, go to the "Actions" tab
2. Click "Add action"
3. For "Authentication", select "None" (or add appropriate authentication if you've implemented it)
4. For "API schema", paste the OpenAPI schema from your server
5. Click "Save"

## Step 4: Configure the GPT's Instructions

Add instructions to your GPT about how to use the Anki API. For example:

```
You are an Anki assistant that helps users create flashcards. You can add cards to the user's Anki decks using the connected API.

Available decks:
- default
- test
- life_tricks

When a user wants to create a flashcard:
1. Ask for the front and back content if not provided
2. Ask which deck they want to add it to
3. Use the /add-card endpoint to add the card
4. Confirm to the user that the card was added successfully

For multiple cards, use the /add-multiple-cards endpoint.
```

## Step 5: Test Your Custom GPT

Try interacting with your GPT with prompts like:

- "Add a flashcard for the definition of photosynthesis"
- "Create a card with 'What is the capital of France?' on the front and 'Paris' on the back"
- "Add these vocabulary words to my Anki deck: [list of words and definitions]"

## Example Conversation

**User**: Add a flashcard about the Pythagorean theorem.

**GPT**: I'd be happy to add a flashcard about the Pythagorean theorem to your Anki deck. 

Which deck would you like to add it to? Your available options are:
- default
- test
- life_tricks

**User**: Add it to the default deck.

**GPT**: Great! I'll add a card about the Pythagorean theorem to your default deck.

For the card, I'll use:
- Front: What is the Pythagorean theorem?
- Back: The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse equals the sum of the squares of the lengths of the other two sides. It can be written as: a² + b² = c², where c is the hypotenuse.

Adding this card to your default deck now...

✅ Success! The card has been added to your default deck.

Is there anything else you'd like to add to your Anki decks?

## Troubleshooting

If your Custom GPT is having trouble connecting to your API:

1. Make sure your server is accessible from the internet
2. Check that the OpenAPI schema is correctly formatted
3. Verify that your server is handling CORS correctly
4. Check the server logs for any errors

## Security Considerations

- The current implementation doesn't include authentication for the API
- Consider adding API key authentication or other security measures for production use
- Make sure your Anki cookie is kept secure and rotated regularly 