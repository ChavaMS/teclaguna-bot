from flask import Flask, render_template, request
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
import numpy as np
import pandas as pd

"""EXCEL"""
xls = pd.ExcelFile('database.xlsx')
df = xls.parse("Entrenamiento principal")
arrs = np.array(df)
info = []
for arr in arrs:
    info = np.concatenate((info,arr), axis=0)
info = info.tolist()

app = Flask(__name__)
CORS(app)

tec_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter", read_only=True)
trainer = ChatterBotCorpusTrainer(tec_bot)
trainer = ListTrainer(tec_bot)
trainer.train(info)

disparate=Statement('mantequilla')

global mantequilla
global mensajeUsuarioAnterior
mensajeUsuarioAnterior = ''
mantequilla = False

trainError = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    global mensajeUsuarioAnterior
    global mantequilla

    if mantequilla:
        trainError = [mensajeUsuarioAnterior, userText]
        print(trainError)
        trainer.train(trainError)
        mantequilla = False
        return 'Aprendí que si preguntas: '+mensajeUsuarioAnterior+'\n Debo responder: '+userText

    if userText=='mantequilla':
        mantequilla = True
        return str('Qué debería haber dicho?')

    mensajeUsuarioAnterior = userText
    return str(tec_bot.get_response(userText))

if __name__ == "__main__":
    app.run()