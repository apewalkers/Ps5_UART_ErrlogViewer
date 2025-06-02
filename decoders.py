# decoders.py
# This file contains functions for decoding various data fields from the UART log.

import datetime

# Constants used by decoder functions
TIME_ZERO = 1325376000  # UNIX timestamp for January 1, 2012
SEQ_DATABASE = {
    "2002": "EmcBootup", "2067": "EmcBootup", "2064": "EmcBootup | FATAL OFF", "218E": "EmcBootup",
    "2003": "Subsystem Peripheral Initialize", "2005": "Subsystem Peripheral Initialize",
    "2004": "Subsystem Peripheral Initialize", "2008": "aEmcTimerIniti", "2009": "aEmcTimerIniti",
    "200A": "aEmcTimerIniti", "200B": "aEmcTimerIniti", "200C": "aPowerGroup2On 1",
    "2109": "aPowerGroup2On 1", "200D": "aPowerGroup2On 1", "2011": "aPowerGroup2On 1",
    "200E": "aPowerGroup2On 1 | Subsystem PG2 reset", "200F": "aPowerGroup2On 1",
    "2010": "aPowerGroup2On 1 | Subsystem PG2 reset", "202E": "aPowerGroup2On 1 | Subsystem PG2 reset",
    "2006": "aPowerGroup2On 1 | Subsystem PG2 reset", "21AF": "aPowerGroup2On 1",
    "21B1": "aPowerGroup2On 1",
    "2014": "aPowerGroup2Off | Flash Controller OFF EFC | Flash Controller OFF EAP | Flash Controller STOP EFC | Flash Controller STOP EAP | FATAL OFF",
    "202F": "aPowerGroup2Off | FATAL OFF", "2015": "aPowerGroup2Off | FATAL OFF",
    "2016": "aPowerGroup2Off | Subsystem PG2 reset | FATAL OFF", "202B": "aPowerGroup2Off | FATAL OFF",
    "2017": "aPowerGroup2Off | FATAL OFF", "210A": "aPowerGroup2Off | FATAL OFF",
    "2018": "aPowerGroup2Off | FATAL OFF", "2019": "aPowerGroup2Off", "201A": "aSbPcieInitiali",
    "2030": "aSbPcieInitiali | aSbPcieInitiali 1 | FATAL OFF",
    "2031": "aSbPcieInitiali | aSbPcieInitiali 1 | FATAL OFF", "2066": "aSbPcieInitiali 1",
    "208D": "aEfcBootModeSet | EAP Boot Mode Set", "210B": "aEfcBootModeSet | EAP Boot Mode Set",
    "210C": "aEfcBootModeSet | EAP Boot Mode Set", "210D": "aEfcBootModeSet",
    "201D": "Flash Controller ON EFC | Flash Controller ON EAP",
    "2027": "Flash Controller ON EFC | Flash Controller ON EAP | Flash Controller Soft reset",
    "2110": "Flash Controller ON EFC | Flash Controller ON EAP",
    "2033": "Flash Controller ON EFC | Flash Controller ON EAP | Flash Controller Soft reset",
    "2089": "Flash Controller ON EFC | Flash Controller ON EAP | Flash Controller Soft reset",
    "2035": "Flash Controller ON EFC | Flash Controller ON EAP | Flash Controller Soft reset | FC NAND Close Not urgent | FC NAND Close Urgent",
    "201C": "Subsystem PCIe USP Enable",
    "2029": "Subsystem PCIe DSP Enable | Subsystem PCIe DSP Enable BT DL",
    "2107": "Subsystem PCIe DSP Enable | PCIE RESET ASSERT NEGATE",
    "2159": "Flash Controller Initialization EFC | Flash Controller Initialization EAP",
    "2045": "Flash Controller Initialization EFC | Flash Controller Initialization EAP",
    "2038": "Flash Controller Initialization EFC",
    "2043": "Flash Controller Initialization EFC | Flash Controller Initialization EAP",
    "2041": "Flash Controller Initialization EFC | Flash Controller Initialization EAP",
    "2047": "Flash Controller Initialization EAP",
    "204C": "Flash Controller OFF EFC | Flash Controller STOP EFC",
    "2108": "Flash Controller OFF EFC | Flash Controller OFF EAP | Flash Controller STOP EFC | Flash Controller STOP EAP | FATAL OFF | Dev WLAN BT PCIE RESET ASSERT | Dev WLAN BT PCIE RESET ASSERT NEGATE",
    "206D": "Flash Controller OFF EFC | Flash Controller OFF EAP | Flash Controller STOP EFC | Flash Controller STOP EAP | FATAL OFF",
    "2034": "Flash Controller OFF EFC | Flash Controller OFF EAP | FATAL OFF",
    "208A": "Flash Controller OFF EFC | Flash Controller OFF EAP | FATAL OFF",
    "210F": "Flash Controller OFF EFC | Flash Controller OFF EAP | FATAL OFF",
    "2028": "Flash Controller OFF EFC | Flash Controller OFF EAP | Flash Controller STOP EFC | Flash Controller STOP EAP | FATAL OFF",
    "201E": "Flash Controller OFF EFC | Flash Controller OFF EAP | FATAL OFF",
    "2046": "Flash Controller OFF EAP | Flash Controller STOP EFC | Flash Controller STOP EAP",
    "2048": "Flash Controller STOP EFC | Flash Controller STOP EAP", "204D": "Flash Controller STOP EAP",
    "2049": "Flash Controller SRAM Keep Enable", "2111": "ACDC 12V ON", "2113": "ACDC 12V ON",
    "2052": "ACDC 12V ON", "2085": "ACDC 12V ON", "2054": "ACDC 12V ON", "2087": "ACDC 12V ON",
    "216F": "USB VBUS On | USB VBUS Off | Dev USB VBUS On", "211B": "USB VBUS On | Dev USB VBUS On",
    "211D": "BD Drive Power On | Dev BD Drive Power On",
    "203A": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "203D": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2126": "Main SoC Power ON Cold Boot | FATAL OFF",
    "2128": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "212A": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2135": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF | Dev VBURN OFF",
    "211F": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "2189": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "218B": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "21B6": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "21B8": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "21BA": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "2023": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2125": "Main SoC Power ON Cold Boot | GDDR6 USB Power On",
    "2167": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "21C1": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "21C3": "Main SoC Power ON Cold Boot", "2121": "Main SoC Power ON Cold Boot",
    "21C5": "Main SoC Power ON Cold Boot",
    "2175": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2133": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2141": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "205F": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "218D": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "21BE": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "21C0": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "21C4": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "2123": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2136": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "2137": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "216D": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit",
    "2060": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "2061": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "2025": "Main SoC Power ON Cold Boot | Main SoC Power ON S3 Exit | Main SoC Power Off | FATAL OFF",
    "2127": "Main SoC Reset Release | Cold reset WA", "204A": "Main SoC Reset Release",
    "2129": "Main SoC Reset Release | Cold reset WA",
    "21A3": "Main SoC Reset Release | USB VBUS On 2 | Dev USBA1 VBUS On",
    "21A5": "Main SoC Reset Release | USB VBUS On 2 | Dev USBA2 VBUS On",
    "21A7": "Main SoC Reset Release | USB VBUS On 2 |",
    "21A9": "Main SoC Reset Release | USB VBUS On 2 | Dev USBA1 VBUS On",
    "21AB": "Main SoC Reset Release | USB VBUS On 2 | Dev USBA2 VBUS On",
    "21AD": "Main SoC Reset Release | USB VBUS On 2 |",
    "212F": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF",
    "2169": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF",
    "2161": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF",
    "21B3": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF",
    "21B5": "Main SoC Reset Release",
    "213C": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "213D": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "213F": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "2050": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "2083": "Main SoC Reset Release", "2187": "Main SoC Reset Release",
    "2195": "Main SoC Reset Release", "2197": "Main SoC Reset Release",
    "2155": "Main SoC Reset Release",
    "205C": "Main SoC Reset Release | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "217F": "Main SoC Reset Release | Cold reset WA",
    "212B": "MSOC Reset Moni High | Main SoC Power Off | FATAL OFF",
    "2157": "MSOC Reset Moni High | Main SoC Power Off | FATAL OFF",
    "208F": "Main SoC Power Off | FATAL OFF",
    "2040": "Main SoC Power Off | FATAL OFF | FC NAND Close Not urgent",
    "2156": "Main SoC Power Off | FATAL OFF",
    "2196": "Main SoC Thermal Moni Stop | Main SoC Power Off | FATAL OFF",
    "2198": "Main SoC Thermal Moni Stop | Main SoC Power Off | FATAL OFF",
    "2188": "Main SoC Thermal Moni Stop | Main SoC Power Off | FATAL OFF",
    "2084": "Main SoC Thermal Moni Stop | Main SoC Power Off | FATAL OFF",
    "2051": "Main SoC Thermal Moni Stop | Main SoC Power Off | FATAL OFF | Cold reset WA",
    "211E": "BD Drive Power Off | FATAL OFF | Dev BD Drive Power Off",
    "211C": "USB VBUS Off | FATAL OFF", "2114": "ACDC 12V Off | FATAL OFF",
    "2112": "ACDC 12V Off | FATAL OFF", "207A": "ACDC 12V Off",
    "2086": "ACDC 12V Off | FATAL OFF", "2053": "ACDC 12V Off | FATAL OFF",
    "2088": "ACDC 12V Off | FATAL OFF", "2055": "ACDC 12V Off | FATAL OFF",
    "204B": "FC NAND Close Not urgent | FC NAND Close Urgent | FATAL OFF",
    "2042": "FC NAND Close Not urgent | FC NAND Close Urgent",
    "2044": "FC NAND Close Not urgent | FC NAND Close Urgent", "2024": "FATAL OFF",
    "2152": "USB OC Moni de assert | FATAL OFF", "2122": "FATAL OFF",
    "21AA": "FATAL OFF | USB OC Moni de assert 2 | ",
    "21AC": "FATAL OFF | USB OC Moni de assert 2 | ",
    "21AE": "FATAL OFF | USB OC Moni de assert 2 | ",
    "21A4": "FATAL OFF | USB VBUS Off 2 | ", "21A6": "FATAL OFF | USB VBUS Off 2 | ",
    "21A8": "FATAL OFF | USB VBUS Off 2 | ", "218C": "FATAL OFF", "218A": "FATAL OFF",
    "2120": "FATAL OFF", "2118": "FATAL OFF | Dev HDMI 5V Power Off",
    "2073": "FATAL OFF | HDMI CECStop", "2075": "FATAL OFF | HDMI CECStop | HDMIStop",
    "2079": "FATAL OFF | HDMI CECStop", "2071": "FATAL OFF | HDMI CECStop",
    "204F": "FATAL OFF | HDMI CECStop", "2022": "FATAL OFF | HDMI CECStop",
    "2116": "FATAL OFF | HDMI CECStop", "208C": "FATAL OFF", "2165": "FATAL OFF",
    "2164": "FATAL OFF", "216C": "FATAL OFF", "21B2": "FATAL OFF", "21B0": "FATAL OFF",
    "2012": "Stop SFlash DMA | FATAL OFF", "2091": "Local Temp.3 OFF | FATAL OFF",
    "2057": "Local Temp.3 OFF | FATAL OFF", "217E": "Fan Servo Parameter Reset | FATAL OFF",
    "2105": "WLAN Module Reset | FATAL OFF | WM Reset ", "2092": "FATAL OFF",
    "212D": "EAP Reset Moni de assert", "212E": "EAP Reset Moni Assert | FATAL OFF",
    "205D": "EAP Reset Moni Assert | Main SoC Power Off | FATAL OFF",
    "213B": "EAP Reset Moni Assert | Main SoC Power Off | FATAL OFF",
    "205E": "FAN CONTROL Parameter Reset", "2065": "EMC SoC Handshake ST",
    "2151": "USB OC Moni Assert", "2068": "HDMI Standby | HDMIStop",
    "2106": "WLAN Module USB Enable | WLAN Module Reset | WM Reset",
    "217B": "WLAN Module Reset | BT WAKE Disabled | WM Reset ",
    "215A": "1GbE NIC Reset de assert", "215B": "1GbE NIC Reset assert",
    "2115": "HDMI CECStart | CECStart", "2021": "HDMI CECStart", "204E": "HDMI CECStart",
    "2070": "HDMI CECStart | CECStop", "2078": "HDMI CECStart | CECStop",
    "206E": "HDMI CECStart | CECStart", "2074": "HDMI CECStart", "2072": "HDMI CECStart",
    "2077": "HDMIStop | CECStop", "215F": "MDCDC ON", "2160": "MDCDC Off",
    "208E": "Titania2 GPIO Glitch Issue WA", "216E": "Check AC IN DETECT",
    "2170": "Check BD DETECT", "2173": "GPI SW Open", "2174": "GPI SW Close",
    "2102": "Devkit IO Expander Initialize", "2177": "Salina PMIC Register Initialize",
    "2178": "Disable AC IN DETECT", "2179": "BT WAKE Enabled",
    "2094": "Stop PCIePLL NoSS part", "217A": "Titania PMIC Register Initialize",
    "203B": "Setup FC for BTFW DL", "2039": "Setup FC for BTFW DL", "217C": "BTFW Download",
    "2095": "Telstar ROM Boot Wait", "201B": "Stop PCIePLL SS NOSS part | FATAL OFF",
    "2082": "Stop PCIePLL SS part",
    "2013": "Stop Subsystem PG2 Bus Error Detection(DDR4 BufferOverflow)",
    "2056": "Local Temp.3 ON", "2090": "Local Temp.3 ON",
    "2180": "FAN Control Start at Restmode during US",
    "2181": "FAN Control Start at Restmode during US",
    "2182": "FAN Control Start at Restmode during US",
    "2193": "FAN Control Start at Restmode during US",
    "2183": "FAN Control Stop at Restmode during USB",
    "2184": "FAN Control Stop at Restmode during USB",
    "2185": "FAN Control Stop at Restmode during USB",
    "2194": "FAN Control Stop at Restmode during USB",
    "2186": "Read Titania PMIC Registe", "219B": "I2C Open", "219C": "I2C Open",
    "219D": "I2C Open", "219E": "I2C Open", "2199": "I2C Open", "219A": "I2C Open",
    "21A0": "Drive FAN Control Stop", "219F": "Drive FAN Control Stop",
    "21A1": "Drive FAN Control Start", "21A2": "Drive FAN Control Start",
    "2117": "Dev HDMI 5V Power On", "2134": "Dev VBURN ON", "FFFF": "Unknown SeqNo"
}

