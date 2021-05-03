from Blockchain import Blockchain
from flask import Flask, render_template
import json

if __name__ == '__main__':
    app = Flask(__name__)
    blockchain = Blockchain()


    @app.route('/chain', methods=['GET'])
    def get_chain():
        chain_data = []
        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        return json.dumps({"length": len(chain_data), "chain": chain_data})

    @app.route('/login', methods=['POST'])

    @app.route('/register', methods=['POST'])

    @app.route('/loginpage', methods=['GET'])

    @app.route('/registerpage', methods=['GET'])


    @app.route("/")
    def index():
        # I tried to lean new framework flask and make views with template html but it didn't work so i did it
        # atrocious way
        return """
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Shitcoin</title>
        </head>
        <body>
            <header id="nav-wrapper>
                <nav id="nav">
                    <div class="nav left">
                        <span class="gradient skew>
                            <h1 class="logo un-skew>
                                <a href="">$4!t©o!n</a>
                            </h1>
                        </span>
                    </div>
                    <div class="nav right">
                        <a href="loginpage" class="nav-link active">
                            <span class="nav-link-span">
                                <span class="u-nav">Login</span>
                            </span>
                        </a>
                        <a href="registerpage" class="nav-link">
                            <span class="nav-link-span">
                                <span class="u-nav">Register</span>
                            </span>
                        </a>
                    </div>
                </nav>
            </header>
            <main>
            </main>
        </body>
        </html>
        """

    app.run(debug=True, port=5000)