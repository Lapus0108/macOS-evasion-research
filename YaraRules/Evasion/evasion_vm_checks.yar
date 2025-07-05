import "vt"

rule EvasionVMChecks {
    meta:
        description = "The sample contains keywords related to virtualization software"
        reference_sample = "907f0377b2a5319296f54aaacf407bad, b93947890eebc7e558995e378bb58a5b"
        
        mitre_tactic = "TA0005" 
        mitre_technique_id = "T1497.001"
        mitre_technique_name = "Virtualization/Sandbox Evasion: System Checks"

    strings:
        $vm1 = "vmware" nocase
        $vm2 = "virtualbox" nocase
        $vm3 = "parallels" nocase

        $vm1_b64 = "vmware" base64
		$vm2_b64 = "VMware" base64
		$vm3_b64 = "parallels" base64
		$vm4_b64 = "Parallels" base64
		$vm5_b64 = "virtualbox" base64
		$vm6_b64 = "VirtualBox" base64

        $vm1_xor = "vmware" xor(0x01-0xff) ascii wide
        $vm2_xor = "virtualbox" xor(0x01-0xff) ascii wide
        $vm3_xor = "parallels" xor(0x01-0xff) ascii wide

        $mac_prefix1 = "00:1C:42" nocase
        $mac_prefix2 = "08:00:27" nocase
        $mac_prefix3 = "00:06:09" nocase
        $mac_prefix4 = "00:0C:29" nocase
        $mac_prefix5 = "00:1C:14" nocase
        $mac_prefix6 = "00:50:56" nocase
        $mac_prefix7 = "00:05:59" nocase
        $mac_prefix8 = "00:16:E3" nocase
        $mac_prefix9 = "00:05:69" nocase
    condition:
        vt.metadata.file_type == vt.FileType.MACH_O
            and vt.metadata.analysis_stats.malicious >= 7 
            and (any of ($vm*) or 2 of ($mac_prefix*)) 
}