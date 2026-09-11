#include <stdlib.h>

char *make_buffer(void) {
    char *buf = malloc(128);
    if (buf == NULL)
        return NULL;
    return buf;
}
