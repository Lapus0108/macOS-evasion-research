| Indicator name | Command | VM Configuration | Syscall hooking | PATH Hijacking |
|----------------|---------|------------------|------------------|-----------------|
| Hardware model | `sysctl -n hw.model` | <div align="center">✔️</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Hardware model | `sudo powermetrics \| grep "Machine model"` | <div align="center">✔️</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Hardware model | `system_profiler SPHardwareDataType \| grep "Model Name"` | <div align="center">✔️</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Model Identifier | `system_profiler SPHardwareDataType \| grep "Model Identifier"` | <div align="center">✔️</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Hardware model | `ioreg -c IOPlatformExpertDevice \| grep "\"model\" = " \| awk -F'"' '{print $4}'` | <div align="center">✔️</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Model Number | `system_profiler SPHardwareDataType \| grep "Model Number"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Serial Number | `system_profiler SPHardwareDataType \| grep "Serial Number"` | <div align="center">✔️</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Serial Number | `ioreg -rdl -c IOPlatformExpertDevice \| grep IOPlatformSerialNumber` | <div align="center">✔️</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Firmware Version | `system_profiler SPHardwareDataType \| grep "System Firmware Version"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Memory size | `sysctl -n hw.memsize` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Disk size | `df -h / \| awk 'NR==2 {print $2}'` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Disk size | `system_profiler SPStorageDataType \| grep "Capacity"` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Disk size | `diskutil info / \| grep "Disk Size:" \| awk -F ' ' '{print $3}'` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Disk size | `diskutil info / \| grep "Container Total Space:" \| awk -F ' ' '{print $4}'` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Disk size | `diskutil list physical \| grep "Apple_APFS " \| awk '{print $5, $6}'` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| CPU Brand | `sysctl -n machdep.cpu.brand_string` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Chip | `system_profiler SPHardwareDataType \| grep "Chip"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| USB Manufacturer | `system_profiler SPUSBDataType \| grep -i Manufacturer` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Vendor ID | `system_profiler SPUSBDataType \| grep -i "Vendor ID"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Operating system release | `uname -v` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| I/O Kit Registry | `ioreg -rdl -c IOPlatformExpertDevice \| grep manufacturer` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| I/O Kit Registry | `ioreg -rdl -c IOUSBHostDevice \| grep "USB Vendor Name"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| I/O Kit Registry | `ioreg -rdl -c IOUSBHostDevice \| grep "idVendor"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| System uptime | `uptime` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| System uptime | `system_profiler SPSoftwareDataType \| grep "Time since boot"` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| System boot time | `sudo powermetrics \| grep "Boot time"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| System boot time | `who -b \| awk '{print $3,$4,$5}'` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| System boot time | `date -r $(sysctl -n kern.boottime \| awk '{print $4}' \| sed 's/,//')` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| System boot time | `last reboot \| head -n 1 \| awk '{print $4,$5,$6}'` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| SIP Status | `csrutil status` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| SIP Status | `nvram csr-active-config` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">—</div> |
| SIP Status | `system_profiler SPSoftwareDataType \| grep "System Integrity Protection"` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| Virtualization Framework | `sysctl -n kern.hv_vmm_present` | <div align="center">—</div> | <div align="center">✔️</div> | <div align="center">✔️</div> |
| MAC Address | `ifconfig \| grep "ether"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| MAC Address | `system_profiler SPNetworkDataType \| grep "MAC Address"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| MAC Address | `ioreg -l \| grep "IOMACAddress"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| MAC Address | `networksetup -listallhardwareports \| grep "Ethernet Address:"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Wi-Fi networks | `system_profiler SPAirPortDataType` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Bluetooth devices | `system_profiler SPBluetoothDataType` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Audio devices | `system_profiler SPAudioDataType` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Storage devices | `system_profiler SPStorageDataType \| grep "Device Name"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Camera presence | `system_profiler SPCameraDataType` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Display resolution | `system_profiler SPDisplaysDataType \| grep "Resolution"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Number of displays | `system_profiler SPDisplaysDataType \| grep "Resolution:" \| wc -l` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Built-in display | `system_profiler SPDisplaysDataType \| grep "Display Type:"` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
| Keyboard / Mouse | `ioreg -r -c IOHIDDevice \| grep -i keyboard` | <div align="center">—</div> | <div align="center">—</div> | <div align="center">✔️</div> |
