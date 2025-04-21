import re
import json
import datetime
import subprocess


def get_command_output(command: list):
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        return {
            'output': result.stdout.strip(),
            'error': result.stderr
        }
    except Exception as e:
        return {
            'output': "",
            'error': str(e)
        }

def command_had_errors(result):
    return len(result['error']) > 0 and len(result['output']) == 0

def get_output_line(output :str, keyword: str):
    for line in output.split('\n'):
        if keyword.lower() in line.lower():
            return line.strip()
    
    return ""

def get_output_lines(output: str, keyword: str):
    lines = []
    for line in output.split('\n'):
        if keyword.lower() in line.lower():
            lines.append(line.strip())
    
    return lines

def remove_multiple_spaces(str: str):
    return re.sub(' +', ' ', str)

def remove_ioreg_formatting(str: str):
    return str.replace('"', '').replace('<', '').replace('>', '')

def calculate_date_diff_minutes(past_date):
    current_time = datetime.datetime.now()

    difference = current_time - past_date
    return int(difference.total_seconds() // 60)

def load_utilities_paths():
    with open("modules/paths.json", "r") as paths_list:
        json_content = json.load(paths_list)
        return json_content['paths']
    
# Calling System Utilities

def get_ioreg_info(class_name:str, full_path: bool):
    binary_path = load_utilities_paths()['ioreg'] if full_path else 'ioreg'
    command = [binary_path, "-rdl", "-c", class_name]
    command_str = ' '.join(command)
    return get_command_output(command), command_str

def get_system_profiler_info(data_type: str, full_path: bool):
    binary_path = load_utilities_paths()['system_profiler'] if full_path else 'system_profiler'
    command = [binary_path, data_type]
    command_str = ' '.join(command)
    return get_command_output(command), command_str

def get_system_profiler_info_json(data_type: str, full_path: bool):
    binary_path = load_utilities_paths()['system_profiler'] if full_path else 'system_profiler'
    command = [binary_path, data_type, "-json"]
    command_str = ' '.join(command)
    return get_command_output(command), command_str

def kill_process(process_name: str):
    try:
        subprocess.run(["pkill", process_name], check=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        pass