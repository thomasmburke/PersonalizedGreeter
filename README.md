# PersonalizedGreeter
A greeting device that welcomes your friends by name the first time it sees them!
## Setup
* Requires Raspberry pi with raspbian jessie OS 
* Follow all steps listed in the environment_setup/raspberry_pi_setup.sh
* Setup a Redis on Google compute engine
* In your virtual environment run the following command after cloning the repo:
```pip3 install -r requirements.txt```
## Current Functionality
* Greet person by name after detecting their face in a frame of the continuous video stream
* Greet with joke/fact option
## Future Functionality
* Include Seasonal greetings
* Personal recorded greetings for specific people
* Walk up music for specific people
    * Prompt people to pick their walk up music
* Group names for when it detects a set of people that associate to one name
## Technology Leveraged
* AWS Rekognition
* AWS Polly
* Raspberry pi
* GCP Compute Engine + Redis
## Materials Used
* Raspberry Pi 3B [$30]
* 5V 2.5A Switching Power Supply with 20AWG MicroUSB cable [$7.50]
* 32GB Class 10 SD card [$5]
* Raspberry Pi case base [$5]
* Mini external USB stereo speaker [$12.50]
* Raspberry Pi Camera Board v2 [$29.95]
### Overall Cost
$89.95 - Honestly not a bad price for a prototype
## Overview of Application Architecture
![alt text](https://github.com/thomasmburke/PersonalizedGreeter/blob/master/docs/PersonalizedGreeter_Application_Architecture.png)
## Greeter in action!
[Personalized Greeter Video Demo](https://www.youtube.com/watch?v=Obe1vZKrkWw)
[![Personalized Greeter Video Demo](https://i.imgur.com/cKCdC3d.png)](https://www.youtube.com/watch?v=Obe1vZKrkWw "Personalized Greeter Video Demo")
