vis-a-vis
=========

A simple Python+shell script to check if your papers have been cited on ADS. 

Works on Mac, probably on Linux just fine. Doubtful on Windows.

Uses Linux `wget` to retreive a predefined list of papers (ADS URLs). Scrapes information using `grep` and `sed`. Returns notice if new citation found, or if [h-index](http://en.wikipedia.org/wiki/H-index) *for the selected papers* goes up.
