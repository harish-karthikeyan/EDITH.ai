import sys

sys.path.insert(0, r"E:\Projects\EDITH.ai")

from ai.damage_predictor import DamagePredictor


predictor = DamagePredictor()


tests = [
    ("elephant", "banana"),
    ("wild_boar", "groundnut"),
    ("deer", "millet"),
    ("monkey", "vegetables"),
    ("leopard", "other"),
]


for species, crop in tests:

    result = predictor.predict(
        species=species,
        crop=crop
    )

    print("\n==============================")
    print("Species    :", result["species"])
    print("Crop       :", result["crop"])
    print("Severity   :", result["severity"])
    print("Damage     :")

    for damage in result["damage_types"]:
        print("  •", damage)

    print("Protection :", result["protection"])