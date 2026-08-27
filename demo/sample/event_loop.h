#ifndef EVENT_LOOP_H
#define EVENT_LOOP_H

#define EVENT_READ 0x01
#define EVENT_WRITE 0x02
#define EVENT_ONCE 0x04

#ifdef USE_EPOLL
#define LOOP_BACKEND "epoll"
#else
#define LOOP_BACKEND "poll"
#endif

using EventHandler = void (*)(int);

struct Watcher {
    int fd;
    int events;
    EventHandler callback;
};

struct EventLoop {
    Watcher watchers[8];
    int watcher_count;
    int running;
};

void loop_init(EventLoop* loop);
void loop_register(EventLoop* loop, int fd, EventHandler callback);
void loop_run(EventLoop* loop);
void loop_stop(EventLoop* loop);

#endif
