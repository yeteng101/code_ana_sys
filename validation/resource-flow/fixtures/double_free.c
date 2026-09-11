#include <stdlib.h>

void double_release(void) {
    char *buf = malloc(64);
    if (buf == NULL)
        return;
    free(buf);
    free(buf);
}
