rule EvasionNetworkBased {
    meta:
        description = "The sample contains network-related commands which can be used for evasion purposes"
        reference_sample = ""
        
        mitre_tactic = "TA0007" 
        mitre_technique_id = "T1016.000"
        mitre_technique_name = "System Network Configuration Discovery"

    strings:
        $sp_cmd = "system_profiler" fullword
        $sp_arg1 = "SPNetworkDataType"
        $sp_arg2 = "SPAirPortDataType"

        $ioreg_cmd = "ioreg"
        $ioreg_arg = "IOMACAddress"
        
        $cmd1 = "networksetup"
        $cmd2 = "ifconfig"
        
        $arg1 = "MAC Address" nocase
        $arg2 = "Ethernet Address" nocase
        $arg3 = "-listallhardwareports"

        $py1 = "getnode()"

    condition:
        any of ($cmd*)
            or any of ("$arg*)
            or any of ("$py*)
            or all of ($ioreg*)
            or ($sp_cmd and any of ("$sp_arg*"))
           
}