def _decode_rtc(rtc_hex): # Removed self
    """Decodes RTC hex value to a human-readable date and time."""
    if rtc_hex == 'N/A':
        return "N/A"
    try:
        unix_timestamp = TIME_ZERO + int(rtc_hex, 16)
        return datetime.datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError, OverflowError):
        return "Invalid RTC"

def _decode_err_code(err_code_hex): # Removed self
    """Provides a short description for an error code."""
    if err_code_hex == 'N/A':
        return "N/A"
    
    TARGET_MSG_LENGTH = 25
    msg_text = f"Unknown Code ({err_code_hex})"
    prefix = ""
    if err_code_hex[0:8] == '80000001':
        msg_text = 'Failed to access thermal sensor'
    elif err_code_hex[0:8] == '80000004':
        prefix = "(CRITICAL) "
        msg_text = 'AC/DC Power Fail'
    elif err_code_hex[0:8] == '80000005':
        prefix = "(CRITICAL) "
        msg_text = 'Main SoC CPU Power Fail'
    elif err_code_hex[0:8] == '80000006':
        prefix = "(CRITICAL) "
        msg_text = 'Main SoC GFX Power Fail'
    elif err_code_hex[0:8] == '80000007':
        msg_text = 'Main SoC Thrm Hi Tempr Abnormal'
    elif err_code_hex[0:8] == '80000008':
        msg_text = 'Drive Dead Notify Timeout'
    elif err_code_hex[0:8] == '80000009':
        prefix = "(Common) "
        msg_text = 'AC Detect CHECK PSU' # Your updated message
    elif err_code_hex[0:8] == '8000000A':
        prefix = "(CRITICAL) "
        msg_text = 'VRM HOT Fatal'
    elif err_code_hex[0:8] == '8000000B':
        msg_text = 'Unexpected Thermal Shutdown'
    elif err_code_hex[0:8] == '8000000C':
        msg_text = 'MSoC Tempr Alert'
    
    # Catch-all for 8005xxxx should come after more specific 80050000 if any
    elif err_code_hex[0:8] == '80050000':
        prefix = "(CRITICAL) "
        msg_text = 'SoC VRM Power Fail (CPU)'
    elif err_code_hex[0:4] == '8005': # Catch-all for 8005 prefix
        prefix = "(CRITICAL) "
        msg_text = 'SoC VRM Power Fail (CPU)' 
    
    elif err_code_hex[0:8] == '80060000':
        prefix = "(CRITICAL) "
        msg_text = 'SoC VRM Power Fail (GFX)'
    elif err_code_hex[0:4] == '8006': # Catch-all for 8006 prefix
        prefix = "(CRITICAL) "
        msg_text = 'SoC VRM Power Fail (GFX)'
        
    elif err_code_hex[0:4] == '8080': # Assuming this is an 8-char code family
        prefix = "(CRITICAL) "
        msg_text = 'Fatal Shutdown by OS request'
    
    elif err_code_hex[0:8] == '80810001':
        prefix = "(CRITICAL) "
        msg_text = 'PSQ Pre_Post Fail' # Simplified your example
    elif err_code_hex[0:8] == '80810002':
        msg_text = 'Power Seq: NVS Access Error'
    elif err_code_hex[0:8] == '80810013':
        msg_text = 'Power Seq: ScCmd DRAM Init Error'
    elif err_code_hex[0:8] == '80810014':
        msg_text = 'Power Seq: ScCmd Link Up Failure'
        
    elif err_code_hex[0:8] == '80830000':
        msg_text = 'Main SoC Sync Flood'
    elif err_code_hex[0:8] == '80840000':
        prefix = "(Common) "
        msg_text = 'PCIe Link Down'
        
    elif err_code_hex[0:8] == '80870001':
        msg_text = 'Flash Cont:RAM Protect Error'
    elif err_code_hex[0:8] == '80870002':
        msg_text = 'Flash Cont:RAM Parity Error'
    elif err_code_hex[0:8] == '80870003':
        msg_text = 'Flash Cont:Boot Failed'
    elif err_code_hex[0:8] == '80870004':
        msg_text = 'Flash Cont:Boot Failed NoRecord'
    elif err_code_hex[0:8] == '80870005':
        msg_text = 'Flash Cont:Boot Failed State Err'
    elif err_code_hex[0:6] == '808710': # 6-char prefix
        msg_text = 'Flash Cont:ScCmd Response Error'
        
    elif err_code_hex[0:4] == '8088':
        msg_text = 'Flash Cont:Boot EAP Error'
    elif err_code_hex[0:4] == '8089':
        msg_text = 'Flash Cont:Boot EFC Error'
    elif err_code_hex[0:4] == '808A':
        msg_text = 'Flash Cont:Temper Error'
    elif err_code_hex[0:4] == '808B':
        msg_text = 'Flash Cont:Watch Dog Timer'
    elif err_code_hex[0:4] == '808C':
        prefix = "(ERROR) "
        msg_text = 'USB Type-C Error' # Corrected spelling
        
    elif err_code_hex[0:8] == '808D0000':
        prefix = "(CRITICAL) "
        msg_text = 'Thermal Shutdown: Main SoC'
    elif err_code_hex[0:8] == '808D0001':
        msg_text = 'Thermal Shutdown: Local Sensor 1'
    elif err_code_hex[0:8] == '808D0002':
        msg_text = 'Thermal Shutdown: Local Sensor 2'
    elif err_code_hex[0:8] == '808D0003':
        msg_text = 'Thermal Shutdown: Local Sensor 3'
        
    elif err_code_hex[0:8] == '808E0000':
        msg_text = 'COM Err:Close Error'
    elif err_code_hex[0:8] == '808E0001':
        msg_text = 'COM Err:Open Error'
    elif err_code_hex[0:8] == '808E0002':
        msg_text = 'COM Err:Host Write Flag Error'
    elif err_code_hex[0:8] == '808E0003':
        msg_text = 'COM Err:EMC Read Flag Error'
    elif err_code_hex[0:8] == '808E0004':
        msg_text = 'COM Err:Write Flag Error'
    elif err_code_hex[0:8] == '808E0005':
        msg_text = 'COM Err:Wait SIG1 Error'
    elif err_code_hex[0:8] == '808E0006':
        msg_text = 'COM Err:Reset request from Host'
    elif err_code_hex[0:8] == '808E0007':
        msg_text = 'COM Err:Checksum Error'
        
    elif err_code_hex[0:8] == '808F0001':
        msg_text = 'SMCU Com Err:Timeout'
    elif err_code_hex[0:8] == '808F0002':
        msg_text = 'SMCU Com Err:Reset'
    elif err_code_hex[0:8] == '808F0003':
        msg_text = 'SMCU Com Err:TIS Error'
    elif err_code_hex[0:8] == '808F00FF':
        msg_text = 'SMCU Com Err:Undefined'
        
    elif err_code_hex[0:4] == '8090':
        prefix = "(CRITICAL) "
        msg_text = 'Fatal Shutdown by Error Add Code'
    elif err_code_hex[0:4] == '8091':
        prefix = "(CRITICAL) "
        msg_text = 'SSD PMIC Error'
        
    elif err_code_hex[0:8] == '80C00114':
        msg_text = 'Watch Dog For SoC'
    elif err_code_hex[0:8] == '80C00115':
        msg_text = 'Watch Dog For EAP'
    elif err_code_hex[0:8] == '80C0012C':
        prefix = "(Common) "
        msg_text = 'BD Drive Detached'
    elif err_code_hex[0:8] == '80C0012D':
        msg_text = 'EMC Watch Dog Timer Error'
    elif err_code_hex[0:8] == '80C0012E':
        msg_text = 'ADC Error (Button)'
    elif err_code_hex[0:8] == '80C0012F':
        msg_text = 'ADC Error (BD Drive)'
    elif err_code_hex[0:8] == '80C00130':
        msg_text = 'ADC Error (AC In Det)'
    elif err_code_hex[0:8] == '80C00131':
        prefix = "(ERROR) "
        msg_text = 'USB Over Current'
    elif err_code_hex[0:8] == '80C00132':
        msg_text = 'FAN Storage Access Failed'
    elif err_code_hex[0:8] == '80C00133':
        msg_text = 'USB-BT FW Header Invalid'
    elif err_code_hex[0:8] == '80C00134':
        msg_text = 'USB-BT BT Command Error'
    elif err_code_hex[0:8] == '80C00135':
        msg_text = 'USB-BT Memory Malloc Failed'
    elif err_code_hex[0:8] == '80C00136':
        msg_text = 'USB-BT Device Not Found'
    elif err_code_hex[0:8] == '80C00137':
        msg_text = 'USB-BT MISC Error'
    elif err_code_hex[0:8] == '80C00138':
        msg_text = 'Flash Cont Interrupt HW Error'
    elif err_code_hex[0:8] == '80C00139':
        msg_text = 'BD Drive Eject Assert Delayed'
        
    elif err_code_hex[0:6] == '80D001': msg_text = 'USB-BT Error (Bulk Out)'
    elif err_code_hex[0:6] == '80D002': msg_text = 'USB-BT Error (Bulk In)'
    elif err_code_hex[0:6] == '80D003': msg_text = 'USB-BT Error (Bt Init)'
    elif err_code_hex[0:6] == '80D004': msg_text = 'USB-BT Error (Download Firmware)'
    elif err_code_hex[0:6] == '80D005': msg_text = 'USB-BT Error (Release Device)'
    elif err_code_hex[0:6] == '80D006': msg_text = 'USB-BT Error (Exec Cmd0)'
    elif err_code_hex[0:6] == '80D007': msg_text = 'USB-BT Error (Exec Cmd1)'
        
    elif err_code_hex[0:2] == 'B0': # B0xxxxxx
        prefix = "(CRITICAL) "
        msg_text = 'Sonics Bus Error'
        
    elif err_code_hex[0:4] == 'C001':
        msg_text = 'Main SoC Access Error (I2C)'
    elif err_code_hex[0:4] == 'C002':
        prefix = "(Common) "
        msg_text = 'SoC thermal sensor issue' # Your updated message
    elif err_code_hex[0:4] == 'C003':
        msg_text = 'Main SoC Access Error (SB-RMI)'
    elif err_code_hex[0:4] == 'C00B':
        msg_text = 'Serial Flash Access Error'
    elif err_code_hex[0:4] == 'C00C':
        msg_text = 'VRM Controller Access Error'
    elif err_code_hex[0:4] == 'C00D':
        msg_text = 'PMIC (Subsystem) Access Error'
    elif err_code_hex[0:4] == 'C010':
        msg_text = 'Flash Controller Access Error'
    elif err_code_hex[0:4] == 'C011':
        msg_text = 'Potentiometer Access Error'
    elif err_code_hex[0:4] == 'C015':
        msg_text = 'PCIe Redriver Access Errror'
    elif err_code_hex[0:4] == 'C016':
        msg_text = 'PMIC (SSD) Access Error'
    elif err_code_hex[0:4] == 'C081':
        msg_text = 'HDMI Tx Access Error'
    elif err_code_hex[0:4] == 'C090':
        msg_text = 'USB Type-C PD Cont Access Error'
    elif err_code_hex[0:4] == 'C091':
        msg_text = 'USB Type-C USB/DP Mux Accss Err'
    elif err_code_hex[0:4] == 'C092':
        msg_text = 'USB Type-C Redriver Access Error'
    elif err_code_hex[0:4] == 'C0FE':
        msg_text = 'Dummy Error Code'
    padded_msg_text = msg_text.strip().ljust(TARGET_MSG_LENGTH)
    final_msg = f"{prefix}{padded_msg_text}"

    if msg_text == f"Unknown Code ({err_code_hex})" and prefix == "":
         return f"Unknown Code ({err_code_hex})"

    if len(msg_text.strip()) < TARGET_MSG_LENGTH and msg_text != f"Unknown Code ({err_code_hex})":
        padded_msg_text = msg_text.strip().ljust(TARGET_MSG_LENGTH)
    else:
        padded_msg_text = msg_text.strip()

    final_msg = f"{prefix}{padded_msg_text}"
    return final_msg.strip()


