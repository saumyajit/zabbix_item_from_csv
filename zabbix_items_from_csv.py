#
# Import required packages.
#
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import logging
import re
import datetime
from xml.dom import minidom

def reader_csv_file(file_name, read_till=99999, skip_header=True, all_oid_range=False):

    # Reading Property file for processing XML file.
    file_reader = open(file_name, "r")

    # Skipping header line.
    if skip_header == True:
        file_reader.next()

    #
    # List to hold all the dictionary values.
    # Every row is a dictionary
    #
    file_list = []

    # line count to read till specific line.
    line_count = 0

    # Reading Lines now.
    for process_line in file_reader:

        # Check if we have a threshold to read line.
        if line_count > read_till:
            break

        # Create a temp dictionary to hold the line.
        line_dict = {}

        # Split line by ','
        list = process_line.split(",")

        # Getting All data into the dictionary
        line_dict['module'] = list[0].lower()                           # Converting to lower case
        line_dict['oid_name'] = re.sub('/', '_per_', list[1].lower())   # removing '/' in field to 'per'
                                                                        #   zabbix does not like / in the key
                                                                        #   Ex : mb/sec will be mb_per_sec
        line_dict['oid'] = list[2]
        line_dict['datatype']  = list[3].upper()                        # making sure we have this as upper case
        line_dict['start'] = list[4]
        line_dict['end'] = list[5]
        line_dict['description'] = list[6].strip()                      # Strip string.
        oid_range_list = []

        if all_oid_range == True:
            oid_range_to_use = int(line_dict['end'])
        else:
            oid_range_to_use = 1

        #
        # Our file has OID range we are taking the range and putting them into a list.
        # Currently we need just the first OID (.0).
        # TODO : Need to change this if we need more than just the firat Element from the file.
        #
        for oid_range in range(int(line_dict['start']), oid_range_to_use):
            oid_range_created = line_dict['oid'] + '.' + str(oid_range)
            oid_range_list.append(oid_range_created)

        line_dict['oid_list'] = oid_range_list                          # Adding the list to dictionary

        # Our row is ready to be added to the list.
        file_list.append(line_dict)
        line_count = line_count + 1

    return file_list


# --------------------------------------------------------
# Generate Complete Export/Import XML File
# --------------------------------------------------------
def generate_items_xml_file_complete(
                                    list_from_file,
                                    host_name,
                                    host_group_name,
                                    host_interface,
                                    item_application_name=None):

    # Date format for the new file created.
    fmt = '%Y-%m-%dT%H:%M:%SZ'

    # Creating the main element.
    zabbix_export = Element('zabbix_export')

    # Sub Element which fall under zabbix_export
    version = SubElement(zabbix_export, 'version')
    date =  SubElement(zabbix_export, 'date')

    # Groups
    groups = SubElement(zabbix_export, 'groups')
    group_under_groups = SubElement(groups, 'group')
    name_under_group = SubElement(group_under_groups, 'name')

    # triggers
    triggers = SubElement(zabbix_export, 'triggers')

    # hosts
    hosts = SubElement(zabbix_export, 'hosts')
    host_under_hosts = SubElement(hosts, 'host')
    host_under_host = SubElement(host_under_hosts, 'host')
    name_under_host = SubElement(host_under_hosts,'name')

    SubElement(host_under_hosts, 'proxy')

    # status and its sub elements
    status_under_host = SubElement(host_under_hosts, 'status')
    ipmi_authtype_under_host = SubElement(host_under_hosts, 'ipmi_authtype')
    ipmi_privilege_under_host = SubElement(host_under_hosts, 'ipmi_privilege')

    # elements under hosts
    SubElement(host_under_hosts, 'ipmi_username')
    SubElement(host_under_hosts, 'ipmi_password')
    SubElement(host_under_hosts, 'templates')

    # Groups under a hosts
    groups_under_hosts = SubElement(host_under_hosts, 'groups')
    group_under_groups_host = SubElement(groups_under_hosts, 'group')
    name_group_under_groups_host = SubElement(group_under_groups_host, 'name')

    # Interfaces
    interfaces_under_host = SubElement(host_under_hosts, 'interfaces')
    interface_under_interfaces_host = SubElement(interfaces_under_host, 'interface')
    default_under_interface = SubElement(interface_under_interfaces_host, 'default')
    type_under_interface = SubElement(interface_under_interfaces_host, 'type')
    useip_under_interface = SubElement(interface_under_interfaces_host, 'useip')
    ip_under_interface = SubElement(interface_under_interfaces_host, 'ip')
    SubElement(interface_under_interfaces_host, 'dns')
    port_under_interface = SubElement(interface_under_interfaces_host, 'port')
    interface_ref_under_interface = SubElement(interface_under_interfaces_host, 'interface_ref')

    # elements under hosts
    SubElement(host_under_hosts, 'applications')
    items = SubElement(host_under_hosts, 'items')
    SubElement(host_under_hosts, 'discovery_rules')

    # macro sub element
    macros = SubElement(host_under_hosts, 'macros')
    macro = SubElement(macros, 'macro')
    sub_macro = SubElement(macro, 'macro')
    value = SubElement(macro, 'value')
    SubElement(host_under_hosts, 'inventory')

    # This information will be from the user.
    date.text = datetime.datetime.now().strftime(fmt)
    host_under_host.text = host_name.upper()
    name_under_host.text = host_name.upper()
    name_under_group.text = host_group_name.upper()
    ip_under_interface.text = host_interface
    name_group_under_groups_host.text = host_group_name.upper()

    # Standard values
    version.text = '2.0'
    status_under_host.text = '0'
    ipmi_authtype_under_host.text = '-1'
    ipmi_privilege_under_host.text = '2'
    default_under_interface.text = '1'
    type_under_interface.text = '2'
    useip_under_interface.text = '1'
    port_under_interface.text = '161'
    interface_ref_under_interface.text = 'if1'
    sub_macro.text = '{$SNMP_COMMUNITY}'
    value.text = 'public'


    #
    # Processing through the list of OID from the list in the dictionary
    # This actually a range as in the csv file
    #   If we have set 'all_oid_range' as true, then we will process all the OID range for each OID
    #   Warning : There will be too many Items in the import file.
    #             BE CAREFUL WITH THE RANGE.
    #
    for row_dict_from_file in list_from_file:

        # For each OID in the list - check function 'reader_csv_file' for more details.
        for oid_list_item in row_dict_from_file['oid_list']:
            item_creator(row_dict_from_file, items, host_name.upper(), triggers, oid_list_item, item_application_name)


    return  zabbix_export


