# gui.py
# This file contains the main UartTerminalGUI class and its methods.

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Toplevel
import serial
import serial.tools.list_ports
import threading
import time
import datetime # Keep for general datetime operations if any, though specific decoding is in decoders.py
import queue
import os
import sys

# Attempt to import Pillow for image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    # This print statement will appear in the console when gui.py is loaded
    # if Pillow is not available.
    print("Pillow library (PIL) not found. Image display will be disabled. Install with: pip install Pillow")

# Import functions from our other modules
import decoders
import error_databases # Assuming error_databases.py contains cod3r_database

# Set working directory to the script's directory
# This is important for finding resources like images in the 'src' subdirectory.
if getattr(sys, 'frozen', False):
    # If the program is frozen (like with PyInstaller), use this path:
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# We don't os.chdir() here as it's better to construct full paths to resources.
# application_path will be used for that.

class UartTerminalGUI:
    # Constants like TIME_ZERO and SEQ_DATABASE are now in decoders.py
    # and will be accessed via the decoders module if needed directly here,
    # or indirectly through the decoder functions.

    def __init__(self, master):
        self.master = master
        master.title("UART Terminal & Error Log Parser")

        self.style = ttk.Style(master)
        self.setup_styles() # Call user's style setup method

        master.configure(bg=self.bg_dark)

        self.serial_connection = None
        self.serial_thread = None
        self.stop_serial_thread = threading.Event()
        self.data_queue = queue.Queue()
        self.parsed_errlogs = []
        self.sending_errlogs_active = False
        self.current_errlog_index_for_sequence = 0

        # To store PhotoImage objects and prevent garbage collection
        self.image_references = {} # Initialize as an instance variable

        self.create_gui_elements()

        self.master.geometry("1000x850")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.populate_com_ports()
        self.process_serial_queue()
        self._update_interactive_button_states()


    def setup_styles(self):
        """Configures the ttk styles for a dark theme."""
        self.style.theme_use('clam')

        self.error_tag_color = "#FF6347" # Tomato Red
        self.warning_temp_color = "#FF8C00" # DarkOrange
        self.critical_error_color = "#FF6347" # Default critical, can be overridden by specific codes

        bg_dark = "#1E1E1E"
        bg_medium = "#2C2C2C"
        bg_light = "#3A3A3A"
        bg_soy = "#1E1E1E" # Background for soy image in detail window
        fg_text = "#E0E0E0"
        border_color = "#444444"
        accent_color = "#6A5ACD" # SlateBlue
        white_text = "#FFFFFF"
        font_family = 'Segoe UI Emoji' # Using a font that supports emojis well

        self.bg_dark = bg_dark
        self.bg_soy = bg_soy
        self.bg_medium = bg_medium
        self.bg_light = bg_light
        self.fg_text = fg_text
        self.border_color = border_color
        self.accent_color = accent_color
        self.white_text = white_text
        self.font_family = font_family

        self.style.configure("TFrame", background=bg_medium)
        self.style.configure("TLabel", background=bg_medium, foreground=fg_text, font=(font_family, 8))
        self.style.configure("Header.TLabel", background=bg_medium, foreground=accent_color,
                             font=(font_family, 9, 'bold'), anchor='w', padding=(0, 5, 0, 5))
        self.style.configure("Credit.TLabel", background=bg_medium, foreground=self.fg_text, # New style for credit
                             font=(font_family, 7, 'italic'))
        self.style.configure("TButton", background=accent_color, foreground=white_text,
                             font=(font_family, 8, 'bold'), borderwidth=0,
                             focusthickness=0, relief="flat", padding=(10, 5))
        self.style.map("TButton", background=[('active', '#7B68EE'), ('pressed', '#5C4BB3'), ('disabled', '#4A4A4A')],
                       foreground=[('active', white_text), ('disabled', border_color)])
        self.style.configure("Dark.TCombobox",
                             fieldbackground=bg_light, background=bg_medium,
                             foreground=fg_text, selectbackground=accent_color,
                             selectforeground=white_text, bordercolor=border_color,
                             arrowcolor=fg_text, padding=(4,4), relief="flat",
                             borderwidth=1, font=(font_family, 8))
        self.style.map("Dark.TCombobox",
                       fieldbackground=[("readonly", bg_light), ("disabled", bg_medium)],
                       background=[("readonly", bg_medium),("disabled", bg_dark)],
                       foreground=[("readonly", fg_text), ("disabled", border_color)],
                       bordercolor=[("focus", accent_color), ("hover", accent_color)],
                       arrowcolor=[("focus", accent_color), ("hover", accent_color), ("disabled", border_color)])
        self.style.configure("Vertical.TScrollbar", background=bg_medium, troughcolor=bg_dark,
                             bordercolor=border_color, arrowcolor=fg_text, relief="flat")
        self.style.map("Vertical.TScrollbar", background=[('active', accent_color)])
        self.style.configure("TSeparator", background=border_color)


    def create_gui_elements(self):
        # --- Connection Setup Section ---
        conn_section_frame = ttk.Frame(self.master, style="TFrame", padding=(10,5,10,0))
        conn_section_frame.pack(fill='x', pady=(10,0))
        ttk.Label(conn_section_frame, text="CONNECTION SETUP", style="Header.TLabel").pack(fill='x')

        conn_widgets_frame = ttk.Frame(conn_section_frame, style="TFrame", padding=(0, 5, 0, 5))
        conn_widgets_frame.pack(fill='x')

        ttk.Label(conn_widgets_frame, text="COM Port:", style="TLabel").grid(row=0, column=0, padx=(0,2), pady=5, sticky="w")
        self.com_port_var = tk.StringVar()
        self.com_port_combo = ttk.Combobox(conn_widgets_frame, textvariable=self.com_port_var, width=15, style='Dark.TCombobox', state='readonly')
        self.com_port_combo.grid(row=0, column=1, padx=(0,10), pady=5, sticky="ew")

        ttk.Label(conn_widgets_frame, text="Baud Rate:", style="TLabel").grid(row=0, column=2, padx=(10,2), pady=5, sticky="w")
        self.baud_rate_var = tk.StringVar(value='115200')
        self.baud_rate_combo = ttk.Combobox(conn_widgets_frame, textvariable=self.baud_rate_var, width=12, style='Dark.TCombobox', state='readonly',
                                            values=['9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600'])
        self.baud_rate_combo.grid(row=0, column=3, padx=(0,10), pady=5, sticky="ew")

        ttk.Label(conn_widgets_frame, text="Adapter:", style="TLabel").grid(row=0, column=4, padx=(10,2), pady=5, sticky="w")
        self.adapter_type_var = tk.StringVar(value="Pico")
        self.adapter_type_combo = ttk.Combobox(conn_widgets_frame, textvariable=self.adapter_type_var, width=15, style='Dark.TCombobox', state='readonly',
                                               values=["Pico", "CH341", "Generic USB-to-TTL(Prolific)", "Other"])
        self.adapter_type_combo.grid(row=0, column=5, padx=(0,10), pady=5, sticky="ew")
        self.adapter_type_combo.bind("<<ComboboxSelected>>", lambda event: self._update_interactive_button_states()) # Though it doesn't affect wiring/pinout buttons anymore

        self.connect_button = ttk.Button(conn_widgets_frame, text="Connect", command=self.toggle_connection, style='TButton', width=10)
        self.connect_button.grid(row=1, column=3, columnspan=1, padx=(0,5), pady=(10,5), sticky="e")

        self.refresh_ports_button = ttk.Button(conn_widgets_frame, text="Refresh", command=self.populate_com_ports, style='TButton', width=8)
        self.refresh_ports_button.grid(row=1, column=4, columnspan=1, padx=(0,5), pady=(10,5), sticky="w")

        conn_widgets_frame.columnconfigure(1, weight=1)
        conn_widgets_frame.columnconfigure(3, weight=1)
        conn_widgets_frame.columnconfigure(5, weight=1)

        # --- Device Commands Section ---
        cmd_section_frame = ttk.Frame(self.master, style="TFrame", padding=(10,5,10,0))
        cmd_section_frame.pack(fill='x', pady=5)
        ttk.Label(cmd_section_frame, text="DEVICE COMMANDS", style="Header.TLabel").pack(fill='x')

        cmd_widgets_frame = ttk.Frame(cmd_section_frame, style="TFrame", padding=(0,5,0,5))
        cmd_widgets_frame.pack(fill='x')

        buttons_container = ttk.Frame(cmd_widgets_frame, style="TFrame")
        buttons_container.pack(pady=5)

        self.version_button = ttk.Button(buttons_container, text="GET Version", command=self.send_version_command, state=tk.DISABLED, style='TButton')
        self.version_button.pack(side="left", padx=5)
        self.errlog_button = ttk.Button(buttons_container, text="GET Error Logs (5)", command=self.send_errlog_command, state=tk.DISABLED, style='TButton')
        self.errlog_button.pack(side="left", padx=5)
        self.custom_cmd_button = ttk.Button(buttons_container, text="Send Custom Command", command=self.open_custom_command_dialog, state=tk.DISABLED, style='TButton')
        self.custom_cmd_button.pack(side="left", padx=5)
        self.clear_errlog_button = ttk.Button(buttons_container, text="Clear Error Logs", command=self.clear_error_logs, state=tk.DISABLED, style='TButton')
        self.clear_errlog_button.pack(side="left", padx=5)
        self.wiring_guide_button = ttk.Button(buttons_container, text="Wiring Guide", command=self.open_wiring_guide_window, state=tk.NORMAL, style='TButton')
        self.wiring_guide_button.pack(side="left", padx=5)
        self.pinout_button = ttk.Button(buttons_container, text="Pinout", command=self.open_pinout_window, state=tk.NORMAL, style='TButton')
        self.pinout_button.pack(side="left", padx=5)

        # --- Main Output Area (Console and Logs) ---
        output_area_frame = ttk.Frame(self.master, style="TFrame")
        output_area_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        console_section_frame = ttk.Frame(output_area_frame, style="TFrame", padding=(0,0,0,0))
        console_section_frame.pack(fill="both", expand=False) # Will grow with intro_text_label
        ttk.Label(console_section_frame, text="UART CONSOLE", style="Header.TLabel").pack(fill='x', padx=(10,0))

        console_intro_container = ttk.Frame(console_section_frame, style="TFrame")
        console_intro_container.pack(fill="both", expand=True, padx=10, pady=(5,0))

        self.general_output_text = scrolledtext.ScrolledText(
            console_intro_container, height=10, width=80, font=("Consolas", 9), wrap=tk.WORD,
            bg=self.bg_light, fg=self.fg_text, insertbackground=self.white_text,
            selectbackground=self.accent_color, selectforeground=self.white_text,
            relief="solid", borderwidth=1, bd=0, highlightthickness=1,
            highlightbackground=self.border_color, highlightcolor=self.accent_color)
        self.general_output_text.pack(side="left", fill="both", expand=False) # Console fixed width, but can expand height
        self.general_output_text.configure(state='disabled')

        intro_text_content = (
            "\n🛠️ Welcome to the UART Tool! Here's how to get started:\n\n"
            "✅ SELECT COM PORT & ADAPTER\n✅ CLICK CONNECT\n\n"
            "📥 GET ERROR LOGS:\n   Click to fetch the latest (5) error logs.\n\n"
            "🔍 VIEW DETAILED LOG:\n   Double-click an error entry for details.\n\n"
            "⌨️ SEND CUSTOM COMMANDS:\n   Use for your own UART commands.\n\n"
            "🧹 CLEAR ERROR LOGS:\n   Clears logs from Console & ListBox.\n\n"
            "� WIRING GUIDE / PINOUT:\n   Access adapter-specific guides.\n\n"
            "💡 If you have questions or need help, just ask!\n\n"
        )
        self.intro_text_label = ttk.Label(
            console_intro_container, text=intro_text_content, font=("Segoe UI Emoji", 9),
            wraplength=320, justify=tk.LEFT, style="TLabel", # TLabel will use its configured bg/fg
            background=self.bg_light, foreground=self.fg_text) # Explicitly set to match console
        self.intro_text_label.pack(side="right", fill="both", expand=True, padx=(10,0))

        logs_section_frame = ttk.Frame(output_area_frame, style="TFrame", padding=(0,0,0,0))
        logs_section_frame.pack(fill="both", expand=True, pady=(5,0))
        ttk.Label(logs_section_frame, text="PARSED ERROR LOGS (Double-Click to Open Log Data)", style="Header.TLabel").pack(fill='x', padx=(10,0))
        listbox_container_frame = ttk.Frame(logs_section_frame, style="TFrame")
        listbox_container_frame.pack(padx=10, pady=(5,0), fill="both", expand=True)
        self.listbox = tk.Listbox(listbox_container_frame, font=("Segoe UI Emoji", 10), selectmode=tk.SINGLE, height=8,
                                bg=self.bg_light, fg=self.fg_text,
                                selectbackground=self.accent_color, selectforeground=self.white_text,
                                relief="solid", borderwidth=1, highlightthickness=0,
                                exportselection=False, bd=0, highlightbackground=self.border_color)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(listbox_container_frame, orient="vertical", command=self.listbox.yview, style='Vertical.TScrollbar')
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind("<Double-Button-1>", self.on_double_click_listbox)

    def _update_interactive_button_states(self):
        is_connected = self.serial_connection and self.serial_connection.is_open
        # Wiring Guide and Pinout buttons are always active, so no need to manage them here.
        if is_connected:
            self.version_button.config(state=tk.NORMAL)
            # Disable errlog button only if sequence is active, otherwise enable if connected
            self.errlog_button.config(state=tk.DISABLED if self.sending_errlogs_active else tk.NORMAL)
            self.custom_cmd_button.config(state=tk.NORMAL)
            self.clear_errlog_button.config(state=tk.NORMAL)
        else:
            self.version_button.config(state=tk.DISABLED)
            self.errlog_button.config(state=tk.DISABLED)
            self.custom_cmd_button.config(state=tk.DISABLED)
            self.clear_errlog_button.config(state=tk.DISABLED)

    def log_to_general_output(self, message, tag=None):
        self.general_output_text.configure(state='normal')
        if not message.endswith('\n'): message += '\n'
        if tag: self.general_output_text.insert(tk.END, message, (tag,))
        else: self.general_output_text.insert(tk.END, message)
        self.general_output_text.see(tk.END)
        self.general_output_text.configure(state='disabled')

    def populate_com_ports(self):
        """
        Populates the COM port dropdown with available ports and their descriptions.
        The com_port_var will store a string like "COMx - Description".
        """
        try:
            com_port_objects = serial.tools.list_ports.comports()
            # Format each entry to include both device and description
            # e.g., "COM3 - USB Serial Port (COM3)"
            # or "COM4 - Prolific USB-to-Serial Comm Port"
            port_details = [f"{port.device} - {port.description}" for port in com_port_objects]
            
            self.com_port_combo['values'] = port_details
            
            if port_details:
                self.com_port_var.set(port_details[0])
                # If you need to log the selected port and its description:
                # self.log_to_general_output(f"Selected default COM port: {port_details[0]}", tag="info_tag")
            else:
                self.com_port_var.set("")
                self.log_to_general_output("No COM ports found.", tag="info_tag")
        except Exception as e:
            self.com_port_var.set("")
            self.com_port_combo['values'] = []
            self.log_to_general_output(f"Error populating COM ports: {e}", tag="error_tag")

    def toggle_connection(self):
        if self.serial_connection and self.serial_connection.is_open: self.disconnect_serial()
        else: self.connect_serial()

    def connect_serial(self):
        port = self.com_port_var.get().split(" - ")[0].strip()
        baud = self.baud_rate_var.get()
        if not port or not baud:
            messagebox.showerror("Error", "COM Port and Baud Rate must be selected.")
            self.log_to_general_output("COM Port/Baud Rate not selected.", tag="error_tag")
            return
        try:
            self.serial_connection = serial.Serial(port, int(baud), timeout=0.1)
            self.log_to_general_output(f"Connected to {port} at {baud} baud.", tag="info_tag")
            self.connect_button.config(text="Disconnect")
            for widget in [self.com_port_combo, self.baud_rate_combo, self.adapter_type_combo, self.refresh_ports_button]:
                widget.config(state=tk.DISABLED)
            self._update_interactive_button_states()
            self.stop_serial_thread.clear()
            self.serial_thread = threading.Thread(target=self.read_serial_data, daemon=True)
            self.serial_thread.start()
        except (serial.SerialException, ValueError) as e:
            error_msg = f"(PC ERROR) Connection failed: {e}"
            if isinstance(e, ValueError): error_msg = f"(PC ERROR) Invalid Baud Rate: {e}"
            # self.data_queue.put(error_msg) # data_queue is for received serial data
            self.log_to_general_output(f"(ERROR) {error_msg}", tag="error_tag")
            if self.serial_connection: self.serial_connection.close()
            self.serial_connection = None
            self._update_interactive_button_states() # Re-enable connection widgets

    def disconnect_serial(self):
        self.sending_errlogs_active = False # Stop any ongoing errlog sequence
        if self.serial_thread and self.serial_thread.is_alive():
            self.stop_serial_thread.set()
            try:
                self.serial_thread.join(timeout=1.0)
                if self.serial_thread.is_alive(): self.log_to_general_output("Serial reader thread did not terminate cleanly.", tag="error_tag")
            except Exception as e: self.log_to_general_output(f"Error joining serial thread: {e}", tag="error_tag")
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.close()
                self.log_to_general_output("Disconnected.", tag="info_tag")
            except Exception as e: self.log_to_general_output(f"Error closing serial port: {e}", tag="error_tag")
        self.serial_connection = None
        self.connect_button.config(text="Connect")
        for widget in [self.com_port_combo, self.baud_rate_combo, self.adapter_type_combo]:
            widget.config(state='readonly') # Re-enable as readonly
        self.refresh_ports_button.config(state=tk.NORMAL)
        self._update_interactive_button_states() # Update command buttons
        self.listbox.delete(0, tk.END) # Clear listbox on disconnect
        self.general_output_text.configure(state='normal')
        self.general_output_text.delete("1.0", tk.END)
        self.general_output_text.configure(state='disabled')
        self.log_to_general_output("Disconnected.", tag="info_tag") # Log after clearing

    def open_custom_command_dialog(self):
        dialog = Toplevel(self.master)
        dialog.title("Send Custom Command"); dialog.geometry("400x180"); dialog.resizable(False, False)
        dialog.configure(bg=self.bg_medium); dialog.transient(self.master); dialog.grab_set()
        ttk.Label(dialog, text="Enter your custom command:", style="TLabel").pack(pady=(15, 8))
        command_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=command_var, width=45, font=(self.font_family, 9))
        entry.pack(pady=(0, 12), ipady=4); entry.focus_set()
        def send_command_local():
            cmd = command_var.get().strip()
            if cmd: self.send_command(cmd); command_var.set(""); entry.focus_set()
        ttk.Button(dialog, text="Send", command=send_command_local, style="TButton").pack(pady=5)
        dialog.bind('<Return>', lambda event: send_command_local())

    def clear_error_logs(self):
        self.listbox.delete(0, tk.END); self.parsed_errlogs.clear()
        self.send_command("errlog clear") # Send command to device if needed

    def _calculate_checksum(self, data_string):
        csum = 0
        for char_val in data_string.encode('utf-8', errors='replace'): csum = (csum + char_val) & 0xFF
        return csum

    def send_command(self, command_str):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                adapter_type = self.adapter_type_var.get()
                
                # Track last command for echo detection
                self.last_sent_command = command_str.strip()
                
                if adapter_type in ["CH341", "Generic USB-to-TTL(Prolific)", "Other"]:
                    checksum = self._calculate_checksum(command_str)
                    checksum_hex = f"{checksum:02X}"
                    full_command = f"{command_str}:{checksum_hex}\n"
                    log_msg = f"Sent (Chksum: {checksum_hex}): {command_str}"
                else:  # Pico or no-checksum
                    full_command = f"{command_str}\n"
                    log_msg = f"Sent: {command_str}"
                
                self.serial_connection.write(full_command.encode('utf-8', errors='replace'))
                self.log_to_general_output(log_msg, tag="sent_tag")

            except serial.SerialException as e:
                self.log_to_general_output(f"Error sending command '{command_str}': {e}", tag="error_tag")
                self.disconnect_serial()
            except Exception as e:
                self.log_to_general_output(f"Unexpected error sending command '{command_str}': {e}", tag="error_tag")
        else:
            self.log_to_general_output(f"Not connected. Cannot send command: {command_str}", tag="error_tag")
            if not (hasattr(self, 'showing_not_connected_warning') and self.showing_not_connected_warning):
                self.showing_not_connected_warning = True
                messagebox.showwarning("Not Connected", "Please connect to a serial port first.")
                self.showing_not_connected_warning = False


    def send_version_command(self): self.send_command("version")

    def send_errlog_command(self):
        if self.sending_errlogs_active: self.log_to_general_output("Errlog sequence already in progress.", tag="info_tag"); return
        if not (self.serial_connection and self.serial_connection.is_open): messagebox.showwarning("Not Connected", "Please connect first."); return
        self.sending_errlogs_active = True; self.errlog_button.config(state=tk.DISABLED) # Disable during sequence
        self.log_to_general_output("Starting errlog sequence (0 to 5)...", tag="info_tag")
        self.current_errlog_index_for_sequence = 0; self._send_one_errlog_in_sequence()

    def _send_one_errlog_in_sequence(self):
        if not self.sending_errlogs_active:
            if self.serial_connection and self.serial_connection.is_open: self.errlog_button.config(state=tk.NORMAL) # Re-enable if still connected
            else: self.errlog_button.config(state=tk.DISABLED)
            return

        if self.current_errlog_index_for_sequence <= 5:
            command_to_send = f"errlog {self.current_errlog_index_for_sequence}"
            if not (self.serial_connection and self.serial_connection.is_open):
                self.log_to_general_output(f"Connection lost. Aborting errlog sequence.", tag="error_tag")
                self.sending_errlogs_active = False; self.errlog_button.config(state=tk.DISABLED); return
            self.send_command(command_to_send)
            self.current_errlog_index_for_sequence += 1
            if self.current_errlog_index_for_sequence <= 5: self.master.after(250, self._send_one_errlog_in_sequence)
            else:
                self.log_to_general_output("Finished sending all errlog parts (0-5).", tag="info_tag")
                self.sending_errlogs_active = False
                if self.serial_connection and self.serial_connection.is_open: self.errlog_button.config(state=tk.NORMAL)
        else: # Should not be reached if logic is correct
            self.log_to_general_output("Errlog sequence completed (unexpected state).", tag="info_tag")
            self.sending_errlogs_active = False
            if self.serial_connection and self.serial_connection.is_open: self.errlog_button.config(state=tk.NORMAL)


    def read_serial_data(self):
        buffer = ""
        echo_handled = False

        while not self.stop_serial_thread.is_set():
            try:
                if self.serial_connection and self.serial_connection.is_open:
                    if self.serial_connection.in_waiting > 0:
                        data = self.serial_connection.read(self.serial_connection.in_waiting)
                        buffer += data.decode('utf-8', errors='replace')

                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            clean_line = line.strip('\r').strip()

                            if not clean_line:
                                continue

                            if hasattr(self, 'last_sent_command') and self.last_sent_command:
                                sent = self.last_sent_command.strip()

                                # Echo handling: print once if exact match
                                if clean_line.lower() == sent.lower():
                                    if not echo_handled:
                                        self.data_queue.put(f"> {sent}")
                                        echo_handled = True
                                    continue

                            # Any non-empty non-echo line
                            self.data_queue.put(clean_line)

                            # Reset echo flag if new valid line received
                            echo_handled = False

                else:
                    if not self.stop_serial_thread.is_set():
                        self.data_queue.put("SERIAL_CONNECTION_LOST")
                    break

            except serial.SerialException:
                if not self.stop_serial_thread.is_set():
                    self.data_queue.put("(PC ERROR) COM PORT UNPLUGGED OR BUSY")
                break

            except Exception as e:
                if not self.stop_serial_thread.is_set():
                    self.data_queue.put(f"UNEXPECTED_READ_ERROR: {e}")
                break

            time.sleep(0.02)





    def process_serial_queue(self):
        try:
            while not self.data_queue.empty():
                line = self.data_queue.get_nowait()
                if line in ["SERIAL_CONNECTION_LOST", "(PC ERROR) COM PORT UNPLUGGED OR BUSY"] or \
                   (isinstance(line, str) and (line.startswith("SERIAL_READ_ERROR:") or line.startswith("UNEXPECTED_READ_ERROR:"))):
                    self.log_to_general_output(f"Serial issue: {line}", tag="error_tag")
                    self.disconnect_serial() # This handles UI updates
                    return # Stop processing queue for now
                self.log_to_general_output(f"> {line.strip()}", tag="recv_tag")
                if line.startswith("OK "): self.parse_and_add_errlog_entry(line)
        finally:
            self.master.after(100, self.process_serial_queue) # Reschedule

    def parse_and_add_errlog_entry(self, line):
        parts = line.split()
        if parts and parts[0] == "OK" and len(parts) == 10:
            try:
                record_data = {'RawLine': line, 'Ack': parts[1], 'Code': parts[2], 'Rtc': parts[3],
                               'PowState': parts[4], 'UpCause': parts[5], 'SeqNo': parts[6],
                               'DevPm': parts[7], 'T_SoC': parts[8]}
                t_env_checksum_part = parts[9]
                if ':' in t_env_checksum_part: record_data['T_Env'], record_data['Checksum'] = t_env_checksum_part.split(':', 1)
                else: record_data['T_Env'] = t_env_checksum_part; record_data['Checksum'] = "N/A"

                # Use TIME_ZERO from the decoders module
                record_data['Rtc_Decoded'] = decoders._decode_rtc(record_data['Rtc'])
                # Store timestamp for sorting if decoding was successful
                if record_data['Rtc_Decoded'] != "Invalid RTC":
                     record_data['Rtc_UnixTimestamp'] = decoders.TIME_ZERO + int(record_data['Rtc'], 16)
                else:
                    record_data['Rtc_UnixTimestamp'] = 0 # For sorting purposes if RTC is invalid

                self.parsed_errlogs.append(record_data)
                self.update_errlog_listbox()
            except Exception as e:
                self.log_to_general_output(f"Error processing errlog line '{line.strip()}': {e}", tag="error_tag")

    def update_errlog_listbox(self):
        self.parsed_errlogs.sort(key=lambda record: record.get('Rtc_UnixTimestamp', 0), reverse=True)
        self.listbox.delete(0, tk.END)
        default_fg = self.listbox.cget('fg')

        for i, record in enumerate(self.parsed_errlogs):
            raw_code = record.get('Code', 'N/A')
            rtc_decoded = record.get('Rtc_Decoded', 'N/A') # Already decoded
            # Use decoders module for functions
            decoded_error_message = decoders._decode_err_code(raw_code).strip() if raw_code != 'N/A' else 'N/A'
            seq_display_part_str = f"SEQ: {decoders._decode_seq_no(record.get('SeqNo', 'N/A'))}" if raw_code == "80810001" else ""
            decoded_t_soc_compact = decoders._decode_temp_soc(record.get('T_SoC', 'N/A')).replace(' °C', '')
            decoded_t_env_compact = decoders._decode_temp_env(record.get('T_Env', 'N/A')).replace(' °C', '')

            listbox_entry_parts = [f"➔", f"{i:02d}", f"RTC: {rtc_decoded}", f"Code: {raw_code} ({decoded_error_message})"]
            if seq_display_part_str: listbox_entry_parts.append(seq_display_part_str)
            listbox_entry_parts.extend([f"SoC: {decoded_t_soc_compact}°", f"ENV: {decoded_t_env_compact}°"])
            self.listbox.insert(tk.END, " | ".join(filter(None, listbox_entry_parts)))

            item_index = self.listbox.size() - 1; current_item_color = default_fg; colored = False
            # Simplified coloring logic for brevity in this example, use your full logic
            if raw_code.startswith("8080") and len(raw_code) == 8: current_item_color = self.critical_error_color; colored = True
            elif raw_code.startswith("C0020303"): current_item_color = "#C5FC00"; colored = True # Lime Green
            elif raw_code.startswith("8081"): current_item_color = self.critical_error_color; colored = True
            # ... (add more of your specific coloring rules)
            elif raw_code.startswith("80000009"): current_item_color = "#00FC00"; colored = True # Bright Green

            if colored: self.listbox.itemconfig(item_index, {'fg': current_item_color})
            elif not colored and decoded_t_soc_compact not in ['N/A', "Invalid Hex Temp"]:
                try:
                    if float(decoded_t_soc_compact) > 50: self.listbox.itemconfig(item_index, {'fg': self.warning_temp_color})
                except ValueError: pass

    def on_double_click_listbox(self, event):
        sel = self.listbox.curselection()
        if sel:
            if 0 <= sel[0] < len(self.parsed_errlogs): self.show_detail_window(sel[0])
            else: messagebox.showerror("Error", "Invalid selection."); self.log_to_general_output("Invalid listbox selection.", "error_tag")

    def show_detail_window(self, index):
        if not (0 <= index < len(self.parsed_errlogs)): return
        record_data = self.parsed_errlogs[index]
        detail_window = Toplevel(self.master); detail_window.configure(bg=self.bg_soy)
        detail_window.title(f"Log Details - Index {index:02d}"); detail_window.transient(self.master)
        detail_window.grab_set(); detail_window.minsize(800, 700)

        field_info = [ # Use functions from decoders and error_databases modules
            ('Raw Line:', 'RawLine', None), ('Code:', 'Code', decoders._decode_err_code),
            ('RTC:', 'Rtc', decoders._decode_rtc), ('Powerstate:', 'PowState', decoders._decode_pw_state),
            ('UPCAUSE:', 'UpCause', decoders._decode_upcause), ('SeqNo (PSQ):', 'SeqNo', decoders._decode_seq_no),
            ('DevPM:', 'DevPm', decoders._decode_devpower), ('TSOC:', 'T_SoC', decoders._decode_temp_soc),
            ('TENV:', 'T_Env', decoders._decode_temp_env), ('Description:', 'Code', error_databases.cod3r_database)] # Updated call

        container = ttk.Frame(detail_window, style='TFrame', padding=(10,5,10,5)); container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=0); container.columnconfigure(1, weight=1); container.columnconfigure(2, weight=2)
        r = 0
        for lbl_txt, key, dec_fn in field_info:
            if lbl_txt == 'System Notes:':
                # Get raw values
                raw_line_raw = record_data.get('RawLine', 'N/A')
                code_raw = record_data.get('Code', 'N/A')
                seq_raw = record_data.get('SeqNo', 'N/A')

                # Decode values (handle None or 'N/A')
                raw_line_dec = raw_line_raw if raw_line_raw == 'N/A' else str(raw_line_raw)  # No decoder for RawLine
                code_dec = decoders._decode_err_code(code_raw) if code_raw != 'N/A' else "N/A"
                seq_dec = decoders._decode_seq_no(seq_raw) if seq_raw != 'N/A' else "N/A"

                # Get cod3r_database description (safe fallback)
                cod3r_desc = error_databases.cod3r_database(code_raw) if code_raw != 'N/A' else "N/A"
                if not cod3r_desc:
                    cod3r_desc = f"No description found for code {code_raw}"

                # Font styles
                lbl_fnt = (self.font_family, 12, "bold")
                lbl_fg = "#2E86C1"
                dec_fnt = (self.font_family, 11)
                dec_fg = self.white_text

                if r > 0:
                    ttk.Separator(container, orient='horizontal').grid(row=r, column=0, columnspan=3, sticky='ew', pady=(8,8))
                    r += 1

                # Label for "Description:"
                ttk.Label(container, text="Description:", font=lbl_fnt, foreground=lbl_fg).grid(
                    row=r, column=0, padx=(0,0.2), pady=6, sticky="nw"
                )

                # Text to copy (only first 3 lines)
                copy_text = (
                    f"{raw_line_dec}\n"
                    f"Code: {code_dec}\n"
                    f"SeqNo (PSQ): {seq_raw} — {seq_dec}"
                )

                def copy_to_clipboard():
                    detail_window.clipboard_clear()
                    detail_window.clipboard_append(copy_text)
                    detail_window.update()

                # Copy button next to the description label
                copy_btn = ttk.Button(container, text="Copy Code To Clipboard", command=copy_to_clipboard)
                copy_btn.grid(row=r, column=1, padx=(5,10), pady=6, sticky="w")

                # Build combined multi-line string with cod3r_database desc appended
                combined_text = (
                    f"{raw_line_dec}\n"
                    f"Code: {code_dec}\n"
                    f"SeqNo (PSQ): {seq_raw} — {seq_dec}\n\n"
                    f"{cod3r_desc}"
                )

                ttk.Label(
                    container,
                    text=combined_text,
                    font=dec_fnt,
                    foreground=dec_fg,
                    wraplength=600,
                    justify="left"
                ).grid(row=r, column=2, padx=(0,5), pady=6, sticky="w")

                r += 1
                continue





            # Normal handling for other fields
            raw_val = record_data.get(key, 'N/A')
            dec_val_str = dec_fn(raw_val) if dec_fn and raw_val != 'N/A' else ("N/A" if dec_fn else "")
            lbl_fnt, lbl_fg, val_fnt, dec_fnt, dec_fg = (self.font_family,8,"bold"), self.fg_text, ("Segoe UI Emoji",10), (self.font_family,10,"bold"), self.fg_text

            ttk.Label(container,text=lbl_txt,font=lbl_fnt,foreground=lbl_fg).grid(row=r,column=0,padx=(0,0.2),pady=6,sticky="nw")
            ttk.Label(container,text=str(raw_val),font=val_fnt,foreground=lbl_fg,wraplength=250).grid(row=r,column=1,padx=(0,0.2),pady=6,sticky="w")
            if dec_val_str:
                cur_fg = dec_fg
                if dec_val_str == "N/A" or "Unknown" in dec_val_str or "Invalid" in dec_val_str:
                    cur_fg = "#AAAAAA"
                elif "Error" in dec_val_str:
                    cur_fg = self.error_tag_color
                ttk.Label(container,text=dec_val_str,font=dec_fnt,foreground=cur_fg,wraplength=350).grid(row=r,column=2,padx=(0,5),pady=6,sticky="w")
            r += 1
        
        # --- Add Error Code Specific Image / Default Image ---
        if PIL_AVAILABLE:
            err_code_val = record_data.get('Code', '')
            image_to_load = None
            placeholder_text_for_image = "No specific image available."
            default_image_filename = "default_image.png"  # User needs to provide this in src/

            # Try full code first (e.g., 80801001.png)
            if err_code_val:
                full_code_image = f"{err_code_val}.png"
                full_code_path = os.path.join(application_path, "src", full_code_image)
                if os.path.exists(full_code_path):
                    image_to_load = full_code_image
                    placeholder_text_for_image = f"Context image for {err_code_val}"
            
            # If no exact match, try 6-digit group image (e.g., 808010.png)
            if not image_to_load and len(err_code_val) >= 6:
                group_code_image = f"{err_code_val[:6]}.png"
                group_code_path = os.path.join(application_path, "src", group_code_image)
                if os.path.exists(group_code_path):
                    image_to_load = group_code_image
                    placeholder_text_for_image = f"Context image for group {err_code_val[:6]}"

            # If no group match, use default image
            if not image_to_load:
                default_image_path = os.path.join(application_path, "src", default_image_filename)
                if os.path.exists(default_image_path):
                    image_to_load = default_image_filename
                    placeholder_text_for_image = "Default context image"

            # Display the image if any was found
            if image_to_load:
                code_image_label = ttk.Label(container, style="TLabel", background=self.bg_light, relief="solid", anchor="center")
                code_image_label.grid(row=r, column=0, columnspan=3, sticky="nsew", padx=5, pady=10)
                self._load_and_display_image(code_image_label, image_to_load, placeholder_text_for_image, max_width=380, max_height=200)
                r += 1

            # else:
                # Optionally, add a text label saying "No image available" if neither specific nor default is found
                # no_image_label = ttk.Label(container, text="No context image available.", style="TLabel")
                # no_image_label.grid(row=r, column=0, columnspan=3, sticky="ew", padx=5, pady=10)
                # r += 1


        # soy.png (small logo, placed separately)
        if PIL_AVAILABLE: 
            try:
                img_path = os.path.join(application_path, "src", "soy.png") 
                if os.path.exists(img_path):
                    pil_img = Image.open(img_path).resize((100, 100), Image.Resampling.LANCZOS)
                    self.image_references['soy_detail_logo'] = ImageTk.PhotoImage(pil_img)
                    soy_label = ttk.Label(detail_window, image=self.image_references['soy_detail_logo'], background=self.bg_medium)
                    soy_label.place(relx=1.0,rely=1.0,anchor="se",x=-10,y=-10)
            except Exception as e: self.log_to_general_output(f"Error loading soy.png for detail window: {e}", "error_tag")

    def _load_and_display_image(self, label_widget, image_filename, placeholder_text, max_width=320, max_height=200):
        """Helper to load, resize, and display an image or show placeholder text."""
        if not PIL_AVAILABLE:
            label_widget.config(text=placeholder_text, image='', font=(self.font_family, 10, "italic"), padding=(10,50))
            return

        image_path = os.path.join(application_path, "src", image_filename) 
        try:
            if not os.path.exists(image_path):
                # If the primary image (specific or default) is not found, display the placeholder text.
                label_widget.config(text=f"{placeholder_text}\n(File not found: {image_filename})", image='', font=(self.font_family, 8, "italic"), padding=(10,10))
                # self.log_to_general_output(f"Image not found: {image_filename}", "info_tag") # Less alarming than error
                return # Stop here if file not found

            pil_img = Image.open(image_path)
            original_width, original_height = pil_img.size
            if original_width == 0 or original_height == 0 : 
                raise ValueError("Image has zero width or height")

            ratio = min(max_width / original_width, max_height / original_height) if original_width > 0 and original_height > 0 else 1
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            new_width = max(1, new_width) 
            new_height = max(1, new_height)

            resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            img_ref_key = f"{label_widget.winfo_id()}_{image_filename}" 
            self.image_references[img_ref_key] = ImageTk.PhotoImage(resized_img)
            
            label_widget.config(image=self.image_references[img_ref_key], text="", padding=(0,0)) 
        except Exception as e: # Catch other PIL errors or general exceptions
            label_widget.config(text=f"{placeholder_text}\n(Error loading: {str(e)[:50]})", image='', font=(self.font_family, 8, "italic"), padding=(10,10))
            # self.log_to_general_output(f"Error loading image {image_filename}: {e}", "error_tag")

    def open_wiring_guide_window(self):
        wiring_window = Toplevel(self.master)
        wiring_window.configure(bg=self.bg_medium)
        wiring_window.transient(self.master)
        wiring_window.grab_set()
        wiring_window.geometry("1000x800")

        adapter_type = self.adapter_type_var.get()
        guide_title_text = f"Wiring Guide: {adapter_type}"
        guide_content_text = (
            f"No specific wiring guide is currently available for the selected '{adapter_type}' adapter.\n\n"
            "General UART Wiring Principles:\n"
            "1. Ensure logic levels (e.g., 3.3V/5V) match target.\n"
            "2. Connect GND to target GND.\n"
            "3. Connect adapter TXD to target RXD.\n"
            "4. Connect adapter RXD to target TXD.\n"
            "5. Only connect VCC if target needs power and voltages match."
        )
        img1_filename, img2_filename = None, None
        img1_desc, img2_desc = "Image 1: General", "Image 2: Details"


        if adapter_type == "CH341":
            guide_title_text = "CH341A Wiring Guide (3.3V UART Mode)"
            guide_content_text = """CH341A Programmer - UART (Serial) Mode & 3.3V Setup

**IMPORTANT: Ensure the CH341A is UNPLUGGED from USB before making any changes.**

**Part 1: Setting 3.3V Logic Level for Serial Interface**
Most CH341A programmers default to 5V logic levels for the serial header pins, which can damage 3.3V target devices.
To ensure 3.3V operation for the TXD/RXD signals:

1.  **Understand CH341A Voltages:** The main 3.3V/5V jumper on many CH341A boards (near the ZIF socket) often only changes the VCC pin for the SPI/I2C modes. The serial TX/RX logic level might still be 5V by default on some boards.
2.  **Check TXD Voltage:** The most reliable way is to power the CH341A (in serial mode, see Part 2) and measure the idle voltage on its TXD pin with a multimeter (TXD to GND). It should be ~3.3V. If it's 5V, you may need a logic level shifter or a CH341A board known to output 3.3V on serial lines.
3.  **Using 3.3V VCC Output (Optional Powering):** If your CH341A board has a dedicated 3.3V output pin on its serial header, you can use this to power a 3.3V target device. Do not assume the main VCC pin on the serial header is 3.3V unless verified.

**Part 2: Setting Serial Mode & Connecting Jumpers for UART**
The CH341A typically has a mode selection jumper (often labeled P/S - Programmer/Serial, usually a 2x3 pin header).

1.  **Enable Serial Mode:**
    * Locate the mode selection jumper.
    * To activate UART/Serial mode, place a jumper cap to connect pins 2 and 3 (usually the pair furthest from the USB connector on that header, or as indicated by your board's silkscreen for "Serial" or "UART"). This isolates the ZIF socket from the serial lines.

2.  **Identify UART Pins on the Serial Header:**
    * Pins are typically labeled: **GND, RXD, TXD**. There might also be **VCC (often +5V)** and a **+3.3V** output pin.
    * **Crucially verify your board's specific pinout.**

3.  **Wiring to Target Device (e.g., MCU):**
    * **CH341A GND** -> **Target Device GND** (Essential common ground).
    * **CH341A TXD** (Transmit, ensure 3.3V logic) -> **Target Device RXD** (Receive input of target).
    * **CH341A RXD** (Receive, ensure 3.3V tolerant) -> **Target Device TXD** (Transmit output of target).
    * **(Optional Power) CH341A +3.3V Pin (if available and verified)** -> **Target Device VCC/3.3V input**.
        * Only if target is 3.3V and needs power from CH341A. If target is self-powered, do not connect any VCC pin.

**After Wiring:**
1.  Carefully double-check all connections, especially GND and signal lines.
2.  Plug the CH341A programmer into a USB port.
3.  In this UART Terminal, select the correct COM port, set "CH341" as adapter.
4.  Click "Connect".

*(Placeholder for images: 1. CH341A board highlighting serial mode jumper and serial pins. 2. Diagram of correct TX/RX cross-connection and GND.)*"""
            img1_filename = "CH341A.png"
            img1_desc = "CH341A: Mode Jumper & Serial Pins"
            # img2_filename = "ch341_wiring.png" # Example if you have a second image
            img2_desc = "CH341A: UART Wiring"


        elif adapter_type == "Generic USB-to-TTL(Prolific)":
            guide_title_text = "Generic USB-to-TTL(Prolific) Wiring Guide (UART)"
            guide_content_text = """Generic USB-to-TTL(Prolific) USB-to-Serial Adapter - UART Wiring

**IMPORTANT: Generic USB-to-TTL(Prolific) modules can operate at 3.3V or 5V logic levels. Verify your module's logic level and ensure it's compatible with your target device to prevent damage.**

**1. Identify UART Pins:**
    * Generic USB-to-TTL(Prolific) modules typically have at least four essential pins clearly labeled:
        * **VCC** (Power output from the adapter. Can be 5V or 3.3V. Some modules provide both via different pins or a selector jumper.)
        * **GND** (Ground)
        * **TXD** (Transmit Data - output from Generic USB-to-TTL(Prolific), its logic level matches the module's operating voltage)
        * **RXD** (Receive Data - input to Generic USB-to-TTL(Prolific), must be tolerant to target's TXD voltage)

**2. Determine and Set Logic Level (If Applicable):**
    * Check module documentation, silkscreen, or measure the TXD pin voltage (to GND) when powered.
    * If your module has a voltage selection jumper (e.g., for 5V/3.3V), set it for your target. The TXD signal level will correspond to this.

**3. Wiring to Target Device:**
    * **Generic USB-to-TTL(Prolific) GND** -> **Target Device GND** (Essential common ground).
    * **Generic USB-to-TTL(Prolific) TXD** -> **Target Device RXD** (Data from Generic USB-to-TTL(Prolific) to target's receive pin).
    * **Generic USB-to-TTL(Prolific) RXD** -> **Target Device TXD** (Data from target's transmit pin to Generic USB-to-TTL(Prolific)).
    * **(Optional Power) Generic USB-to-TTL(Prolific) VCC (or specific +3.3V pin)** -> **Target Device VCC (Matching voltage)**.
        * Only if target needs power from Generic USB-to-TTL(Prolific) and voltage matches (e.g., 3.3V to a 3.3V device).
        * If target is self-powered, it's generally safer NOT to connect VCC from the Generic USB-to-TTL(Prolific).

**After Wiring:**
1.  Double-check all connections.
2.  Plug the Generic USB-to-TTL(Prolific) adapter into USB. Install drivers if needed.
3.  In this UART Terminal, select the correct COM port, set "Generic USB-to-TTL(Prolific)" as adapter.
4.  Click "Connect".

*(Placeholder for images: 1. Common Generic USB-to-TTL(Prolific) module with pin labels. 2. Wiring diagram for Generic USB-to-TTL(Prolific) to a target MCU.)*"""
            # img1_filename = "Generic USB-to-TTL(Prolific)_module.png" # Example
            # img2_filename = "Generic USB-to-TTL(Prolific)_wiring.png" # Example
            img1_desc = "Generic USB-to-TTL(Prolific) Module: Pinout Example (Placeholder)"
            img2_desc = "Generic USB-to-TTL(Prolific): TX/RX/GND to Target (Placeholder)"

        wiring_window.title(guide_title_text)
        main_frame = ttk.Frame(wiring_window, style="TFrame", padding=10); main_frame.pack(fill="both", expand=True)
        ttk.Label(main_frame, text=guide_title_text, style="Header.TLabel", font=(self.font_family, 11, "bold")).pack(fill='x', pady=(0,10))
        
        text_area_container = ttk.Frame(main_frame, style="TFrame"); text_area_container.pack(fill="both", expand=True, pady=(0,10))
        text_area = scrolledtext.ScrolledText(text_area_container, height=15, font=(self.font_family, 9), wrap=tk.WORD, # Reduced height for images
                                             bg=self.bg_light, fg=self.fg_text, insertbackground=self.white_text,
                                             selectbackground=self.accent_color, selectforeground=self.white_text,
                                             relief="solid", borderwidth=1, bd=0, highlightthickness=1,
                                             highlightbackground=self.border_color, highlightcolor=self.accent_color)
        text_area.pack(side="left", fill="both", expand=True)
        text_area.configure(state='normal'); text_area.delete("1.0", tk.END); text_area.insert(tk.END, guide_content_text); text_area.configure(state='disabled')

        images_frame = ttk.Frame(main_frame, style="TFrame"); images_frame.pack(fill="both", expand=True, pady=(10,0)) # expand True
        images_frame.columnconfigure(0, weight=1) # Allow first image column to expand
        images_frame.columnconfigure(1, weight=1) # Allow second image column to expand
        images_frame.rowconfigure(0, weight=1)    # Allow image row to expand

        img_placeholder1 = ttk.Label(images_frame, text=img1_desc, style="TLabel", background=self.bg_light, relief="solid", anchor="center")
        img_placeholder1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5) # Use grid
        if img1_filename: self._load_and_display_image(img_placeholder1, img1_filename, img1_desc, max_width=330, max_height=250)
        else: img_placeholder1.config(font=(self.font_family, 10, "italic"), padding=(10,80))


        img_placeholder2 = ttk.Label(images_frame, text=img2_desc, style="TLabel", background=self.bg_light, relief="solid", anchor="center")
        img_placeholder2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5) # Use grid
        if img2_filename: self._load_and_display_image(img_placeholder2, img2_filename, img2_desc, max_width=330, max_height=250)
        else: img_placeholder2.config(font=(self.font_family, 10, "italic"), padding=(10,80))


        ttk.Button(main_frame, text="Close", command=wiring_window.destroy, style="TButton").pack(pady=(20,10), side="bottom")


    def open_pinout_window(self):
        pinout_window = Toplevel(self.master)
        pinout_window.title("Pinout Information")
        pinout_window.geometry("1050x800")
        pinout_window.configure(bg=self.bg_medium)
        pinout_window.transient(self.master)
        pinout_window.grab_set()

        main_scroll_frame = ttk.Frame(pinout_window, style="TFrame")
        main_scroll_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(main_scroll_frame, bg=self.bg_medium, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_scroll_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        scrollable_frame = ttk.Frame(canvas, style="TFrame", padding=10)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")

        ttk.Label(scrollable_frame, text="Device Pinouts", style="Header.TLabel").pack(fill='x', pady=(0,10))
        pinout_items_frame = ttk.Frame(scrollable_frame, style="TFrame")
        pinout_items_frame.pack(fill="both", expand=True)

        pinout_image_data = [
            {"file": "EDM_010_020_UART.png", "title": "EDM 010/020 UART", "desc": "Pinout for EDM_010/020."},
            {"file": "EDM_03x_UART.png", "title": "EDM 03x UART", "desc": "Pinout for EDM_03x series."},
            {"file": "SLIM_PRO_UART.png", "title": "SLIM/PRO UART", "desc": "Pinout for SLIM/PRO models."},
            #{"file": None, "title": "Image 4: General Purpose", "desc": "Placeholder for another pinout."} # Placeholder for 4th
        ]

        cols = 3
        for i, data in enumerate(pinout_image_data):
            row, col = i // cols, i % cols
            cell_frame = ttk.Frame(pinout_items_frame, style="TFrame", padding=10)
            cell_frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            pinout_items_frame.columnconfigure(col, weight=1)
            
            ttk.Label(cell_frame, text=data["title"], style="Header.TLabel", font=(self.font_family, 9, "bold")).pack(fill="x", pady=(0,3))
            
            img_label = ttk.Label(cell_frame, text=data["desc"], style="TLabel", background=self.bg_light, relief="solid", anchor="center")
            img_label.pack(fill="both", expand=True, pady=(0,5)) # Fill and expand to take space

            if data["file"]:
                self._load_and_display_image(img_label, data["file"], data["desc"], max_width=300, max_height=220) # Adjusted size
            else: # Fallback for placeholder if no file
                 img_label.config(font=(self.font_family, 10, "italic"), padding=(10,80))


            desc_label = ttk.Label(cell_frame, text=data["desc"], style="TLabel", anchor="center", font=(self.font_family, 8), wraplength=280)
            desc_label.pack(fill="x", pady=(3,0))
            
            # Corrected placement of update_wraplength_factory and its binding
            def update_wraplength_factory(label_to_update, cell_frame_widget):
                def _update_wraplength(event):
                    new_wraplength = cell_frame_widget.winfo_width() - 10 
                    if new_wraplength > 20 : 
                        label_to_update.config(wraplength=new_wraplength)
                return _update_wraplength
            
            cell_frame.bind("<Configure>", update_wraplength_factory(desc_label, cell_frame), add="+")
        
        # --- Add Credit Label ---
        credit_text = "Pinout Images Source: stetofix (gbatemp.net)"
        credit_label = ttk.Label(scrollable_frame, text=credit_text, style="Credit.TLabel")
        credit_label.pack(pady=(15, 5), side="bottom") 

        ttk.Button(scrollable_frame, text="Close", command=pinout_window.destroy, style="TButton").pack(pady=(5,10), side="bottom")


    def on_closing(self):
        self.log_to_general_output("Application closing...", tag="info_tag")
        self.disconnect_serial()
        if hasattr(self, 'master') and self.master.winfo_exists(): 
             try: self.master.destroy()
             except tk.TclError: pass 

    # --- Decoder Functions ---
    # (Your extensive decoder functions: _decode_rtc, _decode_err_code, etc. are now called via 'decoders' module)
    # The actual implementations are in decoders.py

    def _decode_rtc(self, rtc_hex):
        return decoders._decode_rtc(rtc_hex)

    def cod3r_database(self, err_code_hex):
        return error_databases.cod3r_database(err_code_hex)

    def _decode_err_code(self, err_code_hex):
        return decoders._decode_err_code(err_code_hex)

    def _decode_pw_state(self, pw_state_hex):
        return decoders._decode_pw_state(pw_state_hex)

    def _decode_upcause(self, bt_trg_hex):
        return decoders._decode_upcause(bt_trg_hex)

    def _decode_devpower(self, dvpw_i_hex):
        return decoders._decode_devpower(dvpw_i_hex)

    def convert_to_celsius(self, hex_value): 
        return decoders.convert_to_celsius(hex_value)

    def _decode_seq_no(self, seq_no_hex):
        return decoders._decode_seq_no(seq_no_hex)

    def _decode_temp_soc(self, t_soc_hex):
        return decoders._decode_temp_soc(t_soc_hex)

    def _decode_temp_env(self, t_env_hex):
        return decoders._decode_temp_env(t_env_hex)

# Note: The main application launch (if __name__ == "__main__":) will be in a separate main.py
