rule EvasionTimeBased {
    meta:
        description = "The sample contains time-related commands which can be used for evasion purposes"
        reference_sample = ""
        
        mitre_tactic = "TA0005" 
        mitre_technique_id = "T1497.003"
        mitre_technique_name = "Virtualization/Sandbox Evasion: Time Based Evasion"

    strings:
        $cmd1 = "who -b"
        $arg1 = "reboot time" nocase

        $pwm_cmd = "powermetrics" fullword
        $pwm_arg = "Boot time"

        $sp_cmd = "system_profiler" fullword
        $sp_arg = "Time since boot" nocase

        $sysctl_cmd = "sysctl" fullword
        $sysctl_arg = "kern.boottime"

    condition:
        any of ($arg*) 
            or any of ($cmd*) 
            or all of ($pwm*) 
            or all of ($sp*) 
            or all of ($sysctl*)
           
}