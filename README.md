# 50_peaks
Quick algorithm and the requisite data for calculating the fastest drive to the peaks/trail-heads of the tallest point in each state

Ripped this off from [Randal Olson](http://randalolson.com/2015/03/08/computing-the-optimal-road-trip-across-the-u-s)

Here is his [Notebook version](https://github.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/blob/master/optimal-road-trip/Computing%20the%20optimal%20road%20trip%20across%20the%20U.S..ipynb)

...just made some minor tweaks and made it into an executable instead of a notebook

Distances are already calculated, but if you want to create new ones, get and API key from Google maps and add it in the `main.py` script.

With the data provided, the algorithm will solve the Travelling Salesman Problem without returning to the origin. 
I did this by just adding a dummy "Start" location that has a distance/duration of 0 to all other locations.
If you want to solve in a loop, just remove the dummy "Start" location.