"""Unit Address conversion Tool """
from __future__ import print_function
import sys
import os
from os import path
from crccheck.crc import Crc8Cdma2000 as crc

UARESFILE = "ua_conv_results.txt"
MACRESFILE = "mac_conv_results.txt"
UAMACFILE = "ua_mac_conv_results.txt"
HELPFILE = '''
                           Useage

                -------------------------------------------------------------------------------------
                1.  Convert a single or txt file UA XXX-XXXXX-XXXXX-XXX to a DAC 0xXXXXXXXXXX format
                        python <script> -ua-conv -s <ua>
                        python <script> -ua-conv -f <file>

                        Example, convert 000-01054-74710-173 to 0x0006496a96
                        python ua.py -ua-conv -s 000-01054-74710-173 
                        python ua.py -ua-conv -f  ua_list.txt
                        
                Note: If using -f, output file will be in the same location your running the script	

                -------------------------------------------------------------------------------------
                2.	Convert a single or txt file  MAC XX:XX:XX:XX:XX to a UA XXX-XXXXX-XXXXX-XXX format
                        python <script> -mac-conv -s <mac>
                        python <script> -mac-conv -f <file>

                        Example, convert 00:06:49:6a:96 to 000-01054-74710-173
                        python ua.py -mac-conv -s 00:06:49:6a:96
                        python ua.py -mac-conv -f  ua_list.txt
                        
                        
                Note: If using -f, output file will be in the same location your running the script

                -------------------------------------------------------------------------------------
                3.	Convert a single or txt file  UA XXX-XXXXX-XXXXX-XXX to a MAC XX:XX:XX:XX:XX format
                        python <script> -ua-mac -s <mac>
                        python <script> -ua-mac -f <file>

                        Example, convert 000-01054-74710-173 to 00:06:49:6a:96 
                        python ua.py -ua-mac -s 000-01054-74710-173
                        python ua.py -ua-mac -f  ua_list.txt
                        
                        
                Note: If using -f, output file will be in the same location your running the script

                -------------------------------------------------------------------------------------
                            '''


def main_script():
    """ Main script """
    if len(sys.argv) < 4:
        print(HELPFILE)
    if sys.argv[1] == "-ua-conv" and sys.argv[2] == "-s" and len(sys.argv) == 4:
        ua_in = sys.argv[3]
        new_ua = gui_ua_to_dacdb_ua_conv(ua_in)
        print(new_ua)
    elif sys.argv[1] == "-mac-conv" and sys.argv[2] == "-s" and len(sys.argv) == 4:
        mac = sys.argv[3]
        new_mac = mac_to_gui_ua_conv(mac)
        print(new_mac)
    elif sys.argv[1] == "-ua-mac" and sys.argv[2] == "-s" and len(sys.argv) == 4:
        mac = sys.argv[3]
        new_mac = gui_ua_to_mac_conv(mac)
        print(new_mac)
    elif sys.argv[1] == "-ua-conv" and sys.argv[2] == "-f" and len(sys.argv) == 4:
        txt_file = sys.argv[3]
        read_file, res_file = file_open_func(txt_file, UARESFILE)
        contents = read_file.read()
        file_as_list = contents.splitlines()
        for line in file_as_list:
            new_ua = gui_ua_to_dacdb_ua_conv(line)
            res_file.write(new_ua + '\n')
        res_file.close()
        read_file.close()
        print("output file: {}".format(UARESFILE))
    elif sys.argv[1] == "-mac-conv" and sys.argv[2] == "-f" and len(sys.argv) == 4:
        txt_file = sys.argv[3]
        read_file, res_file = file_open_func(txt_file, MACRESFILE)
        contents = read_file.read()
        file_as_list = contents.splitlines()
        for line in file_as_list:
            new_ua = mac_to_gui_ua_conv(line)
            res_file.write(new_ua + '\n')
        res_file.close()
        read_file.close()
        print("output file: {}".format(MACRESFILE))
    elif sys.argv[1] == "-ua-mac" and sys.argv[2] == "-f" and len(sys.argv) == 4:
        txt_file = sys.argv[3]
        read_file, res_file = file_open_func(txt_file, UAMACFILE)
        contents = read_file.read()
        file_as_list = contents.splitlines()
        for line in file_as_list:
            new_ua = gui_ua_to_mac_conv(line)
            res_file.write(new_ua + '\n')
        res_file.close()
        read_file.close()
        print("output file: {}".format(UAMACFILE))
    else:
        print(HELPFILE)

def file_open_func(txt_file_to_open, if_exist_file):
    """ Open read and results text files """
    try:
        read_file = open(txt_file_to_open)
    except IOError:
        print("COULD NOT OPEN GIVEN FILE: {}".format(txt_file_to_open))
        sys.exit()
    if path.exists(if_exist_file):
        os.remove(if_exist_file)
    try:
        res_file = open(if_exist_file, "w")
    except IOError:
        print("COULD NOT OPEN GIVEN FILE: {}".format(if_exist_file))
        sys.exit()
    return (read_file, res_file)


