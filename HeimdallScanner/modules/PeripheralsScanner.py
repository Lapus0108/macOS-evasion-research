import json
from utils import *

class PeripheralsScanner:
    SCORES = {
        'low': 10,
        'medium': 20,
        'high': 30
    }

    TOTAL_THRESHOLD = 40

    SEVERITY_LEVELS = {
        'has_camera': 'high',
        'has_keyboard': 'high',
        'connected_bluetooth_devices': 'low',

        'wifi_connected_network': 'medium',
        'wifi_nearby_networks': 'low',

        'built_in_speaker': 'high',
        'built_in_microphone': 'high',
        'audio_bluetooth_devices': 'low',

        'displays_number': 'high',
        'built_in_display': 'high',
        'virtualization_vendor_id': 'high',
        'suspicious_pixels_resolution': 'medium'
    }

    def __init__(self, full_paths: bool):
        self.full_paths = full_paths
        self.utilities_paths = load_utilities_paths()

        self.network = {
            'wifi_connected_network': None,
            'wifi_nearby_networks': 0
        }

        self.audio = {
            'built_in_speaker': False,
            'built_in_microphone': False,
            'audio_bluetooth_devices': 0
        }

        self.displays = {
            'displays_number': 0,
            'built_in_display': False,
            'virtualization_vendor_id': False,
            'suspicious_pixels_resolution': False
        }

        self.misc = {
            'has_camera': False,
            'has_keyboard': False,
            'connected_bluetooth_devices': 0
        }

        self.final_scores = {
            'network': 0,
            'audio': 0,
            'displays': 0,
            'misc': 0
        }

    def scan(self):
        self.check_camera()
        self.check_keyboard()
        self.check_displays()
        self.check_networks()
        self.check_audio_devices()
        self.check_bluetooth_devices()

        return self.calculate_scores()

    def check_camera(self):
        result, command = get_system_profiler_info_json("SPCameraDataType", self.full_paths)

        if not command_had_errors(result):
            command_output = json.loads(result['output'].encode('utf-8'))
            if len(command_output['SPCameraDataType']) > 0:
                self.misc['has_camera'] = True
            else:
                self.increase_score('misc', 'has_camera')

    def check_keyboard(self):
        result, command = get_ioreg_info("IOHIDDevice", self.full_paths)

        if not command_had_errors(result):
            keyboard_lines = get_output_lines(result['output'], "Keyboard")
            for line in keyboard_lines:
                if "Apple Internal Keyboard" in line:
                    self.misc['has_keyboard'] = True

            # Increment score
            if not self.misc['has_keyboard']:
                self.increase_score('misc', 'has_keyboard')

    def check_audio_devices(self):
        result, command = get_system_profiler_info_json("SPAudioDataType", self.full_paths)

        if not command_had_errors(result):
            command_output = json.loads(result['output'])
            devices_info = command_output['SPAudioDataType'][0]["_items"]
            
            for device in devices_info:
                device_type = device["coreaudio_device_transport"] if "coreaudio_device_transport" in device else "unknown"
                manufacturer = device["coreaudio_device_manufacturer"] if "coreaudio_device_manufacturer" in device else "unknown"

                if device_type == "coreaudio_device_type_builtin" and manufacturer == "Apple Inc.":
                    if "Speakers" in device["_name"]:
                        self.audio['built_in_speaker'] = True
                    elif "Microphone" in device["_name"]:
                        self.audio['built_in_microphone'] = True
                    
                if device_type == "coreaudio_device_type_bluetooth":
                    self.audio['audio_bluetooth_devices'] += 1
            
            # Increment score
            if not self.audio['built_in_speaker']:
                self.increase_score('audio', 'built_in_speaker')

            if not self.audio['built_in_microphone']:
                self.increase_score('audio', 'built_in_microphone')

            if self.audio['audio_bluetooth_devices'] == 0:
                self.increase_score('audio', 'audio_bluetooth_devices')  

    def check_bluetooth_devices(self):
        result, command = get_system_profiler_info_json("SPBluetoothDataType", self.full_paths)

        if not command_had_errors(result):
            command_output = json.loads(result['output'])
            devices_info = command_output["SPBluetoothDataType"][0]
            if "device_connected" in devices_info:
                devices_number = len(devices_info["device_connected"])
                self.misc['connected_bluetooth_devices'] = devices_number
                # Increment score
                if devices_number == 0:
                    self.increase_score('misc', 'connected_bluetooth_devices')  

    def check_networks(self):
        result, command = get_system_profiler_info_json("SPAirPortDataType", self.full_paths)

        if not command_had_errors(result):
            command_output = json.loads(result['output'])      
            networks_info = command_output["SPAirPortDataType"][0]
            if "spairport_airport_interfaces" in networks_info and len(networks_info["spairport_airport_interfaces"]) > 0:
                networks_info = networks_info["spairport_airport_interfaces"][0]
                current_network =  networks_info["spairport_current_network_information"]["_name"] if 'spairport_current_network_information' in networks_info else None
                nearby_networks = len(networks_info["spairport_airport_other_local_wireless_networks"])
                
                self.network['wifi_connected_network'] = current_network
                self.network['wifi_nearby_networks'] = nearby_networks

                # Increment score
                if nearby_networks == 0:
                    self.increase_score('network', 'wifi_nearby_networks')  
                
                if current_network is None:
                    self.increase_score('network', 'wifi_connected_network')         

    def check_displays(self):
        result, command = get_system_profiler_info_json("SPDisplaysDataType", self.full_paths)
        
        if not command_had_errors(result):
            command_output = json.loads(result['output'])
            displays_info = command_output['SPDisplaysDataType'][0]
            if "spdisplays_ndrvs" in displays_info:
                displays = displays_info["spdisplays_ndrvs"]
                
                # Number of displays
                self.displays['displays_number'] = len(displays)
                if len(displays) == 0:
                    self.increase_score('displays', 'displays_number')
                
                # Vendor ID associated to VMware or virtualization software
                if "spdisplays_vendor-id" in displays_info and displays_info["spdisplays_vendor-id"] == "0x15ad": 
                    self.displays['virtualization_vendor_id'] = True
                    self.increase_score('displays', 'virtualization_vendor_id')
                
                # Built-In Display
                if "sppci_bus" in displays_info and displays_info["sppci_bus"] == 'spdisplays_builtin':
                    self.displays['built_in_display'] = True

                if "sppci_model" in displays_info and "Apple" in displays_info["sppci_model"]:
                    self.displays['built_in_display'] = True

                # Built-In Display & Resolution 
                for display in displays:
                    if "spdisplays_display_type" in display and "spdisplays_built-in" in display["spdisplays_display_type"]:
                        self.displays['built_in_display'] = True

                    if "_spdisplays_pixels" in display:
                        pixels = display["_spdisplays_pixels"]
                        pixels_parts = pixels.split(" ")
                        if int(pixels_parts[0]) < 1900 or int(pixels_parts[2]) < 1000: # Less than 1920 x 1080
                            self.displays['suspicious_pixels_resolution'] = True
                            self.increase_score('displays', 'suspicious_pixels_resolution')

                # Increment score
                if not self.displays['built_in_display']:
                    self.increase_score('displays', 'built_in_display')
    
    def increase_score(self, category: str, field_name: str):
        if field_name in self.SEVERITY_LEVELS and category in self.final_scores.keys():
            severity_level = self.SEVERITY_LEVELS[field_name]
            self.final_scores[category] += self.SCORES[severity_level]
    
    def calculate_scores(self):
        return [
            {
                'label': "Audio devices",
                'result': f"Score: {self.final_scores['audio']} (Threshold: {self.SCORES['high']})",
                'vm_detected': self.final_scores['audio'] >= self.SCORES['high'],
                'status': 'success'
            },
            {
                'label': "Network connections",
                'result': f"Score: {self.final_scores['network']} (Threshold: {self.SCORES['high']})",
                'vm_detected': self.final_scores['network'] >= self.SCORES['high'],
                'status': 'success'
            },
            {
                'label': "Displays",
                'result': f"Score: {self.final_scores['displays']} (Threshold: {self.SCORES['high']})",
                'vm_detected': self.final_scores['displays'] >= self.SCORES['high'],
                'status': 'success'
            },
            {
                'label': "Misc",
                'result': f"Score: {self.final_scores['misc']} (Threshold: {self.SCORES['high']})",
                'vm_detected': self.final_scores['misc'] >= self.SCORES['high'],
                'status': 'success'
            },
            {
                'label': "Total",
                'result': f"Score: {sum(self.final_scores.values())} (Threshold: {self.TOTAL_THRESHOLD})",
                'vm_detected': sum(self.final_scores.values()) >= self.TOTAL_THRESHOLD,
                'status': 'success'
            }
        ]