from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    from .routes import main
    app.register_blueprint(main)
    
    return app