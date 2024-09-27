import json
with open('daejeon_restaurants.json', 'r', encoding='utf-8') as f:
    results = json.load(f)
    print(results[1])
with open('restaurant_analysis.json', "r", encoding="utf-8") as g:
    asd = json.load(g)
    print(asd[1])

