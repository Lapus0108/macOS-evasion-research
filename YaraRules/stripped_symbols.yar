import "macho"

rule StrippedSymbols {
    meta:
        description = "The sample has no defined symbols"
        reference_sample = "523977991071f837fe518906673c1966, 7f82eacd7735f87bd64bb3a8729d4caa"
        
        mitre_tactic = "TA0005" 
        mitre_technique_id = "T1027.008"
        mitre_technique_name = "Obfuscated Files or Information: Stripped Payloads"

    condition:
        macho.dysymtab.nextdefsym <= 1
}