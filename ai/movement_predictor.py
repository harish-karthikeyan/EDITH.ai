class MovementPredictor:
    """
    EDITH Wildlife Movement Intelligence Engine.

    Estimates movement trend from recent wildlife sightings.
    This is a rule-based baseline for the MVP.
    """

    def predict(
        self,
        species,
        recent_sightings=0,
        previous_sightings=0,
        current_distance_km=10.0,
        previous_distance_km=10.0,
        direction="unknown",
        hours_since_last_sighting=24,
    ):
        species = species.lower().strip().replace(" ", "_")
        direction = direction.lower().strip()

        # --------------------------------------------------
        # 1. Activity trend
        # --------------------------------------------------

        if recent_sightings > previous_sightings:
            activity = "INCREASING"

        elif recent_sightings < previous_sightings:
            activity = "DECREASING"

        else:
            activity = "STABLE"

        # --------------------------------------------------
        # 2. Distance trend
        # --------------------------------------------------

        distance_change = (
            previous_distance_km - current_distance_km
        )

        if distance_change > 1:
            proximity = "APPROACHING FARM"

        elif distance_change < -1:
            proximity = "MOVING AWAY"

        else:
            proximity = "STABLE DISTANCE"

        # --------------------------------------------------
        # 3. Direction
        # --------------------------------------------------

        if direction in [
            "towards_farm",
            "toward_farm",
            "approaching"
        ]:
            direction_status = "TOWARDS FARM"

        elif direction in [
            "away_from_farm",
            "moving_away"
        ]:
            direction_status = "AWAY FROM FARM"

        else:
            direction_status = "UNKNOWN"

        # --------------------------------------------------
        # 4. Intrusion likelihood
        # --------------------------------------------------

        intrusion_points = 0

        if activity == "INCREASING":
            intrusion_points += 30

        if proximity == "APPROACHING FARM":
            intrusion_points += 30

        if direction_status == "TOWARDS FARM":
            intrusion_points += 25

        if current_distance_km <= 2:
            intrusion_points += 15

        intrusion_points = min(intrusion_points, 100)

        # --------------------------------------------------
        # 5. Movement classification
        # --------------------------------------------------

        if intrusion_points >= 70:
            movement_status = "HIGH INTRUSION POTENTIAL"

        elif intrusion_points >= 40:
            movement_status = "INCREASING ACTIVITY"

        elif intrusion_points >= 20:
            movement_status = "MONITOR MOVEMENT"

        else:
            movement_status = "LOW ACTIVITY"

        # --------------------------------------------------
        # 6. Confidence
        # --------------------------------------------------

        data_points = 0

        if recent_sightings > 0:
            data_points += 1

        if previous_sightings > 0:
            data_points += 1

        if current_distance_km >= 0:
            data_points += 1

        if previous_distance_km >= 0:
            data_points += 1

        if direction_status != "UNKNOWN":
            data_points += 1

        if data_points >= 4:
            confidence = "HIGH"

        elif data_points >= 2:
            confidence = "MEDIUM"

        else:
            confidence = "LOW"

        return {
            "species": species,
            "activity": activity,
            "proximity": proximity,
            "direction": direction_status,
            "intrusion_score": intrusion_points,
            "movement_status": movement_status,
            "confidence": confidence,
            "hours_since_last_sighting": hours_since_last_sighting,
        }