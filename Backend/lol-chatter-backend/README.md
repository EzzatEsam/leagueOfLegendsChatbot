# Lol chatbot backend

A fastAPI application for the lol chatbot. handles user authentication, chat sessions and chat history. 
Automatically gets league of legends data from cdn.merakianalytics.com. Provides chatting functionalities using the google generative AI SDK.

## Usage 

### Install dependencies

```bash
poetry install

```
### Run the app
```bash
uvicorn lol_chatter_backend.main:app --reload
```
You can remove the `--reload` flag if you want to run the app without hot reloading functionality.

