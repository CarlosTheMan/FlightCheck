# flightCheck
A python tool that dynamically checks and finds the cheapest flight for any given date range!

# Installation
pip install this repo (Note: Incompatible with python 2.x)

```sh
pip3 install flightCheck
```
or

```sh
pip install flightCheck
```
# Usage
Provide airport of departure and arrival for example: (LAX,MIA,FLL)
```sh
DEPARTURE: LAX
DESTINATION: MCO
```
Provide date range for which to search
```sh
FROM DATE (xxxx-xx-xx): 2024-06-01
TO DATE (xxxx-xx-xx): 2024-06-30
```
Provide expected # of days to be away
```sh
EXPECTED # OF DAYS TO BE GONE: 5
```

This will query real-time results and provide the user with a progress bar to keep track of status!

