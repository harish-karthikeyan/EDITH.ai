import sys

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from ai.edith_controller import EDITHController


edith = EDITHController()


result = edith.analyze(

    species="elephant",

    confidence=0.94,

    crop="banana",

    recent_sightings=5,

    previous_sightings=2,

    current_distance_km=1.5,

    previous_distance_km=5,

    direction="towards_farm",

    hours_since_last_sighting=2,

    night=True,
)


print("\n")
print("==========================================")
print("        EDITH INTELLIGENCE REPORT")
print("==========================================")

print("\n[ DETECTION ]")
print("Species     :", result["detection"]["species"])
print("Confidence  :", result["detection"]["confidence"], "%")

print("\n[ RISK ]")
print("Score       :", result["risk"]["score"])
print("Level       :", result["risk"]["level"])
print("Response    :", result["risk"]["response"])

print("\n[ DAMAGE ]")
print("Severity    :", result["damage"]["severity"])

for damage in result["damage"]["damage_types"]:
    print(" •", damage)

print("\n[ MOVEMENT ]")
print("Activity    :", result["movement"]["activity"])
print("Proximity   :", result["movement"]["proximity"])
print("Direction   :", result["movement"]["direction"])
print("Intrusion   :", result["movement"]["intrusion_score"])
print("Status      :", result["movement"]["status"])
print("Confidence  :", result["movement"]["confidence"])

print("\n==========================================")
print("        EDITH ASSESSMENT COMPLETE")
print("==========================================")