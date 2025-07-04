import os
import re
import lief
import json
from termcolor import colored
from emulator import Emulator
from resources.patterns import patterns
from resources.common_go_packages import common_packages

class MachoParser:
    results_dir_path = "results"

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.load_file(file_path)
        self.default_output_file = os.path.join(self.results_dir_path, f"{self.file_name}_strings.txt")
        self.emulator = Emulator()

        if not os.path.isdir(self.results_dir_path):
            os.makedirs(self.results_dir_path)
            print(f"Created directory {self.results_dir_path}...")

    def load_file(self, file_path: str):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The provided file was not found: {file_path}")

        parsed_binary = lief.parse(file_path)
        if isinstance(parsed_binary, lief.MachO.Binary):
            self.binary = parsed_binary
            self.binary_arch = parsed_binary.header.cpu_type
            self.binary_size = os.path.getsize(self.file_path)

            print(f"Architecture: {colored(self.binary_arch.name, 'blue')}")
            print("File size: " + colored(f'{self.binary_size:,} bytes', 'blue'))

            if not self.is_go_binary():
                print(f"The file '{self.file_path}' is not a GO binary")
                return False

            return True
        else:
            print(f"The file '{file_path}' is NOT a Mach-O binary.")
            return False

    def parse_sections(self):
        for section in self.binary.sections:
            print(f"Segment: {section.segment_name} | Section: {section.name}")
            print(f"\tStart offset: {section.offset:,} ({hex(section.offset)})")
            print(f"\tSize: {section.size:,} ({hex(section.size)})")
    
    def get_sections(self):
        return [sect.name for sect in self.binary.sections]

    def is_go_binary(self):
        sections = self.get_sections()
        if '__gosymtab' in sections or '__gopclntab' in sections:
            return True

        return False

    def get_section_data(self, section_name: str):
        section_info = self.binary.get_section(section_name)
        section_data = None

        if isinstance(section_info, lief.MachO.Section):
            section_data = None
            with open(self.file_path, 'rb') as binary_file:
                binary_file.seek(section_info.offset)
                section_data = binary_file.read(section_info.size)
                
                section_percentage = round(section_info.size / self.binary_size * 100, 2)
                print(f"{section_name} section size: " + colored(f'{section_info.size:,} bytes ({section_percentage}%)', 'blue'))
        else:
            print(f"Unable to find section '{section_name}'")
        
        return section_data, section_info.offset

    def is_target_function(self, function_data: bytes, patterns: list):
        for pattern in patterns:
            if function_data.startswith(pattern['start']):
                function_end_match = re.search(pattern['end'], function_data)
                if function_end_match:
                    return {
                        'pattern_id': pattern['id'],
                        'end_offset': function_end_match.end()
                    }
        
        return None

    def find_target_functions(self):
        text_section_data, text_section_offset = self.get_section_data("__text")
        assert text_section_data is not None

        current_arch = self.binary_arch.name.lower()
        target_patterns = patterns[current_arch]

        symbols_list = [sym for sym in self.binary.symbols if sym.value != 0 and sym.type == 14]
        symbols_list.sort(key=lambda s: s.value)

        functions = []
        common_packages_funcs = 0

        for idx, symbol in enumerate(symbols_list):
            symbol_name = symbol.name[1:].replace("/", ".").replace("_", ".").replace(":", ".")
            package_name = symbol_name.split(".")[0]
            if package_name in common_packages:
                common_packages_funcs += 1
                continue

            try:
                absolute_start_offset = self.binary.virtual_address_to_offset(symbol.value)
            
                if idx == len(symbols_list) - 1:
                    next_start_offset = absolute_start_offset + 30000
                else:
                    next_start_offset = self.binary.virtual_address_to_offset(symbols_list[idx+1].value)

                text_start_offset = absolute_start_offset - text_section_offset
                text_end_offset = next_start_offset - text_section_offset
                search_area = text_section_data[text_start_offset:text_end_offset]

            except Exception as e:
                continue

            check_result = self.is_target_function(search_area, target_patterns)
            if check_result:
                relative_end_offset = check_result['end_offset']
                absolute_end_offset = absolute_start_offset + relative_end_offset
                functions.append({
                    'bytes': search_area[:relative_end_offset],
                    'start_offset': absolute_start_offset,
                    'end_offset': absolute_end_offset,
                    'size': relative_end_offset,
                    'name': symbol.name
                })

                #print(f"[{check_result['pattern_id']}] Function: {symbol.name} | Start offset: {absolute_start_offset:,} ({hex(absolute_start_offset)}) | End: {absolute_end_offset:,} ({hex(absolute_end_offset)}) | Size: {relative_end_offset:,} ({hex(relative_end_offset)})")

        print(f"Target functions found: {len(functions):,}")
        print(f"Excluded functions (from common packages): {common_packages_funcs:,}")

        return functions
    
    def decrypt_strings(self, output_file = None, debug=False):
        functions = self.find_target_functions()

        if not output_file:
            output_file = self.default_output_file

        empty_strings = 0

        successful = []
        empty = []
        exceptions = []

        with open(output_file, "w") as out_file:
            for fn in functions:
                try:
                    if self.binary_arch.name == 'X86_64':
                        decrypted_str = self.emulator.emulate_x86_64(fn['bytes'], fn['name'])
                    else:
                        decrypted_str = self.emulator.emulate_arm64(fn['bytes'], fn['name'])

                    if len(decrypted_str.strip()) > 0:
                        out_file.write(decrypted_str + '\n')
                        successful.append({
                            'fn_start': fn['start_offset'],
                            'fn_end': fn['end_offset'],
                            'name': fn['name']
                        })
                    else:
                        empty_strings += 1
                        empty.append({
                            'fn_start': fn['start_offset'],
                            'fn_end': fn['end_offset'],
                            'name': fn['name']
                        })
                except Exception as e:
                    print(str(e), fn['name'])
                    exceptions.append({
                        'fn_start': fn['start_offset'],
                        'fn_end': fn['end_offset'],
                        'name': fn['name']
                    })
                    pass

            print(f"Successful: {len(successful)}")
            print(f"Empty strings: {empty_strings}")
            print(f"Exceptions: {len(exceptions)}")


        if debug:
            with open(f'{os.path.join(self.results_dir_path, self.file_name)}_exceptions.json', 'w') as exceptions_file:
                json.dump(exceptions, exceptions_file, indent=4)

            with open(f'{os.path.join(self.results_dir_path, self.file_name)}_successful.json', 'w') as success_file:
                json.dump(successful, success_file, indent=4)
            
            with open(f'{os.path.join(self.results_dir_path, self.file_name)}_empty.json', 'w') as empty_file:
                json.dump(empty, empty_file, indent=4)
    