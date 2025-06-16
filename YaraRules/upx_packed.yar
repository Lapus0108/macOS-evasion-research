import "macho"

rule UPXPacked {
    meta:
        description = "The sample is packed using UPX"
        reference_sample = "849476415291d6c22a64d8f71278fd07, 433478699c81d3d73d56664dd5adbdf2"

        mitre_tactic = "TA0005"
        mitre_technique_id = "T1027.002"
        mitre_technique_name = "Obfuscated Files or Information: Software Packing"

    strings:
        $upx1 = "UPX!" // UPX Header
        $upx2 = "This file is packed with the UPX executable packer" // UPX footer

    condition:
        all of ($upx*) or
            for any segment in macho.segments : (
                for any section in segment.sections : (
                    section.sectname == "upxTEXT"
                )
            )
}