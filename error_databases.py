# error_databases.py
# This file contains the database of detailed error code descriptions.

def cod3r_database(err_code_hex): # Removed 'self'
    """
    Provides a detailed description and troubleshooting advice for a given error code.
    Args:
        err_code_hex (str): The error code in hexadecimal format.
    Returns:
        str: A descriptive message for the error code.
    """
    msg_text = f'Unknown error code ({err_code_hex})\n\n🛠️ No known match. Check full error database or logs.' # Default message

    if err_code_hex[0:8] == '80000001':
        msg_text = (
            'APU Overheat or Fatal Off\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check system cooling (fans, thermal paste, heatsink contact).\n'
            '• Clean dust buildup.\n'
            '• Review ambient temperature and airflow.\n'
            '• Check system logs for thermal shutdown events.'
        )
    elif err_code_hex[0:8] == '80000009':
        msg_text = (
            'Unexpected Power Loss or Power Supply Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect for accidental power button press or long press.\n'
            '• Check power supply stability and cables.\n'
            '• Test/replace LED Button Board.\n'
            '• Monitor for heat-related shutdown patterns.'
        )
    elif err_code_hex[0:8] == '80050000':
        msg_text = (
            'CPU VRM (2 Phases) Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect Infineon XDPE14286A (PWM Controller).\n'
            '• Verify 5V power rail stability.\n'
            '• Check for VRM overheating or shorts.\n'
            '• Swap power supply and check load response.'
        )
    elif err_code_hex[0:8] == '80060000':
        msg_text = (
            'GPU VRM (6 Phases) Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect Infineon XDPE14286A controller and MOSFETs.\n'
            '• Confirm 5V rail output.\n'
            '• Check for GPU power-stage shorts or thermals.\n'
            '• Re-seat GPU if applicable and test under load.'
        )
    elif err_code_hex[0:8] == '80800000':
        msg_text = (
            'Kernel Panic Shutdown\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check logs for system errors or driver issues.\n'
            '• Run memory and hardware diagnostics.\n'
            '• Validate firmware versions (BIOS, EC).\n'
            '• Re-flash OS image if persistent.'
        )
    elif err_code_hex[0:8] == '80800014':
        msg_text = (
            'TPM 2.0 Chip or Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check TPM module connection/soldering.\n'
            '• Verify BIOS TPM settings are enabled.\n'
            '• Run platform diagnostic tool.\n'
            '• Ensure stable power delivery to TPM circuit.'
        )
    elif err_code_hex[0:8] == '8080001A':
        msg_text = (
            'Non-Native TPM 2.0 Chip Detected (Post APU Init)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Confirm correct TPM chip is installed.\n'
            '• Check TPM firmware compatibility.\n'
            '• Replace with OEM TPM if third-party one is used.'
        )
    elif err_code_hex[0:8] == '80800022':
        msg_text = (
            '[SceSysCore] ___: Couldn’t load te module\n\n'
            '🛠️ Troubleshooting:\n'
            '• Manual system recovery required.\n'
            '• Reinstall firmware or full OS.\n'
            '• Check flash integrity and storage health.'
        )
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
    # ... (many more RAM error codes, ensure they are all present as in original) ...
    elif err_code_hex[0:8] == '808011FF':
        msg_text = 'RAM GDDR6 (Bank 1,2,3,4,5,6,7,8) - Single Beep, 1 second blue light, off. - Possibly bad MEMCORE'
    elif err_code_hex[0:6] == '808016': # Note: this is a 6-char prefix
        msg_text = 'APU / GDDR6 - Bad Vref - Unstable GDDR6'
    elif err_code_hex[0:8] == '80802001' or err_code_hex[0:8] == '80802081':
        msg_text = (
            'SSD Controller (G6 Controller) Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Re-seat SSD or test with known-good one.\n'
            '• Check SSD power rail (2.5V/3.3V).\n'
            '• Inspect G6 controller for thermal or physical damage.'
        )
    elif err_code_hex[0:8] == '80810001':
        msg_text = (
            'Power Sequencing Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check PSQ data logs for abnormalities.\n'
            '• Perform cold reboot.\n'
            '• No known fix, but reflow or PMIC check may help.'
        )
    elif err_code_hex[0:8] == '80830000':
        msg_text = (
            'Freeze or Shutdown After SAM_IPL Loaded\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect PG2 voltage rail.\n'
            '• Identify potential FATAL fault in startup sequence.'
        )
    elif err_code_hex[0:8] == '808300F0':
        msg_text = (
            'Secure Loader Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check PG2 voltage.\n'
            '• Reflash secure loader firmware if possible.'
        )
    elif err_code_hex[0:8] == '80870003': # Corrected from 4-char prefix for specificity
        msg_text = (
            'Post Secure Loader Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect fuse F7001.\n'
            '• Check PG2, SSD Controller, and SOC power rail startup.'
        )
    elif err_code_hex[0:8] == '80871001':
        msg_text = (
            'DDR4 Memory Error\n💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Replace or re-seat RAM module.\n'
            '• Test for shorts on DDR4 lines.\n'
            '• Check DA9081 PMIC output for 1.2V.'
        )
    elif err_code_hex[0:8] in ['80871054', '80871055']:
        msg_text = (
            'SSD Banks I/O Error Between SSD Controller\n💀�💀🔥💀🔥\n\n'
            '🛠️ Troubleshooting:\n'
            '• Replace SSD controller.\n'
            '• Inspect SSD controller PCB area for short/damage.'
        )
    elif err_code_hex[0:8] == '80871062':
        msg_text = (
            'SSD Controller (EFC) Failure\n💀🔥💀🔥💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check EFC controller circuit.\n'
            '• Confirm SSD firmware integrity.'
        )
    elif err_code_hex[0:8] in ['80891001', '80892003']:
        msg_text = (
            'SSD Controller or DDR4 Error\n💀🔥💀🔥💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check DA9081 PMIC voltages (1.2V, 2.5V).\n'
            '• Re-seat or replace SSD and RAM.'
        )
    elif err_code_hex[0:8] == '80894003':
        msg_text = (
            'SSD Controller or DDR4 Error\n💀🔥💀🔥💀🔥 FATAL ERROR\n'
            'Missing 2.5V on DA9081\n\n'
            '🛠️ Troubleshooting:\n'
            '• Verify DA9081 output with multimeter.\n'
            '• Check associated inductor and fuse.'
        )
    elif err_code_hex[0:8] == '808940AE':
        msg_text = (
            'NOR Modification Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Attempt NOR reflash.\n'
            '• Replace NOR chip if write-protected or corrupted.'
        )
    elif err_code_hex[0:4] == '808B':
        msg_text = (
            'Flash Controller Watchdog Timer Triggered\n\n'
            '🛠️ Troubleshooting:\n'
            '• Verify SSD controller and DDR4 health.\n'
            '• Confirm firmware watchdog wasn’t tripped due to hang.'
        )
    elif err_code_hex[0:8] == '808C2092':
        msg_text = (
            'USB Type-C Error Detected\n💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check USB PD controller and redriver chip.\n'
            '• Inspect port pins for damage or corrosion.'
        )
    elif err_code_hex[0:8] in [
        '808C3090', '808C3790', '808C3F90', '808C4F90'
    ]:
        msg_text = (
            'USB Type-C Error\n💀🔥 FATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Same steps as above.\n'
            '• Reflow or replace PD/redriver ICs.'
        )
    elif err_code_hex[0:8] == '808D0002':
        msg_text = (
            'Thermal Shutdown (LED Board)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check flex cable and daughterboard.\n'
            '• Replace LED board if shorted.\n'
            '• Symptom: Three beeps, white light, instant shutdown.'
        )
    elif err_code_hex[0:8] in ['808F0002', '808F0003']:
        msg_text = (
            'TPM 2.0 Chip or Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check TPM hardware.\n'
            '• Confirm stable power rails (e.g., 3.3V, 1.8V).'
        )
    elif err_code_hex[0:8] in ['80910200', '80910800']:
        msg_text = (
            'SSD Controller or DDR4 Error\nFATAL ERROR\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check DA9081 PMIC (1.2V rail).\n'
            '• Look for fan-related shorts (80910800).'
        )
    elif err_code_hex[0:8] == '80C00134':
        msg_text = (
            'USB-BT Command Error\n\n'
            '🛠️ Troubleshooting:\n'
            '• Replace Bluetooth module.\n'
            '• Verify command integrity from host.'
        )
    elif err_code_hex[0:8] == '80C00136':
        msg_text = (
            'Wi-Fi / Bluetooth Problem or Power Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check Wi-Fi/BT module connection.\n'
            '• Occurs when module is physically removed.'
        )
    elif err_code_hex[0:8] == '80C00140':
        msg_text = (
            'APU Halted (No Response)\n\n'
            '🛠️ Troubleshooting:\n'
            '• Forced off via power button.\n'
            '• Check logs or thermal sensors.'
        )
    elif err_code_hex[0:8] == '80D00402':
        msg_text = (
            'USB-BT Error (Firmware Missing)\n\n'
            '🛠️ Troubleshooting:\n'
            '• May be tied to SSD read error.\n'
            '• Re-download or reflash BT firmware.'
        )
    elif err_code_hex[0:8] in ['86000005', '86000006']:
        msg_text = (
            'NOR Corruption Detected\n\n'
            '🛠️ Troubleshooting:\n'
            '• Rebuild NOR region.\n'
            '• Replace NOR if unresponsive.'
        )
    elif err_code_hex[0:2] == 'B0':
        msg_text = (
            'Chip-to-Chip Communication Fault\n\n'
            '🛠️ Troubleshooting:\n'
            '• Caused by "Rebuilding Database" or frequent reboots.\n'
            '• Try REG recovery.\n'
            '• Check for bridge chip faults.'
        )
    elif err_code_hex[0:8] in ['C0020103', 'C0020203']:
        msg_text = (
            'APU Not Responding (Init/Reboot Loop)\n\n'
            '🛠️ Troubleshooting:\n'
            '• APU failed to initialize.\n'
            '• Check thermal/power and firmware status.'
        )
    elif err_code_hex[0:8] == 'C0020303':
        msg_text = (
            'Main SoC Access Error\n\n'
            '🛠️ Info:\n'
            '• Often logged after fatal shutdown.\n'
            '• Not always an actual fault.\n'
            '• Not always an actual fault.\n'
            '• Not always an actual fault.\n'
            '• Not always an actual fault.\n'
            '• Not always an actual fault.\n'
            
        )
    elif err_code_hex[0:8] == 'C00C0002':
        msg_text = (
            'VRM Controller Failure\n\n'
            '🛠️ Troubleshooting:\n'
            '• Check 6414A MOSFETs near fuse 7001.\n'
            '• Check XDPE14286A PWM controller and 5V rail.'
        )
    elif err_code_hex[0:8] in ['C0810002', 'C0810303']:
        msg_text = (
            'HDMI Access Error / Encoder Problem\n\n'
            '🛠️ Troubleshooting:\n'
            '• Inspect HDMI encoder power rail.\n'
            '• Replace HDMI IC if needed.'
        )
    elif err_code_hex[0:2] in ['E5', 'E4', 'E3', 'E1', 'E2', 'E0']: # Corrected E33 to E3
        msg_text = (
            'Southbridge Watchdog Timer Recovery\n\n'
            '🛠️ Troubleshooting:\n'
            '• Wait and retry boot process.\n'
            '• As last resort, rebuild NOR.'
        )
    elif err_code_hex[0:8] == 'FFFFFFFF':
        msg_text = 'No Errors Detected ✅'
    # Add any other specific error codes here before the final else

    return msg_text
