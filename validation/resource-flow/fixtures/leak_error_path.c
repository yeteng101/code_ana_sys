#include <stdlib.h>

int parse_or_leak(int fail) {
    char *buf = malloc(256);
    if (buf == NULL)
        return -1;
    if (fail)
        return -1;
    free(buf);
    return 0;
}
