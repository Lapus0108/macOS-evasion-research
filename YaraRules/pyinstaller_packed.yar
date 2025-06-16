import "macho"

rule PyInstallerPacked {
    meta:
        description = "The sample is packed using PyInstaller"
        reference_sample = "e47fd9c6f4f1720f76bcbb5d6aa57bf9, fc1959964b921186900058723c7c7306, 7640af49b8e097f177cfcc07ba041fa6"

        mitre_tactic = "TA0005"
        mitre_technique_id = "T1027.002"
        mitre_technique_name = "Obfuscated Files or Information: Software Packing"

    strings:
        $py1 = "PYINSTALLER_STRICT_UNPACK_MODE"
        $py2 = "PYINSTALLER_SUPPRESS_SPLASH_SCREEN"
        $py3 = "_PYI_APPLICATION_HOME_DIR"
        $py4 = "pyi-runtime-tmpdir"
        $py5 = "pyi-contents-directory"
        $py6 = "_MEIXXXXXX"
        $py7 = "_MEIPASS"
        
    condition:
        any of them
}