def _decode_pw_state(pw_state_hex): # Removed self
    """Decodes power state hex to a human-readable string."""
    if pw_state_hex == 'N/A': return "N/A"
    try:
        if not (len(pw_state_hex) == 8 and all(c in '0123456789abcdefABCDEF' for c in pw_state_hex)):
            return "Invalid PwState Hex"
        # ... (rest of your _decode_pw_state logic, ensuring it doesn't use self) ...
        msg1 = '        '
        host_os_state_code = pw_state_hex[2:4].upper()
        if host_os_state_code == '00': msg1 = 'SysReady:'
        elif host_os_state_code == '01': msg1 = 'MaOnStby:'
        elif host_os_state_code == '20': msg1 = 'BIOS____:'
        elif host_os_state_code == '30': msg1 = 'BIOS____:'
        elif host_os_state_code == '40': msg1 = 'EAP_Redy:'
        elif host_os_state_code == 'FF': msg1 = 'HstOsOFF:'
        else:
            prefix_char = pw_state_hex[2].upper()
            if prefix_char == '0': msg1 = 'Reserved:'
            elif prefix_char == '1': msg1 = 'PSP____:'
            elif prefix_char == '4': msg1 = 'EAP____:'
            elif prefix_char in ['5','6','7','8','9','A','B']: msg1 = 'Kernel__:'
            elif prefix_char in ['C','D','E','F']: msg1 = 'IntPrcss:'

        emc_state_code = pw_state_hex[6:8].upper()
        msg2 = '______'
        if emc_state_code == '00': msg2 = 'ACIN_L'
        elif emc_state_code == '01': msg2 = 'Stanby'
        elif emc_state_code == '02': msg2 = 'PG2_ON'
        elif emc_state_code == '03': msg2 = 'EFC_ON'
        elif emc_state_code == '04': msg2 = 'EAP_ON'
        elif emc_state_code == '05': msg2 = 'SOC_ON'
        elif emc_state_code == '06': msg2 = 'ErrDET'
        elif emc_state_code == '07': msg2 = 'FtlErr'
        elif emc_state_code == '08': msg2 = 'NvrBot'
        elif emc_state_code == '09': msg2 = 'FrcOFF'
        elif emc_state_code == '0A': msg2 = 'FofBTd'
        return msg1 + msg2
    except Exception:
        return "Decode PwState Error"

