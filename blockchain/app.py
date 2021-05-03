import uvicorn

from Blockchain import Blockchain
from fastapi import FastAPI, Request
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

    @app.get('/chain')
    def get_chain():
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    # @app.get('/balance')
    # def get_balance():
    #     return None
    #
    # @app.post('/transaction')
    # def make_transaction():
    #     return None
    #
    # @app.post('/login')
    # def login():
    #     message = ''
    #     if request.method == 'POST':
    #         username = request.form.get('username')
    #         password = request.form.get('password')
    #
    #         # if in database and password correct
    #         message = "Correct username and password"
    #         redirect()
    #         # else
    #         message = "Wrong username or password"
    #
    # @app.post('/register')
    # def register():
    #     message = ''
    #     if request.method == 'POST':
    #         email = request.form.get('email')
    #         username = request.form.get('username')
    #         password = request.form.get('password')
    #
    #         # if username already exist
    #         message = "Username is taken please choose other nickname"
    #         return redirect(url_for('registerpage'))
    #         # else
    #         message = "succesfully created"

#    @app.get('/loginpage')
#    def loginpage():
#        return

#    @app.get('/registerpage')
#    def registerpage():
#        return
#
#     @app.get('/homepage')
#     def home():
#         # Should have logic checking if user is actually logged
#         return templates.get_template('home.html')

    uvicorn.run(app, host="127.0.0.1", port=8000)