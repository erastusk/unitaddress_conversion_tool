# Unit Address to Mac Conversion Tool


## Instructions:
1.	Ensure the environment the script is ran from has python 2 or 3 installed.
2.      crcccheck module is required, can be installed using pip as follows:
		pip install crccheck
3.	If a UA or Mac address is valid, a NULL will be returned.



## Script Useage: 
 

                -------------------------------------------------------------------------------------
                1.  Convert a single or txt file UA XXX-XXXXX-XXXXX-XXX to a DAC 0xXXXXXXXXXX format
                        python <script> -ua-conv -s <ua>
                        python <script> -ua-conv -f <file>

                        Example, convert 000-01054-74710-173 to 0x0006496a96
                        python ua.py -ua-conv -s 000-01054-74710-173
                        python ua.py -ua-conv -f  ua_list.txt

                Note: If using -f, output file will be in the same location your running the script

                -------------------------------------------------------------------------------------
                2.      Convert a single or txt file  MAC XX:XX:XX:XX:XX to a UA XXX-XXXXX-XXXXX-XXX format
                        python <script> -mac-conv -s <mac>
                        python <script> -mac-conv -f <file>

                        Example, convert 00:06:49:6a:96 to 000-01054-74710-173
                        python ua.py -mac-conv -s 00:06:49:6a:96
                        python ua.py -mac-conv -f  ua_list.txt


                Note: If using -f, output file will be in the same location your running the script

                -------------------------------------------------------------------------------------
                3.      Convert a single or txt file  UA XXX-XXXXX-XXXXX-XXX to a MAC XX:XX:XX:XX:XX format
                        python <script> -ua-mac -s <mac>
                        python <script> -ua-mac -f <file>

                        Example, convert 000-01054-74710-173 to 00:06:49:6a:96
                        python ua.py -ua-mac -s 000-01054-74710-173
                        python ua.py -ua-mac -f  ua_list.txt


                Note: If using -f, output file will be in the same location your running the script

                -------------------------------------------------------------------------------------		
## Examples
UA -> HEX UA
```
python ua.py -ua-conv -s 000-00978-64864-010
0x0005d54ca0
```

HEX UA -> UA or MAC -> UA
```
python ua.py -mac-conv -s 0x0005d54ca0
000-00978-64864-010
```
```
python ua.py -mac-conv -s 00:05:d5:4c:a0
000-00978-64864-010
```

UA -> MAC
```
python ua.py -ua-mac -s 000-00978-64864-010
00:05:d5:4c:a0
```

UA -> HEX UA - bulk conversion from a text file
```
python ua.py -ua-conv -f ua_txt
output file: ua_conv_results.txt
```

HEX UA -> UA - bulk conversion from a text file
```
python ua.py -ua-mac -f mac_conv_results.txt
output file: ua_mac_conv_results.txt
```

MAC -> UA or HEX UA -> UA - bulk conversion from a text file
```
python ua.py -mac-conv -f ua_only
output file: mac_conv_results.txt
```





   
