# vincenthpd
HPD Crime predictor

Predicts the most likely violent crime in a given area (beat) on a given day.

Is set to automatically predict the following week's worth of crime for each police beat when run.

To use:
1. Install python 2.7, xlutils, and scikit-learn
  https://www.python.org/downloads/
  https://github.com/python-excel/xlutils
  http://scikit-learn.org/dev/install.html
2. Clone this repo
3. Run main.py
4. Results are stored in future.json
5. Convert future.json into a .csv file through an online tool such as http://konklone.io/json/
