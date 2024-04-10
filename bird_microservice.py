from flask import Flask, jsonify, request
import requests
import random

app = Flask(__name__)
EBIRD_API_TOKEN = '9dmqlr17c65a'  # my personal API code, DO NOT SHARE


@app.route('/api/random_bird', methods=['GET'])
def random_bird_name_api():
    """Jsonify the returning string name of bird"""

    random_common_name = get_random_bird_name()
    if random_common_name:
        return jsonify({"random_common_name": random_common_name})
    else:
        jsonify({"error": "Failed to fetch a random bird name."}), 500


def get_random_bird_name():
    """
    Retrieves a randomly selected common bird name from eBird when called.

    Parameters:
    - None

    Returns:
    - random_common_name (str): randomly selected common bird name
    """

    url = 'https://api.ebird.org/v2/ref/taxonomy/ebird'
    headers = {'X-eBirdApiToken': EBIRD_API_TOKEN}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.text.split('\n')  # split the response by lines to extract 2nd line
        common_names = [line.split(',')[1] for line in data if line.strip()]

        if common_names:
            random_common_name = random.choice(common_names)
            return random_common_name
        else:
            return None

    except Exception as e:
        print(f"Failed to fetch eBird taxonomy: {e}")
        return None


@app.route('/api/birds', methods=['GET'])
def get_recent_observations():
    """
    Retrieves recent bird observations based on latitude and longitude.

    Parameters:
    - lat (float): latitude
    - lng (float): longitude

    Returns:
    - list: list of recent bird observations as dictionaries
    """

    lat = request.args.get('lat')
    lng = request.args.get('lng')

    # needed parameters for endpoints from eBird API
    back = request.args.get('back', 2)
    dist = request.args.get('dist', 5)
    hotspot = request.args.get('hotspot', False)
    includeProvisional = request.args.get('includeProvisional', False)
    maxResults = request.args.get('maxResults', None)
    sort = request.args.get('sort', 'date')
    sppLocale = request.args.get('sppLocale', 'en')
    cat = request.args.get('cat', None)

    url = 'https://api.ebird.org/v2/data/obs/geo/recent'
    headers = {'X-eBirdApiToken': EBIRD_API_TOKEN}
    params = {
        'lat': lat,
        'lng': lng,
        'back': back,
        'dist': dist,
        'hotspot': hotspot,
        'includeProvisional': includeProvisional,
        'maxResults': maxResults,
        'sort': sort,
        'sppLocale': sppLocale,
        'cat': cat
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch bird observations"}), response.status_code


if __name__ == '__main__':
    app.run(debug=True, port=5000)

