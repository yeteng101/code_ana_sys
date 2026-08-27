#include "event_loop.h"

#define CALL_WATCHER(watcher, events) ((watcher)->callback(events))

namespace demo {

static int wait_for_events(EventLoop* loop, int timeout) {
    (void)loop;
    (void)timeout;
#ifdef USE_EPOLL
    return EVENT_READ;
#else
    return EVENT_READ | EVENT_WRITE;
#endif
}

static void dispatch_once(EventLoop* loop, Watcher* watcher, int events) {
    (void)loop;
    CALL_WATCHER(watcher, events);
}

static void run_ready_watchers(EventLoop* loop, int events) {
    for (int i = 0; i < loop->watcher_count; ++i) {
        Watcher* watcher = &loop->watchers[i];
        if ((watcher->events & events) != 0) {
            dispatch_once(loop, watcher, events);
        }
    }
}

void loop_init(EventLoop* loop) {
    loop->watcher_count = 0;
    loop->running = 0;
}

void loop_register(EventLoop* loop, int fd, EventHandler callback) {
    Watcher* watcher = &loop->watchers[loop->watcher_count];
    watcher->fd = fd;
    watcher->events = EVENT_READ | EVENT_WRITE;
    watcher->callback = callback;
    loop->watcher_count += 1;
}

void loop_run(EventLoop* loop) {
    loop->running = 1;
    while (loop->running) {
        int events = wait_for_events(loop, 100);
        run_ready_watchers(loop, events);
    }
}

void loop_stop(EventLoop* loop) {
    loop->running = 0;
}

}  // namespace demo
