from ai.risk_engine import RiskEngine
from ai.damage_predictor import DamagePredictor
from ai.movement_predictor import MovementPredictor


class EDITHController:
    """
    Central intelligence controller for EDITH.

    Combines:
        1. Risk Engine
        2. Damage Predictor
        3. Movement Predictor
    """

    def __init__(self):

        self.risk_engine = RiskEngine()
        self.damage_predictor = DamagePredictor()
        self.movement_predictor = MovementPredictor()

    def analyze(
        self,
        species,
        confidence,
        crop="other",
        recent_sightings=0,
        previous_sightings=0,
        current_distance_km=10.0,
        previous_distance_km=10.0,
        direction="unknown",
        hours_since_last_sighting=24,
        night=False,
    ):

        # ---------------------------------------------
        # 1. Risk Analysis
        # ---------------------------------------------

        risk = self.risk_engine.calculate_risk(
            species=species,
            confidence=confidence,
            crop=crop,
            recent_sightings=recent_sightings,
            distance_from_forest_km=current_distance_km,
            night=night,
        )

        # ---------------------------------------------
        # 2. Damage Analysis
        # ---------------------------------------------

        damage = self.damage_predictor.predict(
            species=species,
            crop=crop,
        )

        # ---------------------------------------------
        # 3. Movement Analysis
        # ---------------------------------------------

        movement = self.movement_predictor.predict(
            species=species,
            recent_sightings=recent_sightings,
            previous_sightings=previous_sightings,
            current_distance_km=current_distance_km,
            previous_distance_km=previous_distance_km,
            direction=direction,
            hours_since_last_sighting=hours_since_last_sighting,
        )

        # ---------------------------------------------
        # 4. Unified EDITH Assessment
        # ---------------------------------------------

        assessment = {
            "detection": {
                "species": species,
                "confidence": round(confidence * 100, 1),
            },

            "risk": {
                "score": risk["score"],
                "level": risk["level"],
                "response": risk["response"],
            },

            "damage": {
                "severity": damage["severity"],
                "damage_types": damage["damage_types"],
                "protection": damage["protection"],
            },

            "movement": {
                "activity": movement["activity"],
                "proximity": movement["proximity"],
                "direction": movement["direction"],
                "intrusion_score": movement["intrusion_score"],
                "status": movement["movement_status"],
                "confidence": movement["confidence"],
            },
        }

        return assessment