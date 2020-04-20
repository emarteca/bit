import pandas as pd 
import xml.etree.ElementTree as ET
import sys

def get_failing_tests_and_suites( filename):
	root = ET.parse( filename).getroot()
	# we already know the shape of the tree so we can just hardcode this
	failing_tests = []
	failing_suites = []
	failing_suite_names = []
	for ts in root:
		for t in ts:
			if ts.attrib["failures"] == "1":
				failing_tests += [t.attrib["name"]]
				failing_suites += [ts.attrib["file"]]
				failing_suite_names += [ts.attrib["name"]]
			for e in t:
				if e.tag == "failure":
					failing_tests += [t.attrib["name"]]
					failing_suite_names += [ts.attrib["name"]]
	return( (failing_tests, failing_suites, failing_suite_names))

def get_tests_with_suites( filename, suite_list):
	root = ET.parse( filename).getroot()
	test_list = []
	for ts in root:
		for t in ts:
			if suite_list.count(ts.attrib["name"]) > 0:
				test_list += [t.attrib["name"]]
	return( test_list)
				

def print_DF_to_file( df, filename):
	f = open(filename, 'w');
	f.write(df.to_csv(index = False, header=False))
	f.close()

def main():
	(failing_tests, failing_suites, failing_suite_names) = get_failing_tests_and_suites("test-results.xml")
	failing_tests = get_tests_with_suites("nonbroken-test-results.xml", failing_suite_names)
	print_DF_to_file(pd.DataFrame(failing_tests).drop_duplicates(), "affected_test_descs.txt")
	print_DF_to_file(pd.DataFrame(failing_suites).drop_duplicates(), "test_list.txt")

main()
