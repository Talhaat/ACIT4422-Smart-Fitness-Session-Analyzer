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

