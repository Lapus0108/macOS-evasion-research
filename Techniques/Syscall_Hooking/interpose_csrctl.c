#include <stdio.h>
#include <stdint.h>
#include "csr.h"

typedef uint32_t (*csr_get_active_config_t)(void);

uint32_t custom_csr_get_active_config(void) {
    return 0;
}

__attribute__((used)) static struct {
    const void *replacement;
    const void *original;
} interposers[] __attribute__((section("__DATA,__interpose"))) = {
    { 
        (const void *)custom_csr_get_active_config, 
        (const void *)csr_get_active_config 
    }
};