# error_databases.py
# This file contains the database of detailed error code descriptions.

def cod3r_database(err_code_hex):  # Removed 'self'
    """
    Provides a detailed description and troubleshooting advice for a given error code.
    Args:
        err_code_hex (str): The error code in hexadecimal format.
    Returns:
        str: A descriptive message for the error code.
    """
    msg_text = f'Unknown error code ({err_code_hex})\n\n🛠️ No known match. Check full error database or logs.'  # Default message

    if err_code_hex[0:8] == '80000001':
        msg_text = (
            'APU Overheat or Fatal Off\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check system cooling (fans, thermal paste, heatsink contact).\n'
            '• Clean dust build up.\n'
            '• Review ambient temperature and airflow.\n'
            '• Note : 12 Models can trigger bad PSU or Failing Heatsink'
        )
    elif err_code_hex[0:8] == '80000009':
        msg_text = (
            '• Unexpected Power Loss or Power Supply Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect for accidental power button press or long press.\n'
            '• Check PSU Stability.\n'
            '• Replace LED Button Board.\n'
            '• Replace Front Button.'
        )
    elif err_code_hex[0:8] == '80050000':
        msg_text = (
            '• CPU VRM (2 Phases)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Remove CPU Inductors, Check Each for LOW resistance.\n'
            '• Replace PSU.\n'
            '• Replace XDPE IC.\n'
            '• Check for cracked CPU.'
        )
    elif err_code_hex[0:8] == '80060000':
        msg_text = (
            '• GPU VRM (6 Phases)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Remove GPU Inductors, Check for Low Resistance.\n'
            '• Replace PSU.\n'
            '• Check XDPE IC / Replace.\n'
            '• Check APU for Checks / Liquid Metal Spill.'
        )
    elif err_code_hex[0:8] == '80800000':
        msg_text = (
            '• Kernel Panic Shutdown\n\n'
            '💀🔥 FATAL ERROR:\n'
            '• Appears to be Software Related Error\n'
            '• Possible RAM Related Fault'
        )
    elif err_code_hex[0:6] == '808016':
        msg_text = (
            '• SOC Panic Shutdown\n\n'
            '💀🔥 FATAL ERROR:\n'
            '• Ram or Ram Controller Fault\n'
            '• Seen Previously Due to Vref out-of-sync'
        )
    elif err_code_hex[0:8] == '80800014':
        msg_text = (
            '• TPM 2.0 Chip or Power Failure\n\n'
            '💀🔥 FATAL ERROR:\n'
            '• Check TPM module connection/soldering.'
        )
    elif err_code_hex[0:8] == '8080001A':
        msg_text = (
            '• Non-Native TPM 2.0 Chip Detected (Post APU Init)\n\n'
            '💀🔥 FATAL ERROR:\n'
            '• Check TPM module connection/soldering.'
        )
    elif err_code_hex[0:8] == '80800022':
        msg_text = (
            '• [SceSysCore] ___: Couldn’t load G6 Controller Failed.\n\n'
            '💀🔥 FATAL ERROR:\n'
            '• Reball APU.\n'
            '• Replace APU, SSD, TPM.'
        )
    elif err_code_hex[0:8] == '80810001':
        msg_text = (
            '• Power Sequencing Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check PSQ data logs for abnormalities.\n'
            '• Common Code: Wifi / HDMI Encoder / SOC.\n'
            '• If SOC: Check PSU, Check MEMIO, NBCore, GDDR6, DDR4 SSD Controller XDPE.'
        )
    elif err_code_hex[0:8] == '80830000':
        msg_text = (
            '• PrePost_Function Fail. Secondary Startup Rail.\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check PG2 Rails, 0.9, 1.2, 1.3, 3.3, 5v Pon.\n'
            '• Common Fail around NB Core / MEMIO.'
        )
    elif err_code_hex[0:8] == '808300F0':
        msg_text = (
            '• Secure Loader Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check PG2 voltage.\n'
            '• Common Fail around NB Core / MEMIO.'
        )
    elif err_code_hex[0:8] == '80871001':
        msg_text = (
            '• DDR4 Memory Error\n\n'
            '💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Replace or re-seat RAM(DDR4) module.\n'
            '• Replace or re-seat SSD Controller.'
        )
    elif err_code_hex[0:8] == '80871062':
        msg_text = (
            '• SSD Controller (EFC)\n\n'
            '🛠️ Troubleshooting:\n'
            '💀🔥 FATAL ERROR - SSD CONTROLLER'
        )
    elif err_code_hex[0:8] == '80894003':
        msg_text = (
            '• SSD Controller or DDR4 Error\n\n'
            '💀🔥 FATAL ERROR\n\n'
            '• Missing 2.5V on DA9081\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check/Replace SSD Controller PWIC.\n'
            '• Check/Replace SSD Controller.'
        )
    elif err_code_hex[0:8] == '808940AE':
        msg_text = (
            '• NOR Modification Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Attempt NOR reflash.'
        )
    elif err_code_hex[0:8] == '808C2092':
        msg_text = (
            '• USB Type-C Error Detected\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check USB PD controller and redriver chip.'
        )
    elif err_code_hex[0:8] == '808D0002':
        msg_text = (
            '• Thermal Shutdown (LED Board)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Southbridge PWIC Reported OVP / OCP.\n'
            '• Common Cause : Crushed LED Board Ribbon / Roach Infestation.'
        )
    elif err_code_hex[0:8] == '80C00134':
        msg_text = (
            '• USB-BT Command Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Replace Bluetooth/Wifi module.\n'
            '• Check 1.8 / 3.3v.\n'
            '• NOR Reflash.'
        )
    elif err_code_hex[0:8] == '80C00136':
        msg_text = (
            '• Wi-Fi / Bluetooth Problem or Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check Wi-Fi/BT module connection.\n'
            '• Check 1.8 / 3.3v.'
        )
    elif err_code_hex[0:8] == '80C00140':
        msg_text = (
            '• APU Halted (No Response)\n'
            '🛠️ Troubleshooting:\n'
            '• Common Fault - APU Shutdown before Southbridge.\n'
            '• Common for FATAL Error (Non-Error)\n.'
            '🛠️ Can be caused by pulling AC Plug'
        )
    elif err_code_hex[0:8] == '80D00402':
        msg_text = (
            '• USB-BT Error (Firmware Missing)\n\n'
            '🛠️ Troubleshooting:\n'
            '• USB related errors of WiFi Module (BT).\n'
            '• Replace WIFI Module.\n'
            '• Replace Southbridge PWIC / 1.8v PWIC.\n'
            '• Reflash NOR.'
        )
    elif err_code_hex[0:8] == 'C0020303':
        msg_text = (
            '• System Reported - ERROR FATAL OFF\n\n'
            '🛠️ Info: Often logged after fatal shutdown.\n'
            '• Non - Error > Always Logged at FATAL OFF.'
        )
    elif err_code_hex[0:8] == 'C00C0002':
        msg_text = (
            '• XDPE IC Failed to ACK\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check 6414A MOSFETs near fuse 7001.\n'
            '• Check 5v Caps above F7501 (row of 4).\n'
            '• Replace XDPE IC.'
        )
    elif err_code_hex[0:8] == 'FFFFFFFF':
        msg_text = 'No Errors Detected ✅'
        ## RAM Error Codes
    elif err_code_hex[0:8] == '80801101': msg_text = 'RAM GDDR6 (Bank 1) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801102': msg_text = 'RAM GDDR6 (Bank 2) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801103': msg_text = 'RAM GDDR6 (Bank 1,2) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801104': msg_text = 'RAM GDDR6 (Bank 3) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801105': msg_text = 'RAM GDDR6 (Bank 1,3) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801106': msg_text = 'RAM GDDR6 (Bank 2,3) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801107': msg_text = 'RAM GDDR6 (Bank 1,2,3) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801108': msg_text = 'RAM GDDR6 (Bank 4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801109': msg_text = 'RAM GDDR6 (Bank 1,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110A': msg_text = 'RAM GDDR6 (Bank 2,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110B': msg_text = 'RAM GDDR6 (Bank 1,2,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110C': msg_text = 'RAM GDDR6 (Bank 3,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110D': msg_text = 'RAM GDDR6 (Bank 1,3,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110E': msg_text = 'RAM GDDR6 (Bank 2,3,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080110F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801110': msg_text = 'RAM GDDR6 (Bank 5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801111': msg_text = 'RAM GDDR6 (Bank 1,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801112': msg_text = 'RAM GDDR6 (Bank 2,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801113': msg_text = 'RAM GDDR6 (Bank 1,2,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801114': msg_text = 'RAM GDDR6 (Bank 3,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801115': msg_text = 'RAM GDDR6 (Bank 1,3,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801116': msg_text = 'RAM GDDR6 (Bank 2,3,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801117': msg_text = 'RAM GDDR6 (Bank 1,2,3,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801118': msg_text = 'RAM GDDR6 (Bank 4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801119': msg_text = 'RAM GDDR6 (Bank 1,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111A': msg_text = 'RAM GDDR6 (Bank 2,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111B': msg_text = 'RAM GDDR6 (Bank 1,2,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111C': msg_text = 'RAM GDDR6 (Bank 3,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111D': msg_text = 'RAM GDDR6 (Bank 1,3,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111E': msg_text = 'RAM GDDR6 (Bank 2,3,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080111F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801120': msg_text = 'RAM GDDR6 (Bank 6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801121': msg_text = 'RAM GDDR6 (Bank 1,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801122': msg_text = 'RAM GDDR6 (Bank 2,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801123': msg_text = 'RAM GDDR6 (Bank 1,2,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801124': msg_text = 'RAM GDDR6 (Bank 3,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801125': msg_text = 'RAM GDDR6 (Bank 1,3,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801126': msg_text = 'RAM GDDR6 (Bank 2,3,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801127': msg_text = 'RAM GDDR6 (Bank 1,2,3,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801128': msg_text = 'RAM GDDR6 (Bank 4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801129': msg_text = 'RAM GDDR6 (Bank 1,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112A': msg_text = 'RAM GDDR6 (Bank 2,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112B': msg_text = 'RAM GDDR6 (Bank 1,2,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112C': msg_text = 'RAM GDDR6 (Bank 3,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112D': msg_text = 'RAM GDDR6 (Bank 1,3,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112E': msg_text = 'RAM GDDR6 (Bank 2,3,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080112F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801130': msg_text = 'RAM GDDR6 (Bank 5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801131': msg_text = 'RAM GDDR6 (Bank 1,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801132': msg_text = 'RAM GDDR6 (Bank 2,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801133': msg_text = 'RAM GDDR6 (Bank 1,2,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801134': msg_text = 'RAM GDDR6 (Bank 3,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801135': msg_text = 'RAM GDDR6 (Bank 1,3,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801136': msg_text = 'RAM GDDR6 (Bank 2,3,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801137': msg_text = 'RAM GDDR6 (Bank 1,2,3,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801138': msg_text = 'RAM GDDR6 (Bank 4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801139': msg_text = 'RAM GDDR6 (Bank 1,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113A': msg_text = 'RAM GDDR6 (Bank 2,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113B': msg_text = 'RAM GDDR6 (Bank 1,2,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113C': msg_text = 'RAM GDDR6 (Bank 3,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113D': msg_text = 'RAM GDDR6 (Bank 1,3,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113E': msg_text = 'RAM GDDR6 (Bank 2,3,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080113F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5,6) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801140': msg_text = 'RAM GDDR6 (Bank 7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801141': msg_text = 'RAM GDDR6 (Bank 1,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801142': msg_text = 'RAM GDDR6 (Bank 2,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801143': msg_text = 'RAM GDDR6 (Bank 1,2,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801144': msg_text = 'RAM GDDR6 (Bank 3,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801145': msg_text = 'RAM GDDR6 (Bank 1,3,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801146': msg_text = 'RAM GDDR6 (Bank 2,3,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801147': msg_text = 'RAM GDDR6 (Bank 1,2,3,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801148': msg_text = 'RAM GDDR6 (Bank 4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801149': msg_text = 'RAM GDDR6 (Bank 1,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114A': msg_text = 'RAM GDDR6 (Bank 2,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114B': msg_text = 'RAM GDDR6 (Bank 1,2,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114C': msg_text = 'RAM GDDR6 (Bank 3,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114D': msg_text = 'RAM GDDR6 (Bank 1,3,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114E': msg_text = 'RAM GDDR6 (Bank 2,3,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080114F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801150': msg_text = 'RAM GDDR6 (Bank 5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801151': msg_text = 'RAM GDDR6 (Bank 1,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801152': msg_text = 'RAM GDDR6 (Bank 2,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801153': msg_text = 'RAM GDDR6 (Bank 1,2,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801154': msg_text = 'RAM GDDR6 (Bank 3,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801155': msg_text = 'RAM GDDR6 (Bank 1,3,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801156': msg_text = 'RAM GDDR6 (Bank 2,3,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801157': msg_text = 'RAM GDDR6 (Bank 1,2,3,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801158': msg_text = 'RAM GDDR6 (Bank 4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801159': msg_text = 'RAM GDDR6 (Bank 1,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115A': msg_text = 'RAM GDDR6 (Bank 2,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115B': msg_text = 'RAM GDDR6 (Bank 1,2,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115C': msg_text = 'RAM GDDR6 (Bank 3,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115D': msg_text = 'RAM GDDR6 (Bank 1,3,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115E': msg_text = 'RAM GDDR6 (Bank 2,3,4,5,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080115F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5,7) - Single Beep, 1 second blue light, off.'
    # Duplicated 80801157-8080115F block removed
    elif err_code_hex[0:8] == '80801160': msg_text = 'RAM GDDR6 (Bank 6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801161': msg_text = 'RAM GDDR6 (Bank 1,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801162': msg_text = 'RAM GDDR6 (Bank 2,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801163': msg_text = 'RAM GDDR6 (Bank 1,2,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801164': msg_text = 'RAM GDDR6 (Bank 3,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801165': msg_text = 'RAM GDDR6 (Bank 1,3,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801166': msg_text = 'RAM GDDR6 (Bank 2,3,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801167': msg_text = 'RAM GDDR6 (Bank 1,2,3,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801168': msg_text = 'RAM GDDR6 (Bank 4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801169': msg_text = 'RAM GDDR6 (Bank 1,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116A': msg_text = 'RAM GDDR6 (Bank 2,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116B': msg_text = 'RAM GDDR6 (Bank 1,2,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116C': msg_text = 'RAM GDDR6 (Bank 3,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116D': msg_text = 'RAM GDDR6 (Bank 1,3,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116E': msg_text = 'RAM GDDR6 (Bank 2,3,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080116F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801170': msg_text = 'RAM GDDR6 (Bank 5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801171': msg_text = 'RAM GDDR6 (Bank 1,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801172': msg_text = 'RAM GDDR6 (Bank 2,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801173': msg_text = 'RAM GDDR6 (Bank 1,2,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801174': msg_text = 'RAM GDDR6 (Bank 3,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801175': msg_text = 'RAM GDDR6 (Bank 1,3,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801176': msg_text = 'RAM GDDR6 (Bank 2,3,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801177': msg_text = 'RAM GDDR6 (Bank 1,2,3,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801178': msg_text = 'RAM GDDR6 (Bank 4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801179': msg_text = 'RAM GDDR6 (Bank 1,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117A': msg_text = 'RAM GDDR6 (Bank 2,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117B': msg_text = 'RAM GDDR6 (Bank 1,2,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117C': msg_text = 'RAM GDDR6 (Bank 3,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117D': msg_text = 'RAM GDDR6 (Bank 1,3,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117E': msg_text = 'RAM GDDR6 (Bank 2,3,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080117F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5,6,7) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801180': msg_text = 'RAM GDDR6 (Bank 8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801181': msg_text = 'RAM GDDR6 (Bank 1,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801182': msg_text = 'RAM GDDR6 (Bank 2,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801183': msg_text = 'RAM GDDR6 (Bank 1,2,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801184': msg_text = 'RAM GDDR6 (Bank 3,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801185': msg_text = 'RAM GDDR6 (Bank 1,3,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801186': msg_text = 'RAM GDDR6 (Bank 2,3,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801187': msg_text = 'RAM GDDR6 (Bank 1,2,3,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801188': msg_text = 'RAM GDDR6 (Bank 4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801189': msg_text = 'RAM GDDR6 (Bank 1,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118A': msg_text = 'RAM GDDR6 (Bank 2,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118B': msg_text = 'RAM GDDR6 (Bank 1,2,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118C': msg_text = 'RAM GDDR6 (Bank 3,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118D': msg_text = 'RAM GDDR6 (Bank 1,3,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118E': msg_text = 'RAM GDDR6 (Bank 2,3,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080118F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801190': msg_text = 'RAM GDDR6 (Bank 5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801191': msg_text = 'RAM GDDR6 (Bank 1,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801192': msg_text = 'RAM GDDR6 (Bank 2,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801193': msg_text = 'RAM GDDR6 (Bank 1,2,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801194': msg_text = 'RAM GDDR6 (Bank 3,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801195': msg_text = 'RAM GDDR6 (Bank 1,3,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801196': msg_text = 'RAM GDDR6 (Bank 2,3,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801197': msg_text = 'RAM GDDR6 (Bank 1,2,3,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801198': msg_text = 'RAM GDDR6 (Bank 4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '80801199': msg_text = 'RAM GDDR6 (Bank 1,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119A': msg_text = 'RAM GDDR6 (Bank 2,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119B': msg_text = 'RAM GDDR6 (Bank 1,2,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119C': msg_text = 'RAM GDDR6 (Bank 3,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119D': msg_text = 'RAM GDDR6 (Bank 1,3,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119E': msg_text = 'RAM GDDR6 (Bank 2,3,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '8080119F': msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5,8) - Single Beep, 1 second blue light, off.'
    elif err_code_hex[0:8] == '808011A0': msg_text = 'RAM GDDR6 (Bank 6,8) - Single Beep, 1 second blue light, off.'

    return msg_text
