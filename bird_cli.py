import pyfiglet
import requests
import random


def main():
    """Main function for all program actions."""

    hello_message = pyfiglet.figlet_format("  Bird CLI", font="standard", width=80)
    goodbye_message = pyfiglet.figlet_format("  Goodbye", font="standard", width=80)
    print(hello_message)
    print('      >>>  Welcome Birder to the Bird CLI!')
    print('      >>>  This tool is for you to learn all about Birds.')
    print('      >>>  Use your NUMBER, LETTER, and ENTER keys to explore.')
    while True:
        print("\n")
        action = actions()
        if action == "Bird Pop Quiz":
            bird_questions()
        if action == "Random Bird Name Generator":
            random_bird_name()
        if action == "Find Recent Sightings":
            get_observation()
        if action == "Exit Bird CLI":
            break
    print(goodbye_message)
    quit()


def actions():
    """Main menu of action choices for the user."""

    print("  Select a Task by Number:")
    print("  1. Play Bird Pop Quiz")
    print("  2. Random Bird Name Generator")
    print("  3. Find Recent Sightings")
    print("  4. Exit Bird CLI")
    choice = input("\n  >> Enter your choice: ")
    if choice == "1":
        return "Bird Pop Quiz"
    elif choice == "2":
        return "Random Bird Name Generator"
    elif choice == "3":
        return "Find Recent Sightings"
    elif choice == "4":
        return "Exit Bird CLI"
    else:
        print("\n** Invalid choice. Try again! **")
        return None


def bird_questions():
    """Gives the user a random bird question to test their bird knowledge.
    Gives feedback on user response.
    Gives the option to continue answering questions or end pop quiz.
    """

    questions = [
        {"question": "Is the Bald Eagle the national bird of the United States?", "answer": "yes"},
        {"question": "Can all birds fly?", "answer": "no"},
        {"question": "Is the penguin a bird?", "answer": "yes"},
        {"question": "Do male ostriches lay eggs?", "answer": "no"},
        {"question": "Can hummingbirds hover in air?", "answer": "yes"},
        {"question": "Is the Kiwi bird native to Australia?", "answer": "no"},
        {"question": "Do flamingos feed with their heads upside down?", "answer": "yes"},
        {"question": "Can birds see colors?", "answer": "yes"},
        {"question": "Is the Albatross capable of flying for several days without landing?", "answer": "yes"},
        {"question": "Are all owls nocturnal?", "answer": "no"}
    ]

    print("\n  **  Welcome to the Bird Pop Quiz!  **")

    playing = True

    while playing:
        question = random.choice(questions)
        user_answer = input("\n  >>>  " + question["question"] + " (yes/no): ").lower().strip()

        if user_answer == question["answer"]:
            print("       Correct!")
        else:
            print("       Incorrect. The correct answer is:", question["answer"].capitalize())

        another = input("  >>>  Want another question? (yes/no): ").lower().strip()
        if another != "yes":
            playing = False
        else:
            playing = True

    print("\n  **  Thanks for playing the Bird Pop Quiz!  **")


def get_observation():
    """Searches for recent bird observations near a location by latitude, longitude to 7 decimals."""

    city_locations = {
        'Dallas': ('32.779167', '-96.808891'),
        'Fargo' : ('46.877186', '-96.789803'),
        'Seattle': ('47.608013', '-122.335167'),
        'Portland': ('45.523064', '-122.676483'),
        'Chicago': ('41.881832', '-87.623177'),
        'Miami': ('25.761681', '-80.191788')
    }

    print("\n  >> Get recent sightings by location")
    print("  1. Random City")
    print("  2. Enter Latitude and Longitude")
    choice = input("\n  >> Enter your choice: ")
    if choice == "1":
        city_choices = list(city_locations.keys())
        city = random.choice(city_choices)
        lat, lng = city_locations[city]
        print("  Searching at City: ", city)
    elif choice == "2":
        lat = input("  >> Enter the latitude: ")
        lng = input("  >> Enter the longitude: ")
    else:
        print("\n** Invalid choice. Try again! **")
        return None

    # request for sighting observations from microservice
    try:
        response = requests.get(f"http://127.0.0.1:5000/api/birds", params={'lat': lat, 'lng': lng})
        if response.status_code == 200:
            observations = response.json()
            print("\n  >> Recent Bird Sightings at latitude: " + lat + " longitude: " +lng)
            for observation in observations:
                print("  >> Observation: " + observation['comName'], observation['sciName'], observation['locName'],
                      observation['obsDt'])
        else:
            print("** Failed to fetch bird observations. Try again! **")
    except Exception as e:
        print(f"** Error occurred: {e}. Try again! **")


def random_bird_name():
    """Generates a random bird name and prints common bird name."""

    # request for random name from microservice
    try:
        response = requests.get("http://127.0.0.1:5000/api/random_bird")
        if response.status_code == 200:
            random_bird = response.json()["random_common_name"]
            print("\n  >> Random Bird Name:", random_bird)
        else:
            print("** Error fetching random bird. Try again! **")
    except Exception as e:
        print(f"** Error occurred: {e}. Try again! **")


if __name__ == "__main__":
    main()

