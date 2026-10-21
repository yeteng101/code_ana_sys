#include <poll.h>
#include <string.h>

#define ZERO_BUFFER(buffer, size) memset((buffer), 0, (size))

static void clear_buffer(char *buffer, unsigned long size) {
    ZERO_BUFFER(buffer, size);
}

#ifdef PLATFORM_TEST
static int wait_platform(struct pollfd *fds, int count) {
    return poll(fds, count, 10);
}
#endif
