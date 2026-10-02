class DamagePredictor:
    """
    EDITH Crop Damage Prediction Engine.

    Estimates the likely type and severity of damage
    based on detected species and crop type.
    """

    DAMAGE_PROFILES = {

        "elephant": {
            "damage_types": [
                "Crop destruction",
                "Trampling",
                "Tree damage",
                "Property damage",
                "Human safety risk"
            ],
            "severity": "CRITICAL",
            "protection": "Immediate wildlife response and farmer warning"
        },

        "wild_boar": {
            "damage_types": [
                "Root crop damage",
                "Crop uprooting",
                "Field disturbance"
            ],
            "severity": "HIGH",
            "protection": "Field monitoring and non-harmful deterrent"
        },

        "deer": {
            "damage_types": [
                "Vegetation grazing",
                "Leaf damage",
                "Young crop damage"
            ],
            "severity": "MEDIUM",
            "protection": "Crop boundary monitoring"
        },

        "leopard": {
            "damage_types": [
                "Livestock threat",
                "Human safety risk",
                "Panic/disruption"
            ],
            "severity": "CRITICAL",
            "protection": "Keep people and livestock away and alert authorities"
        },

        "tiger": {
            "damage_types": [
                "Livestock threat",
                "Human safety risk",
                "Panic/disruption"
            ],
            "severity": "CRITICAL",
            "protection": "Keep people and livestock away and alert authorities"
        },

        "bear": {
            "damage_types": [
                "Crop damage",
                "Fruit/tree damage",
                "Property damage",
                "Human safety risk"
            ],
            "severity": "HIGH",
            "protection": "Farmer warning and wildlife authority alert"
        },

        "monkey": {
            "damage_types": [
                "Fruit damage",
                "Vegetable damage",
                "Crop consumption"
            ],
            "severity": "MEDIUM",
            "protection": "Crop monitoring and non-harmful deterrent"
        }
    }

    def predict(self, species, crop="other"):

        species = species.lower().strip().replace(" ", "_")

        profile = self.DAMAGE_PROFILES.get(
            species,
            {
                "damage_types": [
                    "Unknown biological impact"
                ],
                "severity": "UNKNOWN",
                "protection": "Continue monitoring"
            }
        )

        return {
            "species": species,
            "crop": crop,
            "damage_types": profile["damage_types"],
            "severity": profile["severity"],
            "protection": profile["protection"]
        }