import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='/')

#FMP_API_KEY = ""
FMP_API_KEY = os.environ["FMP_API_KEY"]

@app.route('/api/financials/', methods=['GET'])
def get_financials():

    url = f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={FMP_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not isinstance(data, list):
        return jsonify({"error": "Unexpected data format from FMP."}), 500

    trimmed_data = []
    for item in data:
        trimmed_data.append({
            "date": item.get("date"),
            "revenue": item.get("revenue"),
            "netIncome": item.get("netIncome"),
            "grossProfit": item.get("grossProfit"),
            "eps": item.get("eps"),
            "operatingIncome": item.get("operatingIncome"),
        })

    start_year = request.args.get('startYear', type=int, default=None)
    end_year = request.args.get('endYear', type=int, default=None)
    min_revenue = request.args.get('minRevenue', type=float, default=None)
    max_revenue = request.args.get('maxRevenue', type=float, default=None)
    min_net_income = request.args.get('minNetIncome', type=float, default=None)
    max_net_income = request.args.get('maxNetIncome', type=float, default=None)

    filtered_data = []
    for row in trimmed_data:
        date_str = row.get('date', '')
        if date_str:
            try:
                year = int(date_str.split('-')[0])
            except ValueError:
                continue
        else:
            continue

        if start_year and year < start_year:
            continue
        if end_year and year > end_year:
            continue

        revenue = row.get('revenue', 0) or 0
        if min_revenue is not None and revenue < min_revenue:
            continue
        if max_revenue is not None and revenue > max_revenue:
            continue

        net_income = row.get('netIncome', 0) or 0
        if min_net_income is not None and net_income < min_net_income:
            continue
        if max_net_income is not None and net_income > max_net_income:
            continue

        filtered_data.append(row)

    sort_by = request.args.get('sortBy', default='date')  
    sort_order = request.args.get('sortOrder', default='asc') 
    reverse_sort = (sort_order == 'desc')

    def extract_year(item):
        if not item['date']:
            return 0
        return int(item['date'].split('-')[0])

    if sort_by == 'date':
        filtered_data.sort(key=extract_year, reverse=reverse_sort)
    else:
        filtered_data.sort(key=lambda x: x.get(sort_by, 0) or 0, reverse=reverse_sort)

    return jsonify(filtered_data)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
