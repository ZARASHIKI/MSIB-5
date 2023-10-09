import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from http import client
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def test_post():
    return render_template('about.html')


@app.route('/movie', methods=['GET'])
def info_get():
    movie_list = list(db.films.find({},{'_id':False}))
    return jsonify({'movies':movie_list})

@app.route('/movie', methods=['POST'])
def info_post():
    url = request.form['url_give']
    star = request.form['star_give']
    comment = request.form['comment_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    meta_image = soup.select_one('meta[property="og:image"]')
    meta_title = soup.select_one('meta[property="og:title"]')
    meta_description = soup.select_one('meta[name="description"]')
    image = meta_image['content']
    title = meta_title['content']
    desc = meta_description['content']
    doc = {
        'image': image,
        'title': title,
        'description': desc,
        'star': star,
        'comment': comment
    }
    db.films.insert_one(doc)
    return jsonify({
        'msg': 'Berhasil Menyimpan'
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
