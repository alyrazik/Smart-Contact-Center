"""
Testing code
"""

# Imports
import plac
import os
import logging
import sys
import numpy
import pandas


# Import helper functions
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from time import time
from datetime import datetime


# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Regression logger')

def main():
    try:
        #do what you want
        pass

    except Exception:
        logger.exception('Exception occured in running test function')


if __name__ == '__main__':
    plac.call(main)