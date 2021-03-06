import uvicorn

from Blockchain import Blockchain
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from blockchain.database import schemas, crud, models
from blockchain.database.db import SessionLocal, engine
from blockchain import Transaction
import json

if __name__ == '__main__':
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")
    blockchain = Blockchain()
    templates = Jinja2Templates(directory="templates")

    def get_db():
        """
        Creating local session for database for API
        """
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        """

        :param request: Request of user
        :return: Jinja2 interface for user
        """
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get('/homepage', response_class=HTMLResponse)
    def home(request: Request):
        """

        :param request: Request of user
        :return: Jinja2 interface for user
        """
        # TODO: Home html with option of checking balance, making transaction and checking blockchain
        # Should have logic checking if user is actually logged
        return templates.TemplateResponse("home.html", {"request": request})

    @app.get('/login')
    def login(request: Request):
        """

        :param request: Request of user
        :return: Jinja2 interface for user
        """
        result = "Enter your credentials"
        return templates.TemplateResponse("login.html", {"request": request, "result": result})

    @app.post('/login')
    def login(request: Request, login: str = Form(...), password: str = Form(...)):
        """

        :param request: Request of user
        :param login: login of user received from form
        :param password: password of user received form form
        :return: Jinja2 interface for user
        """
        # TODO: Change result to method checking credentials
        result = None
        return templates.TemplateResponse("login.html", {"request": request, "result": result})

    @app.post('/user/create', response_model=schemas.UserCreate)
    def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
        """

        :param user: Information needed for user creation
        :param db: Dependency Injection of database
        :return: result of user creation
        """
        db_user = crud.get_user_by_login(db=db, login=user.login)
        db_email = crud.get_user_by_email(db=db, email=user.email)
        if db_user or db_email:
            raise HTTPException(status_code=400, detail="Account already registered. Please check email/login")
        return crud.create_user(db=db, user=user)

    @app.post('/user/verify')
    def verify_user(login: str, password: str, db: Session = Depends(get_db)):
        """

        :param login: login of user
        :param password: password of user
        :param db: Dependency Injection of database
        :return: result of verification
        """
        db_user = crud.get_user_by_login(db=db, login=login)
        if not db_user or db_user.password != password:
            raise HTTPException(status_code=400, detail="Logon failed")
        # TODO: Add verification to CRUD or create separated method for it
        return "User verified"


    @app.get('/register')
    def register(request: Request):
        """

        :param request: Request of user
        :return: Jinja2 interface for user
        """
        result = "Enter your credentials"
        return templates.TemplateResponse("register.html", {"request": request, "result": result})

    @app.post('/register')
    def register(request: Request, email: str = Form(...), login: str = Form(...), password: str = Form(...)):
        """

        :param request: Request of user
        :param email: Email that user provided in form
        :param login: Login that user provided in form
        :param password: Password that user provided in form
        :return: Jinja2 interface for user
        """
        # TODO: Change result to method creating account
        result = None
        return templates.TemplateResponse("register.html", {"request": request, "result": result})

    @app.get('/chain')
    def get_chain():
        """

        :return: length and description of blockchain
        """
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    @app.get('/balance/{user_id}')
    def get_balance(user_id: int, db: Session = Depends(get_db)):
        """

        :param user_id: id of user
        :return: balance of account
        """
        if model := crud.get_user(db=db, id=user_id):
            return model.balance
        raise HTTPException(status_code=404, detail="User does not exist")


    @app.post('/transaction')
    def make_transaction(sender_id: int, receiver_id: int, amount: float):
        """

        :param sender_id: Id of account from which we want to send money
        :param receiver_id: Id of account to which we want to send money
        :param amount: Amount that we want to send
        :return: Transaction added to blockchain
        """
        sender = crud.get_user(sender_id)
        receiver = crud.get_user(receiver_id)
        if not sender and receiver:
            raise HTTPException(status_code=404, detail="Sender or receiver not found")
        return Blockchain.add_new_transaction(Transaction(sender_id, receiver_id, amount))


    uvicorn.run(app, host="127.0.0.1", port=8000)