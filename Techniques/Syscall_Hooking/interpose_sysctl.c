#include <stdio.h>
#include <string.h>
#include <sys/sysctl.h>
#include <sys/time.h>
#include <stdint.h>
#include <time.h>

#ifndef CPU_BRAND_STRING
#define CPU_BRAND_STRING 107
#endif

#ifndef KERN_HV_VMM_PRESENT
#define KERN_HV_VMM_PRESENT 263
#endif


int custom_sysctl(int *name, u_int namelen, void *oldp, size_t *oldlenp, void *newp, size_t newlen) {
    // hw.memsize
    if (name[0] == CTL_HW && name[1] == HW_MEMSIZE && namelen == 2) {
        if (oldp && oldlenp && *oldlenp >= sizeof(uint64_t)) {
            uint64_t spoofed_memory_size = 17179869184ULL;  // 16 GB
            memcpy(oldp, &spoofed_memory_size, sizeof(uint64_t));
            *oldlenp = sizeof(uint64_t);
            return 0;
        }
    }

    // hw.model
    if (name[0] == CTL_HW && name[1] == HW_MODEL && namelen == 2) {
        const char *spoofed_model = "MacBookPro17,1";
        if (oldp && oldlenp) {
            size_t len = strlen(spoofed_model) + 1;
            if (*oldlenp >= len) {
                memcpy(oldp, spoofed_model, len);
                *oldlenp = len;
                return 0;
            }
        }
    }

    // machdep.cpu.brand_string
    if (name[0] == CTL_MACHDEP && name[1] == CPU_BRAND_STRING && namelen == 3) {
        const char *spoofed_cpu = "Apple M1";
        if (oldp && oldlenp) {
            size_t len = strlen(spoofed_cpu) + 1;
            if (*oldlenp >= len) {
                memcpy(oldp, spoofed_cpu, len);
                *oldlenp = len;
                return 0;
            }
        }
    }

    // kern.hv_vmm_present
    if (name[0] == CTL_KERN && name[1] == KERN_HV_VMM_PRESENT && namelen == 2) {
        if (oldp && oldlenp && *oldlenp >= sizeof(int)) {
            int new_value = 0;
            memcpy(oldp, &new_value, sizeof(int));
            *oldlenp = sizeof(int);
            return 0;
        }
    }

    // kern.boottime
    if (name[0] == CTL_KERN && name[1] == KERN_BOOTTIME && namelen == 2) {
        if (oldp && oldlenp && *oldlenp >= sizeof(struct timeval)) {
            struct timeval spoofed_boottime;
            time_t current_time = time(NULL);
            spoofed_boottime.tv_sec = current_time - (6.5 * 60 * 60);  // 6.5 hours ago
            spoofed_boottime.tv_usec = 0;
            memcpy(oldp, &spoofed_boottime, sizeof(struct timeval));
            *oldlenp = sizeof(struct timeval);
            return 0;
        }
    }

    extern int sysctl(int *, u_int, void *, size_t *, void *, size_t);
    return sysctl(name, namelen, oldp, oldlenp, newp, newlen);
}


__attribute__((used)) static struct {
    const void *replacement;
    const void *original;
} interposers[] __attribute__((section("__DATA,__interpose"))) = {
    { 
        (const void *)custom_sysctl, 
        (const void *)sysctl 
    }
};