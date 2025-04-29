## 🔹 Usage
In order to hook certain system calls, such as `sysctl` (used to retrieve system properties), `sleep` (to combat time-based delays employed by malicious programs) or `csr_get_active_config` (to conceal that SIP is disabled), follow these steps:

1. Compile each C program as a dynamic library using the following command format:
```bash
gcc -dynamiclib interpose_<function>.c -o interpose_<function>.dylib
```

2. Include the obtained `.dylib` in the `DYLD_INSERT_LIBRARIES` environment variable before executing a (potentially malicious) sample. It can be either included for a single command or persistently set in a shell configuration file, such as `~/.zshrc`. For a persistent setup, add the following line to your shell configuration:
```bash
export DYLD_INSERT_LIBRARIES=/Users/vm/hooking/interpose_<function>.dylib
```