from flask import Flask, Blueprint, request, jsonify, abort, make_response, current_app as app
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/")
def get_best_deal():
    request_url = request.args.get("request_url", None)

    if request_url is None:
        abort(make_response(jsonify(error="request url argument not given"), 400))

    html = requests.get(request_url)
    s = BeautifulSoup(html.content, 'html.parser')
    page = s.find(id='mainPageContent')
    dirtyPrices = page.find_all('div', class_='price')
    dirtyTitles = page.find_all('a', class_='title')
    dirtyKms = page.find_all('div', class_='details')
    dirtyUrl = page.find_all('')
    prices = [dirtyPrice.text.strip().replace(",", "")[1:-3] for dirtyPrice in dirtyPrices]
    years = [dirtyTitle.text.strip()[:4] for dirtyTitle in dirtyTitles]
    kms = [''.join(filter(str.isdigit, dirtyKm.text)) for dirtyKm in dirtyKms]


    for year in years: print("Year:",year)
    for km in kms: print("Km:",km)
    for price in prices: print("Price:",price)

    # for price in prices:
    #     if(price )
    # #loop for every object
    # distLeft = 300000 - km
    # kmRating = distLeft / 300000
    # yearLeft = year - (2023 - 15)
    # ageRating = yearLeft / 15
    # if kmRating < ageRating:
    #     lifeScore = kmRating
    # else:
    #     lifeScore = ageRating
    # totalScore = lifeScore / price #lower score is better
    # totalScore = totalScore * 1000

    return 10