def gui_ua_to_dacdb_ua_conv(ua_in):
    """ gui ua to dac db ua main function """
    ua_in = ua_mac_format(ua_in, "ua")
    if ua_in == -1:
        return "NULL"
    dec_to_hex = ua_conv_dec_to_hex(ua_in)
    ua_padded = ua_mac_pad_form(dec_to_hex, "ua")
    return ua_padded


def gui_ua_to_mac_conv(ua_in):
    """ gu ua to mac main function """
    ua_in = ua_mac_format(ua_in, "ua")
    if ua_in == -1:
        return "NULL"
    dec_to_hex = ua_conv_dec_to_hex(ua_in)
    mac_padded = ua_to_mac(dec_to_hex)
    return mac_padded


def mac_to_gui_ua_conv(mac):
    """ mac to gui main function """
    mac = ua_mac_format(mac, "mac")
    if mac == -1:
        return "NULL"
    mac_ua_rt = mac_ua(mac)
    return mac_ua_rt


def ua_mac_format(ua_mac, conv):
    """ ua or mac formatting main function
        Format a UA in XXX-XXXXX-XXXXX-XXX or MAC XX:XX:XX:XX:XX
        Removes -/:
    """
    if conv == "ua":
        ua_mac = ua_mac.split('-')
        ua_mac = "".join(ua_mac)
    else:
        if ":" in ua_mac:
            ua_mac = ua_mac.split(':')
            ua_mac = "".join(ua_mac)
        else:
            ua_mac = ua_mac.split('0x')
            ua_mac = "".join(ua_mac)

    if len(ua_mac) == 16:
        # This is a UA XXX-XXXXX-XXXXX-XXX
        return ua_mac
    elif len(ua_mac) == 10:
        # This is a MAC address xx:xx:xx:xx:xx
        return ua_mac
    # UA or MAC in the wrong format return -1
    return -1


def ua_conv_dec_to_hex(ua_in):
    """ Convert a UA but first dropping the last 3 values which are CRC checksums.
        Convert a UA from dec to hex.
    """
    hex_val = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    conv_dict = {}
    for i, j in enumerate(hex_val):
        conv_dict[i] = j.lower()
    rem_dec = []
    quote = True
    ua_in = int(ua_in[:-3])
    t_in = int(ua_in / 16)
    rem_dec.append(conv_dict[int(ua_in % 16)])
    while quote:
        if t_in != 0:
            rem_dec.append(conv_dict[int(t_in % 16)])
        t_in = int(t_in / 16)
        if t_in == 0:
            quote = False
    return "".join(rem_dec[::-1])


def ua_to_mac(ua_in):
    """ Formatting a MAC address into xx:xx:xx:xx:xx """
    padded_mac = ua_mac_pad_form(ua_in, "mac")
    mac_addr = []
    for t_in, i in enumerate(padded_mac):
        mac_addr.append(i)
        if t_in % 2 == 1 and t_in != 9:
            mac_addr.append(":")
        t_in += 1
    return "".join(mac_addr)


def ua_mac_pad_form(ua_mac, conv):
    """ Padding a UA or MAC  with zeroes infront of the value """
    if conv == "ua":
        ua_new = "0x"
    else:
        ua_new = ""
    len_a = len(ua_mac)
    while len_a != 10:
        ua_new = ua_new + "0"
        len_a += 1
    if conv == "ua":
        return ua_new + ua_mac
    return list(ua_new + ua_mac)


def mac_ua(mac):
    """ Take in a MAC address and convert to a UA.
        First remove colons, convert hex val to int then to a string
        Calculate CRC value from mac and append to UA with "-"
    """
    mac = "".join(mac.split(":"))
    hex_mac = str(int(mac, 16))
    crc_val = str(crc_calc(mac))
    hex_mac_len = len(hex_mac)
    h_mac = ""
    ua_len = 13
    while hex_mac_len != ua_len:
        h_mac = h_mac + "0"
        hex_mac_len += 1
    form_hex = []
    for i, j in enumerate(h_mac + hex_mac + crc_val):
        form_hex.append(j)
        if i == 2 or i == 7 or i == 12:
            form_hex.append("-")
    return "".join(form_hex)


def crc_calc(hex_ua):
    """ Calculating CRC using a Python Module """
    data = bytearray.fromhex(hex_ua)
    data = crc.calc(data)
    data = str(data)
    len_crc = len(data)
    ua_new = ""
    while len_crc != 3:
        ua_new = ua_new + "0"
        len_crc += 1

    return ua_new + data


if __name__ == "__main__":
    main_script()
