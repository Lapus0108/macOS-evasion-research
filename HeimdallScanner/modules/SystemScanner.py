import json
import datetime
from utils import *


class SystemScanner:
    def __init__(self, full_paths: bool):
        self.checks_results = []
        self.full_paths = full_paths
        self.utilities_paths = load_utilities_paths()

    def scan(self):
        self.sp_usb_info, self.sp_usb_cmd = get_system_profiler_info("SPUSBDataType", self.full_paths)
        self.sp_storage_info, self.sp_storage_cmd = get_system_profiler_info("SPStorageDataType", self.full_paths)
        self.sp_network_info, self.sp_network_cmd = get_system_profiler_info("SPNetworkDataType", self.full_paths)
        self.sp_hardware_info, self.sp_hardware_cmd = get_system_profiler_info("SPHardwareDataType", self.full_paths)
        self.sp_software_info, self.sp_software_cmd = get_system_profiler_info("SPSoftwareDataType", self.full_paths)

        self.ioreg_usb_info, self.ioreg_usb_cmd = get_ioreg_info("IOUSBHostDevice", self.full_paths)
        self.ioreg_platform_info, self.ioreg_platform_cmd = get_ioreg_info("IOPlatformExpertDevice", self.full_paths)

        # Identifiers & versions
        self.check_os_release()
        self.check_model_number()
        self.check_serial_number()
        self.check_model_identifier()
        self.check_firmware_version()
        
        # Hardware configuraiton
        self.check_chip()
        self.check_cpu_brand()
        self.check_memory_size()
        self.check_hardware_model()
        self.check_manufacturer()
        self.check_usb_manufacturer()
        self.check_usb_vendor_id()
        self.check_usb_vendor_ioreg()

        # Storage
        self.check_disk_size()
        self.check_storage_devices()

        # Others
        self.check_mac_address()
        self.check_virtualization_framework()
        self.check_sip_status_csrutil()
        self.check_sip_status_sp()
        self.check_sip_status_nvram()

        # Time
        self.check_uptime()
        self.check_boot_time()

        return self.checks_results

    def check_hardware_model(self):
        self.check_hardware_model_sp()
        self.check_hardware_model_ioreg()
        self.check_hardware_model_sysctl()
        self.check_hardware_model_powermetrics()

    def check_hardware_model_sysctl(self):
        label = 'Hardware model (sysctl)'
        binary_path = self.utilities_paths['sysctl'] if self.full_paths else 'sysctl'
        command = [binary_path, "-n", "hw.model"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': result['output'],
                'vm_detected': "VMware" in result['output'] or "Virtual" in result['output'],
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_hardware_model_sp(self):
        label = 'Hardware model (system_profiler)'
        result = self.sp_hardware_info

        if not command_had_errors(result):
            model_name_line = get_output_line(result['output'], "Model Name")
            if len(model_name_line) > 0:
                model_name = model_name_line.split(": ")[1]
            
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': model_name,
                'vm_detected': "virtual" in model_name.lower(),
                'status': 'success'
            })
        else: 
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_hardware_model_powermetrics(self):
        label = 'Hardware model (powermetrics)'
        binary_path = self.utilities_paths['powermetrics'] if self.full_paths else 'powermetrics'
        command = ["timeout", "5", binary_path]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            model_name = get_output_line(result['output'], "Machine model")

            if len(model_name) > 0:
                model_name = model_name.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': model_name,
                'vm_detected': "VMware" in result['output'] or "Virtual" in result['output'],
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_hardware_model_ioreg(self):
        label = 'Hardware model (ioreg)'
        result = self.ioreg_platform_info
        if not command_had_errors(result):
            model_name = get_output_line(result['output'], "\"model\" =")
            if len(model_name) > 0:
                model_name = model_name.split("= ")[1]
            
            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'result': model_name,
                'vm_detected': "vmware" in model_name.lower(),
                'status': 'success'
            })
        else: 
            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'error_message': result['error'],
                'status': 'error'
            })
        
    def check_model_identifier(self):
        label = 'Model identifier'
        result = self.sp_hardware_info
        if not command_had_errors(result):
            model_identifier_line = get_output_line(result['output'], "Model Identifier")
            if len(model_identifier_line) > 0:
                model_identifier = model_identifier_line.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': model_identifier,
                'vm_detected': "VMware" in model_identifier or "Virtual" in model_identifier,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_model_number(self):
        label = 'Model number'
        result = self.sp_hardware_info
        if not command_had_errors(result):
            model_number_line = get_output_line(result['output'], "Model Number")
            model_number = None
            if len(model_number_line) > 0:
                model_number = model_number_line.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': model_number,
                'vm_detected':  model_number and model_number.startswith("VM"),
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_serial_number(self):
        self.check_serial_number_sp()
        self.check_serial_number_ioreg()

    def check_serial_number_sp(self):
        label = 'Serial number (system_profiler)'
        result = self.sp_hardware_info
        if not command_had_errors(result):
            serial_number_line = get_output_line(result['output'], "Serial Number")
            if len(serial_number_line) > 0:
                serial_number = serial_number_line.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': serial_number,
                'vm_detected': serial_number and serial_number.startswith("VM"),
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_serial_number_ioreg(self):
        label = "Serial number (ioreg)"
        result = self.ioreg_platform_info
        if not command_had_errors(result):
            serial_number = get_output_line(result['output'], "IOPlatformSerialNumber")
            if len(serial_number) > 0:
                serial_number = serial_number.split("= ")[1]
                serial_number = remove_ioreg_formatting(serial_number)

            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'result': serial_number,
                'vm_detected': serial_number.startswith("VM"),
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_sip_status_csrutil(self):
        label = 'SIP status (csrutil)'
        binary_path = self.utilities_paths['csrutil'] if self.full_paths else 'csrutil'
        command = [binary_path, "status"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            status = result['output'].strip()
            if len(status) > 0:
                status = status.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': status,
                'vm_detected': "disabled" in status,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_sip_status_sp(self):
        label = 'SIP status (system_profiler)'
        result = self.sp_software_info

        if not command_had_errors(result):
            status_line = get_output_line(result['output'], "System Integrity Protection")
            if len(status_line) > 0:
                status = status_line.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': self.sp_software_cmd,
                'result': status,
                'vm_detected': status.lower() == "disabled",
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_software_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_sip_status_nvram(self):
        label = 'SIP status (nvram)'
        binary_path = self.utilities_paths['nvram'] if self.full_paths else 'nvram'
        command = [binary_path, "csr-active-config"]
        command_str = ' '.join(command)

        result = get_command_output(command)

        # If SIP is enabled, the variable is not found  -> Error (error code 1)
        if command_had_errors(result):
            status = result['output'].strip()
            status_parts = status.split('\t')
            bitmask = status_parts[1] if len(status_parts) > 1 else "-"

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': f"SIP Turned On (Variable not set)",
                'vm_detected': False,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': f"Turned off features bitmask: {bitmask}",
                'vm_detected': True,
                'status': 'success'
            })

    def check_firmware_version(self):
        label = 'System firmware version'
        result = self.sp_hardware_info
        if not command_had_errors(result):
            fw_version_line = get_output_line(result['output'], "System Firmware Version")
            if len(fw_version_line) > 0:
                firmware_version = fw_version_line.split(": ")[1]

            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': firmware_version,
                'vm_detected': firmware_version and firmware_version.startswith("VMW"),
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_disk_size(self):
        threshold = 250

        self.check_disk_size_df(threshold)
        self.check_disk_size_sp(threshold)
        self.check_disk_size_diskutil_info(threshold)
        self.check_disk_size_diskutil_list(threshold)

    def check_disk_size_df(self, threshold: int):
        label = "Disk size (df)"
        binary_path = self.utilities_paths['df'] if self.full_paths else 'df'
        command=[binary_path, "-h", "/"]
        command_str = ' '.join(command)
    
        result = get_command_output(command)
        if not command_had_errors(result):
            size_row = get_output_line(result['output'], "/dev/")
            size_row = remove_multiple_spaces(size_row)
            size_str = size_row.split(" ")[1]

            size = None
            if "Gi" in size_str:
                size = int(size_str.split("Gi")[0])
            elif "Ti" in size_str:
                size = 1000 * float(size_str.split("Ti")[0])

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': size_str,
                'vm_detected': size and size < threshold,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_disk_size_sp(self, threshold: int):
        label = "Disk size (system_profiler)"
        result = self.sp_storage_info

        if not command_had_errors(result):
            capacity_row = get_output_line(result['output'], "Capacity")
            capacity = None
            if len(capacity_row) > 0:
                capacity_str = capacity_row.split("Capacity: ")[1]
                if "GB" in capacity_str:
                    capacity = float(capacity_str.split(" ")[0].replace(",", "."))
                elif "TB" in capacity_str:
                    capacity = 1000 * float(capacity_str.split(" ")[0])

            self.checks_results.append({
                'label': label,
                'command': self.sp_storage_cmd,
                'result': capacity_str,
                'vm_detected': capacity and capacity < threshold,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_storage_cmd,
                'error_message': result['error'],
                'status': 'error'
            }) 

    def check_disk_size_diskutil_info(self, threshold: int):
        label = "Disk size (diskutil info)"
        binary_path = self.utilities_paths['diskutil'] if self.full_paths else 'diskutil'
        command=[binary_path, "info", "/"]
        command_str = ' '.join(command)
    
        result = get_command_output(command)
        if not command_had_errors(result):
            size_row = get_output_line(result['output'], "Disk Size:")
            size_row = remove_multiple_spaces(size_row)

            size = None
            size_str = ""
            if len(size_row) > 0:
                size_str = size_row.split(": ")[1]
                size = float(size_str.split(" ")[0])

                if "Ti" in size_str:
                    size = size * 1000

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': size_str,
                'vm_detected': size and size < threshold,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_disk_size_diskutil_list(self, threshold: int):
        label = "Disk size (diskutil list)"
        binary_path = self.utilities_paths['diskutil'] if self.full_paths else 'diskutil'
        command=[binary_path, "list", "physical"]
        command_str = ' '.join(command)
    
        result = get_command_output(command)
        if not command_had_errors(result):
            size_row = get_output_line(result['output'], "Apple_APFS ")
            size_row = remove_multiple_spaces(size_row)
            
            size = None
            size_str = ""
            if len(size_row) > 0:
                size_str = size_row.split(" ")[4] 
                unit = size_row.split(" ")[5]
                size = float(size_str) * 1000 if unit == "TB" else float(size_str)

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': size_str + " " + unit,
                'vm_detected': size < threshold,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_memory_size(self):
        label = 'Memory size'
        binary_path = self.utilities_paths["sysctl"] if self.full_paths else "sysctl"
        command = [binary_path, "-n", "hw.memsize"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        size_gb_int = int(result['output']) / 1024 / 1024 / 1024

        if not command_had_errors(result):
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': f"{size_gb_int} GB",
                'vm_detected': size_gb_int < 8,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_manufacturer(self):
        label = "Manufacturer"
        result = self.ioreg_platform_info
        if not command_had_errors(result):
            manufacturer_line = get_output_line(result['output'], "manufacturer")
            if len(manufacturer_line) > 0:
                manufacturer = manufacturer_line.split("= ")[1]
                manufacturer = remove_ioreg_formatting(manufacturer)
            else:
                manufacturer = None
        
            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'result': manufacturer,
                'vm_detected': manufacturer and "Apple Inc." not in manufacturer,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.ioreg_platform_cmd,
                'error_message': result['error'],
                'status': 'error'
            })
    
    def check_chip(self):
        label = "Chip"
        result = self.sp_hardware_info
        if not command_had_errors(result):
            chip_line = get_output_line(result['output'], "Chip")
            chip = None
            if len(chip_line) > 0:
                chip = chip_line.split(": ")[1]  

            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'result': chip,
                'vm_detected': chip and "Virtual" in chip,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_hardware_cmd,
                'error_message': result['error'],
                'status': 'error'
            })
    
    def check_cpu_brand(self):
        label = "CPU Brand"
        binary_path = self.utilities_paths["sysctl"] if self.full_paths else "sysctl"
        command = [binary_path, "-n", "machdep.cpu.brand_string"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            brand = result['output'].strip()

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': brand,
                'vm_detected': "Virtual" in brand,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })
    
    def check_os_release(self):
        label = "OS Release"
        binary_path = self.utilities_paths["uname"] if self.full_paths else "uname"
        command = [binary_path, "-v"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            release_verison = result['output'].strip()

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': release_verison,
                'vm_detected': "VMAPPLE" in release_verison,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_virtualization_framework(self):
        label = "Virtualization framework"
        binary_path = self.utilities_paths["sysctl"] if self.full_paths else "sysctl"
        command = [binary_path, "-n", "kern.hv_vmm_present"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            is_present = int(result['output'].strip())

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': is_present,
                'vm_detected': is_present == 1,
                'status': 'success'
            })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })
    
    def check_mac_address(self):
        self.check_mac_address_ifconfig()
        self.check_mac_address_sp()
        self.check_mac_address_ioreg()
        self.check_mac_address_networksetup()

    def check_mac_address_ifconfig(self):
        label = "MAC Address (ifconfig)"
        binary_path = self.utilities_paths["ifconfig"] if self.full_paths else "ifconfig"
        command = [binary_path]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            ether_lines = get_output_lines(result['output'], "ether")
            if len(ether_lines) > 0:
                ether_addresses = [line.split(" ")[1] for line in ether_lines]
                check_result = self.parse_ethernet_addresses(ether_addresses)
                    
                self.checks_results.append({
                    'label': label,
                    'command': command_str,
                    'result': check_result['message'],
                    'vm_detected': check_result['vm_detected'],
                    'status': 'success'
                })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_mac_address_sp(self):
        label = "MAC address (system_profiler)"

        if not command_had_errors(self.sp_network_info):
            ether_lines = get_output_lines(self.sp_network_info['output'], "MAC Address")
            if len(ether_lines) > 0:
                ether_addresses = [line.split("MAC Address: ")[1] for line in ether_lines]
                check_result = self.parse_ethernet_addresses(ether_addresses)

                self.checks_results.append({
                    'label': label,
                    'command': self.sp_network_cmd,
                    'result': check_result['message'],
                    'vm_detected': check_result['vm_detected'],
                    'status': 'success'
                })

        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_network_cmd,
                'error_message': self.sp_network_info['error'],
                'status': 'error'
            })

    def check_mac_address_ioreg(self):
        label = "Ethernet address"
        binary_path = self.utilities_paths["ioreg"] if self.full_paths else "ioreg"
        command = [binary_path, "-l"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            ether_lines = get_output_lines(result['output'], "IOMACAddress")
            if len(ether_lines) > 0:
                ether_addresses = []
                for addr in ether_lines:
                    addr_raw = remove_ioreg_formatting(addr.split("= ")[1])
                    addr_formatted = ":".join([addr_raw[i:i+2] for i in range(0, len(addr_raw), 2)])
                    ether_addresses.append(addr_formatted)

                check_result = self.parse_ethernet_addresses(ether_addresses) 
                self.checks_results.append({
                    'label': label,
                    'command': command_str,
                    'result': check_result['message'],
                    'vm_detected': check_result['vm_detected'],
                    'status': 'success'
                })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_mac_address_networksetup(self):
        label = "MAC Address (networksetup)"
        binary_path = self.utilities_paths["networksetup"] if self.full_paths else "networksetup"
        command = [binary_path, "-listallhardwareports"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            ether_lines = get_output_lines(result['output'], "Ethernet Address:")
            if len(ether_lines) > 0:
                ether_addresses = [line.split(": ")[1] for line in ether_lines]
                check_result = self.parse_ethernet_addresses(ether_addresses)
                    
                self.checks_results.append({
                    'label': label,
                    'command': command_str,
                    'result': check_result['message'],
                    'vm_detected': check_result['vm_detected'],
                    'status': 'success'
                })

        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def parse_ethernet_addresses(self, addresses: list):
        TARGET_BEGINNINGS = {
            '00:1C:42': 'Parallels',
            '08:00:27': 'VirtualBox',
            '00:06:09': 'VMWare',
            '00:0C:29': 'VMWare',
            '00:1C:14': 'VMWare',
            '00:50:56': 'VMWare',
            '00:16:E3': 'Xen'
        }

        target_addr_found = None
        target_prefix_found = None

        for ether_addr in addresses:
            ether_prefix = ether_addr[:8].upper()
            if ether_prefix in TARGET_BEGINNINGS.keys():
                target_addr_found = ether_addr
                target_prefix_found = ether_prefix
                
                if target_addr_found:
                    return {
                        'vm_detected': True,
                        'message': f"The prefix of the Ethernet address {target_addr_found} corresponds to {TARGET_BEGINNINGS[target_prefix_found]}"
                    }
        
        return {
            'vm_detected': False,
            'message': "The Ethernet addresses are not associated to any VM vendor."
        }

    def check_usb_manufacturer(self):
        label = "USB Devices Manufacturer"
        result = self.sp_usb_info

        if not command_had_errors(result):
            manufacturer_lines = get_output_lines(result['output'], "Manufacturer")
            manufacturers = []
            target_manufacturer = None
            if len(manufacturer_lines) > 0:
                for line in manufacturer_lines:
                    man_name = line.split(": ")[1]
                    manufacturers.append(man_name)
                    if "vmware" in man_name.lower():
                        target_manufacturer = "VMware"

            self.checks_results.append({
                'label': label,
                'command': self.sp_usb_cmd,
                'result': ', '.join(manufacturers),
                'vm_detected': target_manufacturer is not None,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_usb_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_usb_vendor_id(self):
        label = "USB Devices Vendor ID"
        result = self.sp_usb_info
        
        if not command_had_errors(result):
            vendor_lines = get_output_lines(result['output'], "Vendor ID")
            vendors = []
            target_vendor = None
            if len(vendor_lines) > 0:
                for line in vendor_lines:
                    vendor_name = line.split(": ")[1]
                    vendors.append(vendor_name)
                    if "vmware" in vendor_name.lower() or "0x0e0f" in vendor_name.lower():
                        target_vendor = "VMware"

            self.checks_results.append({
                'label': label,
                'command': self.sp_usb_cmd,
                'result': ', '.join(vendors),
                'vm_detected': target_vendor is not None,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': self.sp_usb_cmd,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_storage_devices(self):
        label = "Storage devices"
        
        if not command_had_errors(self.sp_storage_info):
            devices_lines = get_output_lines(self.sp_storage_info['output'], "Device Name")
            devices = []
            target_device = None
            if len(devices_lines) > 0:
                for line in devices_lines:
                    device_name = line.split(": ")[1]
                    devices.append(device_name)
                    if "vmware" in device_name.lower():
                        target_device = "VMware"

            self.checks_results.append({
                'label': label,
                'command': self.sp_storage_cmd,
                'result': ', '.join(devices),
                'vm_detected': target_device is not None,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command':self.sp_storage_cmd,
                'error_message': self.sp_storage_info['error'],
                'status': 'error'
            })

    def check_usb_vendor_ioreg(self):
        result = self.ioreg_usb_info
        if not command_had_errors(result):
            vendor_names = get_output_lines(result['output'], "USB Vendor Name")
            vendor_ids = get_output_lines(result['output'], "idVendor")
            
            for line in vendor_names:
                name_value = remove_ioreg_formatting(line.split("= ")[1])
                if "vmware" in name_value.lower():
                    self.checks_results.append({
                        'label': "Vendor Name (ioreg)",
                        'command': self.ioreg_platform_cmd,
                        'result': name_value,
                        'vm_detected': True,
                        'status': 'success'
                    })
                    break
            
            for line in vendor_ids:
                id_value = remove_ioreg_formatting(line.split("= ")[1])
                if int(id_value) == 1599 or int(id_value) == 1452:
                    self.checks_results.append({
                        'label': "Vendor ID (ioreg)",
                        'command': self.ioreg_platform_cmd,
                        'result': f"Vendor ID {id_value} is associated with VMware",
                        'vm_detected': True,
                        'status': 'success'
                    })
                    break
        else:
            self.checks_results.append({
                'label': "Vendor Name/ID (ioreg)",
                'command': self.ioreg_platform_cmd,
                'error_message': result['error'],
                'status': 'error'
            })
    
    def check_uptime(self):
        threshold_minutes = 5
        self.check_uptime_sp(threshold_minutes)

    def check_uptime_sp(self, threshold_minutes: int):
        label = 'Uptime (system_profiler)'
        sp_software_info_json, sp_software_cmd_json = get_system_profiler_info_json("SPSoftwareDataType", self.full_paths)

        if not command_had_errors(sp_software_info_json):
            command_output = json.loads(sp_software_info_json['output'])
            uptime = command_output['SPSoftwareDataType'][0]['uptime']
            uptime = uptime.split(" ")[1]

            # The format is days:hrs:mins:secs
            parts = uptime.split(":")
            if len(parts) > 3: 
                total_minutes = 24 * 60 * int(parts[0]) + 60 * int(parts[1]) + int(parts[2])
                self.checks_results.append({
                    'label': label,
                    'command': sp_software_cmd_json,
                    'result': uptime,
                    'vm_detected': total_minutes < threshold_minutes,
                    'status': 'success'
                })
            else:
                self.checks_results.append({
                    'label': label,
                    'command': sp_software_cmd_json,
                    'error_message': f"Invalid format for uptime: '{uptime}'",
                    'status': 'error'
                })
        else:
            self.checks_results.append({
                'label': label,
                'command': sp_software_cmd_json,
                'error_message': sp_software_info_json['error'],
                'status': 'error'
            })

    def check_boot_time(self):
        threshold_minutes = 10
        
        self.check_boot_time_who(threshold_minutes)
        self.check_boot_time_last(threshold_minutes)
        self.check_boot_time_powermetrics(threshold_minutes)
        self.check_boot_time_sysctl(threshold_minutes)

    def check_boot_time_who(self, threshold_minutes: int):
        label = "Boot time (who)"
        binary_path = self.utilities_paths["who"] if self.full_paths else "who"
        command = [binary_path, "-b"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            boot_date_parts = result['output'].split()[-3:]
            boot_date = datetime.datetime.strptime(" ".join(boot_date_parts), "%b %d %H:%M")
            boot_date_full = boot_date.replace(year=datetime.datetime.now().year)
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': boot_date_full,
                'vm_detected': calculate_date_diff_minutes(boot_date_full) < threshold_minutes,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_boot_time_last(self, threshold_minutes: int):
        label = "Boot time (last)"
        binary_path = self.utilities_paths["last"] if self.full_paths else "last"
        command = [binary_path, "reboot"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            last_boot_line = result['output'].split('\n')[0]
            
            boot_date_parts = last_boot_line.split()[-3:]
            boot_date = datetime.datetime.strptime(" ".join(boot_date_parts), "%b %d %H:%M")
            boot_date_full = boot_date.replace(year=datetime.datetime.now().year)

            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': boot_date_full,
                'vm_detected': calculate_date_diff_minutes(boot_date_full) < threshold_minutes,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_boot_time_powermetrics(self, threshold_minutes: int):
        label = 'Boot time (powermetrics)'
        binary_path = self.utilities_paths["powermetrics"] if self.full_paths else "powermetrics"
        command = ["timeout", "5", binary_path]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            boot_date_line = get_output_line(result['output'], "Boot time:")
            boot_date_raw = boot_date_line.split("Boot time: ")[1]

            boot_date = datetime.datetime.strptime(boot_date_raw, "%a %b %d %H:%M:%S %Y")
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': boot_date,
                'vm_detected': calculate_date_diff_minutes(boot_date) < threshold_minutes,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })

    def check_boot_time_sysctl(self, threshold_minutes: int):
        label = 'Boot time (sysctl)'
        binary_path = self.utilities_paths["sysctl"] if self.full_paths else "sysctl"
        command = [binary_path, "-n", "kern.boottime"]
        command_str = ' '.join(command)

        result = get_command_output(command)
        if not command_had_errors(result):
            boot_date_raw = result['output'].split("} ")[1]
            boot_date = datetime.datetime.strptime(boot_date_raw, "%a %b %d %H:%M:%S %Y")
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'result': boot_date,
                'vm_detected': calculate_date_diff_minutes(boot_date) < threshold_minutes,
                'status': 'success'
            })
        else:
            self.checks_results.append({
                'label': label,
                'command': command_str,
                'error_message': result['error'],
                'status': 'error'
            })