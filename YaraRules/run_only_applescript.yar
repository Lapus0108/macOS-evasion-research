rule RunOnlyAppleScript {
    meta:
        description = "The sample is/contains a run-only AppleScript"
        reference_sample = "ac7729e1aa68ef9fcdbe9e906e36e9a9"
        
        mitre_tactic = "TA0005"
        mitre_technique_id = "T1027.008"
        mitre_technique_name = "Obfuscated Files or Information: Stripped Payloads"

    strings:
        $scpt_start = "FasdUAS "
        $scpt_end = {FA DE DE AD}
    
    condition:
        all of them
}