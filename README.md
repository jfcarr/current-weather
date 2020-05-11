# Current Weather

Gets current weather conditions from the NOAA website, and displays them in a simple text format.

## Prerequisites

Perl v5, with the following libraries:

* REST::Client
* XML::Simple

## Usage

Call the script with a location code; example:

```bash
current-weather.pl KDAY
```

Displays current weather conditions for the KDAY location code (Cox International Airport in Dayton, Ohio); example:

```
Overcast, 46.0 F (7.8 C)
Wind: West at 19.6 MPH (17 KT)
(Weather) Last Updated on May 10 2020, 8:56 pm EDT
```

Location codes can be retrieved here: https://w1.weather.gov/xml/current_obs/seek.php
