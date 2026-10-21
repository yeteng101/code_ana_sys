#include <stdlib.h>

static char *allocate_buffer(void) {
    char *buffer = malloc(32);
    return buffer;
}

static void consume_buffer(void) {
    char *owner = allocate_buffer();
    char *alias = owner;
    free(alias);
}
