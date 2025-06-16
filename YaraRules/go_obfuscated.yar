rule GO_Obfuscated {
    meta:
        description = "The sample is a GO-based binary obfuscated using Gobfuscate/Garble"
        reference_sample = "0d5cac778ec1f9a1471e0d78742d3fe9, a8b00268144f3c9c425f738aff3c7544, 0065314f735cd586a489827ea84ad1a7"

        mitre_tactic = "Defense Evasion"
        mitre_technique_id = "T1027.010"
        mitre_technique_name = "Obfuscated Files or Information: Command Obfuscation"
        
   	strings:
  		$obf1 = {0f b6 ?? ?? ?? 0f b6 ?? ?? ?? 31 d6 40 88 ?? ?? ?? 48 ff c1 48 83 f9 ?? 7c e6 48}
  		$obf2 = {0f b6 ?? ?? ?? 0f b6 ?? ?? ?? 31 ?? 88 ?? ?? ?? 48 ff c0 48 83 f8 ?? 7c e7 48 c7}
  		$obf3 = {64 68 60 38 05 04 00 91 63 68 65 38 85 00 03 CA A5 00 00 8B 9F ?? 00 F1 22 02 00 54}
      	$obf4 = {0f b6 ?? ?? ?? 0f b6 ?? ?? ?? 01 f2 88 54 04 ?? 48 ff c0 48 83 f8 ?? 7c e7 48}
      	$obf5 = {80 D2 08 00 00 14 E3 ?? ?? 91 64 68 60 38 E1 ?? 00 91 25 68 60 38 A4 00 04 CA 24 68 20 38 00 04 00 91 1F ?? 00 F1 0B FF FF 54}
   	
    condition:
      	any of them
}