def item_creator(dictionary, items, host_name, triggers, oid_list_item_from_dictionary, item_application_name):
    #
    # Creating an initial XML Template
    #
    item = SubElement(items, 'item')
    name = SubElement(item, 'name')
    type = SubElement(item, 'type')
    snmp_community = SubElement(item, 'snmp_community')
    multiplier = SubElement(item, 'multiplier')
    snmp_oid = SubElement(item, 'snmp_oid')
    key = SubElement(item, 'key')
    delay = SubElement(item, 'delay')
    history = SubElement(item, 'history')
    trends = SubElement(item, 'trends')
    status = SubElement(item, 'status')
    value_type = SubElement(item, 'value_type')
    SubElement(item, 'allowed_hosts')                                   # If we are not using an element
                                                                        # then do not assign it
    SubElement(item, 'units')                                           #
    delta = SubElement(item, 'delta')
    SubElement(item, 'snmpv3_contextname')
    SubElement(item, 'snmpv3_securityname')
    snmpv3_securitylevel = SubElement(item, 'snmpv3_securitylevel')
    snmpv3_authprotocol = SubElement(item, 'snmpv3_authprotocol')
    SubElement(item, 'snmpv3_authpassphrase')
    snmpv3_privprotocol = SubElement(item, 'snmpv3_privprotocol')
    SubElement(item, 'snmpv3_privpassphrase')
    formula = SubElement(item, 'formula')
    SubElement(item, 'delay_flex')
    SubElement(item, 'params')
    SubElement(item, 'ipmi_sensor')
    data_type = SubElement(item, 'data_type')
    authtype = SubElement(item, 'authtype')
    SubElement(item, 'username')
    SubElement(item, 'password')
    SubElement(item, 'publickey')
    SubElement(item, 'privatekey')
    SubElement(item, 'port')
    description = SubElement(item, 'description')
    inventory_link = SubElement(item, 'inventory_link')
    SubElement(item, 'valuemap')
    applications = SubElement(item, 'applications')
    application = SubElement(applications, 'application')
    application_name = SubElement(application, 'name')
    interface_ref = SubElement(item, 'interface_ref')

    #
    # Setting basic information for the item. Setting Values now.
    #
    name.text = 'From Module : (' + str(dictionary['module']).upper() + '), Sub Category : (' \
                + str(dictionary['oid_name']).upper() + '), Item For OID : ' + oid_list_item_from_dictionary

    # This has to be unique
    key.text = dictionary['module'] +'_'+ dictionary['oid_name'] + '_' + oid_list_item_from_dictionary

    # Setting the OID here.
    snmp_oid.text = oid_list_item_from_dictionary

    #
    # Setting value type to get information in int to string.
    # Based on the input file.
    # TODO : Add more datatype based on the return information.
    #
    if dictionary['datatype'] == 'STRING':
        value_type.text = '1'
    elif dictionary['datatype'] == 'INTEGER':
        value_type.text = '3'
    else:
        value_type.text = '1'


    #
    # Setting SNMP v1, This will change as per requirement.
    # TODO : Put a condition here so that we can change this on the fly.
    #
    type.text = '1'

    #
    # Creating Item with default values. No change here.
    # TODO : Need to add more information here based on requirement.
    #
    delta.text = '0'
    snmpv3_securitylevel.text = '0'
    snmpv3_authprotocol.text = '0'
    snmpv3_privprotocol.text = '0'
    formula.text = '1'
    data_type.text = '0'
    authtype.text = '0'
    inventory_link.text = '0'
    interface_ref.text = 'if1'
    delay.text = '60'
    history.text = '90'
    trends.text = '365'
    status.text = '0'
    snmp_community.text = 'public'
    multiplier.text = '0'

    # Adding Description as in the CSV file.
    description.text = dictionary['description']

    # Creating all the items in a specific Application on Zabbix
    application_name.text = item_application_name

    #
    # Currently we are creating Trigger for status OIDs as we know the return information
    # Assuming INS (In Service) and nis (Not in Service)
    # If currently used OID status changes from anything other then INS we trigger an alarm.
    #
    # TODO : Add more conditions to create different Triggers for different scenario.
    #
    if dictionary['datatype'] == 'STRING' and dictionary['oid_name'] == 'status':
        #
        # Creating a template
        #
        trigger = SubElement(triggers, 'trigger')
        trigger_expression = SubElement(trigger, 'expression')
        trigger_name = SubElement(trigger, 'name')
        SubElement(trigger, 'url')
        trigger_status = SubElement(trigger, 'status')
        trigger_priority = SubElement(trigger, 'priority')
        trigger_description = SubElement(trigger, 'description')
        trigger_type = SubElement(trigger, 'type')
        SubElement(trigger, 'dependencies')

        # Creating a expression - important stuff here.
        # TODO : This might change as per requirement.
        trigger_expression.text = '{' + host_name + ':'+ key.text +'.str("INS")}=0'
        trigger_name.text = 'ATTENTION : On {HOST.NAME}, An Alarm From Module : ('+ str(dictionary['module']).upper() \
                            + '), Sub Category : ('+ str(dictionary['oid_name']).upper() \
                            + '), For OID : ' + dictionary['oid']

        #
        # Setting default values here.
        # And same description as in the CSV file.
        trigger_status.text = '0'
        trigger_priority.text = '1'
        trigger_description.text = description.text
        trigger_type.text = '0'


