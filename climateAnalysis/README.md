# Treatment of series of climate data with discontinuities
Here I use *pandas* to import and work with the data as part of my learning process
of Data Analysis in **Python**.

This is a simple example of the kind of treatment we should apply to a series
of climate data with no metadata.

The climate data (mean annual temperature) is from a group of stations located in the Ebro Basin (NE of Spain). The values span across 42 years so many things could have changed at the stations.

![alt text][logo]

[logo]: https://upload.wikimedia.org/wikipedia/commons/d/d2/SpainEbroBasin.png "Spain Ebro Basin"

The objective of this analysis is to identify sources of variability not caused by climate as changes in the equipment or the methods of acquiring the data. Those will lead to discontinuities in the series.

With the help of close stations we can correct our problem series, so the first steps is to find a correlation between the stations and the we can choose those that fit better. Combining them into a reference series we can see the difference with our original series.

Then we divide the series in two sub-series and look for the lower RSS (residual sum) and we compare it against a sample statistic (F-distribution & Z-test).

Now if we have found a real discontinuity (we should keep subdividing the series to find other discontinuities) we take the most recent data as the good one and use the reference series to improve the older data.
