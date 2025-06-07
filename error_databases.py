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

    return msg_text
