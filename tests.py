from sample_data import generate_fitness_data
from models import Participant, ReferenceProfile, Observation, FitnessSession
from main import is_valid, calculate_summary, classify_session


#Function to build a fitness session for a given scenario
# Input is scenario string, seed and number of windows, return a FitnessSession object.
def build_session(scenario, seed=1, number_of_windows=10):
    profile, observations = generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=seed,
        number_of_windows=number_of_windows,
    )

    reference = ReferenceProfile(
        profile["baseline_heart_rate"],
        profile["baseline_skin_response"],
        profile["baseline_temperature"]
    )
    participant = Participant(profile["participant_id"], reference)
    session = FitnessSession(participant)

    for obs in observations:
        observation = Observation.from_dict(obs)
        observation.mark_validity(is_valid(observation))
        session.add_observation(observation)

    return session


#Function to classify a built session
# Input is a FitnessSession object, return classification string.
def classify(session):
    valid_observations = session.valid_observations()
    activity_summary = calculate_summary([o.activity_level for o in valid_observations])
    return classify_session(
        len(valid_observations),
        len(session.observations),
        activity_summary,
        valid_observations
    )


#Test that a resting scenario session is classified as resting
# Input is none, return is not used. Uses assert to check the result.
def test_resting_session():
    session = build_session("resting")
    assert classify(session) == "resting"


#Test that a moderate_activity scenario session is classified as moderate activity
# Input is none, return is not used. Uses assert to check the result.
def test_moderate_activity_session():
    session = build_session("moderate_activity")
    assert classify(session) == "moderate activity"


#Test that a high_activity scenario session is classified as high activity
# Input is none, return is not used. Uses assert to check the result.
def test_high_activity_session():
    session = build_session("high_activity")
    assert classify(session) == "high activity"


#Test that a recovery scenario session is classified as recovering
# Input is none, return is not used. Uses assert to check the result.
def test_recovery_session():
    session = build_session("recovery")
    assert classify(session) == "recovering"


#Test that a poor_quality scenario session is classified as insufficient data
# Input is none, return is not used. Uses assert to check the result.
def test_poor_quality_session():
    session = build_session("poor_quality")
    assert classify(session) == "insufficient data"


#Test that an observation with values in range is accepted
# Input is none, return is not used. Uses assert to check the result.
def test_valid_observation_accepted():
    observation = Observation(0, 70, 1.5, 32.0, 0.2, 0.95)
    assert is_valid(observation) is True


#Test that an observation with a missing heart rate is rejected
# Input is none, return is not used. Uses assert to check the result.
def test_invalid_observation_rejected():
    observation = Observation(0, None, 1.5, 32.0, 0.2, 0.95)
    assert is_valid(observation) is False


if __name__ == "__main__":
    test_resting_session()
    test_moderate_activity_session()
    test_high_activity_session()
    test_recovery_session()
    test_poor_quality_session()
    test_valid_observation_accepted()
    test_invalid_observation_rejected()
    print("All tests passed")
