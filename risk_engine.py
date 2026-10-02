class RiskEngine:
    """
    EDITH Wildlife Risk Assessment Engine

    Converts detected species + farm/environmental
    factors into a risk score and response level.
    """

    # Base threat scores for the current wildlife MVP
    SPECIES_RISK = {
        "elephant": 90,
        "wildboar": 70,
        "wild_boar": 70,
        "tiger": 95,
        "leopard": 90,
        "bear": 80,
        "monkey": 45,
        "deer": 35,
    }

    # Approximate crop vulnerability
    CROP_RISK = {
        "banana": 80,
        "sugarcane": 85,
        "rice": 75,
        "maize": 70,
        "groundnut": 65,
        "vegetables": 70,
        "coconut": 60,
        "cotton": 55,
        "millet": 60,
        "other": 50,
    }

    def __init__(self):
        self.max_score = 100

    def calculate_risk(
        self,
        species,
        confidence=0.0,
        crop="other",
        recent_sightings=0,
        distance_from_forest_km=10.0,
        night=False,
    ):
        """
        Calculate EDITH's wildlife risk score.

        Parameters
        ----------
        species : str
            Detected animal species.

        confidence : float
            Detection confidence from 0 to 1.

        crop : str
            Crop currently present in the farm.

        recent_sightings : int
            Number of recent wildlife sightings.

        distance_from_forest_km : float
            Approximate distance from wildlife/forest zone.

        night : bool
            Whether the detection occurred at night.
        """

        species = species.lower().replace(" ", "_")
        crop = crop.lower()

        # --------------------------------------------------
        # 1. Species threat
        # --------------------------------------------------

        species_score = self.SPECIES_RISK.get(species, 30)

        # --------------------------------------------------
        # 2. Crop vulnerability
        # --------------------------------------------------

        crop_score = self.CROP_RISK.get(crop, 50)

        # --------------------------------------------------
        # 3. Detection confidence
        # --------------------------------------------------

        confidence_score = max(0, min(confidence * 100, 100))

        # --------------------------------------------------
        # 4. Recent sightings
        # --------------------------------------------------

        sighting_score = min(recent_sightings * 10, 30)

        # --------------------------------------------------
        # 5. Distance factor
        # --------------------------------------------------

        if distance_from_forest_km <= 1:
            distance_score = 20

        elif distance_from_forest_km <= 3:
            distance_score = 15

        elif distance_from_forest_km <= 5:
            distance_score = 10

        elif distance_from_forest_km <= 10:
            distance_score = 5

        else:
            distance_score = 0

        # --------------------------------------------------
        # 6. Night factor
        # --------------------------------------------------

        night_score = 10 if night else 0

        # --------------------------------------------------
        # Weighted risk calculation
        # --------------------------------------------------

        score = (
            species_score * 0.35
            + crop_score * 0.15
            + confidence_score * 0.15
            + sighting_score * 0.15
            + distance_score * 0.10
            + night_score * 0.10
        )

        score = round(min(score, self.max_score), 1)

        # --------------------------------------------------
        # Risk classification
        # --------------------------------------------------

        if score >= 80:
            level = "CRITICAL"

        elif score >= 60:
            level = "HIGH"

        elif score >= 35:
            level = "MEDIUM"

        else:
            level = "LOW"

        # --------------------------------------------------
        # Recommended response
        # --------------------------------------------------

        response = self.get_response(level)

        return {
            "score": score,
            "level": level,
            "species": species,
            "response": response,
        }

    @staticmethod
    def get_response(level):

        responses = {
            "LOW": "MONITOR AREA",

            "MEDIUM": "ALERT FARMER",

            "HIGH": "ALERT AUTHORITIES",

            "CRITICAL": "IMMEDIATE RESPONSE",
        }

        return responses.get(level, "MONITOR AREA")