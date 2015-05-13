# vincenthpd #
# HPD Crime predictor #

### Predicts the most likely violent crime in a given area (beat) on a given day. ###

#### Is set to automatically predict the following week's worth of crime for each police beat when run. ####

#### To use: ####
* Install python 2.7, xlutils, and scikit-learn
  * https://www.python.org/downloads/
  * https://github.com/python-excel/xlutils
  * http://scikit-learn.org/dev/install.html
* Clone this repo
* Run main.py
* Results are stored in future.json
* Convert future.json into a .csv file through an online tool such as http://konklone.io/json/

To start server `cd` into directory and put `python -m SimpleHTTPServer 8000`
