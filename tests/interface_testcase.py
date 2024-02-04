'''
Simple example of a interface configuration testcase using pyATS.

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

from pyats import aetest, topology
from .send_status_update import send_status_update

__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

class CommonSetup(aetest.CommonSetup):
    ''' Common setup tasks - this class is instantiated only once per testscript. '''

    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        '''
        Each iteration of the marked Testcase will be passed the parameter
        "device" with the current device from the testbed.
        '''
        aetest.loop.mark(InterfaceTestcase, device=testbed)

class InterfaceTestcase(aetest.Testcase):
    ''' Simple Testcase for checking that the switch interfaces have the expected operational status. '''

    @aetest.setup
    def connect(self, device):
        '''
        Connect to the device.
        '''
        device.connect(via='rest', log_stdout=False, learn_hostname=True)


    @aetest.test
    def retrieve_interface_status(self, device, interfaces):
        '''
        Setup method to retrieve the interface details from the device.
        '''
        restconf_url = "/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/"
        interfaces_response = device.rest.get(restconf_url)
        if interfaces_response.ok:
            interface_list = interfaces_response.json()["Cisco-IOS-XE-interfaces-oper:interfaces"]["interface"]
            self.interfaces = [interface for interface in interface_list if interface["name"] in interfaces]
            self.passed("Interfaces retrieved")
        else:
            self.interfaces = None
            self.failed(f"Retrieving interface status failed:\n{interfaces_response.text}")


    @aetest.test
    def verify_interface_status(self, steps, device, expected_status):
        '''
        Simple interface test: Using the data collected in the setup, loop through all the
        interfaces and check if their status matches to the expected status.
        '''

        # Mapping the status names to the values returned by YANG model
        # reference: RFC 2863: The Interfaces Group MIB - ifOperStatus
        if expected_status.lower() == "up":
            expected_status = "if-oper-state-ready"
        elif expected_status.lower() == "down":
            expected_status = "if-oper-state-no-pass"
        else:
            self.failed(f"Bad expected status {expected_status} - supported status: 'up' or 'down'.")

        for interface in self.interfaces:
            with steps.start(
                f"{device.name} interface {interface['name']}", continue_=True
                ) as step:

                try:
                    assert interface["oper-status"] == expected_status
                except AssertionError:
                    step.failed(f'{interface["name"]} status {interface["oper-status"]} different from expected status {expected_status}')
                except Exception as err:
                    step.failed(f'Step failed due to an error: {err}')
                else:
                    step.passed(f'{interface["name"]} status {interface["oper-status"]}')

    @aetest.test
    def send_webex_message(self, device, send_webex=False):
        if send_webex:
            title = f"{device.name} interface configuration test"
            send_status_update(self.reporter.section_details[2], title)
        
    @aetest.cleanup
    def disconnect(self, device):
        ''' Cleanup method to disconnect from the device. '''
        device.disconnect()

if __name__ == "__main__":
    print(f"\n{'* '*13}*")
    print("* STARTING INTERFACE TEST *")
    print(f"{'* '*13}*\n")

    my_interfaces = (
        "GigabitEthernet1",
        "GigabitEthernet2",
        "GigabitEthernet3"
    )
    my_expected_status = "UP"

    my_testbed = topology.loader.load("testbed.yaml")

    intf_test = aetest.main(testbed=my_testbed, interfaces=my_interfaces, expected_status=my_expected_status)
