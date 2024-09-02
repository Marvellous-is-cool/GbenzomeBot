from flask import Flask

from threading import Thread
from dotenv import load_dotenv



app = Flask('')



@app.route('/')

def home():

    return "I'm alive"



def run():

  app.run(host='0.0.0.0',port=int(os.getenv('PORT', 8080)))



def keep_alive():  

    t = Thread(target=run)

    t.start()