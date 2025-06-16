import "macho"

rule StrippedSection {
    meta:
        description = "The sample has the section __gosymtab stripped"
        reference_sample = "40947b6bf78578a52e694b863678f4d9"
        
        mitre_tactic = "TA0005" 
        mitre_technique_id = "T1027.008"
        mitre_technique_name = "Obfuscated Files or Information: Stripped Payloads"
        
    condition:
        for any segment in macho.segments : (
			for any section in segment.sections : (
                section.sectname == "__gosymtab" and section.size == 0
            )
        ) 
}