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
Departure: LAX
Destination: MCO
```
Provide date range for which to search
```sh
Departure Date (0000-00-00): 2024-12-01
Return Date (0000-00-00): 2024-12-31
```
Provide expected # of days to be away
```sh
Expected duration of trip: 5
```

Provide preferred airline! (American Airlines, Spirit Airlines, Delta, etc.)
```sh
Preferred Airline? (N = No preference): Spirit Airlines
```
Provide response if stops are preferred
```sh
Stops? (N = No Stops, NP = No preference): N
```

This will query real-time results and provide the user with a progress bar to keep track of status!

![Screen Shot 2024-06-02 at 5 14 06 PM](https://github.com/CarlosTheMan/flightCheck/assets/36449121/85e1aee9-2621-4f9b-bc71-dd147112a0a1)
