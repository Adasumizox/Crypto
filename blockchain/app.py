import uvicorn

from Blockchain import Blockchain
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

if __name__ == '__main__':
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    blockchain = Blockchain()
    templates = Jinja2Templates(directory="templates")

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get('/homepage', response_class=HTMLResponse)
    def home(request: Request):
        # TODO: Home html with option of checking balance, making transaction and checking blockchain
        # Should have logic checking if user is actually logged
        return templates.TemplateResponse("home.html", {"request": request})

    @app.get('/login')
    def login(request: Request):
        result = "Enter your credentials"
        return templates.TemplateResponse("login.html", {"request": request, "result": result})

    @app.post('/login')
    def login(request: Request, login: str = Form(...), password: str = Form(...)):
        # TODO: Change result to method checking credentials
        result = None
        return templates.TemplateResponse("login.html", {"request": request, "result": result})

    @app.get('/register')
    def register(request: Request):
        result = "Enter your credentials"
        return templates.TemplateResponse("register.html", {"request": request, "result": result})

    @app.post('/register')
    def register(request: Request):
        # TODO: Change result to method creating account
        result = None
        return templates.TemplateResponse("register.html", {"request": request, "result": result})

    @app.get('/chain')
    def get_chain():
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    @app.get('/balance')
    def get_balance():
        # TODO: Get balance of account
        return None

    @app.post('/transaction')
    def make_transaction():
        # TODO: Make transaction
        return None


    uvicorn.run(app, host="127.0.0.1", port=8000)