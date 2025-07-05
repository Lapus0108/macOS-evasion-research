rule EvasionCommands {
    meta:
        description = "The sample contains fingerprinting/discovery commands which can be used for evasion purposes"
        reference_sample = ""
        
        mitre_tactic = "TA0007" 
        mitre_technique_id = "T1497.001"
        mitre_technique_name = "Virtualization/Sandbox Evasion: System Checks"

    strings:
        $cmd1 = "ioreg" fullword nocase
        $cmd2 = "sysctl" fullword nocase
        $cmd3 = "sw_vers" fullword nocase
        $cmd4 = "system_profiler" fullword nocase
        $cmd5 = "diskutil list"
        $cmd6 = "diskutil info"
        $cmd7 = "csrutil status"

        $arg_sp_1 = "SPSoftwareDataType"
        $arg_sp_2 = "SPHardwareDataType"
        $arg_sp_2 = "SPMemoryDataType"
        $arg_sp_4 = "SPStorageDataType"
        $arg_sp_5 = "SPUSBDataType"
        $arg_sp_6 = "Vendor ID"
        $arg_sp_7 = "Model Identifier"
        $arg_sp_8 = "System Integrity Protection"

        $arg_sysctl_1 = "hw.model"
        $arg_sysctl_2 = "hw.memsize"
        $arg_sysctl_4 = "kern.hv_vmm_present"
        $arg_sysctl_5 = "machdep.cpu.brand_string"

        $arg_ioreg_1 = "IOHIDDevice"
        $arg_ioreg_3 = "IOUSBHostDevice"
        $arg_ioreg_4 = "IOPlatformExpertDevice"
        $arg_ioreg_5 = "IOPlatformSerialNumber"
        $arg_ioreg_6 = "USB Vendor Name"

    condition:
        any of them
}