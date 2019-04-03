vis-a-vis
=========

## Install

1. Get an [ADS API key](https://github.com/adsabs/adsabs-dev-api#access)
2. Install the [ads Python package](https://ads.readthedocs.io/en/latest/#getting-started)
3. Put your API key in `~/.ads/dev_key`, as instructed in Step 2
4. Download/clone this repo
5. populate `papers.tbl` file with the bibcodes for your papers
6. run `python vis-a-vis.py`

A simple Python+ script to check if selected papers have been cited on ADS. Returns notice if new citation found, or if [h-index](http://en.wikipedia.org/wiki/H-index) *for the selected papers* goes up.
