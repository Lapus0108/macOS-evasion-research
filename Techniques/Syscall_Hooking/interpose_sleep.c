#include <unistd.h>
#include <stdio.h>
#include <time.h>


unsigned int modified_sleep(unsigned int seconds) {
    unsigned int modified_sleep_time = 0; // Seconds

    // printf("Intercepted sleep: Requested %u seconds, modified to %u seconds.\n", seconds, modified_sleep_time);
    return usleep(modified_sleep_time * 1000000);
}

int modified_usleep(useconds_t usec) {
    useconds_t modified_sleep_time = 0; // Microseconds

    // printf("Intercepted usleep: Requested %u seconds, modified to %u seconds.\n", usec / 1000000, modified_sleep_time / 1000000);
    return usleep(modified_sleep_time);
}

int modified_nanosleep(const struct timespec *req, struct timespec *rem) {
    struct timespec modified_sleep_time = {
        .tv_sec = 0, // Seconds
        .tv_nsec = 0 // Nanoseconds
    };

    // printf("Intercepted nanosleep: Requested %ld seconds, modified to %ld seconds.\n", req->tv_sec, modified_sleep_time.tv_sec);
    return nanosleep(&modified_sleep_time, rem);
}

// sleep function
__attribute__((used)) static struct {
    const void *replacement;
    const void *replacee;
} _interpose_sleep __attribute__((section("__DATA,__interpose"))) = {
    (const void *)(unsigned long)&modified_sleep,
    (const void *)(unsigned long)&sleep
};

// usleep function
__attribute__((used)) static struct {
    const void *replacement;
    const void *replacee;
} _interpose_usleep __attribute__((section("__DATA,__interpose"))) = {
    (const void *)(unsigned long)&modified_usleep,
    (const void *)(unsigned long)&usleep
};

// nanosleep function
__attribute__((used)) static struct {
    const void *replacement;
    const void *replacee;
} _interpose_nanosleep __attribute__((section("__DATA,__interpose"))) = {
    (const void *)(unsigned long)&modified_nanosleep,
    (const void *)(unsigned long)&nanosleep
};