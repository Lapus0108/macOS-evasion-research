#include <stdio.h>
#include <string.h>
#include <sys/param.h>
#include <sys/mount.h>
#include <stdint.h>

int custom_statfs(const char *path, struct statfs *buf) {
    extern int statfs(const char *, struct statfs *);
    int result = statfs(path, buf);
    
    if (result != 0 || buf == NULL) {
        return result;
    }
    
    // Configuration: 926Gi total, 10Gi used, 752Gi available
    if (buf != NULL && strcmp(buf->f_mntonname, "/") == 0) {
        // Get the filesystem block size (must use the actual block size)
        uint64_t block_size = buf->f_bsize;
        if (block_size == 0) {
            block_size = 4096;
        }
        
        uint64_t total_bytes = 926ULL * 1024ULL * 1024ULL * 1024ULL;
        uint64_t available_bytes = 752ULL * 1024ULL * 1024ULL * 1024ULL;
        uint64_t used_bytes = 10ULL * 1024ULL * 1024ULL * 1024ULL;
        
        // Calculate blocks based on filesystem block size
        uint64_t total_blocks = total_bytes / block_size;
        uint64_t available_blocks = available_bytes / block_size;
        uint64_t used_blocks = used_bytes / block_size;
        uint64_t free_blocks = total_blocks - used_blocks;
        
        if (available_blocks > free_blocks) {
            available_blocks = free_blocks;
        }
        
        if (total_blocks > 0 && free_blocks <= total_blocks && available_blocks <= free_blocks) {
            buf->f_blocks = total_blocks;
            buf->f_bfree = free_blocks;
            buf->f_bavail = available_blocks;
        }
    }
    
    return result;
}

__attribute__((used)) static struct {
    const void *replacement;
    const void *original;
} interposers[] __attribute__((section("__DATA,__interpose"))) = {
    { 
        (const void *)custom_statfs, 
        (const void *)statfs 
    }
};