def _decode_upcause(bt_trg_hex): # Removed self
    """Decodes boot trigger/up cause hex to a human-readable string."""
    if bt_trg_hex == 'N/A': return "N/A"
    if len(bt_trg_hex) != 8: return "Invalid UpCause Hex"
    cause_map = {
        "40000000": "UART", "00080000": "BT", "00040000": "CEC",
        "00020000": "EAP", "00010000": "SoC", "00000400": "Eject Button",
        "00000200": "DLd", "00000100": "PowerButton", "00000001": "BPW"
    }
    return cause_map.get(bt_trg_hex.upper(), "Unknown UpCause")

def _decode_devpower(dvpw_i_hex): # Removed self
    """Decodes device power state hex to a human-readable string."""
    if dvpw_i_hex == 'N/A': return "N/A"
    try:
        value = int(dvpw_i_hex, 16)
        states = []
        if value & 0x10: states.append('HDD/SSD')
        if value & 0x08: states.append('ODD')
        if value & 0x04: states.append('AcDc')
        if value & 0x02: states.append('Usb')
        if value & 0x01: states.append('Wlan')
        return ' | '.join(states) if states else 'None Active'
    except ValueError:
        return "Invalid DevPower Hex"

def convert_to_celsius(hex_value): # Removed self
    """Converts a hex temperature value to Celsius string."""
    if hex_value == 'N/A' or not hex_value:
        return "N/A"
    try:
        temp_celsius_float = int(hex_value, 16) / 256.0
        return f"{temp_celsius_float:.2f} °C"
    except (ValueError, TypeError):
        return "Invalid Hex Temp"

def _decode_seq_no(seq_no_hex): # Removed self (this is the correct one, remove the duplicate)
    """Decodes sequence number hex using the SEQ_DATABASE."""
    if seq_no_hex == 'N/A' or not seq_no_hex:
        return "N/A"
    return SEQ_DATABASE.get(seq_no_hex.upper(), f"Unknown SeqNo ({seq_no_hex})")

def _decode_temp_soc(t_soc_hex): # Removed self
    """Decodes SoC temperature hex to Celsius."""
    return convert_to_celsius(t_soc_hex) # Call the corrected convert_to_celsius

def _decode_temp_env(t_env_hex): # Removed self
    """Decodes environment temperature hex to Celsius."""
    return convert_to_celsius(t_env_hex) # Call the corrected convert_to_celsius

