import argparse
from ResultsDisplayer import ResultsDisplayer

from modules.SystemScanner import SystemScanner
from modules.ArtifactsScanner import ArtifactsScanner
from modules.PeripheralsScanner import PeripheralsScanner
from modules.UserActivityScanner import UserActivityScanner


class HeimdallScanner:
    def __init__(self):
        print("Initializing Heimdall Virtualization Scanner...\n")
        
        self.init_args()
        self.displayer = ResultsDisplayer()

        self.system_scanner = SystemScanner(self.args.full_paths)
        self.artifacts_scanner = ArtifactsScanner()
        self.peripherals_scanner = PeripheralsScanner(self.args.full_paths)
        self.activity_scanner = UserActivityScanner()
        
    def init_args(self):
        parser = argparse.ArgumentParser(description="Heimdall VM Scanner")
        parser.add_argument(
            '-v', 
            '--verbose', 
            action="store_true", 
            help="Display additional details about the checks that detected a virtual machine"
        )
        parser.add_argument(
            '-f', 
            '--full-paths', 
            action="store_true", 
            help="Run system utilities using their full path instead of only the name (ex: '/usr/sbin/system_profiler' instead of 'system_profiler')"
        )

        self.args = parser.parse_args()

    def run(self):
        system_results = self.system_scanner.scan()
        artifacts_results = self.artifacts_scanner.scan()
        activity_results = self.activity_scanner.scan()
        peripherals_results = self.peripherals_scanner.scan()

        scan_result = {
            'System checks': system_results,
            'VM Artifacts': artifacts_results,
            'Peripherals': peripherals_results,
            'User Activity': activity_results
        }

        self.displayer.show_results(scan_result, self.args.verbose)
        

if __name__ == "__main__":
    scanner = HeimdallScanner()
    scanner.run()
