import zabbix_items_from_csv
from xml.etree import ElementTree

#-----------------------
# Limit reading to first 10 Lines.
#-----------------------
complete_list_dict_device_1 =  zabbix_items_from_csv.reader_csv_file('oid_list_with_range_processed.csv', 10)
xml_tree_device_1 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_1,
                                                            'BLR-DEVICE_1', 'BLR-DEVICE_1',
                                                            '10.12.51.11', 'DEVICE_1')
zabbix_items_from_csv.xml_pretty_me('BLR-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))
#-----------------------
xml_tree_device_1 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_1,
                                                            'CHN-DEVICE_1', 'CHN-DEVICE_1',
                                                            '10.12.51.11', 'DEVICE_1')
zabbix_items_from_csv.xml_pretty_me('CHN-DEVICE_1.xml', ElementTree.tostring(xml_tree_device_1))


#-----------------------
# Read all the lines from the csv file.
#-----------------------
complete_list_dict_device_2 =  zabbix_items_from_csv.reader_csv_file('oid_list_with_range_processed.csv')
xml_tree_device_2 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_2,
                                                             'BLR-DEVICE_2', 'BLR-DEVICE_2',
                                                             '12.12.54.66', 'DEVICE_2')
zabbix_items_from_csv.xml_pretty_me('BLR-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))
#-----------------------
xml_tree_device_2 = zabbix_items_from_csv.\
                            generate_items_xml_file_complete(complete_list_dict_device_2,
                                                             'CHN-DEVICE_2', 'CHN-DEVICE_2',
                                                             '12.12.52.74', 'DEVICE_2')
zabbix_items_from_csv.xml_pretty_me('CHN-DEVICE_2.xml', ElementTree.tostring(xml_tree_device_2))