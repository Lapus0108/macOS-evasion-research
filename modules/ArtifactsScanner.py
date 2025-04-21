import os
import psutil

class ArtifactsScanner:
    files = {
        "/Library/Extensions/VMwareGfx.kext": "VMWare",
        "/Library/LaunchDaemons/com.vmware.launchd.tools.plist": "VMWare",
        "/Library/LaunchAgents/com.vmware.launchd.vmware-tools-userd.plist": "VMWare",
        "/Library/LaunchDaemons/com.parallels.vm.prltoolsd.plist": "Parallels",
        "/Library/LaunchAgents/com.parallels.copypaste.plist": "Parallels"
    }

    directories = {
        "/Library/Application Support/VMware Tools": "VMWare",
        "/Library/Parallels Guest Tools": "Parallels"
    }

    processes = {
        "vmware-tools": "VMWare",
        "VMware Tools": "VMWare"
    }

    def __init__(self):
        self.artifacts_found = {
            'VMWare': [],
            'VirtualBox': [],
            'Parallels': [],
            'QEMU': []
        }

    def scan(self):
        self.check_files()
        self.check_directories()
        self.check_processes()

        return self.artifacts_found
    
    def check_files(self):
        for file_path, vme in self.files.items():
            if os.path.isfile(file_path):
                self.artifacts_found[vme].append({
                    'type': 'file',
                    'path': file_path,
                })
    
    def check_directories(self):
        for dir_path, vme in self.directories.items():
            if os.path.isdir(dir_path):
                self.artifacts_found[vme].append({
                    'type': 'directory',
                    'path': dir_path
                })

    def check_processes(self):
        for process in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(process.info['cmdline']) if process.info['cmdline'] else ''
                if len(cmdline) > 0:
                    for target_process, vme in self.processes.items():
                        if target_process.lower() in cmdline.lower():
                            self.artifacts_found[vme].append({
                                'type': 'process',
                                'cmdline': cmdline,
                                'pid': process.info['pid'],
                                'name': process.info['name']
                            })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False