#!/usr/bin/env python3.6
import os
import unittest
# class for handling a set of commands
# from app import *
from app import *

def main():
	"""This function test will execute all the test_*.py under the folder tests
	for test make sure (virtual) env STAGE already set for test condition, such as (GNU/Linux) run in terminal
	export STAGE="dev"
	"""
	Event.create_table(read_capacity_units=1, write_capacity_units=1) 
	tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	Event.delete_table() 
	if result.wasSuccessful():
	    return 0
	return 1

if __name__ == '__main__':
    main()