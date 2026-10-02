import sys

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from ai.movement_predictor import MovementPredictor


predictor = MovementPredictor()


tests = [

    {
        "species": "elephant",
        "recent_sightings": 5,
        "previous_sightings": 2,
        "current_distance_km": 1.5,
        "previous_distance_km": 5,
        "direction": "towards_farm",
        "hours_since_last_sighting": 2,
    },

    {
        "species": "wild_boar",
        "recent_sightings": 3,
        "previous_sightings": 3,
        "current_distance_km": 4,
        "previous_distance_km": 4.5,
        "direction": "unknown",
        "hours_since_last_sighting": 6,
    },

    {
        "species": "deer",
        "recent_sightings": 1,
        "previous_sightings": 4,
        "current_distance_km": 8,
        "previous_distance_km": 3,
        "direction": "away_from_farm",
        "hours_since_last_sighting": 18,
    },
]


for test in tests:

    result = predictor.predict(**test)

    print("\n==============================")
    print("Species       :", result["species"])
    print("Activity      :", result["activity"])
    print("Proximity     :", result["proximity"])
    print("Direction     :", result["direction"])
    print("Intrusion     :", result["intrusion_score"])
    print("Movement      :", result["movement_status"])
    print("Confidence    :", result["confidence"])
    print(
        "Last sighting :",
        result["hours_since_last_sighting"],
        "hours ago"
    )