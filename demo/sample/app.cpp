#include "event_loop.h"

namespace demo {

static void on_readable(int fd) {
    if (fd == 0) {
        // handle stdin readiness
    }
}

static void on_writable(int fd) {
    if (fd == 1) {
        // handle stdout writability
    }
}

static void on_once(int fd) {
    if (fd == 2) {
        // handle one-shot event
    }
}

void app_main() {
    EventLoop loop;
    loop_init(&loop);
    loop_register(&loop, 0, on_readable);
    loop_register(&loop, 1, on_writable);
    loop_register(&loop, 2, on_once);
    loop_run(&loop);
    loop_stop(&loop);
}

}  // namespace demo
