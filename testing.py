import requests

if __name__ == '__main__':

    # Test for get_random_bird_name function
    print("\nTesting get_random_bird_name function...")
    response = requests.get("http://127.0.0.1:5000/api/random_bird")
    if response.status_code == 200:
        random_bird = response.json()["random_common_name"]
        print("  >> Random Bird Name:", random_bird)
    else:
        print("** Error fetching random bird. Try again! **")

    # Test for get_recent_observations function
    print("\nTesting get_recent_observations function...")
    lat = 42.4613413
    lng = -76.5054578
    response = requests.get(f"http://127.0.0.1:5000/api/birds", params={'lat': lat, 'lng': lng})
    if response.status_code == 200:
        observations = response.json()
        if observations:
            for observation in observations:
                print("  >> Recent Observation: " + observation['comName'], observation['sciName'], observation['locName'],
                      observation['obsDt'], observation['howMany'])
        else:
            print("No observations returned.")
    else:
        print("** Failed to fetch bird observations. Try again! **")
