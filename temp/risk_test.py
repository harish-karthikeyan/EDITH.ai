import sys

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from ai.risk_engine import RiskEngine


engine = RiskEngine()


tests = [
    {
        "species": "elephant",
        "confidence": 0.94,
        "crop": "banana",
        "recent_sightings": 2,
        "distance_from_forest_km": 1,
        "night": True,
    },

    {
        "species": "wild_boar",
        "confidence": 0.91,
        "crop": "groundnut",
        "recent_sightings": 1,
        "distance_from_forest_km": 4,
        "night": True,
    },

    {
        "species": "deer",
        "confidence": 0.88,
        "crop": "millet",
        "recent_sightings": 0,
        "distance_from_forest_km": 10,
        "night": False,
    },
]


for test in tests:

    result = engine.calculate_risk(**test)

    print("\n-----------------------------")
    print("Species :", result["species"])
    print("Score   :", result["score"])
    print("Risk    :", result["level"])
    print("Response:", result["response"])