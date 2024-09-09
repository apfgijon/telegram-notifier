<p align="center">
<img src="web/public/logo.webp" width=200/>
</p>

# Aramo
Develop automated processors for messages from popular Telegram channels.

Use LLMs for process the messages based on your own instructions.

## Setup
### 1. Install TDLib dynamic library
Follow the instructions from [Td](https://github.com/tdlib/td) and build the library to have your `tdjson.dll`.
### 2. Install ollama
Follow the instructions from [Ollama page](https://ollama.com/)
### 3. Install requirements of Aramo backend
`pip install -r requirements.txt`
### 4. Install requirements of Aramo frontend
```
cd web
npm install
```
### 5. Create .env file
Create the .env file with this schema:
```
LANGUAGE=es
APP_ID=<app_id>
API_HASH=<api_hash>
TDJSON_LOCATION=<location of your tdlib.dll>

WAITING_TIMEOUT=1
HOST=localhost
PORT=8080
```
## Run backend
Now you can run the backend and init the app with:
`python main.py`
It will ask you for your phone number to bind the telegram account and the code in your telegram.
Now, it will download all group 10 first messages and process it.
## Run frontend
Acces to frontend and run it
```
cd web
npm run dev
```

## Prepare your own processors
In the file system_pormpts.txt you can define your LLM prompts.
System will use first line as identifier, following lines as system prompt and the message as user prompt.
If you put void line system will use it as separator of more prompts.
