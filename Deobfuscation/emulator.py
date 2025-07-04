from unicorn import *
from unicorn.x86_const import *
from unicorn.arm64_const import *

from capstone import *
from capstone.x86 import *

class Emulator:
    memory_fails =[]

    STACK_BASE = 0x00100000
    STACK_SIZE = 0x00200000 # Size: 1 MB

    TARGET_BASE = 0x00400000
    TARGET_SIZE = 0x00200000 # Size: 1 MB

    DATA_BASE = 0x00700000
    DATA_SIZE = 0x00200000 # Size: 1 MB
    
    @staticmethod
    def align_address(address, alignment=0x1000):
        return (address // alignment) * alignment

    def initialize_memory(self, code, arch: str):
        if arch == "ARM64":
            uc = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
        else:
            uc = Uc(UC_ARCH_X86, UC_MODE_64)

        # Setup the stack zone
        uc.mem_map(self.STACK_BASE, self.STACK_SIZE)
        uc.mem_write(self.STACK_BASE, b"\x00" * self.STACK_SIZE)
        
        RSP = self.STACK_BASE + (self.STACK_SIZE // 2)
        uc.reg_write(UC_X86_REG_RSP, RSP)

        # Setup the code zone
        uc.mem_map(self.TARGET_BASE, self.TARGET_SIZE, UC_PROT_ALL)
        uc.mem_write(self.TARGET_BASE, b"\x00" * self.TARGET_SIZE)

        uc.mem_write(self.TARGET_BASE, code) 

        # Setup the data zone
        uc.mem_map(self.DATA_BASE, self.DATA_SIZE, UC_PROT_ALL)
        uc.mem_write(self.DATA_BASE, b"\x00" * self.DATA_SIZE)

        return uc

    def emulate_x86_64(self, code, function_name: str):
        # Memory initialization
        uc = self.initialize_memory(code, "X86_64")

        # Disassembler initialization
        cs = Cs(CS_ARCH_X86, CS_MODE_64)
        cs.detail = True

        # Hook function called before executing each instruction
        def trace_instruction(uc, address, size, user_data):
            insn = next(cs.disasm(uc.mem_read(address, size), address))
            if insn.mnemonic == 'call':
                uc.emu_stop()
        
        uc.reg_write(UC_X86_REG_R14, self.DATA_BASE)
        uc.hook_add(UC_HOOK_CODE, trace_instruction, None)
        uc.emu_start(
            begin=self.TARGET_BASE, 
            until=self.TARGET_BASE + len(code)
        )

        ptr_string = uc.reg_read(UC_X86_REG_RBX)
        size = uc.reg_read(UC_X86_REG_RCX)
        string_data = uc.mem_read(
            address=ptr_string, 
            size=size
        )

        decrypted_string = string_data.decode('utf-8')
        # if len(decrypted_string) > 0:
        #     print(f"Function: {function_name} -> Extracted string: \"{decrypted_string}\"")

        return decrypted_string
