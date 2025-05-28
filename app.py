from flask import Flask, render_template, request
from models import ProductChatBot
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product_name = request.form['product_name']  
        bot = ProductChatBot()
        result = bot.estimate_price(product_name)  
        return render_template('index.html', result=result, product_name=product_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)