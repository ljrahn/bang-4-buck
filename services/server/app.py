from flask import Flask, Blueprint, request, jsonify, abort, make_response
from bs4 import BeautifulSoup
from utils.helper_functions import async_aiohttp_get_all
import requests

app = Flask(__name__)

#thanks chatGPT

@app.route("/")
def get_best_deal():
    request_url = request.args.get("request_url", None)

    if request_url is None:
        abort(make_response(jsonify(error="request url argument not given"), 400))

    html = requests.get(request_url)
    s = BeautifulSoup(html.content, 'html.parser')

    dirtyPrices = s.find_all('div', class_='price')
    dirtyTitles = s.find_all('a', class_='title')
    dirtyKms = s.find_all('div', class_='details')
    dirtyUrls = s.find_all('a', class_='title')
    prices = [dirtyPrice.text.strip().replace(",", "")[1:-3] for dirtyPrice in dirtyPrices]
    years = [dirtyTitle.text.strip()[:4] for dirtyTitle in dirtyTitles]
    kms = [''.join(filter(str.isdigit, dirtyKm.text)) for dirtyKm in dirtyKms]
    urls = ["https://www.kijiji.ca" + dirtyUrl.get("href") for dirtyUrl in dirtyUrls]

    dirtyLinks = s.find_all('div', class_='pagination')
    dirtyPages = dirtyLinks[0].find_all('a', href=True)
    pages = ["https://www.kijiji.ca" + dirtyPage.get("href") for dirtyPage in dirtyPages]
    numberPages = str(dirtyPages).count("href") - 1
    pages = pages[:numberPages-1]
    print(pages)
    
    if numberPages > 0:
        content_list = async_aiohttp_get_all(pages)
        print(content_list[0])
        for content in content_list:
            s = BeautifulSoup(content, 'html.parser')
            dirtyPrices = s.find_all('div', class_='price')
            dirtyTitles = s.find_all('a', class_='title')
            dirtyKms = s.find_all('div', class_='details')
            dirtyUrls = s.find_all('a', class_='title')
            prices.extend([dirtyPrice.text.strip().replace(",", "")[1:-3] for dirtyPrice in dirtyPrices])
            years.extend([dirtyTitle.text.strip()[:4] for dirtyTitle in dirtyTitles])
            kms.extend([''.join(filter(str.isdigit, dirtyKm.text)) for dirtyKm in dirtyKms])
            urls.extend(["https://www.kijiji.ca" + dirtyUrl.get("href") for dirtyUrl in dirtyUrls])

    # for year in years: print("Year:",year)
    # for km in kms: print("Km:",km)
    # for price in prices: print("Price:",price)
    # for url in urls: print("Url:",url)
    # print(len(years))
    # print(len(kms))
    # print(len(prices))
    # print(len(urls))

    scores = [0] * len(prices)
    for i in range(len(prices)):
        if str.isdigit(kms[i]) and str.isdigit(years[i]) and str.isdigit(prices[i]):
            if int(kms[i]) > 100 and int(kms[i]) < 300000 and int(years[i]) > 2008 and int(prices[i]) > 1000 and urls[i][21] == "/": 
                distLeft = 300000 - int(kms[i])
                kmRating = distLeft / 300000
                yearLeft = int(years[i]) - (2023 - 15)
                ageRating = yearLeft / 20
                if kmRating < ageRating:
                    lifeScore = kmRating
                else:
                    lifeScore = ageRating
                scores[i] = lifeScore / int(prices[i]) * 100000 #higher score is better
                #print(years[i], kms[i], prices[i], scores[i])

    n = 10
    sorted_numbers = [(score, index) for index, score in enumerate(scores)]
    sorted_numbers.sort(key=lambda x: x[0], reverse=True)
    largest_numbers = sorted_numbers[:n]
    winnerIndexs = [index for number, index in largest_numbers]
    winnerUrls = []
    for index in winnerIndexs: winnerUrls.append(urls[index])
    return winnerUrls
