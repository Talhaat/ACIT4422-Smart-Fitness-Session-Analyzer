# ACIT4422-Smart-Fitness-Session-Analyzer
### Student name: **Thomas Talha Løberg**

### Student ID: **thlob4941**
Assignment 1 for program **ACIT4422 Scripting with Python** using Object Oriented programming for **Smart Fitness Session Analyzer, Option A**.

## Summary
This program analyses simulated data from sample_data.py, validate fitness measurements, organize behaviors, calculate summaries, compare session data with participant's reference profile, detects recoveries and classifies sessions as resting, moderate activity, recovering or insufficient data.  


## Classes
* ReferenceProfile
  * Stores the participants baseline measurements such as heart rate, skin response and temperature.
* Participants
  * Represents participants in the system. Stores participants ID and Reference profile 
* Observation
  * Observation represents one measurement window from the fitness session. It stores timestamp, hearth rate, skin response, temperature, activity level, signal quality. It also stores if the session is valid or not.
* FitnessSession
  * Represents complete fitness session for one participant. Stores participant and list of observation objects. Its responseble for adding observations and returning valid observations.
 

## Composition, Encapsulation and Inheritance

* Composition
  * Participant has a ReferenceProfile.
  * FitnessSession has a Participant and a list of Observation objects.
  * Composition is used because the classes work together by containing other objects.

* Encapsulation
  * Observation uses _is_valid as a protected attribute.
  * The value is read through the is_valid property and changed with the mark_validity() method.

* Class method
  * Observation.from_dict() is used to create an Observation object directly from the dictionary made by the data generator.

* Inheritance and overriding
  * Inheritance and overriding are not used in this project.
  * The classes do not have a natural parent and child relationship. Composition fits better because a FitnessSession contains observations and a participant instead of being a type of them.
 

## Assumptions and classification rules
### Assumtions
* Only valid observations are used in session calculations.
* Hearthrate must be between 30 and 220 bpm.
* Skinrespons must not be missing or negative.
* Activity level must be between 0 and 1.
* signal quality must be 0.5 or above.
* Temperature must have a value.
* Session average are computed with the participant's baseline values.

### Classification rules
* Innsificient data
* * Less than 50% observation
* Recovering
* * At least 4 valid observations
  * Avrage hearth rate in second half must be at least 10 bpm
  * Avrage activity in second half must be at least 0.15
* Resting
  * Average activity level is below 0.25
* Moderate activity
  * Average activity level is between 0.25 and 0.65
* High activity
  * Average activity level is 0.65 or above
 
## Example output
'''
Participant: P001
Observations: 10 of 10 usable

Heart rate summary:
Average: 112.8
Minimum: 79
Maximum: 141

Temperature summary:
Average: 33.03
Minimum: 32.73
Maximum: 33.34

Skin response summary:
Average: 1.565
Minimum: 1.3
Maximum: 1.93

Activity level summary:
Average: 0.485
Minimum: 0.04
Maximum: 0.88

Comparison to reference:
Heart rate deviation: 34.8
Temperature deviation: 0.2700000000000031
Skin response deviation: 0.395

Session classification: recovering
Explanation: 10 of 10 observations were usable. Heart rate and activity declined near the end of the session, indicating recovery.
'''
## Known limitation
* Crashes on all-invalid or empty sessions
* Classification limits are fixed values. For example, activity bellow 0.25 is resting and activity above o.65 is high activity. 
* Recovery detection only compare the first half of the session with the second half o the session. This method may bot detect every type of recovery correctly.
* A session is classified as inefficient if less than 50% of the observations are valid. 50% is an assumption for this assignment.
* Program only analyses one participant and one scenario at the time in main.py.
* The data uses simulated data from the provided data generator and have not been tested in real life scenarios.

# Installation and running instrictions
Clone repo: 

```bash
git clone https://github.com/Talhaat/ACIT4422-Smart-Fitness-Session-Analyzer.git
```
unzip file under downloads or where you cloned repo:
'''
unzip ACIT4422-Smart-Fitness-Session-Analyzer.zip
'''

Go into file location:
'''
cd ACIT4422-Smart-Fitness-Session-Analyzer
'''

run data generation, classes and test:
'''
python3 sample_data.py

python3 models.py

python3 test.py
'''

Run main file:
'''
python3 main.py
'''




