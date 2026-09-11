#include <stdlib.h>

int use_after_release(void) {
    char *buf = malloc(32);
    if (buf == NULL)
        return -1;
    free(buf);
    buf[0] = 'x';
    return 0;
}
