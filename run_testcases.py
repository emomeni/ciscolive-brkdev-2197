'''
A main file to run all the testcases.

Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

import pathlib
from pyats import aetest, topology, results

# Importing testcases
from tests import ping_testcase
from tests import interface_testcase

__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

def run_ping_test(testbed:topology.testbed.Testbed,
                  destinations:tuple)->results.result.TestResult:
    '''
    Function to run the ping test

    Arguments:
        testbed (topology.testbed.Testbed) - the testbed to be targeted with the test
        destinations (tuple) - all the ip addresses to ping
    
    Returns:
        pyats TestResult for the ping test
    '''


    print(f"\n{'* '*11}*")
    print("* STARTING PING TEST  *")
    print(f"{'* '*11}*\n")

    ping_test = aetest.main(testable="tests.ping_testcase",
                            testbed=testbed,
                            destinations=destinations)
    return ping_test

def run_interface_test(testbed:topology.testbed.Testbed,
                       interfaces:tuple,
                       expected_status:str)->results.result.TestResult:
    '''
    Function to run an interface test.

    Arguments:
        testbed (topology.testbed.Testbed) - the testbed to be targeted with the test
        interfaces (tuple) - all the interface names to be tested
        expected_status (str) - "up" or "down" depending on the expected operational status
    
    Returns:
        pyats TestResult for the interface test
    '''

    print(f"\n{'* '*13}*")
    print("* STARTING INTERFACE TEST *")
    print(f"{'* '*13}*\n")

    int_test = aetest.main(testable="tests.interface_testcase",
                            testbed=testbed,
                            interfaces=interfaces,
                            expected_status=expected_status)
    return int_test

if __name__ == "__main__":

    print(f"\n{'* '*12}*")
    print("* RUNNING MY TESTCASES  *")
    print(f"{'* '*12}*\n")

    my_destinations = (
        '8.8.8.8',
        '208.67.222.222',
        )
    
    my_interfaces = (
        "GigabitEthernet1",
        "GigabitEthernet2",
        )
    interface_expected_status = "up"

    testbed_path = (pathlib.Path(__file__).parent).joinpath('tests', 'testbed.yaml')
    my_testbed = topology.loader.load(testbed_path)

    ping_test = run_ping_test(my_testbed, my_destinations)
    interface_test = run_interface_test(my_testbed, my_interfaces, interface_expected_status)

    print(f"\n{'* '*40}*")
    print("FINAL RESULTS")
    print(f"Ping test: {ping_test}")
    print(f"Interface test: {interface_test}")