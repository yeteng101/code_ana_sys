#include <fcntl.h>
#include <netdb.h>
#include <pthread.h>
#include <unistd.h>

static int open_and_close(const char *path, int flags) {
    int fd = open(path, flags);
    if (fd < 0) {
        return fd;
    }
    close(fd);
    return 0;
}

static void lock_and_wait(pthread_mutex_t *mutex, pthread_cond_t *cond) {
    pthread_mutex_lock(mutex);
    pthread_cond_wait(cond, mutex);
    pthread_mutex_unlock(mutex);
}

static void resolve_host(const char *host) {
    struct addrinfo *result = NULL;
    getaddrinfo(host, NULL, NULL, &result);
    freeaddrinfo(result);
}
