rule EvasionPeripherals {
    meta:
        description = "The sample checks for connected peripheral devices"
        reference_sample = ""
        
        mitre_tactic = "TA0007" 
        mitre_technique_id = "T1016.000"
        mitre_technique_name = "System Network Configuration Discovery"

    strings:
        $sp_cmd = "system_profiler" fullword
        $sp_arg1 = "SPAudioDataType"
        $sp_arg2 = "SPCameraDataType"
        $sp_arg3 = "SPStorageDataType"
        $sp_arg4 = "SPDisplaysDataType"
        $sp_arg5 = "SPBluetoothDataType"

        $ioreg_cmd = "ioreg" fullword
        $ioreg_arg1 = "IOHIDDevice"

    condition:
        (sp_cmd and any of ($sp_arg*)) 
            or ($ioreg_cmd and any of ($ioreg_arg*))
}