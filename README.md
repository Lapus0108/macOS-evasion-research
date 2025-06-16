# macOS Malware Evasion: A Study on Anti-Fingerprinting Techniques and Sandbox Hardening Approaches

Welcome to the repository containing the tools developed during our research on evasion techniques employed by macOS malware. Our study focused both on methods used to detect virtualized or sandboxed environments, as well as anti-fingerprinting and hardening techniques designed to conceal virtualization and enable evasive malware to run.


## Repository Structure

### 🔍 HeimdallScanner/

Contains a Python-based system scanner designed to evaluate how vulnerable a macOS environment is to VM and sandbox detection techniques. It is a valuable tool for security researchers working on improving anti-evasion methods, as it evaluates the resilience of the system to evasive malware through several types of checks.

### 📄 Samples/

Contains multiple lists of hashes for samples belonging to prevalent macOS malware families that employ VM detection techniques. These MD5 hashes correspond to Mach-O binaries that are **publicly available on VirusTotal**, providing a foundation for ongoing research on this topic. The hashes are organized into separate files based on malware family or variant, along with a unified file that includes all listed samples.

During our research, this set of samples was used to evaluate the effectiveness of various proposed countermeasures against detection of virtual environments.

### 🛡 Techniques/

Provides several scripts that implement the anti-fingerprinting techniques presented in the paper associated with this repository. The proposed solutions are independent of any specific sandbox implementation and can strengthen analysis environments by tackling evasion attempts performed by macOS malware.

### 📂 YaraRules/

Stores a collection of YARA-X rules specifically crafted to detect stripped, packed, or obfuscated Mach-O binaries. These rules are designed to assist in identifying suspicious binaries that attempt to evade signature-based detection rules.

---

### 🚀 Feel free to explore the content of this repository and reach out with any questions