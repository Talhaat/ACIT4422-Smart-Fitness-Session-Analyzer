#----------------------------------------------------------
#--------Main file for running the application-------------
#----------------------------------------------------------

#Importing data from sample_data.py and models.py
from sample_data import available_scenarios, generate_fitness_data

from models import (
    Participant,
    ReferenceProfile,
    Observation,
    FitnessSession
)

# Define main function to run the application
# Input is none and return is not used. Return object using print_report() function
def main():

    profile, observations = generate_fitness_data(
        participant_id="P001",
        scenario="recovery",
        seed=42,
        number_of_windows=10,
    )

    # Referance profile for participant by calling data generator
    reference = ReferenceProfile(
        profile["baseline_heart_rate"],
        profile["baseline_skin_response"],
        profile["baseline_temperature"]
    )

    # Build a reference profile
    participant = Participant(
        profile["participant_id"],
        reference
    )

    # Individual fitness session for participant, creat fitness session object
    session = FitnessSession(participant)

    # Loop through observations, creat objects and append to list.
    for obs in observations:
        observation = Observation.from_dict(obs)
        observation.mark_validity(is_valid(observation))
        session.add_observation(observation)

    #Build the structured result, then print it as a readable report
    report = build_session_report(session, reference)
    print_report(report)


#Function that gathers the whole analysis into one structured dictionary
# Input is session and reference profile objects, return dictionary containing analasys results. 
def build_session_report(session, reference):
    valid_observations = session.valid_observations()


    heart_rate_summary = calculate_summary([o.heart_rate for o in valid_observations])
    temperature_summary = calculate_summary([o.temperature for o in valid_observations])
    skin_response_summary = calculate_summary([o.skin_response for o in valid_observations])
    activity_summary = calculate_summary([o.activity_level for o in valid_observations])

    comparison = compare_to_reference(
        heart_rate_summary,
        temperature_summary,
        skin_response_summary,
        reference
    )

    classification = classify_session(
        len(valid_observations),
        len(session.observations),
        activity_summary,
        valid_observations
    )

    explanation = explain_classification(
        classification,
        activity_summary,
        len(valid_observations),
        len(session.observations)
    )

    return {
        "participant_id": session.participant.participant_id,
        "total_observations": len(session.observations),
        "usable_observations": len(valid_observations),
        "heart_rate_summary": heart_rate_summary,
        "temperature_summary": temperature_summary,
        "skin_response_summary": skin_response_summary,
        "activity_summary": activity_summary,
        "comparison_to_reference": comparison,
        "classification": classification,
        "explanation": explanation,
    }


#Function that prints the structured result as a readable console report
# Input parameter is dictionary containing analasys of report. Print out to consile summary.
def print_report(report):
    print("Participant:", report["participant_id"])
    print("Observations:", report["usable_observations"], "of", report["total_observations"], "usable")

    for label, summary in [
        ("Heart rate", report["heart_rate_summary"]),
        ("Temperature", report["temperature_summary"]),
        ("Skin response", report["skin_response_summary"]),
        ("Activity level", report["activity_summary"]),
    ]:
        print(f"\n{label} summary:")
        print("Average:", summary["average"])
        print("Minimum:", summary["minimum"])
        print("Maximum:", summary["maximum"])

    comparison = report["comparison_to_reference"]
    print("\nComparison to reference:")
    print("Heart rate deviation:", comparison["heart_rate_deviation"])
    print("Temperature deviation:", comparison["temperature_deviation"])
    print("Skin response deviation:", comparison["skin_response_deviation"])

    print("\nSession classification:", report["classification"])
    print("Explanation:", report["explanation"])


#Function to validate if values are valid(Rejection criteria)
# Input is observation object, return boolean value, true or false.
def is_valid(observation):

    if observation.heart_rate is None:
        return False

    if observation.heart_rate < 30 or observation.heart_rate > 220:
        return False

    if observation.temperature is None:
        return False

    if observation.skin_response is None or observation.skin_response < 0:
        return False

    if observation.activity_level is None or observation.activity_level < 0 or observation.activity_level > 1:
        return False

    if observation.signal_quality is None or observation.signal_quality < 0.5:
        return False

    return True


#Function to compare session averages against participant reference values
# Input is three summary dictionaries and a reference profile object, return dictionary containing deviation values.
def compare_to_reference(heart_rate_summary, temperature_summary, skin_response_summary, reference):
    return {
        "heart_rate_deviation": heart_rate_summary["average"] - reference.baseline_heart_rate,
        "temperature_deviation": temperature_summary["average"] - reference.baseline_temperature,
        "skin_response_deviation": skin_response_summary["average"] - reference.baseline_skin_response,
    }


#Function to check if heart rate and activity are declining near the end
# Input is list of observation objects, return boolean value, true or false.
def is_recovering(observations):
    midpoint = len(observations) // 2
    first_half = observations[:midpoint]
    second_half = observations[midpoint:]

    first_heart_rate = sum(o.heart_rate for o in first_half) / len(first_half)
    second_heart_rate = sum(o.heart_rate for o in second_half) / len(second_half)

    first_activity = sum(o.activity_level for o in first_half) / len(first_half)
    second_activity = sum(o.activity_level for o in second_half) / len(second_half)

    return second_heart_rate < first_heart_rate - 10 and second_activity < first_activity - 0.15


#Function to classify the session
# Input is usable count, total count, activity summary dictionary and list of valid observations, return classification string.
def classify_session(usable_count, total_count, activity_summary, valid_observations):
    if total_count == 0 or usable_count / total_count < 0.5:
        return "insufficient data"

    if len(valid_observations) >= 4 and is_recovering(valid_observations):
        return "recovering"

    average_activity = activity_summary["average"]

    if average_activity < 0.25:
        return "resting"
    elif average_activity < 0.65:
        return "moderate activity"
    else:
        return "high activity"


#Function to explain how many observations were usable and why the session got its classification
# Input is classification string, activity summary dictionary, usable count and total count, return explanation string.
def explain_classification(classification, activity_summary, usable_count, total_count):
    if classification == "insufficient data":
        return f"Only {usable_count} of {total_count} observations were usable, not enough to classify reliably."

    if classification == "recovering":
        return f"{usable_count} of {total_count} observations were usable. Heart rate and activity declined near the end of the session, indicating recovery."

    return f"{usable_count} of {total_count} observations were usable. Average activity level was {activity_summary['average']:.2f}, classified as {classification}."


#Function to calculate average, minimum and maximum values
# Input is list of numbers, return dictionary containing average, minimum and maximum.
def calculate_summary(values):

    if len(values) == 0:
        return {
            "average": None,
            "minimum": None,
            "maximum": None
        }

    return {
        "average": sum(values) / len(values),
        "minimum": min(values),
        "maximum": max(values)
    }

if __name__ == "__main__":
    main()