def xml_pretty_me(file_name_for_prettify, string_to_prettify):
    #
    # Open a file and write to it and we are done.
    #
    logging.info("Creating File pretty_%s", file_name_for_prettify)

    # Creating an XML and prettify xml.
    xml = minidom.parseString(string_to_prettify)
    pretty_xml_as_string = xml.toprettyxml()

    # Creating a file to write this information.
    output_file = open(file_name_for_prettify, 'w' )
    output_file.write(pretty_xml_as_string)

    # Done.
    logging.info("Creation Complete")
    output_file.close()

# --------------------------------------------------------
# Process CSV to create zabbix items from OID and range.
# --------------------------------------------------------
if __name__ == '__main__':

    complete_list_dict_device_1 =  reader_csv_file('oid_list_with_range_processed.csv', 10)
    xml_tree_device_1 = generate_items_xml_file_complete(complete_list_dict_device_1, 'BLR-DEVICE_1', 'BLR-DEVICE_1', '10.12.51.11', 'DEVICE_1')
    xml_pretty_me('BLR-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))

    xml_tree_device_1 = generate_items_xml_file_complete(complete_list_dict_device_1, 'CHN-DEVICE_1', 'CHN-DEVICE_1', '10.12.51.11', 'DEVICE_1')
    xml_pretty_me('CHN-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))

    complete_list_dict_device_2 =  reader_csv_file('oid_list_with_range_processed.csv')
    xml_tree_device_2 = generate_items_xml_file_complete(complete_list_dict_device_2, 'BLR-DEVICE_2', 'BLR-DEVICE_2', '12.12.54.66', 'DEVICE_2')
    xml_pretty_me('BLR-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))

    xml_tree_device_2 = generate_items_xml_file_complete(complete_list_dict_device_2, 'CHN-DEVICE_2', 'CHN-DEVICE_2', '12.12.52.74', 'DEVICE_2')
    xml_pretty_me('CHN-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))