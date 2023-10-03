#import pytest
 
from dashboard.utils.datacleaner import DataCleaner

def test():
    assert DataCleaner.test(5) == 5+1