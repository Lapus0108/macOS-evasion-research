import "macho"

rule MPRESSPacked {
    meta:
        description = "The sample is packed with MPRESS or contains an embedded MPRESS-packed sample"
        reference_sample = "15639e92bca8d2c0a54728814eb11a95,1def1957a5c13691731fdc38e01749ab, 188e9b85a8c142f3844ae50a66c77ae0, 107b550359619b8b75fbcc5330893032"

        mitre_tactic = "TA0005"
        mitre_technique_id = "T1027.002"
        mitre_technique_name = "Obfuscated Files or Information: Software Packing"

    strings:
        $mp = /\b_+MPRESS_+v[^\s\x00]+/i
        
    condition:
        any of them or
            for any segment in macho.segments : (
                segment.segname icontains "_mpress_"
                    or for any section in segment.sections : (
                        section.sectname icontains "_mpress_"
                    )
            )
}