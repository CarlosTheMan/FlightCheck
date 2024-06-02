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

![Screen Shot 2024-06-02 at 5 14 06 PM](https://github.com/CarlosTheMan/flightCheck/assets/36449121/85e1aee9-2621-4f9b-bc71-dd147112a0a1)
