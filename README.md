# PS5 UART Error Code Decoder

This repository contains two main components for working with PS5 UART error codes:

1. **Pi Pico UF2 Firmware**  
2. **Windows-Based GUI Tool**

---

## 1. Pi Pico UF2 Firmware

This firmware runs on the Raspberry Pi Pico microcontroller and uses GPIO 0 and GPIO 1 pins as a USB-TTL serial adapter.

### Features
- Implements USB-TTL serial communication via GPIO 0 (TX) and GPIO 1 (RX)
- Compatible with standard serial terminal programs
- Enables PS5 UART error code data collection through USB
- Enables Automatic Checksum of UART commands for use with third party terminals such as Putty

### Usage
1. Flash the provided UF2 firmware file onto your Raspberry Pi Pico.
2. Connect the Pico to the PS5 UART lines via GPIO 0 and GPIO 1.
3. Plug the Pico into your PC via USB.
4. The Pico will enumerate as a USB serial device for UART communication.

---

## 2. Windows-Based GUI Tool

A simple Windows graphical user interface tool designed to:

- Collect UART data from the Pi Pico USB serial device
- Decode PS5 UART error codes in real-time
- Display error information clearly for troubleshooting

![image](https://github.com/user-attachments/assets/ef9eb53d-54a4-46ab-8c33-f4531ff6d85e)
![image](https://github.com/user-attachments/assets/462dfca3-c9c0-43d7-bc68-db0fece4e954)

### Features
- Auto-detects connected Pi Pico USB serial device
- Parses and decodes PS5-specific UART error codes
- Provides user-friendly error descriptions and status
- Logs error data for later analysis

### Usage
1. Connect the Raspberry Pi Pico running the UF2 firmware to your Windows PC.
2. Launch the GUI tool.
3. Select the correct COM port if not auto-detected.
4. Start monitoring to collect and decode UART error codes from your PS5.

---

## Requirements

- Raspberry Pi Pico board
- Windows PC for GUI tool
- USB cable for Pico connection

---

## Installation & Setup

### Firmware
1. Download the latest UF2 firmware from the `releases` section.
2. Hold the BOOTSEL button on the Pico while plugging it into USB.
3. Drag and drop the UF2 file onto the mounted drive.

### GUI Tool
- Run the executable or build from source (if applicable).
- Ensure the Pico is connected and recognized as a serial device.

---

## Contributing

Contributions and suggestions are welcome! Please open issues or pull requests for improvements, bug fixes, or feature requests.

---

## Support Me

If you find this project useful, please consider supporting me:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green)](https://www.paypal.me/dannyjohn08)

Or simply click here: https://www.paypal.me/dannyjohn08

---

## License

Specify your license here (e.g., MIT, GPL, etc.)

---

## Contact

For questions or support, please open an issue or contact me directly.
