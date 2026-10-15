# 代码逆向分析 Demo

- Run: `run_libuv_1.50.0`
- Build profile: `libuv-macos-clang`
- Analyzer: `clang++ -Xclang -ast-dump=json`
- Nodes: 894 / Edges: 2845
- Verification: 59%

## 模块架构

- **core**: 事件循环驱动、停止循环、核心逻辑
  - Files: ``
  - Symbols: `f、func、less_than、pCFArrayCreate、pCFBundleGetBundleWithIdentifier、pCFBundleGetDataPointerForName、pCFBundleGetFunctionPointerForName、pCFBundleGetInfoDictionary、pCFBundleGetMainBundle、pCFRelease、pCFRunLoopAddSource、pCFRunLoopGetCurrent、pCFRunLoopRemoveSource、pCFRunLoopRun、pCFRunLoopSourceCreate、pCFRunLoopSourceSignal、pCFRunLoopStop、pCFRunLoopWakeUp、pCFStringCreateWithCString、pCFStringCreateWithFileSystemRepresentation、pFSEventStreamCreate、pFSEventStreamInvalidate、pFSEventStreamRelease、pFSEventStreamScheduleWithRunLoop、pFSEventStreamStart、pFSEventStreamStop、pLSApplicationCheckIn、pLSGetCurrentApplicationASN、pLSSetApplicationInformationItem、pLSSetApplicationLaunchServicesServerConnectionStatus、uv__getentropy、uv__mkostemp、walk_cb`
- **external (系统与第三方调用)**: 事件等待、初始化、核心逻辑
  - Files: ``
  - Symbols: ``
- **include**: 事件等待、核心逻辑
  - Files: `third_party/libuv/include/uv.h`
  - Symbols: `uv_async_s::async_cb、uv_check_s::check_cb、uv_connect_s::cb、uv_fs_event_s::cb、uv_fs_s::cb、uv_getaddrinfo_s::cb、uv_getnameinfo_s::getnameinfo_cb、uv_handle_s::close_cb、uv_idle_s::idle_cb、uv_poll_s::poll_cb、uv_prepare_s::prepare_cb、uv_process_s::exit_cb、uv_random_s::cb、uv_shutdown_s::cb、uv_signal_s::signal_cb、uv_stream_s::alloc_cb、uv_stream_s::connection_cb、uv_stream_s::read_cb、uv_timer_s::timer_cb、uv_udp_s::alloc_cb、uv_udp_s::recv_cb、uv_udp_send_s::send_cb、uv_work_s::after_work_cb、uv_work_s::work_cb、uv_write_s::cb`
- **src**: 事件循环驱动、事件等待、停止循环、初始化、核心逻辑
  - Files: `third_party/libuv/src/fs-poll.c`, `third_party/libuv/src/heap-inl.h`, `third_party/libuv/src/idna.c`, `third_party/libuv/src/inet.c`, `third_party/libuv/src/queue.h`, `third_party/libuv/src/random.c`, `third_party/libuv/src/strscpy.c`, `third_party/libuv/src/strtok.c`, `third_party/libuv/src/thread-common.c`, `third_party/libuv/src/threadpool.c`, `third_party/libuv/src/timer.c`, `third_party/libuv/src/uv-common.c`
  - Symbols: `poll_ctx::poll_cb、uv__allocator_t::local_calloc、uv__allocator_t::local_free、uv__allocator_t::local_malloc、uv__allocator_t::local_realloc、heap_dequeue、heap_init、heap_insert、heap_min、heap_node_swap、heap_remove、inet_ntop4、inet_ntop6、inet_pton4、inet_pton6、init_once、init_threads、poll_cb、post、reset_once、slow_work_thread_threshold、statbuf_eq、timer_cb、timer_close_cb、timer_heap、uv__calloc、uv__cancelled、uv__count_bufs、uv__free、uv__fs_get_dirent_type、uv__fs_poll_close、uv__fs_readdir_cleanup、uv__fs_scandir_cleanup、uv__get_nbufs、uv__get_surrogate_value、uv__idna_toascii、uv__idna_toascii_label、uv__malloc、uv__metrics_set_provider_entry_time、uv__metrics_update_idle_time、uv__next_timeout、uv__print_handles、uv__queue_add、uv__queue_done、uv__queue_empty、uv__queue_head、uv__queue_init、uv__queue_insert_head、uv__queue_insert_tail、uv__queue_move、uv__queue_next、uv__queue_remove、uv__queue_split、uv__queue_work、uv__random、uv__random_done、uv__random_work、uv__realloc、uv__reallocf、uv__run_timers、uv__strdup、uv__strndup、uv__strscpy、uv__strtok、uv__threadpool_cleanup、uv__timer_close、uv__udp_check_before_send、uv__udp_is_connected、uv__unknown_err_code、uv__utf8_decode1、uv__utf8_decode1_slow、uv__work_cancel、uv__work_done、uv__work_submit、uv__wtf8_decode1、uv_barrier_destroy、uv_barrier_init、uv_barrier_wait、uv_buf_init、uv_cancel、uv_default_loop、uv_err_name、uv_err_name_r、uv_free_cpu_info、uv_fs_event_getpath、uv_fs_poll_getpath、uv_fs_poll_init、uv_fs_poll_start、uv_fs_poll_stop、uv_fs_scandir_next、uv_inet_ntop、uv_inet_pton、uv_ip4_addr、uv_ip4_name、uv_ip6_addr、uv_ip6_name、uv_ip_name、uv_library_shutdown、uv_loop_close、uv_loop_configure、uv_loop_delete、uv_loop_new、uv_metrics_idle_time、uv_metrics_info、uv_now、uv_os_free_environ、uv_os_free_group、uv_os_free_passwd、uv_print_active_handles、uv_print_all_handles、uv_queue_work、uv_random、uv_read_start、uv_recv_buffer_size、uv_send_buffer_size、uv_strerror、uv_strerror_r、uv_tcp_bind、uv_tcp_connect、uv_timer_again、uv_timer_init、uv_timer_start、uv_timer_stop、uv_udp_bind、uv_udp_connect、uv_udp_init、uv_udp_init_ex、uv_udp_recv_start、uv_udp_recv_stop、uv_udp_send、uv_udp_try_send、uv_udp_try_send2、uv_unref、uv_utf16_length_as_wtf8、uv_utf16_to_wtf8、uv_walk、uv_wtf8_length_as_utf16、uv_wtf8_to_utf16、worker`
- **unix**: 事件循环驱动、事件等待、停止循环、初始化、回调注册、核心逻辑
  - Files: `third_party/libuv/src/unix/async.c`, `third_party/libuv/src/unix/bsd-ifaddrs.c`, `third_party/libuv/src/unix/core.c`, `third_party/libuv/src/unix/darwin-proctitle.c`, `third_party/libuv/src/unix/darwin-syscalls.h`, `third_party/libuv/src/unix/darwin.c`, `third_party/libuv/src/unix/dl.c`, `third_party/libuv/src/unix/fs.c`, `third_party/libuv/src/unix/fsevents.c`, `third_party/libuv/src/unix/getaddrinfo.c`, `third_party/libuv/src/unix/getnameinfo.c`, `third_party/libuv/src/unix/internal.h`, `third_party/libuv/src/unix/kqueue.c`, `third_party/libuv/src/unix/loop-watcher.c`, `third_party/libuv/src/unix/loop.c`, `third_party/libuv/src/unix/pipe.c`, `third_party/libuv/src/unix/poll.c`, `third_party/libuv/src/unix/process.c`, `third_party/libuv/src/unix/proctitle.c`, `third_party/libuv/src/unix/random-devurandom.c`, `third_party/libuv/src/unix/random-getentropy.c`, `third_party/libuv/src/unix/signal.c`, `third_party/libuv/src/unix/stream.c`, `third_party/libuv/src/unix/tcp.c`, `third_party/libuv/src/unix/thread.c`, `third_party/libuv/src/unix/tty.c`, `third_party/libuv/src/unix/udp.c`
  - Symbols: `uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np、close$NOCANCEL、includes_nul、init_process_title_mutex_once、maybe_bind_socket、maybe_new_socket、maybe_resize、new_socket、next_power_of_two、recvmsg_x、sendmsg_x、uv___stream_fd、uv__accept、uv__async_close、uv__async_fork、uv__async_io、uv__async_send、uv__async_spin、uv__async_start、uv__async_stop、uv__backend_timeout、uv__basename_r、uv__cf_loop_cb、uv__cf_loop_runner、uv__cf_loop_signal、uv__check_before_write、uv__check_close、uv__cloexec、uv__close、uv__close_nocancel、uv__close_nocheckstdio、uv__cpu_relax、uv__default_stack_size、uv__dlerror、uv__drain、uv__dup2_cloexec、uv__emfile_trick、uv__fd_exists、uv__finish_close、uv__fs_buf_offset、uv__fs_close、uv__fs_closedir、uv__fs_copyfile、uv__fs_done、uv__fs_event、uv__fs_event_close、uv__fs_fdatasync、uv__fs_fstat、uv__fs_fsync、uv__fs_futime、uv__fs_lstat、uv__fs_lutime、uv__fs_mkdtemp、uv__fs_mkstemp、uv__fs_open、uv__fs_opendir、uv__fs_pathmax_size、uv__fs_post、uv__fs_read、uv__fs_readdir、uv__fs_readlink、uv__fs_realpath、uv__fs_scandir、uv__fs_scandir_filter、uv__fs_scandir_sort、uv__fs_sendfile、uv__fs_sendfile_emul、uv__fs_stat、uv__fs_statfs、uv__fs_statx、uv__fs_to_timeval、uv__fs_utime、uv__fs_work、uv__fs_write、uv__fs_write_all、uv__fsevents_cb、uv__fsevents_close、uv__fsevents_create_stream、uv__fsevents_destroy_stream、uv__fsevents_event_cb、uv__fsevents_global_init、uv__fsevents_init、uv__fsevents_loop_delete、uv__fsevents_loop_init、uv__fsevents_push_event、uv__fsevents_reschedule、uv__fstat、uv__getaddrinfo_done、uv__getaddrinfo_translate_error、uv__getaddrinfo_work、uv__getiovmax、uv__getnameinfo_done、uv__getnameinfo_work、uv__getpwuid_r、uv__getrusage、uv__getsockpeername、uv__handle_fd、uv__hrtime、uv__hrtime_init_once、uv__idle_close、uv__ifaddr_exclude、uv__io_active、uv__io_check_fd、uv__io_close、uv__io_feed、uv__io_fork、uv__io_init、uv__io_poll、uv__io_start、uv__io_stop、uv__ipv6_link_local_scope_id、uv__is_ipv6_link_local、uv__kqueue_delete、uv__kqueue_init、uv__kqueue_runtime_detection、uv__loop_alive、uv__loop_close、uv__loop_configure、uv__lstat、uv__make_close_pending、uv__make_pipe、uv__min_stack_size、uv__mkostemp_initonce、uv__nonblock_fcntl、uv__nonblock_ioctl、uv__open_cloexec、uv__open_file、uv__pipe_close、uv__pipe_getsockpeername、uv__pipe_listen、uv__platform_invalidate_fd、uv__platform_loop_delete、uv__platform_loop_init、uv__poll_close、uv__poll_io、uv__poll_stop、uv__preadv、uv__preadv_emul、uv__preadv_or_pwritev、uv__preadv_or_pwritev_emul、uv__prepare_close、uv__process_child_init、uv__process_close、uv__process_close_stream、uv__process_init、uv__process_init_stdio、uv__process_open_stream、uv__process_title_cleanup、uv__pwritev、uv__pwritev_emul、uv__random_devurandom、uv__random_devurandom_init、uv__random_getentropy、uv__random_getentropy_init、uv__random_readpath、uv__read、uv__read_start、uv__recvmsg、uv__run_check、uv__run_closing_handles、uv__run_idle、uv__run_pending、uv__run_prepare、uv__search_path、uv__server_io、uv__set_process_title、uv__set_recverr、uv__setsockopt、uv__setsockopt_maybe_char、uv__signal_block_and_lock、uv__signal_cleanup、uv__signal_close、uv__signal_compare、uv__signal_event、uv__signal_first_handle、uv__signal_global_init、uv__signal_global_once_init、uv__signal_global_reinit、uv__signal_handler、uv__signal_lock、uv__signal_loop_cleanup、uv__signal_loop_fork、uv__signal_loop_once_init、uv__signal_register_handler、uv__signal_start、uv__signal_stop、uv__signal_tree_s_RB_FIND、uv__signal_tree_s_RB_INSERT、uv__signal_tree_s_RB_INSERT_COLOR、uv__signal_tree_s_RB_NEXT、uv__signal_tree_s_RB_NFIND、uv__signal_tree_s_RB_REMOVE、uv__signal_tree_s_RB_REMOVE_COLOR、uv__signal_unlock、uv__signal_unlock_and_unblock、uv__signal_unregister_handler、uv__slurp、uv__sock_reuseaddr、uv__sock_reuseport、uv__socket、uv__socket_sockopt、uv__spawn_and_init_child、uv__spawn_and_init_child_fork、uv__spawn_and_init_child_posix_spawn、uv__spawn_find_path_in_env、uv__spawn_init_can_use_setsid、uv__spawn_init_posix_spawn、uv__spawn_init_posix_spawn_fncs、uv__spawn_resolve_and_spawn、uv__spawn_set_posix_spawn_attrs、uv__spawn_set_posix_spawn_file_actions、uv__stat、uv__stream_close、uv__stream_connect、uv__stream_destroy、uv__stream_eof、uv__stream_flush_write_queue、uv__stream_init、uv__stream_io、uv__stream_open、uv__stream_osx_cb_close、uv__stream_osx_interrupt_select、uv__stream_osx_select、uv__stream_osx_select_cb、uv__stream_queue_fd、uv__stream_recv_cmsg、uv__stream_try_select、uv__tcp_bind、uv__tcp_close、uv__tcp_connect、uv__tcp_keepalive、uv__tcp_listen、uv__tcp_nodelay、uv__tcsetattr、uv__thread_getname、uv__thread_setname、uv__thread_stack_size、uv__to_stat、uv__try_write、uv__tty_close、uv__tty_is_slave、uv__tty_make_raw、uv__udp_bind、uv__udp_close、uv__udp_connect、uv__udp_disconnect、uv__udp_finish_close、uv__udp_init_ex、uv__udp_io、uv__udp_maybe_deferred_bind、uv__udp_prep_pkt、uv__udp_recv_start、uv__udp_recv_stop、uv__udp_recvmmsg、uv__udp_recvmsg、uv__udp_run_completed、uv__udp_send、uv__udp_sendmsg、uv__udp_sendmsg1、uv__udp_sendmsgv、uv__udp_set_membership4、uv__udp_set_membership6、uv__udp_set_source_membership4、uv__udp_set_source_membership6、uv__udp_try_send、uv__udp_try_send2、uv__update_time、uv__wait_children、uv__write、uv__write_callbacks、uv__write_errno、uv__write_int、uv__write_req_finish、uv__write_req_size、uv__write_req_update、uv__writev、uv_accept、uv_async_init、uv_async_send、uv_available_parallelism、uv_backend_timeout、uv_chdir、uv_check_init、uv_check_start、uv_check_stop、uv_clock_gettime、uv_close、uv_cond_broadcast、uv_cond_destroy、uv_cond_init、uv_cond_signal、uv_cond_timedwait、uv_cond_wait、uv_cpu_info、uv_cwd、uv_disable_stdio_inheritance、uv_dlclose、uv_dlopen、uv_dlsym、uv_exepath、uv_fileno、uv_free_interface_addresses、uv_freeaddrinfo、uv_fs_access、uv_fs_chmod、uv_fs_chown、uv_fs_close、uv_fs_closedir、uv_fs_copyfile、uv_fs_event_init、uv_fs_event_start、uv_fs_event_stop、uv_fs_fchmod、uv_fs_fchown、uv_fs_fdatasync、uv_fs_fstat、uv_fs_fsync、uv_fs_ftruncate、uv_fs_futime、uv_fs_lchown、uv_fs_link、uv_fs_lstat、uv_fs_lutime、uv_fs_mkdir、uv_fs_mkdtemp、uv_fs_mkstemp、uv_fs_open、uv_fs_opendir、uv_fs_read、uv_fs_readdir、uv_fs_readlink、uv_fs_realpath、uv_fs_rename、uv_fs_req_cleanup、uv_fs_rmdir、uv_fs_scandir、uv_fs_sendfile、uv_fs_stat、uv_fs_statfs、uv_fs_symlink、uv_fs_unlink、uv_fs_utime、uv_fs_write、uv_get_available_memory、uv_get_free_memory、uv_get_process_title、uv_get_total_memory、uv_getaddrinfo、uv_getnameinfo、uv_getrusage、uv_getrusage_thread、uv_gettimeofday、uv_guess_handle、uv_hrtime、uv_idle_init、uv_idle_start、uv_idle_stop、uv_if_indextoiid、uv_if_indextoname、uv_interface_addresses、uv_is_active、uv_key_create、uv_key_delete、uv_key_get、uv_key_set、uv_kill、uv_listen、uv_loadavg、uv_loop_alive、uv_loop_fork、uv_loop_init、uv_mutex_destroy、uv_mutex_init、uv_mutex_init_recursive、uv_mutex_lock、uv_mutex_trylock、uv_mutex_unlock、uv_once、uv_os_environ、uv_os_get_group、uv_os_get_passwd、uv_os_get_passwd2、uv_os_getenv、uv_os_gethostname、uv_os_getpid、uv_os_getppid、uv_os_getpriority、uv_os_homedir、uv_os_setenv、uv_os_setpriority、uv_os_tmpdir、uv_os_uname、uv_os_unsetenv、uv_pipe、uv_pipe_bind、uv_pipe_bind2、uv_pipe_chmod、uv_pipe_connect、uv_pipe_connect2、uv_pipe_getpeername、uv_pipe_getsockname、uv_pipe_init、uv_pipe_open、uv_pipe_pending_type、uv_poll_init、uv_poll_init_socket、uv_poll_start、uv_poll_stop、uv_prepare_init、uv_prepare_start、uv_prepare_stop、uv_process_kill、uv_read_stop、uv_resident_set_memory、uv_run、uv_rwlock_destroy、uv_rwlock_init、uv_rwlock_rdlock、uv_rwlock_rdunlock、uv_rwlock_tryrdlock、uv_rwlock_trywrlock、uv_rwlock_wrlock、uv_rwlock_wrunlock、uv_sem_destroy、uv_sem_init、uv_sem_post、uv_sem_trywait、uv_sem_wait、uv_set_process_title、uv_setup_args、uv_shutdown、uv_signal_init、uv_signal_start、uv_signal_start_oneshot、uv_signal_stop、uv_sleep、uv_socketpair、uv_spawn、uv_stream_set_blocking、uv_tcp_close_reset、uv_tcp_getpeername、uv_tcp_getsockname、uv_tcp_init、uv_tcp_init_ex、uv_tcp_keepalive、uv_tcp_nodelay、uv_tcp_open、uv_thread_create、uv_thread_create_ex、uv_thread_detach、uv_thread_equal、uv_thread_getname、uv_thread_getpriority、uv_thread_join、uv_thread_self、uv_thread_setname、uv_thread_setpriority、uv_try_write、uv_try_write2、uv_tty_get_winsize、uv_tty_init、uv_tty_reset_mode、uv_tty_set_mode、uv_udp_getpeername、uv_udp_getsockname、uv_udp_open、uv_udp_set_broadcast、uv_udp_set_membership、uv_udp_set_multicast_interface、uv_udp_set_multicast_loop、uv_udp_set_multicast_ttl、uv_udp_set_source_membership、uv_udp_set_ttl、uv_udp_using_recvmmsg、uv_update_time、uv_uptime、uv_write、uv_write2`
- **uv**: 核心逻辑
  - Files: `third_party/libuv/include/uv/threadpool.h`, `third_party/libuv/include/uv/unix.h`
  - Symbols: `uv__io_s::cb、uv__work::done、uv__work::work`

Dependencies: `src -> core`, `src -> external`, `src -> include`, `src -> unix`, `src -> uv`, `unix -> core`, `unix -> external`, `unix -> include`, `unix -> src`, `unix -> uv`, `uv -> src`, `uv -> unix`

## 调用关系图

```mermaid
flowchart TD
  subgraph sg_core["core"]
    N1["f"]
    N2["func"]
    N3["less_than"]
    N4["pCFArrayCreate"]
    N5["pCFBundleGetBundleWithIdentifier"]
    N6["pCFBundleGetDataPointerForName"]
    N7["pCFBundleGetFunctionPointerForName"]
    N8["pCFBundleGetInfoDictionary"]
    N9["pCFBundleGetMainBundle"]
    N10["pCFRelease"]
    N11["pCFRunLoopAddSource"]
    N12["pCFRunLoopGetCurrent"]
    N13["pCFRunLoopRemoveSource"]
    N14["pCFRunLoopRun"]
    N15["pCFRunLoopSourceCreate"]
    N16["pCFRunLoopSourceSignal"]
    N17["pCFRunLoopStop"]
    N18["pCFRunLoopWakeUp"]
    N19["pCFStringCreateWithCString"]
    N20["pCFStringCreateWithFileSystemRepresentation"]
    N21["pFSEventStreamCreate"]
    N22["pFSEventStreamInvalidate"]
    N23["pFSEventStreamRelease"]
    N24["pFSEventStreamScheduleWithRunLoop"]
    N25["pFSEventStreamStart"]
    N26["pFSEventStreamStop"]
    N27["pLSApplicationCheckIn"]
    N28["pLSGetCurrentApplicationASN"]
    N29["pLSSetApplicationInformationItem"]
    N30["pLSSetApplicationLaunchServicesServerConnectionStatus"]
    N31["uv__getentropy"]
    N32["uv__mkostemp"]
    N33["walk_cb"]
  end
  subgraph sg_external["external (系统与第三方调用)"]
    N34["read"]
    N35["pwrite"]
    N36["pthread_setname_np"]
    N37["getpriority"]
    N38["nanosleep"]
    N39["__builtin_va_start"]
    N40["dlerror"]
    N41["pthread_cond_timedwait_relative_np"]
    N42["fchown"]
    N43["setuid"]
    N44["posix_spawn"]
    N45["setenv"]
    N46["pthread_mutexattr_settype"]
    N47["__builtin_constant_p"]
    N48["thread_info"]
    N49["kill"]
    N50["readlink"]
    N51["tcgetattr"]
    N52["symlink"]
    N53["__darwin_fd_isset"]
    N54["pthread_equal"]
    N55["realpath"]
    N56["fdopen"]
    N57["strrchr"]
    N58["pthread_getspecific"]
    N59["posix_spawnattr_init"]
    N60["posix_spawn_file_actions_addinherit_np"]
    N61["sysconf"]
    N62["fcntl"]
    N63["semaphore_timedwait"]
    N64["__builtin_expect"]
    N65["signal"]
    N66["pthread_key_delete"]
    N67["_NSGetExecutablePath"]
    N68["time"]
    N69["pthread_rwlock_trywrlock"]
    N70["unsetenv"]
    N71["pthread_mutex_unlock"]
    N72["atoi"]
    N73["pthread_attr_init"]
    N74["ioctl"]
    N75["pathconf"]
    N76["pthread_getname_np"]
    N77["lstat"]
    N78["pthread_key_create"]
    N79["pthread_getschedparam"]
    N80["clock_gettime"]
    N81["uname"]
    N82["pthread_rwlock_init"]
    N83["semaphore_destroy"]
    N84["getgrgid_r"]
    N85["pthread_mutex_destroy"]
    N86["gettimeofday"]
    N87["semaphore_wait"]
    N88["shutdown"]
    N89["sigprocmask"]
    N90["getaddrinfo"]
    N91["mkstemp"]
    N92["pthread_rwlock_unlock"]
    N93["getrlimit"]
    N94["semaphore_signal"]
    N95["fprintf"]
    N96["sysctl"]
    N97["strnlen"]
    N98["pthread_setschedparam"]
    N99["chown"]
    N100["_NSGetEnviron"]
    N101["sendmsg"]
    N102["getsockname"]
    N103["rmdir"]
    N104["posix_spawn_file_actions_addopen"]
    N105["getenv"]
    N106["pthread_mutexattr_init"]
    N107["mkdir"]
    N108["pthread_cond_destroy"]
    N109["__sigbits"]
    N110["rename"]
    N111["pthread_setspecific"]
    N112["geteuid"]
    N113["tcsetattr"]
    N114["_OSSwapInt16"]
    N115["__builtin___strncpy_chk"]
    N116["pthread_once"]
    N117["ftruncate"]
    N118["futimes"]
    N119["pthread_cond_init"]
    N120["__builtin___snprintf_chk"]
    N121["poll"]
    N122["posix_spawnattr_destroy"]
    N123["mach_continuous_time"]
    N124["strncmp"]
    N125["posix_spawnattr_setsigdefault"]
    N126["_exit"]
    N127["listen"]
    N128["dlclose"]
    N129["posix_spawn_file_actions_destroy"]
    N130["pthread_detach"]
    N131["readv"]
    N132["host_statistics"]
    N133["readdir"]
    N134["closedir"]
    N135["cfmakeraw"]
    N136["isatty"]
    N137["chdir"]
    N138["sigaction"]
    N139["__builtin___memset_chk"]
    N140["pthread_cond_signal"]
    N141["semaphore_create"]
    N142["write"]
    N143["strcmp"]
    N144["posix_spawn_file_actions_adddup2"]
    N145["sched_yield"]
    N146["kqueue"]
    N147["link"]
    N148["perror"]
    N149["if_nametoindex"]
    N150["pthread_mutex_trylock"]
    N151["strchr"]
    N152["vm_deallocate"]
    N153["getifaddrs"]
    N154["memcmp"]
    N155["select"]
    N156["lutimes"]
    N157["free"]
    N158["getpwuid_r"]
    N159["getpid"]
    N160["getpagesize"]
    N161["dlopen"]
    N162["mkdtemp"]
    N163["strlen"]
    N164["pthread_cond_wait"]
    N165["setsockopt"]
    N166["mach_port_deallocate"]
    N167["pthread_rwlock_destroy"]
    N168["pthread_rwlock_tryrdlock"]
    N169["fsync"]
    N170["__darwin_fd_set"]
    N171["recvmsg"]
    N172["setsid"]
    N173["sscanf_l"]
    N174["posix_spawn_file_actions_addclose"]
    N175["mach_thread_self"]
    N176["__assert_rtn"]
    N177["socket"]
    N178["__error"]
    N179["pthread_atfork"]
    N180["writev"]
    N181["posix_spawnattr_setflags"]
    N182["dup2"]
    N183["mach_host_self"]
    N184["access"]
    N185["fstat"]
    N186["scandir"]
    N187["setgid"]
    N188["sendfile"]
    N189["pthread_rwlock_rdlock"]
    N190["accept"]
    N191["opendir"]
    N192["utimes"]
    N193["futimens"]
    N194["bind"]
    N195["dlsym"]
    N196["socketpair"]
    N197["pthread_rwlock_wrlock"]
    N198["kevent"]
    N199["pthread_mutex_init"]
    N200["pthread_mutexattr_destroy"]
    N201["pthread_attr_destroy"]
    N202["__builtin___memmove_chk"]
    N203["memchr"]
    N204["getrusage"]
    N205["freeifaddrs"]
    N206["statfs"]
    N207["if_indextoname"]
    N208["pread"]
    N209["setpriority"]
    N210["getsockopt"]
    N211["pthread_create"]
    N212["fchmod"]
    N213["connect"]
    N214["__builtin___memcpy_chk"]
    N215["host_processor_info"]
    N216["stat"]
    N217["setgroups"]
    N218["sched_get_priority_min"]
    N219["fork"]
    N220["pthread_sigmask"]
    N221["pthread_mutex_lock"]
    N222["posix_spawn_file_actions_init"]
    N223["pthread_self"]
    N224["getppid"]
    N225["gethostname"]
    N226["chmod"]
    N227["freeaddrinfo"]
    N228["lchown"]
    N229["__builtin_va_end"]
    N230["pthread_cond_broadcast"]
    N231["_OSSwapInt32"]
    N232["execvp"]
    N233["__builtin_object_size"]
    N234["getnameinfo"]
    N235["mach_timebase_info"]
    N236["task_info"]
    N237["posix_spawnattr_setsigmask"]
    N238["pthread_join"]
    N239["abort"]
    N240["ttyname_r"]
    N241["__builtin___strcpy_chk"]
    N242["pipe"]
    N243["sched_get_priority_max"]
    N244["open"]
    N245["waitpid"]
    N246["pthread_attr_setstacksize"]
    N247["getcwd"]
    N248["sysctlbyname"]
    N249["unlink"]
  end
  subgraph sg_include["include"]
    N250["uv_async_s::async_cb"]
    N251["uv_check_s::check_cb"]
    N252["uv_connect_s::cb"]
    N253["uv_fs_event_s::cb"]
    N254["uv_fs_s::cb"]
    N255["uv_getaddrinfo_s::cb"]
    N256["uv_getnameinfo_s::getnameinfo_cb"]
    N257["uv_handle_s::close_cb"]
    N258["uv_idle_s::idle_cb"]
    N259["uv_poll_s::poll_cb"]
    N260["uv_prepare_s::prepare_cb"]
    N261["uv_process_s::exit_cb"]
    N262["uv_random_s::cb"]
    N263["uv_shutdown_s::cb"]
    N264["uv_signal_s::signal_cb"]
    N265["uv_stream_s::alloc_cb"]
    N266["uv_stream_s::connection_cb"]
    N267["uv_stream_s::read_cb"]
    N268["uv_timer_s::timer_cb"]
    N269["uv_udp_s::alloc_cb"]
    N270["uv_udp_s::recv_cb"]
    N271["uv_udp_send_s::send_cb"]
    N272["uv_work_s::after_work_cb"]
    N273["uv_work_s::work_cb"]
    N274["uv_write_s::cb"]
  end
  subgraph sg_src["src"]
    N275["poll_ctx::poll_cb"]
    N276["uv__allocator_t::local_calloc"]
    N277["uv__allocator_t::local_free"]
    N278["uv__allocator_t::local_malloc"]
    N279["uv__allocator_t::local_realloc"]
    N280["heap_dequeue"]
    N281["heap_init"]
    N282["heap_insert"]
    N283["heap_min"]
    N284["heap_node_swap"]
    N285["heap_remove"]
    N286["inet_ntop4"]
    N287["inet_ntop6"]
    N288["inet_pton4"]
    N289["inet_pton6"]
    N290["init_once"]
    N291["init_threads"]
    N292["poll_cb"]
    N293["post"]
    N294["reset_once"]
    N295["slow_work_thread_threshold"]
    N296["statbuf_eq"]
    N297["timer_cb"]
    N298["timer_close_cb"]
    N299["timer_heap"]
    N300["uv__calloc"]
    N301["uv__cancelled"]
    N302["uv__count_bufs"]
    N303["uv__free"]
    N304["uv__fs_get_dirent_type"]
    N305["uv__fs_poll_close"]
    N306["uv__fs_readdir_cleanup"]
    N307["uv__fs_scandir_cleanup"]
    N308["uv__get_nbufs"]
    N309["uv__get_surrogate_value"]
    N310["uv__idna_toascii"]
    N311["uv__idna_toascii_label"]
    N312["uv__malloc"]
    N313["uv__metrics_set_provider_entry_time"]
    N314["uv__metrics_update_idle_time"]
    N315["uv__next_timeout"]
    N316["uv__print_handles"]
    N317["uv__queue_add"]
    N318["uv__queue_done"]
    N319["uv__queue_empty"]
    N320["uv__queue_head"]
    N321["uv__queue_init"]
    N322["uv__queue_insert_head"]
    N323["uv__queue_insert_tail"]
    N324["uv__queue_move"]
    N325["uv__queue_next"]
    N326["uv__queue_remove"]
    N327["uv__queue_split"]
    N328["uv__queue_work"]
    N329["uv__random"]
    N330["uv__random_done"]
    N331["uv__random_work"]
    N332["uv__realloc"]
    N333["uv__reallocf"]
    N334["uv__run_timers"]
    N335["uv__strdup"]
    N336["uv__strndup"]
    N337["uv__strscpy"]
    N338["uv__strtok"]
    N339["uv__threadpool_cleanup"]
    N340["uv__timer_close"]
    N341["uv__udp_check_before_send"]
    N342["uv__udp_is_connected"]
    N343["uv__unknown_err_code"]
    N344["uv__utf8_decode1"]
    N345["uv__utf8_decode1_slow"]
    N346["uv__work_cancel"]
    N347["uv__work_done"]
    N348["uv__work_submit"]
    N349["uv__wtf8_decode1"]
    N350["uv_barrier_destroy"]
    N351["uv_barrier_init"]
    N352["uv_barrier_wait"]
    N353["uv_buf_init"]
    N354["uv_cancel"]
    N355["uv_default_loop"]
    N356["uv_err_name"]
    N357["uv_err_name_r"]
    N358["uv_free_cpu_info"]
    N359["uv_fs_event_getpath"]
    N360["uv_fs_poll_getpath"]
    N361["uv_fs_poll_init"]
    N362["uv_fs_poll_start"]
    N363["uv_fs_poll_stop"]
    N364["uv_fs_scandir_next"]
    N365["uv_inet_ntop"]
    N366["uv_inet_pton"]
    N367["uv_ip4_addr"]
    N368["uv_ip4_name"]
    N369["uv_ip6_addr"]
    N370["uv_ip6_name"]
    N371["uv_ip_name"]
    N372["uv_library_shutdown"]
    N373["uv_loop_close"]
    N374["uv_loop_configure"]
    N375["uv_loop_delete"]
    N376["uv_loop_new"]
    N377["uv_metrics_idle_time"]
    N378["uv_metrics_info"]
    N379["uv_now"]
    N380["uv_os_free_environ"]
    N381["uv_os_free_group"]
    N382["uv_os_free_passwd"]
    N383["uv_print_active_handles"]
    N384["uv_print_all_handles"]
    N385["uv_queue_work"]
    N386["uv_random"]
    N387["uv_read_start"]
    N388["uv_recv_buffer_size"]
    N389["uv_send_buffer_size"]
    N390["uv_strerror"]
    N391["uv_strerror_r"]
    N392["uv_tcp_bind"]
    N393["uv_tcp_connect"]
    N394["uv_timer_again"]
    N395["uv_timer_init"]
    N396["uv_timer_start"]
    N397["uv_timer_stop"]
    N398["uv_udp_bind"]
    N399["uv_udp_connect"]
    N400["uv_udp_init"]
    N401["uv_udp_init_ex"]
    N402["uv_udp_recv_start"]
    N403["uv_udp_recv_stop"]
    N404["uv_udp_send"]
    N405["uv_udp_try_send"]
    N406["uv_udp_try_send2"]
    N407["uv_unref"]
    N408["uv_utf16_length_as_wtf8"]
    N409["uv_utf16_to_wtf8"]
    N410["uv_walk"]
    N411["uv_wtf8_length_as_utf16"]
    N412["uv_wtf8_to_utf16"]
    N413["worker"]
  end
  subgraph sg_unix["unix"]
    N414["uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np"]
    N415["close$NOCANCEL"]
    N416["includes_nul"]
    N417["init_process_title_mutex_once"]
    N418["maybe_bind_socket"]
    N419["maybe_new_socket"]
    N420["maybe_resize"]
    N421["new_socket"]
    N422["next_power_of_two"]
    N423["recvmsg_x"]
    N424["sendmsg_x"]
    N425["uv___stream_fd"]
    N426["uv__accept"]
    N427["uv__async_close"]
    N428["uv__async_fork"]
    N429["uv__async_io"]
    N430["uv__async_send"]
    N431["uv__async_spin"]
    N432["uv__async_start"]
    N433["uv__async_stop"]
    N434["uv__backend_timeout"]
    N435["uv__basename_r"]
    N436["uv__cf_loop_cb"]
    N437["uv__cf_loop_runner"]
    N438["uv__cf_loop_signal"]
    N439["uv__check_before_write"]
    N440["uv__check_close"]
    N441["uv__cloexec"]
    N442["uv__close"]
    N443["uv__close_nocancel"]
    N444["uv__close_nocheckstdio"]
    N445["uv__cpu_relax"]
    N446["uv__default_stack_size"]
    N447["uv__dlerror"]
    N448["uv__drain"]
    N449["uv__dup2_cloexec"]
    N450["uv__emfile_trick"]
    N451["uv__fd_exists"]
    N452["uv__finish_close"]
    N453["uv__fs_buf_offset"]
    N454["uv__fs_close"]
    N455["uv__fs_closedir"]
    N456["uv__fs_copyfile"]
    N457["uv__fs_done"]
    N458["uv__fs_event"]
    N459["uv__fs_event_close"]
    N460["uv__fs_fdatasync"]
    N461["uv__fs_fstat"]
    N462["uv__fs_fsync"]
    N463["uv__fs_futime"]
    N464["uv__fs_lstat"]
    N465["uv__fs_lutime"]
    N466["uv__fs_mkdtemp"]
    N467["uv__fs_mkstemp"]
    N468["uv__fs_open"]
    N469["uv__fs_opendir"]
    N470["uv__fs_pathmax_size"]
    N471["uv__fs_post"]
    N472["uv__fs_read"]
    N473["uv__fs_readdir"]
    N474["uv__fs_readlink"]
    N475["uv__fs_realpath"]
    N476["uv__fs_scandir"]
    N477["uv__fs_scandir_filter"]
    N478["uv__fs_scandir_sort"]
    N479["uv__fs_sendfile"]
    N480["uv__fs_sendfile_emul"]
    N481["uv__fs_stat"]
    N482["uv__fs_statfs"]
    N483["uv__fs_statx"]
    N484["uv__fs_to_timeval"]
    N485["uv__fs_utime"]
    N486["uv__fs_work"]
    N487["uv__fs_write"]
    N488["uv__fs_write_all"]
    N489["uv__fsevents_cb"]
    N490["uv__fsevents_close"]
    N491["uv__fsevents_create_stream"]
    N492["uv__fsevents_destroy_stream"]
    N493["uv__fsevents_event_cb"]
    N494["uv__fsevents_global_init"]
    N495["uv__fsevents_init"]
    N496["uv__fsevents_loop_delete"]
    N497["uv__fsevents_loop_init"]
    N498["uv__fsevents_push_event"]
    N499["uv__fsevents_reschedule"]
    N500["uv__fstat"]
    N501["uv__getaddrinfo_done"]
    N502["uv__getaddrinfo_translate_error"]
    N503["uv__getaddrinfo_work"]
    N504["uv__getiovmax"]
    N505["uv__getnameinfo_done"]
    N506["uv__getnameinfo_work"]
    N507["uv__getpwuid_r"]
    N508["uv__getrusage"]
    N509["uv__getsockpeername"]
    N510["uv__handle_fd"]
    N511["uv__hrtime"]
    N512["uv__hrtime_init_once"]
    N513["uv__idle_close"]
    N514["uv__ifaddr_exclude"]
    N515["uv__io_active"]
    N516["uv__io_check_fd"]
    N517["uv__io_close"]
    N518["uv__io_feed"]
    N519["uv__io_fork"]
    N520["uv__io_init"]
    N521["uv__io_poll"]
    N522["uv__io_start"]
    N523["uv__io_stop"]
    N524["uv__ipv6_link_local_scope_id"]
    N525["uv__is_ipv6_link_local"]
    N526["uv__kqueue_delete"]
    N527["uv__kqueue_init"]
    N528["uv__kqueue_runtime_detection"]
    N529["uv__loop_alive"]
    N530["uv__loop_close"]
    N531["uv__loop_configure"]
    N532["uv__lstat"]
    N533["uv__make_close_pending"]
    N534["uv__make_pipe"]
    N535["uv__min_stack_size"]
    N536["uv__mkostemp_initonce"]
    N537["uv__nonblock_fcntl"]
    N538["uv__nonblock_ioctl"]
    N539["uv__open_cloexec"]
    N540["uv__open_file"]
    N541["uv__pipe_close"]
    N542["uv__pipe_getsockpeername"]
    N543["uv__pipe_listen"]
    N544["uv__platform_invalidate_fd"]
    N545["uv__platform_loop_delete"]
    N546["uv__platform_loop_init"]
    N547["uv__poll_close"]
    N548["uv__poll_io"]
    N549["uv__poll_stop"]
    N550["uv__preadv"]
    N551["uv__preadv_emul"]
    N552["uv__preadv_or_pwritev"]
    N553["uv__preadv_or_pwritev_emul"]
    N554["uv__prepare_close"]
    N555["uv__process_child_init"]
    N556["uv__process_close"]
    N557["uv__process_close_stream"]
    N558["uv__process_init"]
    N559["uv__process_init_stdio"]
    N560["uv__process_open_stream"]
    N561["uv__process_title_cleanup"]
    N562["uv__pwritev"]
    N563["uv__pwritev_emul"]
    N564["uv__random_devurandom"]
    N565["uv__random_devurandom_init"]
    N566["uv__random_getentropy"]
    N567["uv__random_getentropy_init"]
    N568["uv__random_readpath"]
    N569["uv__read"]
    N570["uv__read_start"]
    N571["uv__recvmsg"]
    N572["uv__run_check"]
    N573["uv__run_closing_handles"]
    N574["uv__run_idle"]
    N575["uv__run_pending"]
    N576["uv__run_prepare"]
    N577["uv__search_path"]
    N578["uv__server_io"]
    N579["uv__set_process_title"]
    N580["uv__set_recverr"]
    N581["uv__setsockopt"]
    N582["uv__setsockopt_maybe_char"]
    N583["uv__signal_block_and_lock"]
    N584["uv__signal_cleanup"]
    N585["uv__signal_close"]
    N586["uv__signal_compare"]
    N587["uv__signal_event"]
    N588["uv__signal_first_handle"]
    N589["uv__signal_global_init"]
    N590["uv__signal_global_once_init"]
    N591["uv__signal_global_reinit"]
    N592["uv__signal_handler"]
    N593["uv__signal_lock"]
    N594["uv__signal_loop_cleanup"]
    N595["uv__signal_loop_fork"]
    N596["uv__signal_loop_once_init"]
    N597["uv__signal_register_handler"]
    N598["uv__signal_start"]
    N599["uv__signal_stop"]
    N600["uv__signal_tree_s_RB_FIND"]
    N601["uv__signal_tree_s_RB_INSERT"]
    N602["uv__signal_tree_s_RB_INSERT_COLOR"]
    N603["uv__signal_tree_s_RB_NEXT"]
    N604["uv__signal_tree_s_RB_NFIND"]
    N605["uv__signal_tree_s_RB_REMOVE"]
    N606["uv__signal_tree_s_RB_REMOVE_COLOR"]
    N607["uv__signal_unlock"]
    N608["uv__signal_unlock_and_unblock"]
    N609["uv__signal_unregister_handler"]
    N610["uv__slurp"]
    N611["uv__sock_reuseaddr"]
    N612["uv__sock_reuseport"]
    N613["uv__socket"]
    N614["uv__socket_sockopt"]
    N615["uv__spawn_and_init_child"]
    N616["uv__spawn_and_init_child_fork"]
    N617["uv__spawn_and_init_child_posix_spawn"]
    N618["uv__spawn_find_path_in_env"]
    N619["uv__spawn_init_can_use_setsid"]
    N620["uv__spawn_init_posix_spawn"]
    N621["uv__spawn_init_posix_spawn_fncs"]
    N622["uv__spawn_resolve_and_spawn"]
    N623["uv__spawn_set_posix_spawn_attrs"]
    N624["uv__spawn_set_posix_spawn_file_actions"]
    N625["uv__stat"]
    N626["uv__stream_close"]
    N627["uv__stream_connect"]
    N628["uv__stream_destroy"]
    N629["uv__stream_eof"]
    N630["uv__stream_flush_write_queue"]
    N631["uv__stream_init"]
    N632["uv__stream_io"]
    N633["uv__stream_open"]
    N634["uv__stream_osx_cb_close"]
    N635["uv__stream_osx_interrupt_select"]
    N636["uv__stream_osx_select"]
    N637["uv__stream_osx_select_cb"]
    N638["uv__stream_queue_fd"]
    N639["uv__stream_recv_cmsg"]
    N640["uv__stream_try_select"]
    N641["uv__tcp_bind"]
    N642["uv__tcp_close"]
    N643["uv__tcp_connect"]
    N644["uv__tcp_keepalive"]
    N645["uv__tcp_listen"]
    N646["uv__tcp_nodelay"]
    N647["uv__tcsetattr"]
    N648["uv__thread_getname"]
    N649["uv__thread_setname"]
    N650["uv__thread_stack_size"]
    N651["uv__to_stat"]
    N652["uv__try_write"]
    N653["uv__tty_close"]
    N654["uv__tty_is_slave"]
    N655["uv__tty_make_raw"]
    N656["uv__udp_bind"]
    N657["uv__udp_close"]
    N658["uv__udp_connect"]
    N659["uv__udp_disconnect"]
    N660["uv__udp_finish_close"]
    N661["uv__udp_init_ex"]
    N662["uv__udp_io"]
    N663["uv__udp_maybe_deferred_bind"]
    N664["uv__udp_prep_pkt"]
    N665["uv__udp_recv_start"]
    N666["uv__udp_recv_stop"]
    N667["uv__udp_recvmmsg"]
    N668["uv__udp_recvmsg"]
    N669["uv__udp_run_completed"]
    N670["uv__udp_send"]
    N671["uv__udp_sendmsg"]
    N672["uv__udp_sendmsg1"]
    N673["uv__udp_sendmsgv"]
    N674["uv__udp_set_membership4"]
    N675["uv__udp_set_membership6"]
    N676["uv__udp_set_source_membership4"]
    N677["uv__udp_set_source_membership6"]
    N678["uv__udp_try_send"]
    N679["uv__udp_try_send2"]
    N680["uv__update_time"]
    N681["uv__wait_children"]
    N682["uv__write"]
    N683["uv__write_callbacks"]
    N684["uv__write_errno"]
    N685["uv__write_int"]
    N686["uv__write_req_finish"]
    N687["uv__write_req_size"]
    N688["uv__write_req_update"]
    N689["uv__writev"]
    N690["uv_accept"]
    N691["uv_async_init"]
    N692["uv_async_send"]
    N693["uv_available_parallelism"]
    N694["uv_backend_timeout"]
    N695["uv_chdir"]
    N696["uv_check_init"]
    N697["uv_check_start"]
    N698["uv_check_stop"]
    N699["uv_clock_gettime"]
    N700["uv_close"]
    N701["uv_cond_broadcast"]
    N702["uv_cond_destroy"]
    N703["uv_cond_init"]
    N704["uv_cond_signal"]
    N705["uv_cond_timedwait"]
    N706["uv_cond_wait"]
    N707["uv_cpu_info"]
    N708["uv_cwd"]
    N709["uv_disable_stdio_inheritance"]
    N710["uv_dlclose"]
    N711["uv_dlopen"]
    N712["uv_dlsym"]
    N713["uv_exepath"]
    N714["uv_fileno"]
    N715["uv_free_interface_addresses"]
    N716["uv_freeaddrinfo"]
    N717["uv_fs_access"]
    N718["uv_fs_chmod"]
    N719["uv_fs_chown"]
    N720["uv_fs_close"]
    N721["uv_fs_closedir"]
    N722["uv_fs_copyfile"]
    N723["uv_fs_event_init"]
    N724["uv_fs_event_start"]
    N725["uv_fs_event_stop"]
    N726["uv_fs_fchmod"]
    N727["uv_fs_fchown"]
    N728["uv_fs_fdatasync"]
    N729["uv_fs_fstat"]
    N730["uv_fs_fsync"]
    N731["uv_fs_ftruncate"]
    N732["uv_fs_futime"]
    N733["uv_fs_lchown"]
    N734["uv_fs_link"]
    N735["uv_fs_lstat"]
    N736["uv_fs_lutime"]
    N737["uv_fs_mkdir"]
    N738["uv_fs_mkdtemp"]
    N739["uv_fs_mkstemp"]
    N740["uv_fs_open"]
    N741["uv_fs_opendir"]
    N742["uv_fs_read"]
    N743["uv_fs_readdir"]
    N744["uv_fs_readlink"]
    N745["uv_fs_realpath"]
    N746["uv_fs_rename"]
    N747["uv_fs_req_cleanup"]
    N748["uv_fs_rmdir"]
    N749["uv_fs_scandir"]
    N750["uv_fs_sendfile"]
    N751["uv_fs_stat"]
    N752["uv_fs_statfs"]
    N753["uv_fs_symlink"]
    N754["uv_fs_unlink"]
    N755["uv_fs_utime"]
    N756["uv_fs_write"]
    N757["uv_get_available_memory"]
    N758["uv_get_free_memory"]
    N759["uv_get_process_title"]
    N760["uv_get_total_memory"]
    N761["uv_getaddrinfo"]
    N762["uv_getnameinfo"]
    N763["uv_getrusage"]
    N764["uv_getrusage_thread"]
    N765["uv_gettimeofday"]
    N766["uv_guess_handle"]
    N767["uv_hrtime"]
    N768["uv_idle_init"]
    N769["uv_idle_start"]
    N770["uv_idle_stop"]
    N771["uv_if_indextoiid"]
    N772["uv_if_indextoname"]
    N773["uv_interface_addresses"]
    N774["uv_is_active"]
    N775["uv_key_create"]
    N776["uv_key_delete"]
    N777["uv_key_get"]
    N778["uv_key_set"]
    N779["uv_kill"]
    N780["uv_listen"]
    N781["uv_loadavg"]
    N782["uv_loop_alive"]
    N783["uv_loop_fork"]
    N784["uv_loop_init"]
    N785["uv_mutex_destroy"]
    N786["uv_mutex_init"]
    N787["uv_mutex_init_recursive"]
    N788["uv_mutex_lock"]
    N789["uv_mutex_trylock"]
    N790["uv_mutex_unlock"]
    N791["uv_once"]
    N792["uv_os_environ"]
    N793["uv_os_get_group"]
    N794["uv_os_get_passwd"]
    N795["uv_os_get_passwd2"]
    N796["uv_os_getenv"]
    N797["uv_os_gethostname"]
    N798["uv_os_getpid"]
    N799["uv_os_getppid"]
    N800["uv_os_getpriority"]
    N801["uv_os_homedir"]
    N802["uv_os_setenv"]
    N803["uv_os_setpriority"]
    N804["uv_os_tmpdir"]
    N805["uv_os_uname"]
    N806["uv_os_unsetenv"]
    N807["uv_pipe"]
    N808["uv_pipe_bind"]
    N809["uv_pipe_bind2"]
    N810["uv_pipe_chmod"]
    N811["uv_pipe_connect"]
    N812["uv_pipe_connect2"]
    N813["uv_pipe_getpeername"]
    N814["uv_pipe_getsockname"]
    N815["uv_pipe_init"]
    N816["uv_pipe_open"]
    N817["uv_pipe_pending_type"]
    N818["uv_poll_init"]
    N819["uv_poll_init_socket"]
    N820["uv_poll_start"]
    N821["uv_poll_stop"]
    N822["uv_prepare_init"]
    N823["uv_prepare_start"]
    N824["uv_prepare_stop"]
    N825["uv_process_kill"]
    N826["uv_read_stop"]
    N827["uv_resident_set_memory"]
    N828["uv_run"]
    N829["uv_rwlock_destroy"]
    N830["uv_rwlock_init"]
    N831["uv_rwlock_rdlock"]
    N832["uv_rwlock_rdunlock"]
    N833["uv_rwlock_tryrdlock"]
    N834["uv_rwlock_trywrlock"]
    N835["uv_rwlock_wrlock"]
    N836["uv_rwlock_wrunlock"]
    N837["uv_sem_destroy"]
    N838["uv_sem_init"]
    N839["uv_sem_post"]
    N840["uv_sem_trywait"]
    N841["uv_sem_wait"]
    N842["uv_set_process_title"]
    N843["uv_setup_args"]
    N844["uv_shutdown"]
    N845["uv_signal_init"]
    N846["uv_signal_start"]
    N847["uv_signal_start_oneshot"]
    N848["uv_signal_stop"]
    N849["uv_sleep"]
    N850["uv_socketpair"]
    N851["uv_spawn"]
    N852["uv_stream_set_blocking"]
    N853["uv_tcp_close_reset"]
    N854["uv_tcp_getpeername"]
    N855["uv_tcp_getsockname"]
    N856["uv_tcp_init"]
    N857["uv_tcp_init_ex"]
    N858["uv_tcp_keepalive"]
    N859["uv_tcp_nodelay"]
    N860["uv_tcp_open"]
    N861["uv_thread_create"]
    N862["uv_thread_create_ex"]
    N863["uv_thread_detach"]
    N864["uv_thread_equal"]
    N865["uv_thread_getname"]
    N866["uv_thread_getpriority"]
    N867["uv_thread_join"]
    N868["uv_thread_self"]
    N869["uv_thread_setname"]
    N870["uv_thread_setpriority"]
    N871["uv_try_write"]
    N872["uv_try_write2"]
    N873["uv_tty_get_winsize"]
    N874["uv_tty_init"]
    N875["uv_tty_reset_mode"]
    N876["uv_tty_set_mode"]
    N877["uv_udp_getpeername"]
    N878["uv_udp_getsockname"]
    N879["uv_udp_open"]
    N880["uv_udp_set_broadcast"]
    N881["uv_udp_set_membership"]
    N882["uv_udp_set_multicast_interface"]
    N883["uv_udp_set_multicast_loop"]
    N884["uv_udp_set_multicast_ttl"]
    N885["uv_udp_set_source_membership"]
    N886["uv_udp_set_ttl"]
    N887["uv_udp_using_recvmmsg"]
    N888["uv_update_time"]
    N889["uv_uptime"]
    N890["uv_write"]
    N891["uv_write2"]
  end
  subgraph sg_uv["uv"]
    N892["uv__io_s::cb"]
    N893["uv__work::done"]
    N894["uv__work::work"]
  end
  N786 --> N46
  N548 -. fd_ready .-> N259
  N637 --> N176
  N489 --> N320
  N700 --> N653
  N676 --> N231
  N647 --> N178
  N626 --> N837
  N643 --> N178
  N560 --> N633
  N400 --> N401
  N429 -. fd_ready .-> N250
  N807 --> N441
  N669 --> N64
  N499 -. fd_ready .-> N4
  N491 --> N176
  N718 --> N335
  N741 --> N64
  N632 --> N176
  N499 --> N790
  N656 --> N178
  N347 -. fd_ready .-> N893
  N784 --> N691
  N811 --> N812
  N436 --> N320
  N521 --> N176
  N488 --> N487
  N570 --> N425
  N507 --> N312
  N735 --> N335
  N559 --> N850
  N644 --> N178
  N489 --> N324
  N882 --> N178
  N787 --> N199
  N525 --> N233
  N495 --> N786
  N486 --> N472
  N344 --> N176
  N433 --> N523
  N521 --> N64
  N413 -. fd_ready .-> N894
  N836 --> N92
  N448 --> N178
  N615 --> N835
  N495 --> N497
  N853 --> N165
  N457 --> N64
  N848 --> N599
  N809 --> N303
  N747 --> N303
  N413 --> N323
  N546 --> N178
  N717 --> N335
  N724 --> N178
  N700 --> N176
  N662 --> N669
  N410 --> N319
  N363 --> N176
  N289 --> N214
  N578 --> N523
  N844 --> N319
  N633 --> N178
  N643 --> N522
  N413 --> N788
  N784 --> N546
  N413 --> N320
  N316 --> N355
  N444 --> N176
  N577 --> N214
  N457 -. fd_ready .-> N254
  N752 --> N64
  N336 --> N214
  N793 --> N176
  N610 --> N34
  N636 --> N178
  N367 --> N47
  N851 --> N559
  N809 --> N416
  N413 --> N319
  N544 --> N64
  N743 --> N348
  N809 --> N425
  N429 --> N319
  N287 --> N139
  N507 --> N214
  N598 --> N608
  N592 --> N588
  N434 --> N319
  N791 --> N116
  N552 --> N40
  N820 --> N549
  N568 --> N442
  N650 --> N446
  N640 --> N178
  N801 --> N382
  N509 --> N714
  N555 --> N684
  N576 --> N320
  N682 --> N635
  N881 --> N367
  N528 --> N146
  N291 --> N841
  N673 --> N664
  N880 --> N178
  N628 -. fd_ready .-> N252
  N668 -. fd_ready .-> N270
  N409 --> N408
  N579 --> N128
  N766 --> N210
  N627 --> N683
  N773 --> N178
  N891 --> N321
  N421 --> N418
  N682 --> N686
  N784 --> N321
  N459 --> N725
  N842 --> N579
  N360 --> N214
  N500 --> N185
  N429 --> N326
  N659 --> N178
  N376 --> N303
  N669 -. fd_ready .-> N271
  N592 --> N178
  N527 --> N441
  N542 --> N509
  N683 --> N319
  N716 --> N227
  N548 -. fd_ready .-> N259
  N681 --> N176
  N597 --> N178
  N649 --> N115
  N439 --> N176
  N486 --> N110
  N683 -. fd_ready .-> N274
  N849 --> N64
  N874 --> N62
  N870 --> N218
  N607 --> N178
  N589 --> N591
  N489 --> N303
  N667 -. fd_ready .-> N270
  N579 -. fd_ready .-> N27
  N547 --> N549
  N587 --> N233
  N690 --> N879
  N297 --> N64
  N617 --> N129
  N793 --> N241
  N718 --> N348
  N293 --> N790
  N636 --> N239
  N447 --> N40
  N640 --> N148
  N753 --> N163
  N793 --> N84
  N496 --> N239
  N521 --> N64
  N669 --> N320
  N375 --> N64
  N850 --> N442
  N487 --> N562
  N499 --> N790
  N311 --> N64
  N497 --> N494
  N346 --> N788
  N661 --> N321
  N329 --> N566
  N636 --> N841
  N640 --> N312
  N628 --> N176
  N351 --> N303
  N591 --> N239
  N495 --> N438
  N493 --> N154
  N413 --> N323
  N428 --> N324
  N797 --> N214
  N579 -. fd_ready .-> N19
  N339 --> N785
  N640 --> N700
  N334 --> N326
  N497 --> N785
  N759 --> N790
  N583 --> N239
  N700 --> N440
  N746 --> N163
  N828 --> N334
  N640 --> N442
  N889 --> N96
  N632 --> N64
  N687 --> N176
  N352 --> N701
  N530 --> N545
  N608 --> N239
  N614 --> N178
  N496 --> N837
  N506 --> N234
  N652 --> N504
  N526 --> N198
  N334 --> N321
  N552 --> N195
  N521 --> N320
  N555 --> N217
  N442 --> N64
  N439 --> N176
  N626 --> N442
  N286 --> N337
  N803 --> N178
  N682 --> N176
  N293 --> N319
  N705 --> N41
  N643 --> N214
  N713 --> N233
  N530 --> N303
  N521 --> N220
  N608 --> N239
  N663 --> N139
  N742 --> N486
  N439 --> N425
  N456 --> N193
  N298 --> N303
  N748 --> N348
  N631 --> N539
  N784 --> N786
  N495 --> N163
  N575 --> N319
  N761 --> N503
  N481 --> N483
  N675 --> N178
  N583 --> N593
  N792 --> N100
  N462 --> N62
  N577 --> N303
  N572 --> N326
  N554 --> N824
  N293 --> N790
  N746 --> N214
  N639 --> N214
  N616 --> N109
  N492 -. fd_ready .-> N23
  N516 --> N198
  N360 --> N233
  N494 --> N128
  N297 --> N239
  N497 -. fd_ready .-> N15
  N404 --> N670
  N560 --> N239
  N622 --> N151
  N530 --> N785
  N499 --> N303
  N501 --> N64
  N667 --> N353
  N660 --> N326
  N690 --> N176
  N633 --> N64
  N499 --> N839
  N499 --> N491
  N715 --> N303
  N636 --> N53
  N494 --> N161
  N860 --> N451
  N497 --> N300
  N665 --> N515
  N493 --> N233
  N741 --> N176
  N670 --> N176
  N851 --> N323
  N764 --> N233
  N681 --> N320
  N784 --> N830
  N811 --> N163
  N654 --> N74
  N363 --> N774
  N694 --> N434
  N845 --> N323
  N490 --> N788
  N436 --> N324
  N521 --> N319
  N640 --> N837
  N479 --> N178
  N537 --> N62
  N413 --> N790
  N848 --> N64
  N605 --> N606
  N718 --> N486
  N695 --> N137
  N597 --> N139
  N624 --> N176
  N658 --> N178
  N285 --> N284
  N587 --> N34
  N659 --> N178
  N318 -. fd_ready .-> N272
  N724 --> N522
  N676 --> N366
  N805 --> N337
  N569 --> N635
  N594 --> N442
  N496 --> N837
  N707 --> N335
  N486 --> N178
  N617 --> N623
  N874 --> N633
  N776 --> N66
  N704 --> N239
  N759 --> N233
  N511 --> N791
  N418 --> N194
  N526 --> N239
  N874 --> N240
  N745 --> N335
  N581 --> N165
  N517 --> N523
  N360 --> N64
  N643 --> N321
  N641 --> N194
  N624 --> N144
  N521 --> N314
  N814 --> N542
  N671 --> N302
  N682 --> N425
  N677 --> N233
  N433 --> N326
  N733 --> N348
  N729 --> N348
  N777 --> N58
  N486 --> N460
  N753 --> N312
  N644 --> N165
  N541 --> N303
  N521 --> N239
  N516 --> N500
  N629 -. fd_ready .-> N267
  N764 --> N48
  N707 --> N248
  N694 --> N319
  N876 --> N51
  N579 -. fd_ready .-> N8
  N681 --> N321
  N839 --> N239
  N577 --> N335
  N494 --> N195
  N521 --> N64
  N667 -. fd_ready .-> N270
  N615 --> N178
  N397 --> N299
  N643 --> N213
  N508 --> N178
  N615 --> N791
  N639 --> N233
  N700 --> N541
  N832 --> N239
  N577 --> N233
  N652 --> N510
  N491 -. fd_ready .-> N24
  N830 --> N82
  N363 --> N774
  N550 --> N552
  N494 --> N221
  N747 --> N307
  N690 --> N303
  N874 --> N178
  N668 -. fd_ready .-> N270
  N307 --> N157
  N662 --> N64
  N652 --> N233
  N413 --> N692
  N463 --> N484
  N633 --> N176
  N520 --> N176
  N797 --> N225
  N670 --> N323
  N373 --> N139
  N670 --> N214
  N497 --> N785
  N636 --> N239
  N456 --> N740
  N600 --> N586
  N291 --> N862
  N360 --> N163
  N522 --> N176
  N577 --> N163
  N719 --> N335
  N405 --> N678
  N843 --> N163
  N624 --> N64
  N540 --> N539
  N755 --> N176
  N517 --> N326
  N366 --> N214
  N366 --> N288
  N571 --> N171
  N780 --> N645
  N499 --> N790
  N646 --> N165
  N575 --> N324
  N572 --> N319
  N800 --> N37
  N441 --> N62
  N828 --> N680
  N851 --> N444
  N784 --> N545
  N287 --> N286
  N575 -. fd_ready .-> N892
  N681 --> N178
  N663 --> N176
  N627 --> N176
  N448 --> N635
  N579 --> N195
  N494 --> N128
  N707 --> N215
  N542 --> N233
  N648 --> N233
  N667 -. fd_ready .-> N270
  N579 -. fd_ready .-> N19
  N719 --> N64
  N873 --> N425
  N456 --> N178
  N624 --> N176
  N742 --> N214
  N318 --> N64
  N643 --> N178
  N305 --> N533
  N339 --> N303
  N626 --> N442
  N643 --> N518
  N428 --> N320
  N577 --> N303
  N333 --> N332
  N641 --> N612
  N673 --> N178
  N713 --> N163
  N362 --> N303
  N850 --> N538
  N413 --> N704
  N429 --> N320
  N490 --> N320
  N828 --> N319
  N522 --> N64
  N429 --> N239
  N501 -. fd_ready .-> N255
  N488 --> N303
  N727 --> N486
  N350 --> N303
  N448 --> N176
  N314 --> N790
  N403 --> N666
  N454 --> N443
  N486 --> N52
  N347 --> N790
  N756 --> N348
  N300 -. fd_ready .-> N276
  N312 -. fd_ready .-> N278
  N543 --> N522
  N552 -. fd_ready .-> N1
  N690 --> N233
  N631 --> N321
  N691 --> N323
  N672 --> N178
  N528 --> N442
  N569 --> N425
  N599 --> N608
  N610 --> N178
  N343 --> N120
  N285 -. fd_ready .-> N3
  N697 --> N322
  N721 --> N348
  N671 --> N325
  N762 --> N506
  N629 --> N635
  N821 --> N64
  N785 --> N239
  N334 --> N321
  N501 --> N303
  N592 --> N178
  N350 --> N702
  N436 --> N303
  N668 -. fd_ready .-> N269
  N782 --> N529
  N850 --> N442
  N598 --> N601
  N636 --> N170
  N708 --> N178
  N493 --> N321
  N630 --> N319
  N682 --> N522
  N616 --> N220
  N442 --> N444
  N643 --> N425
  N494 --> N161
  N708 --> N247
  N471 --> N348
  N448 --> N88
  N591 --> N534
  N668 --> N178
  N480 --> N178
  N818 --> N323
  N628 --> N683
  N572 --> N324
  N311 --> N344
  N681 --> N64
  N816 --> N62
  N870 --> N98
  N583 --> N239
  N707 --> N152
  N857 --> N631
  N622 --> N97
  N528 --> N198
  N293 --> N323
  N674 --> N231
  N742 --> N312
  N521 --> N314
  N491 -. fd_ready .-> N25
  N490 --> N319
  N495 --> N55
  N350 --> N706
  N428 --> N319
  N670 --> N522
  N598 --> N64
  N622 --> N44
  N696 --> N323
  N681 --> N321
  N595 --> N596
  N668 -. fd_ready .-> N270
  N870 --> N178
  N731 --> N486
  N631 --> N539
  N381 --> N303
  N640 --> N198
  N761 --> N233
  N851 --> N560
  N761 --> N163
  N740 --> N176
  N365 --> N287
  N496 -. fd_ready .-> N10
  N850 --> N441
  N490 --> N785
  N843 --> N214
  N570 --> N64
  N644 --> N178
  N628 --> N176
  N616 --> N109
  N765 --> N178
  N486 --> N469
  N340 --> N397
  N712 --> N40
  N480 --> N142
  N708 --> N163
  N297 --> N176
  N637 --> N64
  N801 --> N794
  N637 --> N632
  N524 --> N525
  N668 --> N64
  N592 --> N593
  N479 --> N178
  N891 --> N439
  N773 --> N143
  N587 -. fd_ready .-> N264
  N670 --> N671
  N787 --> N239
  N656 --> N178
  N882 --> N139
  N490 --> N326
  N616 --> N109
  N311 --> N64
  N671 --> N326
  N530 --> N829
  N555 --> N244
  N490 --> N788
  N315 --> N299
  N794 --> N112
  N624 --> N176
  N667 --> N139
  N771 --> N772
  N490 --> N176
  N574 --> N326
  N577 --> N163
  N640 --> N196
  N616 --> N219
  N438 --> N176
  N497 --> N841
  N489 -. fd_ready .-> N253
  N438 -. fd_ready .-> N18
  N753 --> N486
  N494 --> N195
  N681 -. fd_ready .-> N261
  N609 --> N233
  N640 --> N837
  N677 --> N165
  N738 --> N348
  N480 --> N178
  N820 --> N176
  N579 --> N649
  N521 --> N176
  N645 --> N127
  N795 --> N507
  N762 --> N233
  N650 --> N160
  N426 --> N190
  N489 -. fd_ready .-> N253
  N579 -. fd_ready .-> N19
  N433 --> N323
  N499 -. fd_ready .-> N10
  N479 --> N480
  N842 --> N139
  N783 --> N428
  N328 -. fd_ready .-> N273
  N521 --> N64
  N660 --> N64
  N436 --> N499
  N643 --> N176
  N776 --> N239
  N742 --> N348
  N566 -. fd_ready .-> N31
  N496 --> N303
  N608 --> N607
  N828 --> N574
  N683 --> N303
  N497 --> N837
  N635 --> N176
  N717 --> N176
  N467 --> N442
  N452 -. fd_ready .-> N257
  N522 --> N176
  N677 --> N233
  N849 --> N176
  N521 --> N239
  N841 --> N87
  N870 --> N79
  N303 --> N178
  N812 --> N233
  N448 --> N176
  N749 --> N176
  N812 --> N213
  N280 --> N285
  N779 --> N49
  N810 --> N625
  N885 --> N369
  N287 --> N163
  N615 --> N444
  N875 --> N647
  N816 --> N178
  N497 --> N233
  N685 --> N142
  N762 --> N505
  N491 --> N64
  N530 --> N64
  N676 --> N139
  N475 --> N312
  N499 --> N312
  N877 --> N509
  N635 --> N178
  N788 --> N221
  N640 --> N146
  N426 --> N442
  N347 --> N320
  N544 --> N176
  N452 --> N64
  N555 --> N232
  N682 --> N320
  N444 --> N178
  N438 --> N788
  N682 --> N688
  N875 --> N178
  N418 --> N139
  N313 --> N767
  N691 --> N323
  N650 --> N535
  N628 --> N64
  N374 --> N229
  N784 --> N139
  N475 --> N55
  N702 --> N41
  N831 --> N189
  N286 --> N233
  N456 --> N42
  N314 --> N788
  N570 --> N176
  N747 --> N303
  N474 --> N50
  N793 --> N163
  N761 --> N348
  N837 --> N239
  N577 --> N55
  N786 --> N239
  N722 --> N233
  N307 --> N308
  N862 --> N211
  N497 --> N239
  N467 --> N178
  N576 --> N319
  N818 --> N537
  N494 --> N195
  N667 -. fd_ready .-> N270
  N661 --> N323
  N374 --> N39
  N456 --> N754
  N632 --> N627
  N882 --> N231
  N636 --> N840
  N882 --> N64
  N507 --> N233
  N410 --> N326
  N480 --> N178
  N485 --> N484
  N626 --> N64
  N599 --> N583
  N859 --> N646
  N756 --> N233
  N555 --> N684
  N670 --> N302
  N467 --> N163
  N619 --> N173
  N448 --> N523
  N303 -. fd_ready .-> N277
  N757 --> N758
  N624 -. fd_ready .-> N414
  N668 --> N178
  N579 --> N195
  N891 --> N635
  N639 --> N638
  N495 --> N691
  N530 --> N790
  N851 --> N198
  N467 --> N91
  N494 --> N195
  N850 --> N196
  N753 --> N348
  N555 --> N684
  N599 --> N64
  N862 --> N535
  N289 --> N139
  N653 --> N647
  N699 --> N80
  N707 --> N178
  N410 --> N320
  N632 --> N569
  N667 --> N423
  N339 --> N239
  N783 --> N519
  N640 --> N838
  N626 --> N867
  N853 --> N425
  N719 --> N486
  N891 --> N176
  N482 --> N312
  N467 --> N441
  N487 --> N142
  N807 --> N538
  N800 --> N178
  N784 --> N829
  N616 --> N239
  N497 --> N239
  N882 --> N239
  N555 --> N100
  N464 --> N532
  N773 --> N205
  N536 --> N195
  N521 --> N64
  N624 --> N176
  N363 --> N64
  N733 --> N64
  N501 --> N303
  N852 --> N538
  N579 -. fd_ready .-> N28
  N362 --> N300
  N858 --> N425
  N879 --> N342
  N765 --> N86
  N852 --> N425
  N626 --> N442
  N579 --> N128
  N521 --> N109
  N522 --> N420
  N874 --> N539
  N541 --> N249
  N809 --> N178
  N578 --> N450
  N673 --> N178
  N678 --> N302
  N669 --> N176
  N456 --> N178
  N292 -. fd_ready .-> N275
  N576 -. fd_ready .-> N260
  N882 --> N165
  N719 --> N176
  N533 --> N64
  N499 --> N64
  N623 --> N237
  N362 --> N379
  N369 --> N214
  N570 --> N64
  N490 --> N841
  N493 --> N319
  N682 --> N64
  N437 -. fd_ready .-> N13
  N413 --> N839
  N819 --> N818
  N486 --> N178
  N693 --> N61
  N289 --> N233
  N644 --> N178
  N420 --> N422
  N487 --> N35
  N437 --> N839
  N681 --> N64
  N495 --> N312
  N568 --> N442
  N426 --> N178
  N652 --> N425
  N626 --> N442
  N784 --> N321
  N330 -. fd_ready .-> N262
  N856 --> N857
  N366 --> N233
  N851 --> N557
  N469 --> N191
  N398 --> N656
  N706 --> N239
  N622 --> N97
  N499 --> N788
  N555 --> N444
  N805 --> N337
  N467 --> N791
  N680 --> N511
  N372 --> N339
  N369 --> N149
  N413 --> N319
  N549 --> N523
  N592 --> N178
  N473 --> N304
  N413 --> N295
  N346 --> N788
  N391 --> N233
  N724 --> N444
  N591 --> N584
  N842 --> N790
  N344 --> N345
  N433 --> N431
  N759 --> N790
  N599 --> N64
  N427 --> N326
  N690 --> N633
  N634 --> N303
  N743 --> N486
  N369 --> N366
  N764 --> N166
  N687 --> N64
  N666 --> N523
  N807 --> N441
  N426 --> N538
  N626 --> N826
  N542 --> N139
  N574 -. fd_ready .-> N258
  N467 -. fd_ready .-> N32
  N430 --> N239
  N410 -. fd_ready .-> N33
  N369 --> N47
  N421 --> N633
  N798 --> N159
  N772 --> N97
  N599 --> N588
  N734 --> N486
  N742 --> N233
  N616 --> N109
  N346 --> N319
  N570 --> N635
  N670 --> N64
  N711 --> N161
  N636 --> N233
  N374 --> N531
  N486 --> N461
  N769 --> N322
  N717 --> N64
  N626 --> N176
  N569 --> N639
  N505 -. fd_ready .-> N256
  N804 --> N105
  N313 --> N788
  N640 --> N691
  N493 --> N139
  N425 --> N176
  N828 --> N575
  N486 --> N462
  N663 --> N64
  N376 --> N784
  N411 --> N349
  N691 --> N432
  N396 --> N299
  N501 --> N176
  N882 --> N233
  N522 --> N64
  N456 --> N747
  N693 --> N248
  N584 --> N442
  N507 --> N233
  N486 --> N476
  N618 --> N124
  N713 --> N214
  N874 --> N442
  N599 --> N176
  N652 --> N64
  N624 --> N64
  N494 --> N195
  N501 --> N303
  N490 -. fd_ready .-> N253
  N559 --> N64
  N496 --> N319
  N636 --> N64
  N677 --> N369
  N578 --> N176
  N548 --> N523
  N686 --> N303
  N298 --> N176
  N673 --> N672
  N675 --> N369
  N687 --> N302
  N816 --> N451
  N628 --> N64
  N670 --> N312
  N367 --> N114
  N486 --> N456
  N569 --> N522
  N787 --> N239
  N555 --> N89
  N569 --> N425
  N438 --> N790
  N587 --> N599
  N785 --> N85
  N498 --> N176
  N521 --> N681
  N537 --> N178
  N844 --> N425
  N655 --> N64
  N786 --> N106
  N748 --> N64
  N521 --> N314
  N744 --> N486
  N702 --> N239
  N741 --> N335
  N287 --> N337
  N291 --> N239
  N555 --> N684
  N862 --> N239
  N591 --> N239
  N644 --> N165
  N729 --> N486
  N671 --> N326
  N475 --> N303
  N439 --> N64
  N683 --> N64
  N812 --> N139
  N764 --> N166
  N825 --> N779
  N627 --> N64
  N391 --> N120
  N521 --> N176
  N670 --> N176
  N656 --> N165
  N522 --> N323
  N805 --> N178
  N627 -. fd_ready .-> N252
  N493 --> N64
  N486 --> N107
  N352 --> N788
  N675 --> N233
  N413 --> N321
  N758 --> N183
  N730 --> N486
  N676 --> N178
  N507 --> N303
  N497 --> N239
  N671 --> N320
  N498 --> N64
  N668 --> N178
  N297 --> N751
  N523 --> N319
  N524 --> N153
  N660 --> N176
  N405 --> N341
  N412 --> N349
  N291 --> N321
  N762 --> N348
  N700 --> N340
  N456 --> N212
  N493 --> N323
  N494 --> N195
  N494 --> N195
  N493 --> N151
  N313 --> N790
  N812 --> N522
  N493 --> N176
  N334 --> N283
  N335 --> N163
  N626 --> N515
  N617 --> N176
  N335 --> N312
  N810 --> N178
  N364 --> N157
  N631 --> N321
  N658 --> N178
  N756 --> N312
  N851 --> N303
  N663 --> N233
  N314 --> N767
  N620 --> N619
  N334 --> N299
  N609 --> N138
  N843 --> N163
  N497 --> N201
  N377 --> N767
  N364 --> N308
  N639 --> N95
  N706 --> N178
  N866 --> N178
  N306 --> N303
  N521 --> N64
  N375 --> N373
  N874 --> N178
  N363 --> N700
  N361 --> N323
  N653 --> N626
  N672 --> N101
  N749 --> N348
  N438 --> N64
  N668 --> N64
  N643 --> N178
  N874 --> N178
  N673 --> N178
  N615 --> N178
  N891 --> N312
  N452 --> N176
  N733 --> N176
  N847 --> N598
  N860 --> N538
  N812 --> N416
  N848 --> N176
  N632 --> N64
  N413 --> N319
  N818 --> N451
  N622 --> N151
  N584 --> N442
  N700 --> N459
  N725 --> N442
  N843 --> N163
  N758 --> N61
  N792 --> N100
  N486 --> N473
  N486 --> N455
  N449 --> N441
  N637 --> N839
  N530 --> N319
  N559 --> N176
  N628 --> N515
  N408 --> N176
  N373 --> N530
  N592 --> N142
  N291 --> N72
  N643 --> N525
  N293 --> N788
  N853 --> N178
  N517 --> N544
  N432 --> N539
  N576 --> N326
  N297 --> N379
  N334 --> N394
  N681 --> N176
  N835 --> N239
  N523 --> N176
  N875 --> N178
  N425 --> N64
  N700 --> N305
  N786 --> N239
  N746 --> N233
  N681 --> N325
  N804 --> N105
  N486 --> N226
  N351 --> N703
  N828 --> N572
  N433 --> N319
  N650 --> N446
  N656 --> N580
  N577 --> N55
  N506 --> N502
  N615 --> N245
  N636 --> N139
  N530 --> N788
  N291 --> N703
  N494 --> N195
  N717 --> N486
  N495 --> N303
  N770 --> N326
  N430 --> N178
  N473 --> N178
  N784 --> N321
  N497 --> N837
  N668 --> N233
  N702 --> N108
  N669 --> N303
  N467 --> N178
  N521 --> N198
  N543 --> N425
  N293 --> N323
  N659 --> N139
  N700 --> N64
  N362 --> N395
  N491 --> N139
  N569 --> N635
  N335 --> N233
  N756 --> N214
  N828 --> N314
  N873 --> N178
  N615 --> N34
  N661 --> N520
  N413 --> N325
  N615 --> N239
  N800 --> N178
  N700 --> N657
  N599 --> N176
  N758 --> N132
  N640 --> N442
  N369 --> N233
  N636 --> N692
  N544 --> N176
  N521 -. fd_ready .-> N892
  N502 --> N178
  N862 --> N73
  N786 --> N199
  N433 --> N442
  N649 --> N36
  N784 --> N594
  N512 --> N235
  N657 --> N517
  N493 --> N214
  N568 --> N34
  N724 --> N500
  N810 --> N425
  N627 --> N64
  N639 --> N176
  N809 --> N194
  N455 --> N303
  N587 --> N64
  N569 --> N64
  N833 --> N239
  N429 --> N64
  N664 --> N233
  N608 --> N220
  N420 --> N239
  N286 --> N120
  N882 --> N178
  N488 --> N453
  N746 --> N486
  N479 --> N178
  N659 --> N233
  N579 --> N161
  N385 --> N348
  N613 --> N177
  N754 --> N486
  N812 --> N178
  N522 --> N64
  N310 --> N311
  N746 --> N348
  N761 --> N310
  N674 --> N165
  N406 --> N679
  N700 --> N554
  N581 --> N165
  N710 --> N128
  N733 --> N486
  N637 --> N64
  N346 --> N788
  N480 --> N178
  N670 --> N522
  N480 --> N178
  N615 --> N442
  N457 --> N176
  N715 --> N303
  N787 --> N200
  N829 --> N239
  N429 --> N34
  N486 --> N467
  N649 --> N233
  N677 --> N663
  N578 --> N426
  N587 --> N202
  N502 --> N176
  N391 --> N120
  N794 --> N507
  N862 --> N201
  N607 --> N142
  N592 --> N176
  N566 -. fd_ready .-> N31
  N486 --> N239
  N291 --> N105
  N285 -. fd_ready .-> N3
  N521 --> N178
  N519 --> N527
  N764 --> N139
  N538 --> N178
  N879 --> N538
  N682 --> N319
  N739 --> N486
  N501 --> N176
  N579 -. fd_ready .-> N5
  N551 --> N553
  N857 --> N442
  N515 --> N64
  N346 --> N323
  N577 --> N233
  N537 --> N178
  N832 --> N92
  N660 --> N64
  N670 --> N176
  N734 --> N214
  N394 --> N397
  N472 --> N303
  N298 --> N533
  N851 --> N321
  N559 --> N176
  N660 --> N64
  N636 --> N515
  N660 --> N320
  N426 --> N176
  N640 --> N442
  N530 --> N442
  N515 --> N176
  N486 --> N466
  N566 --> N178
  N579 --> N195
  N467 --> N239
  N486 --> N212
  N458 --> N198
  N372 --> N584
  N617 --> N64
  N793 --> N312
  N529 --> N319
  N523 --> N326
  N577 --> N184
  N740 --> N335
  N812 --> N633
  N430 --> N239
  N506 --> N239
  N797 --> N163
  N486 --> N475
  N644 --> N165
  N592 --> N603
  N588 --> N604
  N301 --> N239
  N638 --> N312
  N520 --> N321
  N474 --> N312
  N417 --> N786
  N335 --> N214
  N598 --> N608
  N789 --> N239
  N443 --> N415
  N701 --> N239
  N641 --> N178
  N786 --> N239
  N596 --> N522
  N842 --> N233
  N616 --> N239
  N521 --> N64
  N871 --> N872
  N464 --> N483
  N329 --> N564
  N448 --> N64
  N292 --> N296
  N555 --> N442
  N448 --> N176
  N477 --> N143
  N613 --> N178
  N472 --> N131
  N828 --> N529
  N838 --> N239
  N569 --> N178
  N745 --> N176
  N674 --> N233
  N721 --> N486
  N456 --> N500
  N496 --> N438
  N351 --> N312
  N707 --> N61
  N569 --> N34
  N773 --> N205
  N683 --> N320
  N560 --> N442
  N683 --> N324
  N766 --> N102
  N362 --> N751
  N289 --> N233
  N521 --> N313
  N404 --> N341
  N623 --> N181
  N568 --> N178
  N539 --> N178
  N780 --> N543
  N569 --> N629
  N346 --> N790
  N773 --> N214
  N632 --> N683
  N569 --> N571
  N700 --> N585
  N667 --> N178
  N515 --> N64
  N702 --> N239
  N421 --> N442
  N519 --> N303
  N291 --> N321
  N784 --> N233
  N592 --> N607
  N359 --> N233
  N458 --> N239
  N670 --> N214
  N521 --> N239
  N594 --> N599
  N347 --> N324
  N419 --> N425
  N797 --> N233
  N578 --> N176
  N876 --> N655
  N616 --> N109
  N881 --> N674
  N676 --> N663
  N686 --> N326
  N352 --> N706
  N576 --> N324
  N783 --> N319
  N418 --> N233
  N831 --> N239
  N732 --> N486
  N409 --> N408
  N582 --> N581
  N452 --> N64
  N859 --> N425
  N493 --> N498
  N773 --> N335
  N456 --> N747
  N587 --> N239
  N631 --> N323
  N454 --> N178
  N310 --> N311
  N820 --> N64
  N744 --> N348
  N458 --> N62
  N844 --> N176
  N521 --> N64
  N489 --> N326
  N456 --> N747
  N480 --> N208
  N648 --> N178
  N530 --> N64
  N615 --> N245
  N851 --> N323
  N409 --> N176
  N495 --> N407
  N495 --> N178
  N793 --> N163
  N670 --> N663
  N862 --> N160
  N806 --> N178
  N409 --> N64
  N842 --> N233
  N496 --> N320
  N668 --> N887
  N497 --> N838
  N555 --> N137
  N522 --> N176
  N530 --> N303
  N668 --> N233
  N756 --> N486
  N713 --> N178
  N573 --> N452
  N637 --> N515
  N713 --> N55
  N521 --> N198
  N704 --> N140
  N386 --> N329
  N579 -. fd_ready .-> N19
  N643 --> N178
  N647 --> N113
  N616 --> N109
  N702 --> N239
  N722 --> N348
  N552 --> N233
  N724 --> N303
  N876 --> N647
  N499 --> N64
  N857 --> N421
  N569 -. fd_ready .-> N265
  N536 --> N40
  N628 --> N448
  N652 --> N178
  N671 --> N319
  N577 --> N151
  N501 --> N64
  N682 --> N635
  N386 --> N348
  N465 --> N484
  N620 --> N621
  N307 --> N157
  N755 --> N348
  N521 --> N176
  N611 --> N165
  N364 --> N304
  N412 --> N176
  N324 --> N319
  N773 --> N205
  N476 --> N186
  N759 --> N214
  N682 --> N652
  N292 --> N700
  N632 --> N448
  N772 --> N207
  N623 --> N59
  N809 --> N214
  N851 --> N303
  N626 --> N839
  N682 --> N686
  N722 --> N214
  N718 --> N64
  N556 --> N326
  N505 --> N64
  N681 --> N326
  N738 --> N335
  N626 --> N635
  N627 --> N319
  N740 --> N348
  N784 --> N321
  N677 --> N178
  N735 --> N64
  N727 --> N348
  N448 -. fd_ready .-> N263
  N496 --> N785
  N456 --> N178
  N449 --> N442
  N681 --> N323
  N793 --> N303
  N792 --> N303
  N674 --> N178
  N876 --> N425
  N569 -. fd_ready .-> N267
  N818 --> N516
  N472 --> N34
  N419 --> N418
  N772 --> N233
  N784 --> N321
  N579 -. fd_ready .-> N19
  N660 --> N176
  N646 --> N178
  N636 --> N64
  N495 --> N64
  N737 --> N176
  N496 --> N326
  N507 --> N163
  N413 --> N321
  N494 --> N195
  N598 --> N597
  N521 --> N198
  N518 --> N319
  N726 --> N486
  N862 --> N650
  N610 --> N178
  N465 --> N484
  N523 --> N176
  N643 --> N178
  N679 --> N673
  N684 --> N685
  N624 --> N129
  N350 --> N785
  N752 --> N176
  N291 --> N321
  N465 --> N156
  N669 --> N302
  N734 --> N348
  N671 --> N673
  N796 --> N105
  N613 --> N538
  N568 --> N442
  N828 --> N521
  N698 --> N326
  N641 --> N178
  N637 --> N176
  N473 --> N143
  N801 --> N382
  N577 --> N338
  N490 --> N326
  N509 --> N178
  N636 --> N53
  N287 --> N233
  N874 --> N326
  N494 --> N195
  N761 --> N163
  N494 --> N71
  N402 --> N665
  N428 --> N442
  N595 --> N442
  N343 --> N233
  N642 --> N626
  N555 --> N178
  N524 --> N205
  N659 --> N178
  N428 --> N442
  N801 --> N163
  N348 --> N293
  N613 --> N442
  N412 --> N64
  N494 --> N195
  N652 --> N233
  N570 --> N176
  N840 --> N239
  N689 --> N180
  N818 --> N538
  N388 --> N614
  N462 --> N62
  N488 --> N504
  N521 --> N176
  N288 --> N233
  N491 --> N233
  N380 --> N303
  N376 --> N312
  N553 --> N208
  N537 --> N62
  N793 --> N312
  N805 --> N337
  N537 --> N178
  N773 --> N233
  N685 --> N126
  N643 --> N233
  N753 --> N214
  N686 --> N323
  N669 --> N523
  N663 --> N656
  N555 --> N172
  N668 -. fd_ready .-> N270
  N670 --> N319
  N587 --> N178
  N700 --> N64
  N486 --> N479
  N439 --> N64
  N884 --> N582
  N868 --> N223
  N377 --> N790
  N648 --> N76
  N762 --> N233
  N740 --> N64
  N472 --> N208
  N744 --> N176
  N635 --> N142
  N891 --> N323
  N579 -. fd_ready .-> N7
  N870 --> N178
  N568 --> N539
  N809 --> N312
  N490 --> N303
  N297 --> N64
  N521 -. fd_ready .-> N892
  N521 --> N64
  N346 --> N790
  N637 --> N632
  N569 --> N176
  N494 --> N195
  N683 --> N176
  N523 --> N323
  N617 --> N122
  N507 --> N303
  N530 --> N785
  N636 --> N155
  N604 --> N586
  N486 --> N178
  N499 -. fd_ready .-> N20
  N641 --> N178
  N773 --> N300
  N555 --> N187
  N633 --> N646
  N282 --> N284
  N699 --> N80
  N569 -. fd_ready .-> N267
  N676 --> N233
  N738 --> N486
  N809 --> N214
  N633 --> N178
  N650 --> N446
  N749 --> N64
  N678 --> N176
  N352 --> N790
  N458 --> N435
  N628 --> N176
  N652 --> N139
  N639 --> N64
  N640 --> N442
  N598 --> N599
  N649 --> N178
  N444 --> N178
  N292 --> N239
  N736 --> N486
  N578 --> N64
  N495 --> N323
  N731 --> N348
  N656 --> N178
  N752 --> N348
  N493 --> N788
  N708 --> N178
  N866 --> N79
  N678 --> N672
  N457 --> N176
  N668 --> N176
  N439 --> N510
  N291 --> N312
  N490 --> N790
  N784 --> N303
  N622 --> N214
  N734 --> N163
  N664 --> N139
  N652 --> N425
  N495 --> N321
  N844 --> N518
  N597 --> N233
  N656 --> N611
  N761 --> N163
  N287 --> N120
  N834 --> N69
  N334 --> N319
  N497 --> N139
  N499 --> N176
  N593 --> N34
  N579 -. fd_ready .-> N7
  N754 --> N64
  N420 --> N333
  N720 --> N486
  N492 -. fd_ready .-> N26
  N318 --> N176
  N449 --> N178
  N479 --> N188
  N755 --> N486
  N677 --> N139
  N444 --> N443
  N674 --> N47
  N773 --> N514
  N292 -. fd_ready .-> N275
  N812 --> N178
  N881 --> N369
  N435 --> N57
  N364 --> N176
  N616 --> N555
  N497 --> N321
  N834 --> N239
  N569 --> N64
  N579 -. fd_ready .-> N7
  N700 --> N427
  N720 --> N348
  N891 --> N682
  N579 -. fd_ready .-> N29
  N627 --> N64
  N460 --> N462
  N660 --> N319
  N885 --> N677
  N466 --> N162
  N660 --> N64
  N669 --> N319
  N690 --> N202
  N543 --> N127
  N842 --> N788
  N430 --> N178
  N533 --> N64
  N615 --> N176
  N503 --> N502
  N334 --> N323
  N670 --> N64
  N855 --> N509
  N485 --> N192
  N490 --> N700
  N555 --> N684
  N563 --> N553
  N636 --> N515
  N362 --> N233
  N663 --> N139
  N672 --> N178
  N755 --> N335
  N570 --> N522
  N487 --> N180
  N810 --> N178
  N450 --> N539
  N452 --> N533
  N655 --> N176
  N542 --> N233
  N570 --> N64
  N669 --> N176
  N486 --> N99
  N599 --> N597
  N494 --> N195
  N429 --> N178
  N712 --> N195
  N481 --> N625
  N736 --> N348
  N682 --> N64
  N662 --> N176
  N516 --> N178
  N369 --> N114
  N670 --> N233
  N627 --> N64
  N629 --> N523
  N419 --> N421
  N393 --> N643
  N681 --> N319
  N292 --> N396
  N735 --> N348
  N436 --> N326
  N597 --> N138
  N486 --> N488
  N526 --> N178
  N290 --> N239
  N670 --> N64
  N520 --> N64
  N759 --> N788
  N688 --> N64
  N432 --> N791
  N560 --> N538
  N641 --> N178
  N891 --> N214
  N801 --> N233
  N816 --> N633
  N718 --> N176
  N626 --> N837
  N444 --> N64
  N433 --> N324
  N433 --> N320
  N577 --> N105
  N565 --> N568
  N753 --> N233
  N792 --> N335
  N762 --> N214
  N714 --> N425
  N577 --> N233
  N521 --> N176
  N294 --> N214
  N429 --> N324
  N499 --> N498
  N867 --> N238
  N707 --> N248
  N644 --> N178
  N569 --> N353
  N641 --> N178
  N668 --> N139
  N784 --> N139
  N655 --> N135
  N574 --> N324
  N350 --> N176
  N736 --> N335
  N745 --> N486
  N851 --> N64
  N432 --> N520
  N566 --> N178
  N511 --> N123
  N469 --> N303
  N589 --> N179
  N316 --> N95
  N735 --> N176
  N568 --> N442
  N630 --> N323
  N452 --> N176
  N761 --> N312
  N840 --> N63
  N578 -. fd_ready .-> N266
  N610 --> N239
  N577 --> N214
  N572 -. fd_ready .-> N251
  N813 --> N542
  N626 --> N700
  N541 --> N626
  N793 --> N233
  N817 --> N766
  N666 --> N515
  N521 --> N526
  N494 --> N195
  N728 --> N348
  N710 --> N303
  N826 --> N523
  N706 --> N178
  N495 --> N335
  N807 --> N538
  N613 --> N441
  N761 --> N233
  N874 --> N442
  N594 --> N442
  N490 --> N64
  N489 --> N790
  N595 --> N523
  N815 --> N631
  N820 --> N176
  N669 -. fd_ready .-> N271
  N767 --> N511
  N818 --> N520
  N486 --> N228
  N849 --> N38
  N292 --> N747
  N438 -. fd_ready .-> N16
  N360 --> N774
  N784 --> N281
  N632 --> N64
  N690 --> N442
  N438 --> N312
  N456 --> N500
  N452 --> N64
  N820 --> N522
  N652 --> N178
  N413 --> N790
  N596 --> N520
  N383 --> N316
  N493 --> N790
  N700 --> N176
  N494 --> N195
  N891 --> N64
  N796 --> N163
  N290 --> N291
  N672 --> N664
  N671 --> N323
  N436 --> N788
  N807 --> N242
  N339 --> N293
  N790 --> N71
  N626 --> N517
  N839 --> N94
  N624 --> N222
  N456 --> N747
  N632 --> N319
  N373 --> N233
  N773 --> N514
  N413 --> N788
  N641 --> N165
  N521 --> N176
  N527 --> N146
  N334 -. fd_ready .-> N268
  N652 --> N101
  N521 --> N680
  N703 --> N119
  N650 --> N93
  N766 --> N500
  N874 --> N631
  N737 --> N486
  N648 --> N115
  N523 --> N176
  N675 --> N165
  N645 --> N522
  N437 -. fd_ready .-> N12
  N628 --> N176
  N688 --> N176
  N683 --> N687
  N668 --> N139
  N627 --> N210
  N572 --> N323
  N615 --> N176
  N430 --> N198
  N622 --> N44
  N499 --> N790
  N660 --> N176
  N821 --> N176
  N854 --> N509
  N668 --> N667
  N486 --> N474
  N882 --> N369
  N656 --> N612
  N532 --> N77
  N355 --> N784
  N702 --> N71
  N741 --> N348
  N879 --> N451
  N456 --> N178
  N699 --> N178
  N546 --> N527
  N851 --> N239
  N792 --> N303
  N615 --> N64
  N358 --> N303
  N339 --> N702
  N448 --> N319
  N812 --> N425
  N755 --> N64
  N669 --> N326
  N432 --> N198
  N828 --> N680
  N873 --> N178
  N881 --> N663
  N513 --> N770
  N667 --> N178
  N539 --> N244
  N627 --> N630
  N824 --> N326
  N641 --> N178
  N426 --> N441
  N495 --> N790
  N577 --> N178
  N773 --> N514
  N632 --> N425
  N671 --> N320
  N689 --> N142
  N444 --> N178
  N540 --> N56
  N627 --> N176
  N311 --> N344
  N700 --> N556
  N745 --> N348
  N639 --> N64
  N555 --> N43
  N579 --> N195
  N784 --> N300
  N616 --> N178
  N809 --> N613
  N540 --> N442
  N661 --> N613
  N452 --> N176
  N678 --> N64
  N577 --> N120
  N395 --> N321
  N725 --> N517
  N632 --> N425
  N705 --> N239
  N793 --> N233
  N521 --> N526
  N625 --> N216
  N555 --> N182
  N668 --> N176
  N863 --> N130
  N549 --> N544
  N527 --> N178
  N888 --> N680
  N523 --> N64
  N641 --> N419
  N429 --> N176
  N724 --> N520
  N521 --> N314
  N807 --> N442
  N851 --> N64
  N828 --> N319
  N534 --> N807
  N836 --> N239
  N874 --> N654
  N474 --> N470
  N533 --> N176
  N364 --> N64
  N569 --> N64
  N579 -. fd_ready .-> N6
  N447 --> N335
  N640 --> N178
  N808 --> N809
  N523 --> N64
  N681 --> N178
  N570 --> N176
  N331 --> N329
  N473 --> N335
  N723 --> N323
  N507 --> N214
  N652 --> N178
  N674 --> N139
  N663 --> N239
  N497 --> N211
  N523 --> N64
  N311 --> N64
  N885 --> N367
  N636 --> N34
  N615 --> N534
  N291 --> N838
  N467 --> N832
  N455 --> N134
  N475 --> N178
  N512 --> N239
  N627 --> N425
  N627 --> N176
  N751 --> N64
  N724 --> N303
  N489 --> N788
  N486 --> N147
  N555 --> N537
  N858 --> N644
  N783 --> N323
  N502 --> N239
  N501 --> N176
  N347 --> N319
  N821 --> N549
  N626 --> N442
  N828 --> N529
  N497 --> N838
  N530 --> N594
  N591 --> N607
  N522 --> N176
  N809 --> N442
  N784 --> N321
  N569 -. fd_ready .-> N267
  N569 --> N523
  N711 --> N40
  N357 --> N337
  N542 --> N214
  N853 --> N178
  N499 --> N325
  N636 --> N176
  N784 --> N233
  N700 --> N642
  N440 --> N698
  N724 --> N495
  N450 --> N426
  N372 --> N561
  N292 --> N774
  N579 -. fd_ready .-> N30
  N562 --> N552
  N793 --> N163
  N310 --> N344
  N636 --> N53
  N659 --> N213
  N812 --> N233
  N595 --> N442
  N801 --> N214
  N845 --> N596
  N495 --> N785
  N585 --> N599
  N598 --> N176
  N521 --> N321
  N874 --> N640
  N621 --> N195
  N609 --> N239
  N851 --> N615
  N632 --> N629
  N495 --> N303
  N366 --> N151
  N520 --> N64
  N660 --> N669
  N456 --> N178
  N542 --> N203
  N842 --> N791
  N883 --> N582
  N486 --> N184
  N387 --> N570
  N537 --> N178
  N587 --> N176
  N881 --> N663
  N804 --> N233
  N369 --> N233
  N399 --> N659
  N480 --> N121
  N702 --> N239
  N377 --> N788
  N810 --> N814
  N800 --> N178
  N870 --> N243
  N792 --> N151
  N578 --> N64
  N578 --> N64
  N843 --> N312
  N683 --> N326
  N761 --> N214
  N735 --> N486
  N656 --> N194
  N333 --> N303
  N408 --> N64
  N876 --> N178
  N707 --> N248
  N567 --> N195
  N368 --> N365
  N579 -. fd_ready .-> N9
  N873 --> N74
  N805 --> N337
  N712 --> N447
  N364 --> N157
  N495 --> N157
  N658 --> N178
  N347 --> N326
  N428 --> N523
  N378 --> N233
  N751 --> N335
  N555 --> N684
  N754 --> N335
  N739 --> N335
  N637 --> N515
  N558 --> N233
  N357 --> N120
  N497 --> N650
  N499 --> N790
  N862 --> N239
  N853 --> N700
  N521 --> N176
  N665 --> N522
  N627 --> N176
  N891 --> N522
  N457 --> N64
  N291 --> N786
  N616 --> N109
  N356 --> N343
  N413 --> N326
  N452 --> N628
  N627 --> N425
  N849 --> N178
  N766 --> N136
  N488 --> N178
  N569 -. fd_ready .-> N267
  N891 --> N233
  N380 --> N303
  N413 --> N704
  N700 --> N547
  N872 --> N652
  N675 --> N139
  N482 --> N206
  N492 -. fd_ready .-> N22
  N633 --> N178
  N362 --> N163
  N662 --> N671
  N636 --> N170
  N804 --> N105
  N807 --> N442
  N763 --> N508
  N668 --> N64
  N778 --> N111
  N632 --> N176
  N431 --> N445
  N761 --> N233
  N617 --> N122
  N354 --> N346
  N592 --> N233
  N633 --> N165
  N761 --> N214
  N432 --> N534
  N768 --> N323
  N456 --> N117
  N686 --> N518
  N788 --> N239
  N351 --> N786
  N810 --> N226
  N365 --> N286
  N486 --> N103
  N575 --> N321
  N521 --> N681
  N880 --> N165
  N885 --> N367
  N797 --> N178
  N885 --> N369
  N583 --> N220
  N501 --> N64
  N690 --> N64
  N644 --> N165
  N754 --> N348
  N882 --> N367
  N508 --> N204
  N754 --> N176
  N590 --> N791
  N518 --> N323
  N822 --> N323
  N293 --> N704
  N796 --> N233
  N707 --> N152
  N505 --> N176
  N363 --> N176
  N521 --> N220
  N552 --> N214
  N413 --> N320
  N622 --> N233
  N843 --> N233
  N463 --> N118
  N545 --> N496
  N486 --> N249
  N530 --> N442
  N773 --> N233
  N789 --> N150
  N521 --> N64
  N787 --> N46
  N736 --> N176
  N578 --> N425
  N297 --> N176
  N574 --> N319
  N579 --> N195
  N663 --> N233
  N635 --> N64
  N363 --> N64
  N851 --> N178
  N505 --> N64
  N486 --> N463
  N687 --> N64
  N784 --> N680
  N784 --> N321
  N702 --> N85
  N521 --> N526
  N850 --> N178
  N493 --> N233
  N369 --> N139
  N291 --> N239
  N624 --> N60
  N350 --> N64
  N462 --> N169
  N632 --> N176
  N764 --> N175
  N784 --> N303
  N461 --> N651
  N396 --> N282
  N429 --> N178
  N499 --> N788
  N456 --> N444
  N498 --> N692
  N677 --> N214
  N521 -. fd_ready .-> N892
  N553 --> N35
  N366 --> N289
  N636 --> N178
  N311 --> N344
  N724 --> N335
  N638 --> N332
  N498 --> N790
  N362 --> N214
  N803 --> N209
  N579 --> N195
  N498 --> N317
  N409 --> N312
  N521 --> N526
  N359 --> N214
  N661 --> N321
  N844 --> N64
  N472 --> N504
  N784 --> N590
  N391 --> N233
  N751 --> N176
  N865 --> N648
  N577 --> N338
  N760 --> N96
  N568 --> N178
  N615 --> N178
  N543 --> N178
  N891 --> N302
  N681 --> N320
  N432 --> N522
  N574 --> N320
  N401 --> N661
  N311 --> N344
  N555 --> N239
  N330 --> N64
  N480 --> N34
  N553 --> N178
  N636 --> N53
  N499 --> N788
  N748 --> N486
  N722 --> N312
  N734 --> N312
  N413 --> N706
  N816 --> N640
  N521 --> N64
  N812 --> N178
  N598 --> N583
  N555 --> N65
  N643 --> N178
  N665 --> N663
  N436 -. fd_ready .-> N17
  N334 --> N397
  N486 --> N485
  N292 --> N774
  N793 --> N303
  N473 --> N178
  N291 --> N239
  N874 --> N449
  N823 --> N322
  N708 --> N247
  N344 --> N64
  N725 --> N303
  N652 --> N689
  N601 --> N602
  N418 --> N178
  N521 --> N176
  N671 --> N319
  N367 --> N139
  N336 --> N233
  N610 --> N539
  N579 -. fd_ready .-> N19
  N762 --> N214
  N695 --> N178
  N494 --> N195
  N569 --> N178
  N285 --> N284
  N485 --> N484
  N811 --> N321
  N748 --> N335
  N615 --> N616
  N722 --> N486
  N530 --> N176
  N645 --> N419
  N633 --> N178
  N668 --> N176
  N719 --> N348
  N294 --> N233
  N410 --> N323
  N342 --> N877
  N412 --> N176
  N346 --> N790
  N734 --> N233
  N523 --> N64
  N886 --> N582
  N640 --> N861
  N468 --> N244
  N479 --> N178
  N622 --> N618
  N702 --> N199
  N673 --> N424
  N569 --> N178
  N433 --> N442
  N627 --> N425
  N486 --> N468
  N346 --> N692
  N668 --> N353
  N701 --> N230
  N812 --> N425
  N351 --> N785
  N796 --> N214
  N516 --> N62
  N809 --> N233
  N656 --> N613
  N561 --> N303
  N671 --> N518
  N652 --> N176
  N793 --> N214
  N624 --> N144
  N730 --> N348
  N569 --> N178
  N640 --> N838
  N615 --> N178
  N744 --> N64
  N288 --> N151
  N682 --> N523
  N890 --> N891
  N334 --> N320
  N499 --> N492
  N599 --> N609
  N579 --> N161
  N339 --> N867
  N389 --> N614
  N744 --> N335
  N441 --> N178
  N864 --> N54
  N476 --> N157
  N357 --> N233
  N783 --> N595
  N568 --> N442
  N521 --> N326
  N889 --> N178
  N538 --> N178
  N657 --> N442
  N828 --> N319
  N429 --> N323
  N520 --> N176
  N749 --> N335
  N633 --> N178
  N626 --> N839
  N495 --> N176
  N564 --> N568
  N790 --> N239
  N367 --> N233
  N682 --> N176
  N497 --> N321
  N413 --> N320
  N828 --> N575
  N724 --> N244
  N812 --> N321
  N347 --> N788
  N395 --> N323
  N507 --> N233
  N681 --> N245
  N851 --> N312
  N350 --> N790
  N858 --> N425
  N522 --> N64
  N726 --> N348
  N409 --> N309
  N421 --> N613
  N412 --> N176
  N812 --> N214
  N685 --> N178
  N431 --> N145
  N311 --> N176
  N507 --> N163
  N630 --> N326
  N711 --> N447
  N706 --> N164
  N809 --> N233
  N707 --> N183
  N622 --> N214
  N505 --> N176
  N690 --> N522
  N737 --> N64
  N669 --> N64
  N676 --> N47
  N559 --> N64
  N515 --> N176
  N802 --> N178
  N784 --> N785
  N751 --> N486
  N659 --> N178
  N816 --> N538
  N708 --> N178
  N669 --> N515
  N412 --> N64
  N490 --> N324
  N474 --> N333
  N486 --> N465
  N842 --> N163
  N827 --> N176
  N472 --> N550
  N626 --> N303
  N464 --> N651
  N636 --> N233
  N857 --> N326
  N732 --> N348
  N520 --> N321
  N343 --> N335
  N837 --> N83
  N575 --> N320
  N652 --> N178
  N456 --> N178
  N324 --> N327
  N450 --> N442
  N491 -. fd_ready .-> N21
  N521 --> N64
  N555 --> N441
  N456 --> N750
  N507 --> N214
  N530 --> N433
  N643 --> N419
  N375 --> N176
  N491 -. fd_ready .-> N22
  N784 --> N321
  N413 --> N326
  N747 --> N303
  N569 -. fd_ready .-> N267
  N793 --> N303
  N702 --> N239
  N633 --> N644
  N862 --> N246
  N622 --> N163
  N521 -. fd_ready .-> N892
  N559 --> N425
  N889 --> N68
  N558 --> N139
  N456 --> N444
  N507 --> N163
  N631 --> N520
  N521 --> N176
  N725 --> N490
  N583 --> N239
  N315 --> N283
  N853 --> N178
  N382 --> N303
  N486 --> N117
  N456 --> N740
  N397 --> N285
  N872 --> N439
  N752 --> N335
  N773 --> N139
  N784 --> N785
  N882 --> N176
  N793 --> N64
  N599 --> N605
  N828 --> N576
  N496 --> N867
  N792 --> N303
  N475 --> N470
  N399 --> N658
  N574 --> N323
  N842 --> N214
  N616 --> N239
  N521 --> N319
  N436 --> N790
  N669 --> N319
  N784 --> N786
  N826 --> N635
  N497 --> N786
  N816 --> N178
  N828 --> N680
  N292 --> N379
  N496 --> N785
  N733 --> N335
  N287 --> N233
  N615 --> N617
  N569 --> N176
  N741 --> N486
  N428 --> N432
  N717 --> N348
  N396 --> N397
  N722 --> N163
  N332 -. fd_ready .-> N279
  N413 --> N869
  N346 --> N791
  N750 --> N348
  N647 --> N178
  N632 --> N682
  N844 --> N64
  N662 --> N668
  N442 --> N176
  N683 --> N319
  N624 --> N537
  N481 --> N651
  N427 --> N431
  N367 --> N366
  N597 --> N239
  N571 --> N178
  N851 --> N176
  N610 --> N176
  N778 --> N239
  N416 --> N203
  N418 --> N178
  N668 --> N171
  N447 --> N303
  N587 --> N178
  N467 --> N831
  N497 --> N73
  N598 --> N588
  N624 --> N174
  N489 --> N319
  N791 --> N239
  N869 --> N649
  N745 --> N64
  N690 --> N176
  N330 --> N176
  N473 --> N133
  N881 --> N675
  N569 --> N425
  N804 --> N214
  N486 --> N464
  N750 --> N486
  N486 --> N482
  N579 -. fd_ready .-> N19
  N555 --> N685
  N615 --> N64
  N490 --> N303
  N702 --> N221
  N601 --> N586
  N652 --> N214
  N555 --> N62
  N436 --> N319
  N628 --> N64
  N486 --> N454
  N736 --> N64
  N572 --> N320
  N624 --> N104
  N568 --> N178
  N494 --> N195
  N523 --> N176
  N497 --> N303
  N479 --> N178
  N611 --> N178
  N623 --> N125
  N352 --> N701
  N438 --> N323
  N667 --> N178
  N613 --> N165
  N494 --> N195
  N641 --> N178
  N579 -. fd_ready .-> N7
  N645 --> N178
  N687 --> N176
  N578 --> N176
  N486 --> N481
  N627 --> N523
  N728 --> N486
  N870 --> N178
  N311 --> N176
  N681 --> N325
  N827 --> N236
  N639 --> N176
  N811 --> N518
  N752 --> N486
  N289 --> N151
  N592 --> N139
  N690 --> N442
  N503 --> N90
  N543 --> N425
  N486 --> N42
  N874 --> N766
  N829 --> N167
  N833 --> N168
  N707 --> N312
  N596 --> N534
  N772 --> N178
  N784 --> N321
  N566 --> N791
  N346 --> N326
  N350 --> N239
  N628 --> N630
  N792 --> N300
  N291 --> N239
  N564 --> N791
  N748 --> N176
  N617 --> N622
  N806 --> N70
  N792 --> N100
  N507 --> N158
  N802 --> N45
  N828 --> N334
  N885 --> N676
  N461 --> N500
  N614 --> N165
  N467 --> N143
  N672 --> N178
  N761 --> N501
  N530 --> N176
  N749 --> N486
  N878 --> N509
  N850 --> N538
  N739 --> N348
  N622 --> N100
  N592 --> N178
  N643 --> N64
  N640 --> N303
  N812 --> N518
  N571 --> N441
  N775 --> N78
  N491 -. fd_ready .-> N23
  N838 --> N141
  N628 --> N64
  N509 -. fd_ready .-> N2
  N807 --> N178
  N624 --> N64
  N820 --> N64
  N348 --> N791
  N480 --> N178
  N660 --> N323
  N448 --> N425
  N336 --> N163
  N557 --> N626
  N737 --> N348
  N497 --> N246
  N350 --> N788
  N677 --> N233
  N413 --> N295
  N516 --> N178
  N660 --> N515
  N851 --> N444
  N658 --> N663
  N841 --> N239
  N449 --> N182
  N496 --> N303
  N746 --> N312
  N448 --> N64
  N413 --> N788
  N676 --> N165
  N289 --> N288
  N787 --> N239
  N474 --> N178
  N636 --> N176
  N499 -. fd_ready .-> N10
  N324 --> N321
  N521 --> N198
  N702 --> N239
  N305 --> N363
  N397 --> N321
  N428 --> N323
  N525 --> N214
  N747 --> N306
  N581 --> N178
  N812 --> N613
  N678 --> N663
  N820 --> N451
  N828 --> N434
  N478 --> N143
  N521 --> N64
  N463 --> N484
  N879 --> N611
  N493 --> N163
  N384 --> N316
  N394 --> N396
  N430 --> N142
  N289 --> N151
  N809 --> N233
  N370 --> N365
  N332 --> N303
  N569 --> N176
  N479 --> N178
  N507 --> N312
  N835 --> N197
  N636 --> N178
  N448 --> N64
  N772 --> N214
  N378 --> N214
  N639 --> N442
  N352 --> N706
  N290 --> N179
  N808 --> N163
  N410 --> N324
  N497 --> N786
  N412 --> N64
  N282 -. fd_ready .-> N3
  N469 --> N312
  N804 --> N105
  N700 --> N513
  N861 --> N862
  N850 --> N441
  N615 --> N836
  N805 --> N81
  N499 --> N176
  N538 --> N74
  N652 --> N178
  N493 --> N312
  N700 --> N533
  N851 --> N176
  N876 --> N178
  N860 --> N633
  N311 --> N176
  N369 --> N151
  N616 --> N109
  N624 --> N64
  N641 --> N165
  N521 --> N176
  N874 --> N538
  N610 --> N64
  N660 --> N176
  N761 --> N214
  N786 --> N200
  N502 --> N64
  N592 --> N64
  N521 --> N176
  N643 --> N524
  N882 --> N47
  N360 --> N176
  N523 --> N321
  N474 --> N303
  N640 --> N178
  N846 --> N598
  N751 --> N348
  N452 --> N660
  N874 --> N62
  N490 --> N438
  N413 --> N790
  N473 --> N303
  N434 --> N319
  N636 --> N170
  N437 -. fd_ready .-> N11
  N614 --> N210
  N740 --> N486
  N458 -. fd_ready .-> N253
  N359 --> N163
  N658 --> N213
  N495 --> N788
  N470 --> N75
  N614 --> N425
  N533 --> N176
  N827 --> N64
  N555 --> N684
  N709 --> N441
  N684 --> N178
  N844 --> N176
  N692 --> N430
  N713 --> N67
  N413 --> N323
  N575 --> N326
  N828 --> N573
  N450 --> N442
  N787 --> N106
  N426 --> N178
  N499 --> N790
  N426 --> N64
  N632 --> N425
  N490 --> N790
  N882 --> N165
  N640 --> N178
  N617 --> N624
  N622 --> N233
  N674 --> N366
  N432 --> N178
  N390 --> N343
  N616 --> N220
  N667 --> N233
  N434 --> N315
  N781 --> N96
  N336 --> N312
  N589 --> N239
  N759 --> N791
  N408 --> N309
  N681 --> N326
  N392 --> N641
  N737 --> N335
  N291 --> N837
  N437 -. fd_ready .-> N14
  N670 --> N233
  N623 --> N122
  N507 --> N303
  N461 --> N483
  N298 --> N64
  N521 --> N176
  N619 --> N96
  N681 --> N239
  N482 --> N178
  N452 --> N326
  N609 --> N139
  N362 --> N774
  N303 --> N178
  N784 --> N558
  N799 --> N224
  N358 --> N303
  N640 --> N442
  N804 --> N163
  N498 --> N788
  N375 --> N303
  N671 --> N320
  N576 --> N323
  N555 --> N684
  N544 --> N64
  N371 --> N365
  N779 --> N178
  N441 --> N178
  N428 --> N326
  N418 --> N102
  N677 --> N214
  N671 --> N323
  N522 --> N319
  N593 --> N178
  N859 --> N425
  N630 --> N320
  N568 --> N500
  N812 --> N425
  N371 --> N365
  N397 --> N326
  N285 -. fd_ready .-> N3
  N690 --> N64
  N288 --> N214
  N809 --> N139
  N636 --> N139
  N773 --> N153
  N592 --> N178
  N801 --> N796
  N610 --> N444
  N893 -. fd_ready .-> N457
  N893 -. fd_ready .-> N501
  N893 -. fd_ready .-> N505
  N893 -. fd_ready .-> N318
  N893 -. fd_ready .-> N330
  N894 -. fd_ready .-> N301
  N894 -. fd_ready .-> N486
  N894 -. fd_ready .-> N503
  N894 -. fd_ready .-> N506
  N894 -. fd_ready .-> N328
  N894 -. fd_ready .-> N331
  N892 -. fd_ready .-> N429
  N892 -. fd_ready .-> N458
  N892 -. fd_ready .-> N548
  N892 -. fd_ready .-> N578
  N892 -. fd_ready .-> N587
  N892 -. fd_ready .-> N632
  N892 -. fd_ready .-> N662
  N892 -. fd_ready .-> N587
  N892 -. fd_ready .-> N587
  N892 -. fd_ready .-> N587
  N892 -. fd_ready .-> N587
```

## 关键调用链

- `uv_run -> uv__run_timers -> uv__queue_remove` (leaf)
- `uv_run -> uv__run_timers -> uv__queue_init` (leaf)
- `uv_run -> uv__run_timers -> uv__queue_init` (leaf)
- `uv_run -> uv__run_timers -> heap_min` (leaf)
- `uv_run -> uv__run_timers -> timer_heap` (leaf)
- `uv_run -> uv__run_timers -> uv_timer_again -> uv_timer_stop -> timer_heap` (leaf)
- `uv_run -> uv__run_timers -> uv_timer_again -> uv_timer_stop -> heap_remove -> heap_node_swap` (leaf)
- `uv_run -> uv__run_timers -> uv_timer_again -> uv_timer_stop -> heap_remove -> less_than` (leaf)
- `uv_run -> uv__run_timers -> uv_timer_again -> uv_timer_stop -> heap_remove -> less_than` (leaf)
- `uv_run -> uv__run_timers -> uv_timer_again -> uv_timer_stop -> heap_remove -> heap_node_swap` (leaf)

## 自然语言分析

# 自然语言分析

## 模块架构
仓库由 core、external (系统与第三方调用)、include、src、unix、uv 组成。入口负责初始化运行时、注册回调并驱动主循环；事件循环组件负责等待就绪事件、遍历句柄并分发回调。

## 关键调用链
入口 `uv_run` 的关键路径是：`uv_run -> uv__io_poll`。

## 异步回调链
fd_ready 事件在 third_party/libuv/src/heap-inl.h:222 触发回调，但候选为空，需要进一步分析。

## 函数指针
静态分析发现回调字段存在多个候选：`uv__async_io、uv__cancelled、uv__fs_done、uv__fs_event、uv__fs_work、uv__getaddrinfo_done、uv__getaddrinfo_work、uv__getnameinfo_done、uv__getnameinfo_work、uv__poll_io、uv__queue_done、uv__queue_work、uv__random_done、uv__random_work、uv__server_io、uv__signal_event、uv__stream_io、uv__udp_io`，无法唯一确定目标，置信度为 0.30。

## 复杂宏
本次分析覆盖：ACCESS_ONCE (third_party/libuv/test/benchmark-async-pummel.c:29)、ARRAY_END (third_party/libuv/src/uv-common.h:55)、ARRAY_SIZE (third_party/libuv/src/uv-common.h:54)、EV_OOBAND (third_party/libuv/src/unix/kqueue.c:48)、F_OK (third_party/libuv/include/uv/win.h:659)、INIT (third_party/libuv/src/unix/fs.c:90)、UV_EXTERN (third_party/libuv/include/uv.h:39)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 59%，报告状态为 not ready；所有结论均引用源码文件、行号和原始代码片段。

## 异步回调链

- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/poll.c:64` -> `third_party/libuv/src/unix/poll.c:64` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/async.c:208` -> `third_party/libuv/src/unix/async.c:208` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:463` -> `third_party/libuv/src/unix/fsevents.c:463` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/random.c:116` -> `third_party/libuv/src/threadpool.c:330` -> callbacks: uv__fs_done, uv__getaddrinfo_done, uv__getnameinfo_done, uv__queue_done, uv__random_done
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:299` -> `third_party/libuv/src/threadpool.c:123` -> callbacks: uv__cancelled, uv__fs_work, uv__getaddrinfo_work, uv__getnameinfo_work, uv__queue_work, uv__random_work
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:1778` -> `third_party/libuv/src/unix/fs.c:1778` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:461` -> `third_party/libuv/src/unix/stream.c:461` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:269` -> `third_party/libuv/src/unix/udp.c:269` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:125` -> `third_party/libuv/src/unix/udp.c:125` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/poll.c:50` -> `third_party/libuv/src/unix/poll.c:50` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:927` -> `third_party/libuv/src/unix/stream.c:927` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:206` -> `third_party/libuv/src/unix/udp.c:206` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:146` -> `third_party/libuv/src/unix/darwin-proctitle.c:146` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:393` -> `third_party/libuv/src/unix/fsevents.c:393` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:622` -> `third_party/libuv/src/unix/fsevents.c:622` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:365` -> `third_party/libuv/src/threadpool.c:365` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:938` -> `third_party/libuv/src/unix/stream.c:938` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:195` -> `third_party/libuv/src/unix/udp.c:195` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:371` -> `third_party/libuv/src/unix/fsevents.c:371` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:271` -> `third_party/libuv/src/unix/udp.c:271` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/core.c:854` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:215` -> `third_party/libuv/src/unix/udp.c:215` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:159` -> `third_party/libuv/src/unix/darwin-proctitle.c:159` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/getaddrinfo.c:134` -> `third_party/libuv/src/unix/getaddrinfo.c:134` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:93` -> `third_party/libuv/src/uv-common.c:93` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:77` -> `third_party/libuv/src/uv-common.c:77` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:494` -> `third_party/libuv/src/unix/fs.c:494` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:224` -> `third_party/libuv/src/heap-inl.h:224` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:241` -> `third_party/libuv/src/unix/udp.c:241` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:372` -> `third_party/libuv/src/unix/fsevents.c:372` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:278` -> `third_party/libuv/src/unix/udp.c:278` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:698` -> `third_party/libuv/src/unix/fsevents.c:698` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/signal.c:478` -> `third_party/libuv/src/unix/signal.c:478` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:188` -> `third_party/libuv/src/unix/fsevents.c:188` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:782` -> `third_party/libuv/src/unix/fsevents.c:782` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/process.c:174` -> `third_party/libuv/src/unix/process.c:174` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:189` -> `third_party/libuv/src/unix/fsevents.c:189` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:130` -> `third_party/libuv/src/unix/darwin-proctitle.c:130` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:476` -> `third_party/libuv/src/unix/fsevents.c:476` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:352` -> `third_party/libuv/src/threadpool.c:352` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/random-getentropy.c:53` -> `third_party/libuv/src/unix/random-getentropy.c:53` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/core.c:363` -> `third_party/libuv/src/unix/core.c:363` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:197` -> `third_party/libuv/src/unix/udp.c:197` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:88` -> `third_party/libuv/src/uv-common.c:88` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/process.c:552` -> `third_party/libuv/src/unix/process.c:552` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:149` -> `third_party/libuv/src/unix/darwin-proctitle.c:149` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/fs-poll.c:202` -> `third_party/libuv/src/fs-poll.c:202` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:66` -> `third_party/libuv/src/unix/loop-watcher.c:66` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:720` -> `third_party/libuv/src/unix/fsevents.c:720` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/random.c:90` -> `third_party/libuv/src/random.c:90` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:68` -> `third_party/libuv/src/unix/loop-watcher.c:68` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:329` -> `third_party/libuv/src/unix/fs.c:329` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:568` -> `third_party/libuv/src/uv-common.c:568` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/getnameinfo.c:73` -> `third_party/libuv/src/unix/getnameinfo.c:73` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:894` -> `third_party/libuv/src/unix/fsevents.c:894` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1283` -> `third_party/libuv/src/unix/stream.c:1283` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:379` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/random-getentropy.c:50` -> `third_party/libuv/src/unix/random-getentropy.c:50` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:235` -> `third_party/libuv/src/heap-inl.h:235` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:138` -> `third_party/libuv/src/unix/darwin-proctitle.c:138` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1052` -> `third_party/libuv/src/unix/stream.c:1052` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:657` -> `third_party/libuv/src/unix/stream.c:657` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1055` -> `third_party/libuv/src/unix/stream.c:1055` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:110` -> `third_party/libuv/src/unix/darwin-proctitle.c:110` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:243` -> `third_party/libuv/src/unix/udp.c:243` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:128` -> `third_party/libuv/src/unix/darwin-proctitle.c:128` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:443` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:451` -> `third_party/libuv/src/unix/fsevents.c:451` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1092` -> `third_party/libuv/src/unix/stream.c:1092` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:109` -> `third_party/libuv/src/unix/darwin-proctitle.c:109` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:389` -> `third_party/libuv/src/unix/fsevents.c:389` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/fs-poll.c:215` -> `third_party/libuv/src/fs-poll.c:215` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:102` -> `third_party/libuv/src/unix/darwin-proctitle.c:102` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:156` -> `third_party/libuv/src/unix/darwin-proctitle.c:156` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:528` -> `third_party/libuv/src/unix/stream.c:528` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:67` -> `third_party/libuv/src/unix/loop-watcher.c:67` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:123` -> `third_party/libuv/src/unix/udp.c:123` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:781` -> `third_party/libuv/src/unix/fsevents.c:781` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/timer.c:193` -> `third_party/libuv/src/timer.c:193` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:711` -> `third_party/libuv/src/unix/fsevents.c:711` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:115` -> `third_party/libuv/src/unix/darwin-proctitle.c:115` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1120` -> `third_party/libuv/src/unix/stream.c:1120` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:143` -> `third_party/libuv/src/unix/darwin-proctitle.c:143` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1148` -> `third_party/libuv/src/unix/stream.c:1148` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:392` -> `third_party/libuv/src/unix/fsevents.c:392` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:369` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:753` -> `third_party/libuv/src/unix/fsevents.c:753` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:103` -> `third_party/libuv/src/unix/darwin-proctitle.c:103` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:362` -> `third_party/libuv/src/unix/fsevents.c:362` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:373` -> `third_party/libuv/src/unix/fsevents.c:373` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1101` -> `third_party/libuv/src/unix/stream.c:1101` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:423` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:98` -> `third_party/libuv/src/uv-common.c:98` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:116` -> `third_party/libuv/src/unix/darwin-proctitle.c:116` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:136` -> `third_party/libuv/src/unix/darwin-proctitle.c:136` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:374` -> `third_party/libuv/src/unix/fsevents.c:374` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/core.c:1815` -> `third_party/libuv/src/unix/core.c:1815` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:480` -> `third_party/libuv/src/unix/fsevents.c:480` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:146` -> `third_party/libuv/src/heap-inl.h:146` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:713` -> `third_party/libuv/src/unix/fsevents.c:713` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/kqueue.c:545` -> `third_party/libuv/src/unix/kqueue.c:545` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:719` -> `third_party/libuv/src/unix/fsevents.c:719` -> callbacks: none
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:222` -> `third_party/libuv/src/heap-inl.h:222` -> callbacks: none
  - Confidence: 0.30, loop back: True

## 函数指针候选

- `uv_poll_s::poll_cb` @ `third_party/libuv/src/unix/poll.c:64`
  - Candidates: none
  - Confidence: 0.30
- `uv_async_s::async_cb` @ `third_party/libuv/src/unix/async.c:208`
  - Candidates: none
  - Confidence: 0.30
- `pCFArrayCreate` @ `third_party/libuv/src/unix/fsevents.c:463`
  - Candidates: none
  - Confidence: 0.30
- `uv__work::done` @ `third_party/libuv/src/threadpool.c:330`
  - Candidates: `uv__fs_done` (third_party/libuv/src/unix/fs.c:1767), `uv__getaddrinfo_done` (third_party/libuv/src/unix/getaddrinfo.c:108), `uv__getnameinfo_done` (third_party/libuv/src/unix/getnameinfo.c:55), `uv__queue_done` (third_party/libuv/src/threadpool.c:356), `uv__random_done` (third_party/libuv/src/random.c:81)
  - Confidence: 0.60
- `uv__work::work` @ `third_party/libuv/src/threadpool.c:123`
  - Candidates: `uv__cancelled` (third_party/libuv/src/threadpool.c:49), `uv__fs_work` (third_party/libuv/src/unix/fs.c:1695), `uv__getaddrinfo_work` (third_party/libuv/src/unix/getaddrinfo.c:98), `uv__getnameinfo_work` (third_party/libuv/src/unix/getnameinfo.c:31), `uv__queue_work` (third_party/libuv/src/threadpool.c:349), `uv__random_work` (third_party/libuv/src/random.c:73)
  - Confidence: 0.60
- `uv_fs_s::cb` @ `third_party/libuv/src/unix/fs.c:1778`
  - Candidates: none
  - Confidence: 0.30
- `uv_connect_s::cb` @ `third_party/libuv/src/unix/stream.c:461`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:269`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_send_s::send_cb` @ `third_party/libuv/src/unix/udp.c:125`
  - Candidates: none
  - Confidence: 0.30
- `uv_poll_s::poll_cb` @ `third_party/libuv/src/unix/poll.c:50`
  - Candidates: none
  - Confidence: 0.30
- `uv_write_s::cb` @ `third_party/libuv/src/unix/stream.c:927`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:206`
  - Candidates: none
  - Confidence: 0.30
- `pLSApplicationCheckIn` @ `third_party/libuv/src/unix/darwin-proctitle.c:146`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:96`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamRelease` @ `third_party/libuv/src/unix/fsevents.c:393`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopSourceCreate` @ `third_party/libuv/src/unix/fsevents.c:622`
  - Candidates: none
  - Confidence: 0.30
- `uv_work_s::after_work_cb` @ `third_party/libuv/src/threadpool.c:365`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:938`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetInfoDictionary` @ `third_party/libuv/src/unix/darwin-proctitle.c:147`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:195`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamScheduleWithRunLoop` @ `third_party/libuv/src/unix/fsevents.c:371`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:271`
  - Candidates: none
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/core.c:854`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:215`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:159`
  - Candidates: none
  - Confidence: 0.30
- `uv_getaddrinfo_s::cb` @ `third_party/libuv/src/unix/getaddrinfo.c:134`
  - Candidates: none
  - Confidence: 0.30
- `uv__allocator_t::local_calloc` @ `third_party/libuv/src/uv-common.c:93`
  - Candidates: none
  - Confidence: 0.30
- `uv__allocator_t::local_malloc` @ `third_party/libuv/src/uv-common.c:77`
  - Candidates: none
  - Confidence: 0.30
- `f` @ `third_party/libuv/src/unix/fs.c:494`
  - Candidates: none
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:224`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::alloc_cb` @ `third_party/libuv/src/unix/udp.c:241`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamStart` @ `third_party/libuv/src/unix/fsevents.c:372`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:278`
  - Candidates: none
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:698`
  - Candidates: none
  - Confidence: 0.30
- `uv_signal_s::signal_cb` @ `third_party/libuv/src/unix/signal.c:478`
  - Candidates: none
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:188`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopWakeUp` @ `third_party/libuv/src/unix/fsevents.c:782`
  - Candidates: none
  - Confidence: 0.30
- `uv_process_s::exit_cb` @ `third_party/libuv/src/unix/process.c:174`
  - Candidates: none
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:189`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:130`
  - Candidates: none
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:476`
  - Candidates: none
  - Confidence: 0.30
- `uv_work_s::work_cb` @ `third_party/libuv/src/threadpool.c:352`
  - Candidates: none
  - Confidence: 0.30
- `uv__getentropy` @ `third_party/libuv/src/unix/random-getentropy.c:53`
  - Candidates: none
  - Confidence: 0.30
- `uv_handle_s::close_cb` @ `third_party/libuv/src/unix/core.c:363`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:197`
  - Candidates: none
  - Confidence: 0.30
- `uv__allocator_t::local_free` @ `third_party/libuv/src/uv-common.c:88`
  - Candidates: none
  - Confidence: 0.30
- `uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np` @ `third_party/libuv/src/unix/process.c:552`
  - Candidates: none
  - Confidence: 0.30
- `pLSGetCurrentApplicationASN` @ `third_party/libuv/src/unix/darwin-proctitle.c:149`
  - Candidates: none
  - Confidence: 0.30
- `poll_ctx::poll_cb` @ `third_party/libuv/src/fs-poll.c:202`
  - Candidates: none
  - Confidence: 0.30
- `uv_prepare_s::prepare_cb` @ `third_party/libuv/src/unix/loop-watcher.c:66`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopRemoveSource` @ `third_party/libuv/src/unix/fsevents.c:720`
  - Candidates: none
  - Confidence: 0.30
- `uv_random_s::cb` @ `third_party/libuv/src/random.c:90`
  - Candidates: none
  - Confidence: 0.30
- `uv_idle_s::idle_cb` @ `third_party/libuv/src/unix/loop-watcher.c:68`
  - Candidates: none
  - Confidence: 0.30
- `uv__mkostemp` @ `third_party/libuv/src/unix/fs.c:329`
  - Candidates: none
  - Confidence: 0.30
- `walk_cb` @ `third_party/libuv/src/uv-common.c:568`
  - Candidates: none
  - Confidence: 0.30
- `uv_getnameinfo_s::getnameinfo_cb` @ `third_party/libuv/src/unix/getnameinfo.c:73`
  - Candidates: none
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:894`
  - Candidates: none
  - Confidence: 0.30
- `uv_connect_s::cb` @ `third_party/libuv/src/unix/stream.c:1283`
  - Candidates: none
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:379`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv__getentropy` @ `third_party/libuv/src/unix/random-getentropy.c:50`
  - Candidates: none
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:235`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetBundleWithIdentifier` @ `third_party/libuv/src/unix/darwin-proctitle.c:96`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:138`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::alloc_cb` @ `third_party/libuv/src/unix/stream.c:1052`
  - Candidates: none
  - Confidence: 0.30
- `uv_shutdown_s::cb` @ `third_party/libuv/src/unix/stream.c:657`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1055`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:110`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:243`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:128`
  - Candidates: none
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:443`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `pCFStringCreateWithFileSystemRepresentation` @ `third_party/libuv/src/unix/fsevents.c:451`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1092`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:109`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamStop` @ `third_party/libuv/src/unix/fsevents.c:389`
  - Candidates: none
  - Confidence: 0.30
- `poll_ctx::poll_cb` @ `third_party/libuv/src/fs-poll.c:215`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:102`
  - Candidates: none
  - Confidence: 0.30
- `pLSSetApplicationInformationItem` @ `third_party/libuv/src/unix/darwin-proctitle.c:156`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::connection_cb` @ `third_party/libuv/src/unix/stream.c:528`
  - Candidates: none
  - Confidence: 0.30
- `uv_check_s::check_cb` @ `third_party/libuv/src/unix/loop-watcher.c:67`
  - Candidates: none
  - Confidence: 0.30
- `uv_udp_send_s::send_cb` @ `third_party/libuv/src/unix/udp.c:123`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopSourceSignal` @ `third_party/libuv/src/unix/fsevents.c:781`
  - Candidates: none
  - Confidence: 0.30
- `uv_timer_s::timer_cb` @ `third_party/libuv/src/timer.c:193`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopGetCurrent` @ `third_party/libuv/src/unix/fsevents.c:711`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetDataPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:115`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1120`
  - Candidates: none
  - Confidence: 0.30
- `pLSSetApplicationLaunchServicesServerConnectionStatus` @ `third_party/libuv/src/unix/darwin-proctitle.c:143`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetMainBundle` @ `third_party/libuv/src/unix/darwin-proctitle.c:147`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1148`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamInvalidate` @ `third_party/libuv/src/unix/fsevents.c:392`
  - Candidates: none
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:369`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `pCFRunLoopStop` @ `third_party/libuv/src/unix/fsevents.c:753`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:103`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamCreate` @ `third_party/libuv/src/unix/fsevents.c:362`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamInvalidate` @ `third_party/libuv/src/unix/fsevents.c:373`
  - Candidates: none
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1101`
  - Candidates: none
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:423`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv__allocator_t::local_realloc` @ `third_party/libuv/src/uv-common.c:98`
  - Candidates: none
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:116`
  - Candidates: none
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:136`
  - Candidates: none
  - Confidence: 0.30
- `pFSEventStreamRelease` @ `third_party/libuv/src/unix/fsevents.c:374`
  - Candidates: none
  - Confidence: 0.30
- `func` @ `third_party/libuv/src/unix/core.c:1815`
  - Candidates: none
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:480`
  - Candidates: none
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:146`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopAddSource` @ `third_party/libuv/src/unix/fsevents.c:713`
  - Candidates: none
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/kqueue.c:545`
  - Candidates: none
  - Confidence: 0.30
- `pCFRunLoopRun` @ `third_party/libuv/src/unix/fsevents.c:719`
  - Candidates: none
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:222`
  - Candidates: none
  - Confidence: 0.30

## 宏分析

| macro | file:line | definition | call sites |
| --- | --- | --- | --- |

## Evidence

| id | kind | file:line | snippet |
| --- | --- | --- | --- |
| `ev_000b23142dc4` | call_site | `third_party/libuv/src/idna.c:202` | `assert(c != UINT_MAX);` |
| `ev_0099a80275c3` | call_site | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_00c2485d9608` | call_site | `third_party/libuv/src/unix/core.c:919` | `assert(0 != events);` |
| `ev_00df72f55b6c` | call_site | `third_party/libuv/src/unix/stream.c:1049` | `assert(stream->alloc_cb != NULL);` |
| `ev_00e9ac8a4910` | call_site | `third_party/libuv/src/unix/core.c:982` | `uv__platform_invalidate_fd(loop, w->fd);` |
| `ev_00f2122909b4` | call_site | `third_party/libuv/src/unix/udp.c:71` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_00f7eb56e9b1` | call_site | `third_party/libuv/src/unix/signal.c:549` | `uv__signal_block_and_lock(&saved_sigmask);` |
| `ev_01159db36d01` | call_site | `third_party/libuv/src/unix/loop.c:37` | `memset(loop, 0, sizeof(*loop));` |
| `ev_01191424f420` | call_site | `third_party/libuv/src/unix/async.c:395` | `uv__close(loop->async_io_watcher.fd);` |
| `ev_012033a59c71` | call_site | `third_party/libuv/src/unix/core.c:207` | `uv__fs_event_close((uv_fs_event_t*)handle);` |
| `ev_014226a28fb1` | call_site | `third_party/libuv/src/idna.c:252` | `assert(c != UINT_MAX);` |
| `ev_0146c582c419` | call_site | `third_party/libuv/src/unix/signal.c:304` | `return uv__signal_loop_once_init(loop);` |
| `ev_015e590b91ce` | call_site | `third_party/libuv/src/unix/stream.c:999` | `assert(count % sizeof(fd) == 0);` |
| `ev_01aff5894276` | call_site | `third_party/libuv/src/unix/kqueue.c:648` | `uv__io_close(handle->loop, &handle->event_watcher);` |
| `ev_01d3a88243c6` | call_site | `third_party/libuv/src/unix/pipe.c:464` | `r = uv_pipe_getsockname(handle, name_buffer, &name_len);` |
| `ev_01e85e2afc3f` | call_site | `third_party/libuv/src/unix/core.c:1300` | `pwd->username = uv__malloc(name_size + homedir_size + shell_size);` |
| `ev_01f147aabaa1` | call_site | `third_party/libuv/src/unix/core.c:921` | `assert(w->fd < INT_MAX);` |
| `ev_020ff09db377` | call_site | `third_party/libuv/src/unix/udp.c:698` | `return UV__ERR(errno);` |
| `ev_02531d0740c8` | call_site | `third_party/libuv/src/unix/tcp.c:626` | `uv__stream_close((uv_stream_t*)handle);` |
| `ev_0279a97cd469` | call_site | `third_party/libuv/src/unix/fs.c:324` | `uv_once(&once, uv__mkostemp_initonce);` |
| `ev_027d7b7b1f88` | call_site | `third_party/libuv/src/unix/kqueue.c:297` | `assert(timeout != -1);` |
| `ev_027dfc586c9e` | call_site | `third_party/libuv/src/unix/tty.c:91` | `result = ioctl(fd, TIOCPTYGNAME, &dummy) != 0;` |
| `ev_02965414d861` | call_site | `third_party/libuv/src/unix/thread.c:349` | `err = pthread_mutex_init(mutex, &attr);` |
| `ev_02985e12ffba` | call_site | `third_party/libuv/src/unix/udp.c:618` | `if (!uv__queue_empty(&handle->write_queue))` |
| `ev_02b7456f70d9` | call_site | `third_party/libuv/src/unix/random-getentropy.c:50` | `if (uv__getentropy((char *) buf + pos, stride))` |
| `ev_02c74b2207ca` | call_site | `third_party/libuv/src/heap-inl.h:240` | `heap_remove(heap, heap->min, less_than);` |
| `ev_02ea4b5938e9` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_02f4d997a1db` | call_site | `third_party/libuv/src/unix/core.c:994` | `assert(0 != events);` |
| `ev_030814a4f4a5` | call_site | `third_party/libuv/src/unix/process.c:395` | `abort();` |
| `ev_0314cf1dc8db` | call_site | `third_party/libuv/src/unix/fs.c:781` | `uv__free(buf);` |
| `ev_033bc133d3cf` | call_site | `third_party/libuv/src/uv-common.c:87` | `saved_errno = errno;` |
| `ev_035fa2815964` | call_site | `third_party/libuv/src/unix/stream.c:630` | `assert(uv__queue_empty(&stream->write_queue));` |
| `ev_0364e38a089a` | call_site | `third_party/libuv/src/unix/kqueue.c:624` | `uv__io_init(&handle->event_watcher, uv__fs_event, fd);` |
| `ev_036f33a2ad9c` | call_site | `third_party/libuv/src/unix/stream.c:1060` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_03874c5ae3f7` | call_site | `third_party/libuv/src/unix/async.c:301` | `err = uv__make_pipe(pipefd, UV_NONBLOCK_PIPE);` |
| `ev_03906ae61fe0` | call_site | `third_party/libuv/src/unix/stream.c:855` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_0393d9427046` | call_site | `third_party/libuv/src/unix/stream.c:1200` | `uv__stream_connect(stream);` |
| `ev_03dfa2cb8984` | call_site | `third_party/libuv/src/unix/process.c:581` | `assert(err != ENOSYS);` |
| `ev_03e34d02d472` | call_site | `third_party/libuv/src/unix/stream.c:997` | `assert(cmsg->cmsg_len >= CMSG_LEN(0));` |
| `ev_03fc299c658d` | call_site | `third_party/libuv/src/unix/process.c:933` | `while (err == -1 && errno == EINTR);` |
| `ev_04087c5005c8` | call_site | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_0408a0462534` | call_site | `third_party/libuv/src/unix/pipe.c:57` | `return uv_pipe_bind2(handle, name, strlen(name), 0);` |
| `ev_0427e78eb346` | call_site | `third_party/libuv/src/unix/core.c:1322` | `uv__free(buf);` |
| `ev_042b369b6a2c` | call_site | `third_party/libuv/src/unix/process.c:792` | `err = uv__spawn_resolve_and_spawn(options, &attrs, &actions, pid);` |
| `ev_04333cafe1e7` | call_site | `third_party/libuv/src/unix/core.c:776` | `*size = strlen(buffer);` |
| `ev_043a1f8589cf` | call_site | `third_party/libuv/src/threadpool.c:125` | `uv_mutex_lock(&w->loop->wq_mutex);` |
| `ev_0448c388a5ad` | call_site | `third_party/libuv/src/unix/core.c:1356` | `r = getgrgid_r(gid, &gp, buf, bufsize, &result);` |
| `ev_0465118eabf7` | call_site | `third_party/libuv/src/unix/fsevents.c:544` | `V(core_foundation_handle, CFRunLoopAddSource);` |
| `ev_048840dd2d4c` | call_site | `third_party/libuv/src/unix/udp.c:608` | `uv__queue_insert_tail(&handle->write_queue, &req->queue);` |
| `ev_04b38854c433` | call_site | `third_party/libuv/src/unix/stream.c:444` | `q = uv__queue_head(&stream->write_queue);` |
| `ev_04f9e46838a6` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_051b2ccc6da3` | call_site | `third_party/libuv/src/unix/process.c:1069` | `uv__close_nocheckstdio(pipes[i][0]);` |
| `ev_052fa201b701` | call_site | `third_party/libuv/src/unix/udp.c:80` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_054f9c48d7bf` | call_site | `third_party/libuv/src/unix/udp.c:647` | `assert(handle->flags & UV_HANDLE_UDP_CONNECTED);` |
| `ev_0577f6d20c2e` | call_site | `third_party/libuv/src/unix/thread.c:174` | `abort();` |
| `ev_0599dac89e4b` | call_site | `third_party/libuv/src/unix/udp.c:249` | `nread = uv__udp_recvmmsg(handle, &buf);` |
| `ev_05db920f945a` | call_site | `third_party/libuv/src/unix/stream.c:1393` | `assert(!(stream->flags & UV_HANDLE_BLOCKING_WRITES));` |
| `ev_05fa39cb8e53` | call_site | `third_party/libuv/src/unix/stream.c:806` | `memcpy(CMSG_DATA(&cmsg.hdr), &fd_to_send, sizeof(fd_to_send));` |
| `ev_05fc0d2fa4f9` | call_site | `third_party/libuv/src/unix/core.c:646` | `assert(fd > STDERR_FILENO);  /* Catch stdio close bugs. */` |
| `ev_06390490032e` | call_site | `third_party/libuv/src/unix/fsevents.c:784` | `uv_mutex_unlock(&loop->cf_mutex);` |
| `ev_069cf24160a2` | call_site | `third_party/libuv/src/unix/udp.c:1203` | `if (uv__io_active(&handle->io_watcher, POLLIN))` |
| `ev_069ecdbb3330` | call_site | `third_party/libuv/src/thread-common.c:76` | `uv_mutex_destroy(&b->mutex);` |
| `ev_06ad08d97789` | call_site | `third_party/libuv/src/unix/stream.c:411` | `assert(fd >= 0);` |
| `ev_06c512c5551c` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_06d4479a269e` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_06f62b33c793` | call_site | `third_party/libuv/src/unix/darwin.c:202` | `sysctlbyname("hw.cpufrequency", &cpuspeed, &size, NULL, 0);` |
| `ev_06fccd917d92` | call_site | `third_party/libuv/src/unix/stream.c:1417` | `return uv_try_write2(stream, bufs, nbufs, NULL);` |
| `ev_070f7f7cab78` | call_site | `third_party/libuv/src/unix/core.c:203` | `uv__process_close((uv_process_t*)handle);` |
| `ev_071e3c08967f` | call_site | `third_party/libuv/src/unix/core.c:1200` | `uv_os_free_passwd(&pwd);` |
| `ev_0727e487e343` | call_site | `third_party/libuv/src/unix/stream.c:673` | `assert(req->bufs != NULL);` |
| `ev_073780448ada` | call_site | `third_party/libuv/src/unix/core.c:1844` | `rc = nanosleep(&timeout, &timeout);` |
| `ev_0765f48cee8c` | call_site | `third_party/libuv/src/thread-common.c:146` | `uv__free(barrier->b);` |
| `ev_0771490f398d` | call_site | `third_party/libuv/src/unix/fs.c:2188` | `PATH2;` |
| `ev_0771734f76e1` | call_site | `third_party/libuv/src/unix/core.c:1298` | `homedir_size = strlen(pw.pw_dir) + 1;` |
| `ev_078c1e540b51` | call_site | `third_party/libuv/src/unix/process.c:979` | `uv__queue_init(&process->queue);` |
| `ev_078db7b024ce` | call_site | `third_party/libuv/src/uv-common.c:753` | `uv__fs_scandir_free(dents[*nbufs - 1]);` |
| `ev_07b965b1f445` | call_site | `third_party/libuv/src/unix/process.c:149` | `uv__queue_remove(&process->queue);` |
| `ev_07f77952c987` | call_site | `third_party/libuv/src/unix/async.c:81` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_ASYNC);` |
| `ev_08156833025e` | call_site | `third_party/libuv/src/uv-common.c:296` | `return uv_inet_pton(AF_INET6, ip, &addr->sin6_addr);` |
| `ev_0821a6ac16cc` | call_site | `third_party/libuv/src/thread-common.c:99` | `uv_mutex_lock(&b->mutex);` |
| `ev_08567c743fbb` | call_site | `third_party/libuv/src/unix/tcp.c:343` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_085cc41c90e4` | call_site | `third_party/libuv/src/unix/stream.c:792` | `assert(fd_to_send >= 0);` |
| `ev_085f482686dc` | call_site | `third_party/libuv/src/unix/process.c:539` | `err = posix_spawn_file_actions_init(actions);` |
| `ev_08609fc4ffe6` | call_site | `third_party/libuv/src/unix/fs.c:2302` | `PATH2;` |
| `ev_0875828abb2f` | call_site | `third_party/libuv/src/unix/process.c:1000` | `err = uv__process_init_stdio(options->stdio + i, pipes[i]);` |
| `ev_087672101eb1` | call_site | `third_party/libuv/src/unix/fsevents.c:857` | `uv__free(handle->realpath);` |
| `ev_08896b29ba51` | call_site | `third_party/libuv/src/unix/core.c:1127` | `n = read(fd, buf, len - 1);` |
| `ev_088b3589a37e` | call_site | `third_party/libuv/src/unix/fsevents.c:463` | `cf_paths = pCFArrayCreate(NULL, (const void**) paths, path_count, NULL);` |
| `ev_08973798df7c` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:104` | `req->retcode = uv__getaddrinfo_translate_error(err);` |
| `ev_08b9c1f9fe16` | call_site | `third_party/libuv/src/unix/process.c:516` | `err = posix_spawnattr_setsigmask(attrs, &signal_set);` |
| `ev_08d113fd8759` | call_site | `third_party/libuv/src/threadpool.c:180` | `if (uv_thread_join(threads + i))` |
| `ev_08d9b95f8371` | call_site | `third_party/libuv/src/unix/stream.c:450` | `uv__queue_insert_tail(&stream->write_completed_queue, &req->queue);` |
| `ev_08ebbe24d60d` | call_site | `third_party/libuv/src/threadpool.c:83` | `uv_cond_signal(&cond);` |
| `ev_08f884d423bd` | call_site | `third_party/libuv/src/unix/core.c:1873` | `return UV__ERR(errno);` |
| `ev_0914e47376ef` | call_site | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_09154c6d60e1` | call_site | `third_party/libuv/src/unix/core.c:935` | `if (uv__queue_empty(&w->watcher_queue))` |
| `ev_0926a75b183f` | call_site | `third_party/libuv/src/unix/tcp.c:440` | `if (listen(tcp->io_watcher.fd, backlog))` |
| `ev_093829324527` | call_site | `third_party/libuv/src/unix/fs.c:2279` | `uv__free(req->bufs);` |
| `ev_09788166177e` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:203` | `req->hostname = memcpy(buf + len, hostname, hostname_len);` |
| `ev_097ed80f1651` | call_site | `third_party/libuv/src/unix/udp.c:149` | `uv__udp_sendmsg(handle);` |
| `ev_0984d1f5ef5c` | call_site | `third_party/libuv/src/unix/fs.c:2214` | `PATH;` |
| `ev_09b661c71631` | call_site | `third_party/libuv/src/unix/core.c:1178` | `r = uv_os_getenv("HOME", buffer, size);` |
| `ev_09d049855a37` | call_site | `third_party/libuv/src/unix/stream.c:871` | `uv__write_req_finish(req);` |
| `ev_09d5a5629162` | call_site | `third_party/libuv/src/unix/fs.c:1268` | `err = UV__ERR(errno);` |
| `ev_09e35b70d7ff` | call_site | `third_party/libuv/src/unix/kqueue.c:442` | `uv__metrics_update_idle_time(loop);` |
| `ev_0a02e3d53aed` | call_site | `third_party/libuv/src/unix/fsevents.c:753` | `pCFRunLoopStop(state->loop);` |
| `ev_0a0bf9855264` | call_site | `third_party/libuv/src/unix/fs.c:891` | `nread = read(in_fd, buf, buflen);` |
| `ev_0a3ebcc6e0e6` | call_site | `third_party/libuv/src/unix/pipe.c:115` | `memcpy(pipe_fname, name, namelen);` |
| `ev_0a723121eb46` | call_site | `third_party/libuv/src/unix/pipe.c:152` | `if (uv__stream_fd(handle) == -1)` |
| `ev_0ab2ec3cdc18` | call_site | `third_party/libuv/src/unix/process.c:199` | `assert(container->data.stream != NULL);` |
| `ev_0ac74bc0d37b` | call_site | `third_party/libuv/src/unix/fs.c:2173` | `PATH;` |
| `ev_0acf8b5703b6` | call_site | `third_party/libuv/src/unix/core.c:1400` | `memcpy(grp->groupname, gp.gr_name, name_size);` |
| `ev_0ad168aac4b3` | call_site | `third_party/libuv/src/unix/stream.c:429` | `errno != EINVAL) {` |
| `ev_0add7b33578b` | call_site | `third_party/libuv/src/uv-common.c:660` | `return uv__socket_sockopt(handle, SO_SNDBUF, value);` |
| `ev_0ae131588cf4` | call_site | `third_party/libuv/src/unix/udp.c:374` | `err = uv__socket(addr->sa_family, SOCK_DGRAM, 0);` |
| `ev_0ae206425830` | call_site | `third_party/libuv/src/unix/core.c:477` | `uv__update_time(loop);` |
| `ev_0ae351a5ebe6` | call_site | `third_party/libuv/src/unix/core.c:906` | `assert(cb != NULL);` |
| `ev_0aed3132411a` | call_site | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_0af44505b21e` | call_site | `third_party/libuv/src/unix/thread.c:397` | `abort();` |
| `ev_0b12ee44159c` | call_site | `third_party/libuv/src/unix/fs.c:911` | `n = write(out_fd, buf + nwritten, nread - nwritten);` |
| `ev_0b13f84304fd` | call_site | `third_party/libuv/src/unix/stream.c:324` | `return UV__ERR(errno);` |
| `ev_0b21a241c66c` | call_site | `third_party/libuv/src/unix/fs.c:483` | `dlerror();  /* Clear errors. */` |
| `ev_0b32440d409b` | call_site | `third_party/libuv/src/unix/stream.c:1360` | `uv__queue_init(&req->queue);` |
| `ev_0b641cd4ba7a` | call_site | `third_party/libuv/src/unix/stream.c:846` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_0b66f2ef9447` | call_site | `third_party/libuv/src/unix/kqueue.c:107` | `return UV__ERR(errno);` |
| `ev_0b6bc55bcc21` | call_site | `third_party/libuv/src/unix/stream.c:170` | `memset(s->sread, 0, s->sread_sz);` |
| `ev_0b6d896dd956` | call_site | `third_party/libuv/src/unix/tcp.c:43` | `memset(&s, 0, sizeof(s));` |
| `ev_0b7f077ccfe8` | call_site | `third_party/libuv/src/unix/core.c:1504` | `memcpy(buffer, var, len + 1);` |
| `ev_0b850cbf1e7c` | call_site | `third_party/libuv/src/unix/fs.c:1736` | `X(READDIR, uv__fs_readdir(req));` |
| `ev_0b8777b9050a` | call_site | `third_party/libuv/src/unix/fs.c:1954` | `PATH;` |
| `ev_0ba616e1022a` | call_site | `third_party/libuv/src/unix/loop.c:123` | `uv__free(lfields);` |
| `ev_0ba9d64a6df2` | call_site | `third_party/libuv/src/unix/core.c:314` | `assert(handle->flags & UV_HANDLE_CLOSING);` |
| `ev_0bdb2483fe67` | call_site | `third_party/libuv/src/unix/thread.c:792` | `if (pthread_mutex_unlock(&mutex))` |
| `ev_0bee1b07507e` | call_site | `third_party/libuv/src/unix/poll.c:113` | `assert(!uv__is_closing(handle));` |
| `ev_0c2a91addccc` | call_site | `third_party/libuv/src/unix/process.c:386` | `if ((options->flags & UV_PROCESS_SETUID) && setuid(options->uid))` |
| `ev_0c33fbe29fb3` | call_site | `third_party/libuv/src/unix/stream.c:1393` | `assert(!(stream->flags & UV_HANDLE_BLOCKING_WRITES));` |
| `ev_0c3d62e20202` | call_site | `third_party/libuv/src/unix/stream.c:770` | `iovmax = uv__getiovmax();` |
| `ev_0c52da5265f1` | assignment | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_0c6499185fe5` | call_site | `third_party/libuv/src/unix/stream.c:176` | `FD_SET(fd, s->swrite);` |
| `ev_0c69ae2c2101` | call_site | `third_party/libuv/src/unix/thread.c:779` | `if (pthread_mutex_init(&mutex, NULL))` |
| `ev_0c6ef3706c2a` | call_site | `third_party/libuv/src/unix/core.c:1396` | `assert(gr_mem == (char*)grp->members + mem_size);` |
| `ev_0c807921a91f` | call_site | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_0cad6778fed2` | call_site | `third_party/libuv/src/unix/proctitle.c:139` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_0cc23d1508bd` | call_site | `third_party/libuv/src/unix/process.c:464` | `err = posix_spawnattr_init(attrs);` |
| `ev_0ccc461ace9e` | call_site | `third_party/libuv/src/threadpool.c:294` | `uv_mutex_unlock(&mutex);` |
| `ev_0cf79e0eeb4b` | call_site | `third_party/libuv/src/unix/tcp.c:167` | `if (setsockopt(tcp->io_watcher.fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)))` |
| `ev_0cfb02b0bb30` | call_site | `third_party/libuv/src/unix/thread.c:331` | `if (pthread_mutexattr_destroy(&attr))` |
| `ev_0d005a0b5917` | call_site | `third_party/libuv/src/unix/thread.c:829` | `abort();` |
| `ev_0d2e2bbaf2b8` | call_site | `third_party/libuv/src/unix/core.c:1393` | `strcpy(gr_mem, gp.gr_mem[r]);` |
| `ev_0d62d8f5e472` | call_site | `third_party/libuv/src/unix/fs.c:361` | `uv_rwlock_rdunlock(&req->loop->cloexec_lock);` |
| `ev_0d7e53814be3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_0da8802e9929` | call_site | `third_party/libuv/src/unix/stream.c:396` | `uv__close(fds[1]);` |
| `ev_0dc2ddae96f7` | call_site | `third_party/libuv/src/unix/kqueue.c:661` | `uv_fs_event_stop(handle);` |
| `ev_0dc31ccdc432` | call_site | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_0dd7009b3894` | call_site | `third_party/libuv/src/uv-common.c:981` | `uv__threadpool_cleanup();` |
| `ev_0de39aac0beb` | call_site | `third_party/libuv/src/unix/process.c:150` | `uv__queue_insert_tail(&pending, &process->queue);` |
| `ev_0df4792c3291` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:91` | `abort();` |
| `ev_0e410bb4266d` | call_site | `third_party/libuv/src/unix/stream.c:309` | `uv__close(kq);` |
| `ev_0e4978a54264` | call_site | `third_party/libuv/src/unix/core.c:635` | `rc = UV__ERR(errno);` |
| `ev_0e54f9990020` | call_site | `third_party/libuv/src/timer.c:100` | `heap_remove(timer_heap(handle->loop),` |
| `ev_0e731eb327a2` | call_site | `third_party/libuv/src/unix/kqueue.c:545` | `handle->cb(handle, path, events, 0);` |
| `ev_0e7eb843685d` | call_site | `third_party/libuv/src/unix/fs.c:2188` | `PATH2;` |
| `ev_0e7f5d7e79fe` | call_site | `third_party/libuv/src/thread-common.c:142` | `uv_mutex_destroy(&b->mutex);` |
| `ev_0e9038561362` | call_site | `third_party/libuv/src/unix/poll.c:99` | `return uv_poll_init(loop, handle, socket);` |
| `ev_0e91e20f0c27` | call_site | `third_party/libuv/src/unix/fs.c:1232` | `r = pwrite(fd, bufs->iov_base, bufs->iov_len, off);` |
| `ev_0ed3b6899154` | call_site | `third_party/libuv/src/uv-common.c:202` | `snprintf(buf, sizeof(buf), "Unknown system error %d", err);` |
| `ev_0eefec2cc83a` | call_site | `third_party/libuv/src/unix/fsevents.c:842` | `assert(handle != NULL);` |
| `ev_0efc91732fce` | call_site | `third_party/libuv/src/unix/fs.c:199` | `return uv__fs_fsync(req);` |
| `ev_0f0adf6b31e9` | call_site | `third_party/libuv/src/unix/core.c:535` | `setsockopt(sockfd, SOL_SOCKET, SO_NOSIGPIPE, &on, sizeof(on));` |
| `ev_0f24b47a3ae9` | call_site | `third_party/libuv/src/unix/fsevents.c:236` | `assert(state != NULL);` |
| `ev_0f2c22d93b25` | call_site | `third_party/libuv/src/uv-common.c:202` | `snprintf(buf, sizeof(buf), "Unknown system error %d", err);` |
| `ev_0f2dc5cbb7f1` | call_site | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_0f3c91f9fb8a` | call_site | `third_party/libuv/src/unix/core.c:1920` | `uv__free(cloned_path);` |
| `ev_0f536d0c1d57` | call_site | `third_party/libuv/src/unix/fs.c:310` | `path_length = strlen(path);` |
| `ev_0f57ac66b50d` | call_site | `third_party/libuv/src/unix/fsevents.c:825` | `uv_async_init(handle->loop, handle->cf_cb, uv__fsevents_cb);` |
| `ev_0f5d759ead61` | call_site | `third_party/libuv/src/uv-common.c:834` | `err = uv__loop_configure(loop, option, ap);` |
| `ev_0f5fafde2d68` | call_site | `third_party/libuv/src/unix/stream.c:1459` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_0f84d8f546f4` | call_site | `third_party/libuv/src/unix/fsevents.c:690` | `uv__queue_remove(q);` |
| `ev_0fc3728e42bf` | call_site | `third_party/libuv/src/unix/kqueue.c:57` | `return UV__ERR(errno);` |
| `ev_0fd87609ba65` | call_site | `third_party/libuv/src/unix/thread.c:782` | `if (pthread_mutex_lock(&mutex))` |
| `ev_100056da66f7` | call_site | `third_party/libuv/src/unix/signal.c:560` | `uv__signal_unregister_handler(handle->signum);` |
| `ev_1001cb55f96d` | call_site | `third_party/libuv/src/unix/core.c:167` | `uv__pipe_close((uv_pipe_t*)handle);` |
| `ev_101b07054235` | call_site | `third_party/libuv/src/unix/stream.c:1055` | `stream->read_cb(stream, UV_ENOBUFS, &buf);` |
| `ev_10338a425d04` | call_site | `third_party/libuv/src/unix/fs.c:2053` | `req->bufs = uv__malloc(nbufs * sizeof(*bufs));` |
| `ev_103f3d15aef3` | call_site | `third_party/libuv/src/unix/core.c:694` | `return UV__ERR(errno);` |
| `ev_1054dccef848` | call_site | `third_party/libuv/src/uv-common.c:292` | `addr->sin6_scope_id = if_nametoindex(zone_index);` |
| `ev_10739f1bfcae` | call_site | `third_party/libuv/src/unix/udp.c:927` | `} else if (uv_ip6_addr(multicast_addr, 0, &addr6) == 0) {` |
| `ev_1077ab830b32` | call_site | `third_party/libuv/src/unix/core.c:1610` | `return UV__ERR(errno);` |
| `ev_108e3bbd81e0` | call_site | `third_party/libuv/src/unix/udp.c:791` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_10914ef3eb01` | call_site | `third_party/libuv/src/unix/signal.c:448` | `if (r == -1 && errno == EINTR)` |
| `ev_109c43001394` | call_site | `third_party/libuv/src/unix/stream.c:1263` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_10a3d4c1a7d8` | call_site | `third_party/libuv/src/unix/core.c:1400` | `memcpy(grp->groupname, gp.gr_name, name_size);` |
| `ev_10a4f102c0a2` | call_site | `third_party/libuv/src/unix/process.c:118` | `q = uv__queue_next(q);` |
| `ev_10bcfe1571d7` | call_site | `third_party/libuv/src/unix/core.c:1904` | `if (access(abspath, X_OK) == 0) {` |
| `ev_10cf35ec529c` | call_site | `third_party/libuv/src/unix/stream.c:694` | `assert(n <= stream->write_queue_size);` |
| `ev_1106e0e1586f` | call_site | `third_party/libuv/src/unix/thread.c:800` | `abort();` |
| `ev_11569a89e3da` | call_site | `third_party/libuv/src/unix/fs.c:493` | `memcpy(&f, &p, sizeof(p));` |
| `ev_11b0320b6221` | call_site | `third_party/libuv/src/unix/fs.c:1164` | `return utimes(req->path, tv);` |
| `ev_11b2b673095b` | call_site | `third_party/libuv/src/unix/loop.c:94` | `err = uv_mutex_init(&loop->wq_mutex);` |
| `ev_11c0728870bb` | call_site | `third_party/libuv/src/unix/pipe.c:135` | `uv__close(sockfd);` |
| `ev_11cd93e668d8` | call_site | `third_party/libuv/src/unix/async.c:86` | `uv__queue_insert_tail(&loop->async_handles, &handle->queue);` |
| `ev_11d58236657a` | call_site | `third_party/libuv/src/unix/thread.c:343` | `if (pthread_mutexattr_init(&attr))` |
| `ev_11d98fe57417` | call_site | `third_party/libuv/src/unix/stream.c:1252` | `assert(req);` |
| `ev_11e0852d6f59` | call_site | `third_party/libuv/src/unix/core.c:1274` | `buf = uv__malloc(bufsize);` |
| `ev_11ece5d14204` | call_site | `third_party/libuv/src/unix/udp.c:268` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK)` |
| `ev_11edff8b9729` | call_site | `third_party/libuv/src/unix/signal.c:198` | `handle = RB_NEXT(uv__signal_tree_s, handle)) {` |
| `ev_11fb3adcf41a` | call_site | `third_party/libuv/src/unix/fs.c:356` | `abort();` |
| `ev_11fda6899df4` | call_site | `third_party/libuv/src/threadpool.c:113` | `if (!uv__queue_empty(&slow_io_pending_wq)) {` |
| `ev_1216d1324f1e` | call_site | `third_party/libuv/src/unix/core.c:160` | `assert(!uv__is_closing(handle));` |
| `ev_12184091e12a` | call_site | `third_party/libuv/src/unix/stream.c:1064` | `nread = read(uv__stream_fd(stream), buf.base, buf.len);` |
| `ev_1234eba3e0db` | call_site | `third_party/libuv/src/unix/process.c:252` | `uv__stream_close(container->data.stream);` |
| `ev_12364a436224` | call_site | `third_party/libuv/src/idna.c:408` | `assert(w_target_len == 0);` |
| `ev_123f68ab8359` | call_site | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_12436a1dd0b3` | call_site | `third_party/libuv/src/unix/thread.c:478` | `abort();` |
| `ev_124c685c2158` | assignment | `third_party/libuv/src/unix/pipe.c:171` | `handle->io_watcher.cb = uv__server_io;` |
| `ev_1277a4f1694e` | call_site | `third_party/libuv/src/unix/core.c:854` | `w->cb(loop, w, POLLOUT);` |
| `ev_12e8d927696a` | call_site | `third_party/libuv/src/unix/process.c:837` | `abort();` |
| `ev_12fb150da2f1` | call_site | `third_party/libuv/src/unix/stream.c:1372` | `stream->write_queue_size += uv__count_bufs(bufs, nbufs);` |
| `ev_12fb7ada444f` | call_site | `third_party/libuv/src/threadpool.c:84` | `uv_mutex_unlock(&mutex);` |
| `ev_1320b044b486` | call_site | `third_party/libuv/src/unix/kqueue.c:422` | `uv__metrics_update_idle_time(loop);` |
| `ev_1350b0651caf` | call_site | `third_party/libuv/src/unix/tcp.c:405` | `if (0 != setsockopt(fd, SOL_SOCKET, SO_LINGER, &l, sizeof(l))) {` |
| `ev_13668eda86db` | call_site | `third_party/libuv/src/unix/stream.c:102` | `err = uv__open_cloexec("/dev/null", O_RDONLY);` |
| `ev_13917c12f56a` | call_site | `third_party/libuv/src/uv-common.c:1005` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_13a15aaa8721` | call_site | `third_party/libuv/src/unix/poll.c:150` | `uv__io_start(handle->loop, &handle->io_watcher, events);` |
| `ev_13e5b7b7d213` | call_site | `third_party/libuv/src/unix/fs.c:1234` | `r = uv__pwritev(fd, bufs, nbufs, off);` |
| `ev_13ec1cee758e` | call_site | `third_party/libuv/src/unix/dl.c:36` | `lib->handle = dlopen(filename, RTLD_LAZY);` |
| `ev_13f8c58fad47` | call_site | `third_party/libuv/src/fs-poll.c:224` | `uv_close((uv_handle_t*)&ctx->timer_handle, timer_close_cb);` |
| `ev_143e69c8c53b` | call_site | `third_party/libuv/src/uv-common.c:438` | `return uv__udp_connect(handle, addr, addrlen);` |
| `ev_146e0ed4d5a7` | call_site | `third_party/libuv/src/inet.c:127` | `int err = inet_ntop4(src+12, tp, sizeof tmp - (tp - tmp));` |
| `ev_14b6e48c7c1b` | call_site | `third_party/libuv/src/unix/fsevents.c:203` | `uv__queue_add(&handle->cf_events, events);` |
| `ev_14bba1929b2d` | call_site | `third_party/libuv/src/unix/core.c:347` | `uv__stream_destroy((uv_stream_t*)handle);` |
| `ev_14d1b7093987` | call_site | `third_party/libuv/src/unix/stream.c:1299` | `assert((stream->type == UV_TCP \|\|` |
| `ev_14d7bfe12fd2` | call_site | `third_party/libuv/src/unix/process.c:969` | `assert(!(options->flags & ~(UV_PROCESS_DETACHED \|` |
| `ev_14ecddbcb26b` | call_site | `third_party/libuv/src/unix/pipe.c:294` | `memset(&saddr, 0, sizeof saddr);` |
| `ev_150365d5d208` | call_site | `third_party/libuv/src/unix/random-devurandom.c:59` | `uv__close(fd);` |
| `ev_15138841a177` | call_site | `third_party/libuv/src/unix/process.c:112` | `uv__queue_init(&pending);` |
| `ev_151a6ce00ebc` | call_site | `third_party/libuv/src/unix/pipe.c:295` | `memcpy(&saddr.sun_path, name, namelen);` |
| `ev_152d208c9f6a` | call_site | `third_party/libuv/src/unix/process.c:366` | `uv__close(close_fd);` |
| `ev_15404d94cfff` | call_site | `third_party/libuv/src/unix/core.c:993` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_154ab79e326e` | call_site | `third_party/libuv/src/unix/signal.c:249` | `memset(&sa, 0, sizeof(sa));` |
| `ev_158456aaded4` | call_site | `third_party/libuv/src/heap-inl.h:236` | `heap_node_swap(heap, child->parent, child);` |
| `ev_159dde9488ae` | call_site | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_15a979b79734` | assignment | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_15c81bcc736a` | call_site | `third_party/libuv/src/unix/signal.c:272` | `uv__io_init(&loop->signal_io_watcher,` |
| `ev_15d65074e759` | call_site | `third_party/libuv/src/unix/core.c:606` | `return close$NOCANCEL(fd);` |
| `ev_15de36d378a1` | call_site | `third_party/libuv/src/unix/thread.c:351` | `if (pthread_mutexattr_destroy(&attr))` |
| `ev_15e8a9868f48` | call_site | `third_party/libuv/src/timer.c:77` | `uv_timer_stop(handle);` |
| `ev_15eda5d1072f` | call_site | `third_party/libuv/src/unix/core.c:907` | `assert(fd >= -1);` |
| `ev_15fdf97bfacf` | call_site | `third_party/libuv/src/heap-inl.h:228` | `heap_node_swap(heap, child, smallest);` |
| `ev_16190108c135` | call_site | `third_party/libuv/src/unix/tty.c:77` | `return UV__ERR(errno);` |
| `ev_161fa29f4521` | call_site | `third_party/libuv/src/unix/thread.c:788` | `err = pthread_cond_timedwait_relative_np(cond, &mutex, &ts);` |
| `ev_1621b4b551a3` | call_site | `third_party/libuv/src/unix/fs.c:1752` | `} while (r == -1 && errno == EINTR && retry_on_eintr);` |
| `ev_1651cc5b3538` | call_site | `third_party/libuv/src/unix/core.c:187` | `uv__check_close((uv_check_t*)handle);` |
| `ev_1673588870eb` | call_site | `third_party/libuv/src/unix/process.c:969` | `assert(!(options->flags & ~(UV_PROCESS_DETACHED \|` |
| `ev_169065a4fa17` | call_site | `third_party/libuv/src/unix/stream.c:427` | `if (setsockopt(fd, SOL_SOCKET, SO_OOBINLINE, &enable, sizeof(enable)) &&` |
| `ev_16ab7a80375d` | call_site | `third_party/libuv/src/unix/fsevents.c:199` | `uv_mutex_lock(&handle->cf_mutex);` |
| `ev_16b0f25d0fc4` | call_site | `third_party/libuv/src/unix/core.c:650` | `return uv__close_nocheckstdio(fd);` |
| `ev_16e2f283b418` | call_site | `third_party/libuv/src/unix/process.c:261` | `while (n == -1 && errno == EINTR);` |
| `ev_1714d1ba7203` | call_site | `third_party/libuv/src/unix/process.c:718` | `l = strnlen(path, PATH_MAX - 1) + 1;` |
| `ev_1744a673f164` | call_site | `third_party/libuv/src/unix/process.c:581` | `assert(err != ENOSYS);` |
| `ev_174a5e7a8a0d` | call_site | `third_party/libuv/src/unix/stream.c:1106` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_176a1561fc32` | call_site | `third_party/libuv/src/unix/fs.c:1436` | `uv_fs_unlink(NULL, &fs_req, req->new_path, NULL);` |
| `ev_17730c09a72c` | call_site | `third_party/libuv/src/unix/stream.c:1526` | `uv_close((uv_handle_t*) &s->async, uv__stream_osx_cb_close);` |
| `ev_17784e63f8cf` | call_site | `third_party/libuv/src/unix/process.c:95` | `memset(&loop->child_watcher, 0, sizeof(loop->child_watcher));` |
| `ev_17828bd372ad` | call_site | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_179df896b056` | call_site | `third_party/libuv/src/unix/core.c:1914` | `uv__free(cloned_path);` |
| `ev_17b78eca251b` | call_site | `third_party/libuv/src/unix/process.c:601` | `assert(err != ENOSYS);` |
| `ev_17c4f6dfe095` | call_site | `third_party/libuv/src/unix/pipe.c:288` | `err = uv__socket(AF_UNIX, SOCK_STREAM, 0);` |
| `ev_17ef84923eda` | call_site | `third_party/libuv/src/unix/pipe.c:200` | `if (uv__fd_exists(handle->loop, fd))` |
| `ev_17fb293b0605` | call_site | `third_party/libuv/src/unix/signal.c:239` | `return UV__ERR(errno);` |
| `ev_1812f2811ac8` | call_site | `third_party/libuv/src/timer.c:199` | `uv_timer_stop(handle);` |
| `ev_182a9947b2ac` | call_site | `third_party/libuv/src/unix/process.c:916` | `err = uv__spawn_and_init_child_fork(options, stdio_count, pipes, signal_pipe[1], pid);` |
| `ev_185b8efc41eb` | call_site | `third_party/libuv/src/unix/fs.c:1716` | `X(CLOSE, uv__fs_close(req->file));` |
| `ev_185ee6e42be8` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_186a53e8ac1c` | call_site | `third_party/libuv/src/uv-common.c:609` | `uv__print_handles(loop, 0, stream);` |
| `ev_18762baaeb2f` | call_site | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_18887fab6fc1` | call_site | `third_party/libuv/src/threadpool.c:226` | `uv__queue_init(&run_slow_work_message);` |
| `ev_18897c1bee11` | call_site | `third_party/libuv/src/unix/tcp.c:43` | `memset(&s, 0, sizeof(s));` |
| `ev_188e05cab09e` | call_site | `third_party/libuv/src/unix/udp.c:130` | `uv__io_stop(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_189d9ca7af89` | assignment | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_18a4e4d976a5` | call_site | `third_party/libuv/src/unix/udp.c:771` | `memset(&mreq, 0, sizeof(mreq));` |
| `ev_18c6719c8092` | call_site | `third_party/libuv/src/unix/tty.c:448` | `if (getsockopt(file, SOL_SOCKET, SO_TYPE, &type, &len))` |
| `ev_18f01deeaf81` | call_site | `third_party/libuv/src/unix/async.c:283` | `err = uv__open_cloexec("/dev/null", O_RDONLY);` |
| `ev_191c8adc3c04` | call_site | `third_party/libuv/src/unix/stream.c:870` | `if (uv__write_req_update(stream, req, n)) {` |
| `ev_1922842120f4` | call_site | `third_party/libuv/src/unix/loop.c:85` | `err = uv__process_init(loop);` |
| `ev_1924d2ee9785` | call_site | `third_party/libuv/src/unix/thread.c:455` | `abort();` |
| `ev_192eb781235e` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_1950ee129b80` | call_site | `third_party/libuv/src/unix/udp.c:866` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_UDP);` |
| `ev_195f897256f3` | call_site | `third_party/libuv/src/unix/loop.c:57` | `uv__queue_init(&loop->prepare_handles);` |
| `ev_1961fbcd972a` | call_site | `third_party/libuv/src/unix/fsevents.c:876` | `uv__queue_remove(&handle->cf_member);` |
| `ev_196f2a5f3c08` | call_site | `third_party/libuv/src/threadpool.c:129` | `uv_async_send(&w->loop->wq_async);` |
| `ev_1976025509c2` | call_site | `third_party/libuv/src/unix/tcp.c:572` | `return UV__ERR(errno);` |
| `ev_197e4f060ef4` | call_site | `third_party/libuv/src/unix/process.c:687` | `char** env = environ;` |
| `ev_19eb78f41da1` | call_site | `third_party/libuv/src/unix/getnameinfo.c:118` | `uv__getnameinfo_done(&req->work_req, 0);` |
| `ev_1a365af838f0` | call_site | `third_party/libuv/src/unix/fs.c:1747` | `X(UTIME, uv__fs_utime(req));` |
| `ev_1a6171ff7ebe` | call_site | `third_party/libuv/src/unix/core.c:710` | `while (r == -1 && errno == EINTR);` |
| `ev_1a93bc043711` | call_site | `third_party/libuv/src/unix/signal.c:257` | `abort();` |
| `ev_1ad94a95adf3` | call_site | `third_party/libuv/src/unix/process.c:141` | `abort();` |
| `ev_1ade9781b7ce` | call_site | `third_party/libuv/src/unix/core.c:920` | `assert(w->fd >= 0);` |
| `ev_1affd60a4a39` | call_site | `third_party/libuv/src/unix/kqueue.c:185` | `assert(uv__queue_empty(&loop->watcher_queue));` |
| `ev_1b0d13deedae` | call_site | `third_party/libuv/src/fs-poll.c:124` | `assert(ctx->parent_handle == handle);` |
| `ev_1b39518b0531` | call_site | `third_party/libuv/src/unix/fsevents.c:451` | `pCFStringCreateWithFileSystemRepresentation(NULL, curr->realpath);` |
| `ev_1b40786835df` | call_site | `third_party/libuv/src/threadpool.c:62` | `uv_thread_setname("libuv-worker");` |
| `ev_1b588ed3faec` | call_site | `third_party/libuv/src/threadpool.c:365` | `req->after_work_cb(req, err);` |
| `ev_1b6e96eff7fe` | call_site | `third_party/libuv/src/unix/fs.c:1733` | `X(READ, uv__fs_read(req));` |
| `ev_1b7d50ad29e9` | call_site | `third_party/libuv/src/unix/tty.c:150` | `type = uv_guess_handle(fd);` |
| `ev_1b9716ee2bfd` | call_site | `third_party/libuv/src/inet.c:133` | `tp += snprintf(tp, sizeof tmp - (tp - tmp), "%x", words[i]);` |
| `ev_1baa24c389d1` | call_site | `third_party/libuv/src/unix/process.c:595` | `err = posix_spawn_file_actions_addopen(` |
| `ev_1bad3006cd6a` | call_site | `third_party/libuv/src/unix/fsevents.c:321` | `uv__fsevents_push_event(handle, &head, 0);` |
| `ev_1bbfcc053b16` | call_site | `third_party/libuv/src/random.c:107` | `return uv__random(buf, buflen);` |
| `ev_1befa26dc27e` | assignment | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_1c17689a22fb` | call_site | `third_party/libuv/src/timer.c:186` | `while (!uv__queue_empty(&ready_queue)) {` |
| `ev_1c2251217b59` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_1c2eef4e65c4` | call_site | `third_party/libuv/src/unix/udp.c:256` | `memset(&peer, 0, sizeof(peer));` |
| `ev_1c369546ef01` | call_site | `third_party/libuv/src/unix/core.c:315` | `assert(!(handle->flags & UV_HANDLE_CLOSED));` |
| `ev_1c37fd0d67c5` | call_site | `third_party/libuv/src/unix/process.c:147` | `assert(pid == process->pid);` |
| `ev_1c69a1a72174` | call_site | `third_party/libuv/src/threadpool.c:186` | `uv_mutex_destroy(&mutex);` |
| `ev_1c824f8b9990` | call_site | `third_party/libuv/src/uv-common.c:656` | `return uv__socket_sockopt(handle, SO_RCVBUF, value);` |
| `ev_1c91c7033e3c` | call_site | `third_party/libuv/src/unix/udp.c:74` | `while (!uv__queue_empty(&handle->write_queue)) {` |
| `ev_1c9f7c728bcf` | call_site | `third_party/libuv/src/unix/stream.c:1051` | `buf = uv_buf_init(NULL, 0);` |
| `ev_1cdb46ab598f` | call_site | `third_party/libuv/src/unix/udp.c:587` | `assert(addrlen <= sizeof(req->u.storage));` |
| `ev_1ce730048d23` | call_site | `third_party/libuv/src/unix/signal.c:73` | `if (pthread_atfork(NULL, NULL, &uv__signal_global_reinit))` |
| `ev_1cf43bc2d4aa` | call_site | `third_party/libuv/src/unix/stream.c:1375` | `uv__queue_insert_tail(&stream->write_queue, &req->queue);` |
| `ev_1d0055eebef7` | call_site | `third_party/libuv/src/unix/kqueue.c:376` | `assert(w->events == POLLIN);` |
| `ev_1d044a6853e0` | call_site | `third_party/libuv/src/threadpool.c:293` | `uv_mutex_unlock(&w->loop->wq_mutex);` |
| `ev_1d2b41462cb4` | call_site | `third_party/libuv/src/unix/fsevents.c:369` | `assert(ref != NULL);` |
| `ev_1d665169561c` | call_site | `third_party/libuv/src/unix/core.c:1297` | `name_size = strlen(pw.pw_name) + 1;` |
| `ev_1d7da1647578` | call_site | `third_party/libuv/src/unix/pipe.c:205` | `while (mode == -1 && errno == EINTR);` |
| `ev_1db00dd783b7` | call_site | `third_party/libuv/src/unix/async.c:175` | `r = read(w->fd, buf, sizeof(buf));` |
| `ev_1dbd168c6b89` | call_site | `third_party/libuv/src/unix/fs.c:538` | `r = readv(fd, bufs, nbufs);` |
| `ev_1dd084c56ca2` | call_site | `third_party/libuv/src/unix/tty.c:163` | `return UV__ERR(errno);` |
| `ev_1dec4b5253c6` | call_site | `third_party/libuv/src/unix/kqueue.c:286` | `nfds = kevent(loop->backend_fd,` |
| `ev_1df17e865a17` | call_site | `third_party/libuv/src/unix/fs.c:348` | `r = mkstemp(path);` |
| `ev_1df22000481a` | call_site | `third_party/libuv/src/threadpool.c:128` | `uv__queue_insert_tail(&w->loop->wq, &w->wq);` |
| `ev_1e06d69349ee` | call_site | `third_party/libuv/src/unix/core.c:1222` | `CHECK_ENV_VAR("TMPDIR");` |
| `ev_1e1df29d03f3` | call_site | `third_party/libuv/src/fs-poll.c:181` | `ctx->start_time = uv_now(ctx->loop);` |
| `ev_1e1e2504a33d` | call_site | `third_party/libuv/src/unix/signal.c:493` | `memmove(buf, buf + end, bytes);` |
| `ev_1e2691eede8e` | call_site | `third_party/libuv/src/unix/core.c:1383` | `uv__free(buf);` |
| `ev_1e46d8ab3b13` | call_site | `third_party/libuv/src/unix/stream.c:919` | `stream->write_queue_size -= uv__write_req_size(req);` |
| `ev_1e486deaf79a` | call_site | `third_party/libuv/src/unix/stream.c:1148` | `stream->read_cb(stream, nread, &buf);` |
| `ev_1e668ff5c772` | call_site | `third_party/libuv/src/unix/thread.c:413` | `abort();` |
| `ev_1e760e93bc9d` | call_site | `third_party/libuv/src/unix/core.c:769` | `if (getcwd(scratch, sizeof(scratch)) == NULL)` |
| `ev_1e8b54b6b43f` | call_site | `third_party/libuv/src/unix/core.c:270` | `assert(!(handle->flags & UV_HANDLE_CLOSED));` |
| `ev_1e963594aac4` | assignment | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_1eb9fcad6871` | call_site | `third_party/libuv/src/unix/pipe.c:394` | `memcpy(buffer, sa.sun_path, addrlen);` |
| `ev_1ec7a13834f3` | call_site | `third_party/libuv/src/unix/signal.c:151` | `if (uv__signal_lock())` |
| `ev_1ed3b77b8bc6` | call_site | `third_party/libuv/src/unix/fsevents.c:323` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_1ef966f004d1` | call_site | `third_party/libuv/src/unix/pipe.c:323` | `err = uv__stream_open((uv_stream_t*)handle,` |
| `ev_1efd46fbd09f` | call_site | `third_party/libuv/src/unix/fs.c:819` | `buf = uv__malloc(len + 1);` |
| `ev_1f144a4c3ef4` | call_site | `third_party/libuv/src/unix/fsevents.c:476` | `pCFRelease(paths[--i]);` |
| `ev_1f36ebffd4fa` | call_site | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_1f51f354d39e` | call_site | `third_party/libuv/src/uv-common.c:283` | `memcpy(address_part, ip, address_part_size);` |
| `ev_1f5983a8da73` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:203` | `req->hostname = memcpy(buf + len, hostname, hostname_len);` |
| `ev_1f5b02715f98` | call_site | `third_party/libuv/src/unix/getnameinfo.c:65` | `assert(req->retcode == 0);` |
| `ev_1f8cdd8237be` | call_site | `third_party/libuv/src/unix/poll.c:90` | `uv__handle_init(loop, (uv_handle_t*) handle, UV_POLL);` |
| `ev_1f965ef19eb1` | call_site | `third_party/libuv/src/unix/stream.c:369` | `err = uv_thread_create(&s->thread, uv__stream_osx_select, stream);` |
| `ev_1fbffc39a03b` | call_site | `third_party/libuv/src/unix/thread.c:177` | `abort();` |
| `ev_1fc8a2019bd4` | call_site | `third_party/libuv/src/unix/signal.c:107` | `abort();` |
| `ev_1fe6fd14bac4` | call_site | `third_party/libuv/src/unix/internal.h:400` | `loop->time = uv__hrtime(UV_CLOCK_FAST) / 1000000;` |
| `ev_1fea5146b4a3` | call_site | `third_party/libuv/src/unix/fs.c:930` | `while (n == -1 && errno == EINTR);` |
| `ev_1ffb25112b0b` | call_site | `third_party/libuv/src/unix/signal.c:157` | `if (uv__signal_unlock())` |
| `ev_200d24dce59c` | call_site | `third_party/libuv/src/unix/udp.c:1168` | `abort();` |
| `ev_2014c933c325` | call_site | `third_party/libuv/src/unix/tcp.c:321` | `else if (errno == ECONNREFUSED` |
| `ev_2031de935e23` | call_site | `third_party/libuv/src/idna.c:474` | `target_len = uv_utf16_length_as_wtf8(w_source_ptr, w_source_len);` |
| `ev_2093d77d68e8` | call_site | `third_party/libuv/src/unix/udp.c:1159` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_20a9835f3114` | call_site | `third_party/libuv/src/unix/kqueue.c:377` | `assert(w->pevents == POLLIN);` |
| `ev_20d56305fccd` | call_site | `third_party/libuv/src/unix/core.c:966` | `assert(loop->nfds > 0);` |
| `ev_20df1bc281ce` | call_site | `third_party/libuv/src/unix/core.c:1526` | `if (unsetenv(name) != 0)` |
| `ev_20e4abf5aeff` | call_site | `third_party/libuv/src/unix/udp.c:1119` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_20f84a920a0a` | call_site | `third_party/libuv/src/uv-common.c:976` | `uv__signal_cleanup();` |
| `ev_2111c058684b` | call_site | `third_party/libuv/src/unix/signal.c:121` | `r = read(uv__signal_lock_pipefd[0], &data, sizeof data);` |
| `ev_211bf80d72e4` | call_site | `third_party/libuv/src/unix/fs.c:1873` | `PATH;` |
| `ev_2124d94aafb6` | call_site | `third_party/libuv/src/unix/tcp.c:309` | `errno = 0;` |
| `ev_214363ec942e` | call_site | `third_party/libuv/src/unix/stream.c:582` | `assert(queued_fds->offset > 0);` |
| `ev_214a0dca31d2` | call_site | `third_party/libuv/src/unix/stream.c:495` | `err = uv__accept(accept_fd);` |
| `ev_2158f3537e80` | call_site | `third_party/libuv/src/unix/stream.c:1194` | `assert(stream->type == UV_TCP \|\|` |
| `ev_2186a4128abe` | call_site | `third_party/libuv/src/unix/core.c:523` | `err = uv__nonblock(sockfd, 1);` |
| `ev_21c1a60dfc72` | call_site | `third_party/libuv/src/thread-common.c:136` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_21c5e01aaae6` | assignment | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_21d0071e7c2c` | call_site | `third_party/libuv/src/unix/stream.c:820` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK \|\| errno == ENOBUFS)` |
| `ev_21d6d0fd92de` | call_site | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_21e10f1599d9` | call_site | `third_party/libuv/src/unix/fs.c:2214` | `PATH;` |
| `ev_220821ab287b` | call_site | `third_party/libuv/src/unix/fs.c:2188` | `PATH2;` |
| `ev_221aba5940c9` | call_site | `third_party/libuv/src/unix/fs.c:2022` | `PATH;` |
| `ev_2223081a7d37` | call_site | `third_party/libuv/src/unix/fs.c:293` | `dlerror();` |
| `ev_2229444bffa6` | call_site | `third_party/libuv/src/unix/udp.c:1178` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_22514685a0b0` | call_site | `third_party/libuv/src/unix/stream.c:1092` | `stream->read_cb(stream, 0, &buf);` |
| `ev_22785e8672f9` | call_site | `third_party/libuv/src/unix/signal.c:365` | `return uv__signal_start(handle, signal_cb, signum, 1);` |
| `ev_2295b201528b` | call_site | `third_party/libuv/src/unix/kqueue.c:313` | `uv__wait_children(loop);` |
| `ev_22b84b78a1ea` | call_site | `third_party/libuv/src/unix/stream.c:515` | `assert(stream->accepted_fd == -1);` |
| `ev_22cc04c95ed7` | call_site | `third_party/libuv/src/unix/stream.c:1298` | `assert(nbufs > 0);` |
| `ev_22f0c5242538` | call_site | `third_party/libuv/src/unix/stream.c:1276` | `uv__req_unregister(stream->loop);` |
| `ev_22f3005306b9` | call_site | `third_party/libuv/src/inet.c:236` | `pch = strchr((xdigits = xdigits_u), ch);` |
| `ev_2309c0efb781` | call_site | `third_party/libuv/src/unix/core.c:450` | `uv__run_pending(loop);` |
| `ev_2333b73a5524` | call_site | `third_party/libuv/src/unix/darwin.c:81` | `return UV__ERR(errno);` |
| `ev_2352f4db56f1` | call_site | `third_party/libuv/src/unix/kqueue.c:278` | `pthread_sigmask(SIG_BLOCK, pset, NULL);` |
| `ev_23676ec42321` | call_site | `third_party/libuv/src/unix/tcp.c:310` | `r = connect(uv__stream_fd(handle), addr, addrlen);` |
| `ev_237b1c56f72f` | call_site | `third_party/libuv/src/unix/core.c:1895` | `cloned_path = uv__strdup(path_env);` |
| `ev_242b54e4fb8b` | call_site | `third_party/libuv/src/unix/proctitle.c:117` | `memset(pt->str + len, '\0', pt->cap - len);` |
| `ev_2443cbbb6d83` | call_site | `third_party/libuv/src/unix/async.c:77` | `err = uv__async_start(loop);` |
| `ev_244a73c75855` | assignment | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_244efb868811` | call_site | `third_party/libuv/src/unix/pipe.c:130` | `err = UV__ERR(errno);` |
| `ev_245286f76ef8` | call_site | `third_party/libuv/src/unix/process.c:825` | `if (pthread_sigmask(SIG_BLOCK, &signewset, &sigoldset) != 0)` |
| `ev_246eb9941f82` | call_site | `third_party/libuv/src/unix/process.c:714` | `k = strnlen(options->file, NAME_MAX + 1);` |
| `ev_247397b03ad3` | call_site | `third_party/libuv/src/unix/async.c:343` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_247770121995` | call_site | `third_party/libuv/src/unix/darwin.c:107` | `return (uint64_t) info.free_count * sysconf(_SC_PAGESIZE);` |
| `ev_247de283aa35` | call_site | `third_party/libuv/src/unix/core.c:1757` | `r = uv__strscpy(buffer->sysname, buf.sysname, sizeof(buffer->sysname));` |
| `ev_247e633779b6` | call_site | `third_party/libuv/src/unix/pipe.c:406` | `return uv__pipe_getsockpeername(handle, getsockname, buffer, size);` |
| `ev_24c4d3d07a71` | call_site | `third_party/libuv/src/unix/core.c:434` | `uv__update_time(loop);` |
| `ev_24c9fde5800e` | call_site | `third_party/libuv/src/unix/stream.c:558` | `err = uv_udp_open((uv_udp_t*) client, server->accepted_fd);` |
| `ev_24fd32cb6aaf` | call_site | `third_party/libuv/src/unix/stream.c:1197` | `assert(!(stream->flags & UV_HANDLE_CLOSING));` |
| `ev_250452310790` | call_site | `third_party/libuv/src/unix/core.c:1902` | `if (realpath(trypath, abspath) == abspath) {` |
| `ev_250c9873d9ad` | call_site | `third_party/libuv/src/unix/fs.c:1810` | `PATH;` |
| `ev_25193af07a4c` | call_site | `third_party/libuv/src/unix/udp.c:536` | `errno = 0;` |
| `ev_254531256ec4` | call_site | `third_party/libuv/src/unix/core.c:260` | `r = setsockopt(fd, SOL_SOCKET, optname, (const void*) value, len);` |
| `ev_2564d14b945f` | call_site | `third_party/libuv/src/unix/loop.c:200` | `uv__free(loop->watchers);` |
| `ev_259947cdf592` | assignment | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_25ccb94fcece` | call_site | `third_party/libuv/src/unix/core.c:1406` | `uv__free(buf);` |
| `ev_25ea9ff53180` | call_site | `third_party/libuv/src/unix/core.c:952` | `assert(w->fd >= 0);` |
| `ev_25f435432947` | call_site | `third_party/libuv/src/unix/signal.c:101` | `uv__signal_cleanup();` |
| `ev_25fe48dcc414` | call_site | `third_party/libuv/src/unix/tcp.c:222` | `memcpy(b, &a6->sin6_addr, sizeof(b));` |
| `ev_262c5845d265` | call_site | `third_party/libuv/src/unix/pipe.c:204` | `mode = fcntl(fd, F_GETFL);` |
| `ev_2641405cd83f` | call_site | `third_party/libuv/src/unix/udp.c:76` | `uv__queue_remove(q);` |
| `ev_26451329530e` | call_site | `third_party/libuv/src/unix/fs.c:2302` | `PATH2;` |
| `ev_26458e8bbe0c` | call_site | `third_party/libuv/src/unix/fs.c:2022` | `PATH;` |
| `ev_26590af6eae4` | call_site | `third_party/libuv/src/unix/process.c:818` | `sigdelset(&signewset, SIGSTOP);` |
| `ev_266842e5e212` | call_site | `third_party/libuv/src/unix/udp.c:961` | `return uv__udp_set_source_membership6(handle,` |
| `ev_26743a85708e` | call_site | `third_party/libuv/src/unix/fs.c:1744` | `X(STATFS, uv__fs_statfs(req));` |
| `ev_267697074afc` | call_site | `third_party/libuv/src/unix/tcp.c:436` | `err = maybe_new_socket(tcp, AF_INET, flags);` |
| `ev_269c403b197b` | call_site | `third_party/libuv/src/unix/core.c:678` | `return UV__ERR(errno);` |
| `ev_26c39bba40e0` | call_site | `third_party/libuv/src/unix/poll.c:113` | `assert(!uv__is_closing(handle));` |
| `ev_26e2518d5997` | call_site | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_26e7d1fa12de` | call_site | `third_party/libuv/src/unix/loop.c:53` | `uv__queue_init(&loop->wq);` |
| `ev_26ed9ad222f8` | call_site | `third_party/libuv/src/unix/tty.c:238` | `uv__stream_open((uv_stream_t*) tty, fd, flags);` |
| `ev_27122d7f20af` | call_site | `third_party/libuv/src/unix/kqueue.c:367` | `assert(fd == w->fd);` |
| `ev_2779eaf2bddf` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:243` | `memcpy(buffer, ifname_buf, len);` |
| `ev_277a473389b1` | call_site | `third_party/libuv/src/unix/core.c:920` | `assert(w->fd >= 0);` |
| `ev_2780cc7f6233` | call_site | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_27dc5557057a` | call_site | `third_party/libuv/src/unix/thread.c:347` | `abort();` |
| `ev_27eca0072f7a` | call_site | `third_party/libuv/src/unix/poll.c:124` | `assert((pevents & ~(UV_READABLE \| UV_WRITABLE \| UV_DISCONNECT \|` |
| `ev_27fcb433f9d2` | call_site | `third_party/libuv/src/unix/proctitle.c:79` | `size = strlen(argv[i]) + 1;` |
| `ev_28140a455c47` | call_site | `third_party/libuv/src/threadpool.c:181` | `abort();` |
| `ev_282a09a82bd0` | call_site | `third_party/libuv/src/unix/stream.c:657` | `req->cb(req, err);` |
| `ev_283113a6e77c` | call_site | `third_party/libuv/src/unix/core.c:793` | `if (chdir(dir))` |
| `ev_2842d0bacf25` | call_site | `third_party/libuv/src/unix/kqueue.c:217` | `if (kevent(loop->backend_fd, events, nevents, NULL, 0, NULL))` |
| `ev_2849b173f63a` | call_site | `third_party/libuv/src/unix/fs.c:919` | `if (errno != EAGAIN && errno != EWOULDBLOCK) {` |
| `ev_28c7c6f6ac33` | call_site | `third_party/libuv/src/uv-common.c:975` | `uv__process_title_cleanup();` |
| `ev_28e43f0eba1c` | call_site | `third_party/libuv/src/unix/async.c:374` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_28edb14e9754` | call_site | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_28f24dfaf31b` | call_site | `third_party/libuv/src/unix/loop.c:66` | `uv__queue_init(&loop->watcher_queue);` |
| `ev_293bb8500433` | call_site | `third_party/libuv/src/unix/process.c:235` | `abort();` |
| `ev_293dcadb4b4b` | call_site | `third_party/libuv/src/unix/fs.c:1342` | `err = UV__ERR(errno);` |
| `ev_295073cc0f70` | call_site | `third_party/libuv/src/unix/core.c:415` | `if (uv__queue_empty(&loop->watcher_queue))` |
| `ev_299140d1d1a0` | call_site | `third_party/libuv/src/unix/core.c:1577` | `return getppid();` |
| `ev_2a0a2c452c08` | call_site | `third_party/libuv/src/unix/darwin.c:138` | `if (sysctl(which, ARRAY_SIZE(which), &info, &size, NULL, 0) < 0) return;` |
| `ev_2a0e91c3bceb` | call_site | `third_party/libuv/src/unix/random-devurandom.c:45` | `return UV__ERR(errno);` |
| `ev_2a2f0293c273` | call_site | `third_party/libuv/src/unix/stream.c:443` | `while (!uv__queue_empty(&stream->write_queue)) {` |
| `ev_2a453d775952` | call_site | `third_party/libuv/src/unix/tcp.c:340` | `uv__queue_init(&req->queue);` |
| `ev_2a6570dc3adc` | call_site | `third_party/libuv/src/random.c:42` | `rc = uv__random_devurandom(buf, buflen);` |
| `ev_2a75d7d985ea` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_2a957e05db81` | call_site | `third_party/libuv/src/unix/udp.c:263` | `nread = recvmsg(handle->io_watcher.fd, &h, 0);` |
| `ev_2ab12d34bb84` | call_site | `third_party/libuv/src/unix/tty.c:202` | `uv__close(newfd);` |
| `ev_2ab4a7c580e9` | call_site | `third_party/libuv/src/inet.c:263` | `int err = inet_pton4(curtok, tp);` |
| `ev_2ab7f36c505f` | call_site | `third_party/libuv/src/unix/loop.c:111` | `uv_rwlock_destroy(&loop->cloexec_lock);` |
| `ev_2abedf8382bd` | call_site | `third_party/libuv/src/unix/core.c:464` | `for (r = 0; r < 8 && !uv__queue_empty(&loop->pending_queue); r++)` |
| `ev_2ae01ea483ec` | call_site | `third_party/libuv/src/threadpool.c:159` | `uv_cond_signal(&cond);` |
| `ev_2afded09a586` | call_site | `third_party/libuv/src/unix/core.c:199` | `uv__timer_close((uv_timer_t*)handle);` |
| `ev_2b0f4c1dc954` | call_site | `third_party/libuv/src/unix/fs.c:1624` | `ret = uv__fs_statx(fd, "", /* is_fstat */ 1, /* is_lstat */ 0, buf);` |
| `ev_2b195d2040ab` | call_site | `third_party/libuv/src/unix/fs.c:1260` | `srcfd = uv_fs_open(NULL, &fs_req, req->path, O_RDONLY, 0, NULL);` |
| `ev_2b5b63f15a5a` | call_site | `third_party/libuv/src/unix/thread.c:819` | `r = pthread_cond_wait(cond, mutex);` |
| `ev_2b6353eb5ff5` | call_site | `third_party/libuv/src/unix/kqueue.c:294` | `assert(errno == EINTR);` |
| `ev_2b7b6f7ff748` | call_site | `third_party/libuv/src/unix/tcp.c:222` | `memcpy(b, &a6->sin6_addr, sizeof(b));` |
| `ev_2b82d8a51685` | call_site | `third_party/libuv/src/unix/process.c:921` | `uv__close(signal_pipe[1]);` |
| `ev_2b9f9acc3278` | call_site | `third_party/libuv/src/unix/tty.c:399` | `if (uv__fstat(file, &s)) {` |
| `ev_2bc111a36657` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:163` | `hostname + strlen(hostname),` |
| `ev_2bce6a759afe` | call_site | `third_party/libuv/src/unix/core.c:658` | `r = ioctl(fd, FIONBIO, &set);` |
| `ev_2bd2c0837fad` | call_site | `third_party/libuv/src/unix/core.c:1077` | `mach_port_deallocate(mach_task_self(), thread);` |
| `ev_2bf0cdbd36da` | call_site | `third_party/libuv/src/unix/stream.c:539` | `assert(server->loop == client->loop);` |
| `ev_2bf0e24e4dd5` | call_site | `third_party/libuv/src/unix/core.c:171` | `uv__tty_close((uv_tty_t*)handle);` |
| `ev_2bf4506213f8` | call_site | `third_party/libuv/src/threadpool.c:184` | `uv__free(threads);` |
| `ev_2bf7002ee2f7` | call_site | `third_party/libuv/src/unix/process.c:741` | `err = posix_spawn(pid, b, actions, attrs, options->args, env);` |
| `ev_2bf92316f70d` | call_site | `third_party/libuv/src/unix/fsevents.c:755` | `uv__fsevents_reschedule(state, loop, s->type);` |
| `ev_2c08727cb225` | call_site | `third_party/libuv/src/unix/stream.c:528` | `stream->connection_cb(stream, 0);` |
| `ev_2c198a0c4899` | assignment | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_2c25343d7a44` | call_site | `third_party/libuv/src/unix/stream.c:295` | `perror("(libuv) kqueue()");` |
| `ev_2c340322e6b4` | call_site | `third_party/libuv/src/unix/stream.c:1494` | `assert(handle->type == UV_TCP \|\|` |
| `ev_2cfb4e3abba1` | call_site | `third_party/libuv/src/heap-inl.h:224` | `if (child->right != NULL && less_than(child->right, smallest))` |
| `ev_2d04e55ca2f8` | call_site | `third_party/libuv/src/unix/getnameinfo.c:94` | `memcpy(&req->storage,` |
| `ev_2d1d72224d5d` | call_site | `third_party/libuv/src/threadpool.c:262` | `init_threads();` |
| `ev_2d1f6ba70205` | call_site | `third_party/libuv/src/inet.c:222` | `memset((tp = tmp), '\0', sizeof tmp);` |
| `ev_2d3756c7b8da` | call_site | `third_party/libuv/src/unix/tty.c:220` | `r = uv__stream_try_select((uv_stream_t*) tty, &fd);` |
| `ev_2d5361663989` | call_site | `third_party/libuv/src/unix/udp.c:85` | `assert(handle->send_queue_size == 0);` |
| `ev_2d5b243aca20` | call_site | `third_party/libuv/src/unix/tcp.c:68` | `sockfd = uv__socket(domain, SOCK_STREAM, 0);` |
| `ev_2d5e75678d05` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:90` | `assert(!"unknown EAI_* error code");` |
| `ev_2d74c1b81633` | call_site | `third_party/libuv/src/unix/tcp.c:362` | `return uv__stream_open((uv_stream_t*)handle,` |
| `ev_2d7f13f78ecd` | call_site | `third_party/libuv/src/unix/udp.c:587` | `assert(addrlen <= sizeof(req->u.storage));` |
| `ev_2d8a74aae8b0` | call_site | `third_party/libuv/src/unix/fsevents.c:776` | `uv_mutex_lock(&loop->cf_mutex);` |
| `ev_2d9486c581f5` | call_site | `third_party/libuv/src/uv-common.c:565` | `uv__queue_insert_tail(&loop->handle_queue, q);` |
| `ev_2d9cf9a4d8fb` | call_site | `third_party/libuv/src/unix/tcp.c:79` | `return maybe_bind_socket(sockfd);` |
| `ev_2da1a80bcc23` | call_site | `third_party/libuv/src/unix/stream.c:1451` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_2dd96e0feb4c` | call_site | `third_party/libuv/src/unix/udp.c:123` | `req->send_cb(req, 0);` |
| `ev_2de974c4d369` | call_site | `third_party/libuv/src/unix/process.c:941` | `assert(err == *pid);` |
| `ev_2df1e6bc90a9` | call_site | `third_party/libuv/src/unix/tcp.c:57` | `if (bind(fd, &s.addr, slen))` |
| `ev_2e0cf5832e86` | call_site | `third_party/libuv/src/fs-poll.c:223` | `if (!uv_is_active((uv_handle_t*)handle) \|\| uv__is_closing(handle)) {` |
| `ev_2e46251f0255` | call_site | `third_party/libuv/src/inet.c:163` | `memcpy(s, src, len);` |
| `ev_2e585bcf4e2e` | call_site | `third_party/libuv/src/unix/pipe.c:245` | `uv__queue_init(&req->queue);` |
| `ev_2e5c5fbf900f` | call_site | `third_party/libuv/src/unix/stream.c:1545` | `uv__close(handle->accepted_fd);` |
| `ev_2e6adc050a47` | call_site | `third_party/libuv/src/unix/thread.c:403` | `abort();` |
| `ev_2e8143da6e14` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:96` | `pCFBundleGetBundleWithIdentifier(S("com.apple.LaunchServices"));` |
| `ev_2e85879d4882` | call_site | `third_party/libuv/src/unix/fsevents.c:808` | `handle->realpath_len = strlen(handle->realpath);` |
| `ev_2e8d2d3250be` | call_site | `third_party/libuv/src/unix/stream.c:171` | `memset(s->swrite, 0, s->swrite_sz);` |
| `ev_2ea2a914aa1b` | call_site | `third_party/libuv/src/unix/process.c:733` | `memcpy(b, p, z - p);` |
| `ev_2ea8082ed409` | call_site | `third_party/libuv/src/unix/process.c:449` | `uv__spawn_init_posix_spawn_fncs();` |
| `ev_2ee575ffd2de` | call_site | `third_party/libuv/src/unix/udp.c:1363` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_2f1eccabf002` | call_site | `third_party/libuv/src/unix/getnameinfo.c:90` | `memcpy(&req->storage,` |
| `ev_2f2b06fe242a` | call_site | `third_party/libuv/src/unix/fs.c:787` | `buf = uv__reallocf(buf, len + 1);` |
| `ev_2f3f4db09079` | call_site | `third_party/libuv/src/threadpool.c:289` | `cancelled = !uv__queue_empty(&w->wq) && w->work != NULL;` |
| `ev_2f58287cba6b` | call_site | `third_party/libuv/src/unix/stream.c:1264` | `getsockopt(uv__stream_fd(stream),` |
| `ev_2f5eb6274162` | call_site | `third_party/libuv/src/unix/stream.c:860` | `assert(req->handle == stream);` |
| `ev_2f6ac20e287f` | call_site | `third_party/libuv/src/unix/core.c:1492` | `var = getenv(name);` |
| `ev_2f7dda6bfb75` | call_site | `third_party/libuv/src/unix/udp.c:248` | `if (uv_udp_using_recvmmsg(handle)) {` |
| `ev_2f806e37dde4` | call_site | `third_party/libuv/src/uv-common.c:261` | `return uv_inet_pton(AF_INET, ip, &(addr->sin_addr.s_addr));` |
| `ev_2f975143006f` | call_site | `third_party/libuv/src/unix/tcp.c:202` | `return UV__ERR(errno);` |
| `ev_2fc3d59778ea` | call_site | `third_party/libuv/src/fs-poll.c:253` | `assert(last->previous != NULL);` |
| `ev_2fde093c255a` | call_site | `third_party/libuv/src/unix/async.c:192` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_2fe623fc68af` | call_site | `third_party/libuv/src/uv-common.c:68` | `m = uv__malloc(len + 1);` |
| `ev_30225b99c9f1` | call_site | `third_party/libuv/src/uv-common.c:957` | `uv__free(cpu_infos);` |
| `ev_30507b8a5743` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:90` | `freeifaddrs(addrs);` |
| `ev_3069032b5070` | call_site | `third_party/libuv/src/unix/udp.c:907` | `if (uv__udp_is_connected(handle))` |
| `ev_306b6ec05335` | call_site | `third_party/libuv/src/fs-poll.c:230` | `interval -= (uv_now(ctx->loop) - ctx->start_time) % interval;` |
| `ev_30919218a1f1` | call_site | `third_party/libuv/src/unix/fsevents.c:271` | `if (memcmp(path, handle->realpath, handle->realpath_len) != 0)` |
| `ev_309729e6dad5` | call_site | `third_party/libuv/src/thread-common.c:143` | `uv_cond_destroy((uv_cond_t*) &b->cond);` |
| `ev_3097c84378f8` | call_site | `third_party/libuv/src/unix/kqueue.c:228` | `abort();` |
| `ev_30a606aa4ca3` | assignment | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_30c77f45b00f` | call_site | `third_party/libuv/src/unix/process.c:363` | `uv__nonblock_fcntl(fd, 0);` |
| `ev_30e09d139b42` | call_site | `third_party/libuv/src/unix/fs.c:2140` | `PATH2;` |
| `ev_30ed22223da6` | call_site | `third_party/libuv/src/unix/fsevents.c:818` | `handle->cf_cb = uv__malloc(sizeof(*handle->cf_cb));` |
| `ev_30ff8b024343` | call_site | `third_party/libuv/src/unix/proctitle.c:136` | `uv_mutex_lock(&process_title_mutex);` |
| `ev_3104aee8ac8b` | call_site | `third_party/libuv/src/unix/pipe.c:443` | `return uv_guess_handle(handle->accepted_fd);` |
| `ev_3117fdd19179` | call_site | `third_party/libuv/src/unix/stream.c:833` | `if (errno == EPROTOTYPE)` |
| `ev_31214efee850` | call_site | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_314bdfa42d7d` | call_site | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_316a0f657bdf` | call_site | `third_party/libuv/src/heap-inl.h:146` | `while (newnode->parent != NULL && less_than(newnode, newnode->parent))` |
| `ev_316e1ab00ed3` | call_site | `third_party/libuv/src/unix/fs.c:1598` | `uv__to_stat(&pbuf, buf);` |
| `ev_3170248b77e9` | call_site | `third_party/libuv/src/unix/proctitle.c:68` | `new_argv = uv__malloc(size);` |
| `ev_3177919be106` | call_site | `third_party/libuv/src/unix/thread.c:959` | `strncpy(name, thread_name, size - 1);` |
| `ev_317ac5996e3f` | call_site | `third_party/libuv/src/unix/udp.c:990` | `r = setsockopt(handle->io_watcher.fd,` |
| `ev_31a97e201c86` | call_site | `third_party/libuv/src/unix/udp.c:713` | `memset(&mreq, 0, sizeof mreq);` |
| `ev_31b23c175816` | call_site | `third_party/libuv/src/unix/fsevents.c:699` | `uv__free(state);` |
| `ev_31b8a4b1cb83` | assignment | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_31bdf6e88b2a` | call_site | `third_party/libuv/src/unix/fs.c:2084` | `PATH;` |
| `ev_31d9e33334d7` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:96` | `pCFBundleGetBundleWithIdentifier(S("com.apple.LaunchServices"));` |
| `ev_31e09e0e8d86` | call_site | `third_party/libuv/src/threadpool.c:259` | `if (pthread_atfork(NULL, NULL, &reset_once))` |
| `ev_321a4b96b42f` | call_site | `third_party/libuv/src/unix/core.c:570` | `peerfd = accept(sockfd, NULL, NULL);` |
| `ev_3225614f7117` | call_site | `third_party/libuv/src/unix/core.c:1752` | `if (uname(&buf) == -1) {` |
| `ev_32728ea0fc70` | call_site | `third_party/libuv/src/unix/stream.c:136` | `while (r == -1 && errno == EINTR);` |
| `ev_328342f2c2e0` | call_site | `third_party/libuv/src/unix/core.c:230` | `uv__signal_close((uv_signal_t*) handle);` |
| `ev_32ba635dd96b` | call_site | `third_party/libuv/src/unix/fs.c:1810` | `PATH;` |
| `ev_32c419832f76` | call_site | `third_party/libuv/src/unix/core.c:263` | `return UV__ERR(errno);` |
| `ev_32ca5944a889` | call_site | `third_party/libuv/src/unix/process.c:384` | `uv__write_errno(error_fd);` |
| `ev_32d7ade0bfa5` | call_site | `third_party/libuv/src/unix/kqueue.c:431` | `uv__wait_children(loop);` |
| `ev_32e83598423c` | call_site | `third_party/libuv/src/unix/udp.c:442` | `memset(addr, 0, sizeof *addr);` |
| `ev_32f478844005` | call_site | `third_party/libuv/src/unix/tcp.c:565` | `if (setsockopt(fd, IPPROTO_TCP, TCP_KEEPINTVL, &intvl, sizeof(intvl)))` |
| `ev_32feed37e13f` | call_site | `third_party/libuv/src/unix/fsevents.c:696` | `uv_sem_destroy(&state->fsevent_sem);` |
| `ev_3317c301ac1d` | call_site | `third_party/libuv/src/unix/tcp.c:197` | `if (err == -1 && errno != EADDRINUSE) {` |
| `ev_333d65dd5d0f` | call_site | `third_party/libuv/src/unix/stream.c:1442` | `assert(stream->type == UV_TCP \|\| stream->type == UV_NAMED_PIPE \|\|` |
| `ev_3340efa324e2` | call_site | `third_party/libuv/src/unix/core.c:1557` | `memcpy(buffer, buf, len + 1);` |
| `ev_334d13d28e80` | call_site | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_337c398f9950` | assignment | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_33c2014b7ca1` | call_site | `third_party/libuv/src/unix/kqueue.c:332` | `assert(loop->watchers != NULL);` |
| `ev_33c26d46e417` | call_site | `third_party/libuv/src/unix/core.c:630` | `assert(fd > -1);  /* Catch uninitialized io_watcher.fd bugs. */` |
| `ev_33d410574c08` | assignment | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_33d83c1d8263` | call_site | `third_party/libuv/src/unix/pipe.c:167` | `if (listen(uv__stream_fd(handle), backlog))` |
| `ev_34265ee6c4b8` | call_site | `third_party/libuv/src/unix/core.c:1772` | `r = uv__strscpy(buffer->release, buf.release, sizeof(buffer->release));` |
| `ev_345944618114` | call_site | `third_party/libuv/src/unix/fs.c:822` | `errno = ENOMEM;` |
| `ev_348013706178` | call_site | `third_party/libuv/src/unix/process.c:132` | `while (pid == -1 && errno == EINTR);` |
| `ev_348b88fd494a` | call_site | `third_party/libuv/src/unix/core.c:1703` | `max = sched_get_priority_max(policy);` |
| `ev_34caa6c717be` | call_site | `third_party/libuv/src/unix/signal.c:229` | `memset(&sa, 0, sizeof(sa));` |
| `ev_34fe0c6ea62e` | call_site | `third_party/libuv/src/unix/udp.c:1237` | `memset(h, 0, sizeof(*h));` |
| `ev_3511aeaee023` | call_site | `third_party/libuv/src/unix/fs.c:892` | `while (nread == -1 && errno == EINTR);` |
| `ev_353c4309676a` | call_site | `third_party/libuv/src/unix/fsevents.c:597` | `err = uv_mutex_init(&loop->cf_mutex);` |
| `ev_354e1c03ede9` | call_site | `third_party/libuv/src/unix/core.c:1753` | `r = UV__ERR(errno);` |
| `ev_354f7f3ab324` | call_site | `third_party/libuv/src/threadpool.c:108` | `q = uv__queue_head(&slow_io_pending_wq);` |
| `ev_3557efaad119` | call_site | `third_party/libuv/src/unix/kqueue.c:468` | `assert(timeout > 0);` |
| `ev_357d3ffb0b75` | call_site | `third_party/libuv/src/unix/process.c:909` | `err = uv__make_pipe(signal_pipe, 0);` |
| `ev_358cd53fc2e2` | call_site | `third_party/libuv/src/unix/core.c:432` | `r = uv__loop_alive(loop);` |
| `ev_359eadf67b2d` | call_site | `third_party/libuv/src/unix/fsevents.c:640` | `abort();` |
| `ev_35a5f978caed` | call_site | `third_party/libuv/src/timer.c:89` | `heap_insert(timer_heap(handle->loop),` |
| `ev_35af205c4d00` | call_site | `third_party/libuv/src/unix/core.c:1198` | `memcpy(buffer, pwd.homedir, len + 1);` |
| `ev_35d3b86d0f5a` | call_site | `third_party/libuv/src/unix/process.c:836` | `if (pthread_sigmask(SIG_SETMASK, &sigoldset, NULL) != 0)` |
| `ev_35e72a0cafc4` | call_site | `third_party/libuv/src/unix/fs.c:699` | `if (0 != statfs(req->path, &buf))` |
| `ev_35f8f6d9850e` | call_site | `third_party/libuv/src/uv-common.c:509` | `addrlen = uv__udp_check_before_send(handle, addr);` |
| `ev_35f9b6b78ec3` | call_site | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_361ecd4f2ad6` | call_site | `third_party/libuv/src/unix/core.c:1094` | `return UV__ERR(errno);` |
| `ev_36290f58d893` | assignment | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_3640a16324bc` | assignment | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_365ba62f606d` | call_site | `third_party/libuv/src/unix/tcp.c:566` | `return UV__ERR(errno);` |
| `ev_368533d26e47` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:115` | `display_name_key = pCFBundleGetDataPointerForName(launch_services_bundle,` |
| `ev_368e6ff64468` | call_site | `third_party/libuv/src/unix/fs.c:2199` | `PATH;` |
| `ev_369c941d05b6` | call_site | `third_party/libuv/src/fs-poll.c:214` | `if (ctx->busy_polling < 0 \|\| !statbuf_eq(&ctx->statbuf, statbuf))` |
| `ev_36a318f0ce85` | call_site | `third_party/libuv/src/idna.c:497` | `code_point = uv__get_surrogate_value(w_source_ptr, w_source_len);` |
| `ev_36a99a209dfa` | call_site | `third_party/libuv/src/fs-poll.c:153` | `required_len = strlen(ctx->path);` |
| `ev_36a9cdf3e5c8` | call_site | `third_party/libuv/src/unix/stream.c:312` | `return UV__ERR(errno);` |
| `ev_36aabdf686c8` | call_site | `third_party/libuv/src/unix/process.c:1027` | `if (kevent(loop->backend_fd, &event, 1, NULL, 0, NULL)) {` |
| `ev_36b1f9ed36cc` | call_site | `third_party/libuv/src/unix/fs.c:543` | `r = uv__preadv(fd, bufs, nbufs, off);` |
| `ev_36c516a8c3c1` | call_site | `third_party/libuv/src/unix/thread.c:793` | `abort();` |
| `ev_36cb5c78883d` | call_site | `third_party/libuv/src/thread-common.c:102` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_36dae95e80b3` | call_site | `third_party/libuv/src/unix/stream.c:333` | `s = uv__malloc(sizeof(*s) + sread_sz + swrite_sz);` |
| `ev_36eb24fa9546` | call_site | `third_party/libuv/src/unix/stream.c:228` | `assert((s->events == 0) \|\| (stream->flags & UV_HANDLE_CLOSING));` |
| `ev_36ef1a16d4f6` | call_site | `third_party/libuv/src/unix/udp.c:246` | `assert(buf.base != NULL);` |
| `ev_36fbc2ec6099` | call_site | `third_party/libuv/src/unix/stream.c:588` | `memmove(queued_fds->fds,` |
| `ev_37010c37446b` | call_site | `third_party/libuv/src/inet.c:235` | `if ((pch = strchr((xdigits = xdigits_l), ch)) == NULL)` |
| `ev_37129fa210fa` | call_site | `third_party/libuv/src/unix/fs.c:2243` | `memcpy(req->bufs, bufs, nbufs * sizeof(*bufs));` |
| `ev_3713a9c8fb51` | call_site | `third_party/libuv/src/uv-common.c:93` | `return uv__allocator.local_calloc(count, size);` |
| `ev_3717f5d00c57` | call_site | `third_party/libuv/src/unix/tty.c:358` | `uv__tcsetattr(fd, TCSANOW, &orig_termios);` |
| `ev_374464ee690c` | call_site | `third_party/libuv/src/unix/loop.c:185` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_374b3592f790` | call_site | `third_party/libuv/src/unix/udp.c:103` | `q = uv__queue_head(&handle->write_completed_queue);` |
| `ev_377b1f8429df` | call_site | `third_party/libuv/src/unix/signal.c:287` | `uv__close(loop->signal_pipefd[0]);` |
| `ev_37960dbc90d3` | call_site | `third_party/libuv/src/unix/fs.c:1730` | `X(MKDTEMP, uv__fs_mkdtemp(req));` |
| `ev_37dc1b8a6d6f` | call_site | `third_party/libuv/src/unix/udp.c:104` | `uv__queue_remove(q);` |
| `ev_37f7415ebd24` | call_site | `third_party/libuv/src/unix/tty.c:73` | `rc = tcsetattr(fd, how, term);` |
| `ev_3800f3cbc795` | call_site | `third_party/libuv/src/unix/fs.c:1726` | `X(LUTIME, uv__fs_lutime(req));` |
| `ev_380d680f77e0` | call_site | `third_party/libuv/src/unix/fs.c:2140` | `PATH2;` |
| `ev_381f3f57f54d` | call_site | `third_party/libuv/src/unix/fsevents.c:662` | `uv_mutex_destroy(&loop->cf_mutex);` |
| `ev_384a5d3ba77e` | call_site | `third_party/libuv/src/unix/signal.c:343` | `uv__handle_init(loop, (uv_handle_t*) handle, UV_SIGNAL);` |
| `ev_385254c7e5ac` | call_site | `third_party/libuv/src/unix/core.c:472` | `uv__metrics_update_idle_time(loop);` |
| `ev_386a0ee7097f` | call_site | `third_party/libuv/src/uv-common.c:911` | `assert(err == 0);` |
| `ev_388ae875a13e` | assignment | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_3895519364a0` | call_site | `third_party/libuv/src/timer.c:59` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_TIMER);` |
| `ev_38a3cb2ec3da` | call_site | `third_party/libuv/src/unix/loop.c:157` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_38a67460302e` | call_site | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_391541eec937` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_391e69ab4864` | call_site | `third_party/libuv/src/unix/fs.c:1725` | `X(FUTIME, uv__fs_futime(req));` |
| `ev_391f7b5ae52c` | assignment | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_39474c4bbafc` | call_site | `third_party/libuv/src/unix/internal.h:436` | `rc = stat(path, s);` |
| `ev_396feb52b102` | call_site | `third_party/libuv/src/unix/stream.c:456` | `assert(!uv__io_active(&stream->io_watcher, POLLIN \| POLLOUT));` |
| `ev_3972ff248a0c` | call_site | `third_party/libuv/src/unix/stream.c:1470` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_39930c549419` | call_site | `third_party/libuv/src/unix/fs.c:529` | `iovmax = uv__getiovmax();` |
| `ev_39e03bfc37c1` | call_site | `third_party/libuv/src/unix/tcp.c:294` | `err = maybe_new_socket(handle,` |
| `ev_39e40d25f575` | call_site | `third_party/libuv/src/unix/udp.c:830` | `memcpy(&mreq.gsr_group, multicast_addr, sizeof(*multicast_addr));` |
| `ev_39ecd25f3ca8` | call_site | `third_party/libuv/src/unix/fs.c:1873` | `PATH;` |
| `ev_3a05db9c1854` | call_site | `third_party/libuv/src/unix/darwin.c:160` | `assert(err == KERN_SUCCESS);` |
| `ev_3a33ed5af871` | call_site | `third_party/libuv/src/unix/stream.c:1299` | `assert((stream->type == UV_TCP \|\|` |
| `ev_3a67df38aa61` | call_site | `third_party/libuv/src/unix/fs.c:639` | `res = readdir(dir->dir);` |
| `ev_3a84a44ea40a` | call_site | `third_party/libuv/src/unix/process.c:390` | `environ = options->env;` |
| `ev_3a9f18ed1970` | call_site | `third_party/libuv/src/unix/process.c:735` | `memcpy(b + (z - p) + (z > p), options->file, k + 1);` |
| `ev_3aa416f9ff63` | call_site | `third_party/libuv/src/unix/udp.c:215` | `handle->recv_cb(handle, 0, buf, NULL, UV_UDP_MMSG_FREE);` |
| `ev_3aa9d5228b9d` | call_site | `third_party/libuv/src/unix/fsevents.c:804` | `handle->realpath = uv__strdup(buf);` |
| `ev_3abda8191213` | call_site | `third_party/libuv/src/unix/process.c:636` | `assert(err != ENOSYS);` |
| `ev_3aeb1da5f61d` | call_site | `third_party/libuv/src/uv-common.c:158` | `uv__free(grp->members);` |
| `ev_3afdccaa2f17` | call_site | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_3b15b85ef85e` | call_site | `third_party/libuv/src/uv-common.c:864` | `if (uv_loop_init(loop)) {` |
| `ev_3b2af92d9b76` | call_site | `third_party/libuv/src/unix/tcp.c:92` | `sockfd = uv__stream_fd(handle);` |
| `ev_3b3d6976360e` | call_site | `third_party/libuv/src/uv-common.c:226` | `return uv__unknown_err_code(err);` |
| `ev_3b4a6055d7b8` | call_site | `third_party/libuv/src/unix/poll.c:126` | `assert(!uv__is_closing(handle));` |
| `ev_3b53fab5959e` | call_site | `third_party/libuv/src/unix/fs.c:1739` | `X(REALPATH, uv__fs_realpath(req));` |
| `ev_3b55cb8f7ccb` | call_site | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_3b592785b8d0` | call_site | `third_party/libuv/src/unix/process.c:823` | `sigdelset(&signewset, SIGSYS);` |
| `ev_3b7b0ab6b8e2` | call_site | `third_party/libuv/src/unix/core.c:1905` | `abspath_size = strlen(abspath);` |
| `ev_3b8099a64d27` | call_site | `third_party/libuv/src/unix/fs.c:354` | `r = uv__close(r);` |
| `ev_3b942de3815c` | call_site | `third_party/libuv/src/unix/core.c:1070` | `memset(rusage, 0, sizeof(*rusage));` |
| `ev_3baa270ceee6` | call_site | `third_party/libuv/src/unix/kqueue.c:443` | `loop->signal_io_watcher.cb(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_3bafd2a27c12` | call_site | `third_party/libuv/src/unix/udp.c:109` | `handle->send_queue_size -= uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_3bd42f44be98` | call_site | `third_party/libuv/src/unix/process.c:115` | `q = uv__queue_head(h);` |
| `ev_3bd5fab5e7fc` | call_site | `third_party/libuv/src/unix/async.c:58` | `if (kevent(kq, ev, 2, ev, 1, &timeout) < 1 \|\|` |
| `ev_3bd7043bc67f` | call_site | `third_party/libuv/src/unix/fsevents.c:389` | `pFSEventStreamStop(state->fsevent_stream);` |
| `ev_3beb65947784` | call_site | `third_party/libuv/src/unix/stream.c:225` | `uv_sem_wait(&s->async_sem);` |
| `ev_3c01b7fc8ace` | call_site | `third_party/libuv/src/unix/fs.c:1738` | `X(READLINK, uv__fs_readlink(req));` |
| `ev_3c1ae8f72bdf` | call_site | `third_party/libuv/src/unix/signal.c:571` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_3c2a258a8bbd` | call_site | `third_party/libuv/src/unix/random-getentropy.c:51` | `return UV__ERR(errno);` |
| `ev_3c46f0034804` | call_site | `third_party/libuv/src/unix/darwin.c:214` | `*cpu_infos = uv__malloc(numcpus * sizeof(**cpu_infos));` |
| `ev_3c4ded37bf2c` | call_site | `third_party/libuv/src/unix/tcp.c:558` | `if (setsockopt(fd, IPPROTO_TCP, TCP_KEEPALIVE, &idle, sizeof(idle)))` |
| `ev_3c55aae9ae85` | call_site | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_3c9a9e112c0f` | call_site | `third_party/libuv/src/unix/udp.c:462` | `return uv__udp_bind(handle, &taddr.addr, addrlen, flags);` |
| `ev_3ca7ab3b4a85` | call_site | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_3ca994e340f6` | call_site | `third_party/libuv/src/unix/stream.c:1457` | `uv__io_start(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_3cbf38ed895b` | call_site | `third_party/libuv/src/unix/pipe.c:368` | `err = uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_3cbf6f2943ac` | call_site | `third_party/libuv/src/unix/stream.c:392` | `uv__free(s);` |
| `ev_3cd8f67d62ee` | call_site | `third_party/libuv/src/timer.c:119` | `uv_timer_start(handle, handle->timer_cb, handle->repeat, handle->repeat);` |
| `ev_3cde0a7762bb` | call_site | `third_party/libuv/src/unix/fs.c:1774` | `assert(req->result == 0);` |
| `ev_3d08a523a678` | call_site | `third_party/libuv/src/unix/stream.c:1232` | `uv__write_callbacks(stream);` |
| `ev_3d0a8c7b247e` | call_site | `third_party/libuv/src/unix/thread.c:122` | `return uv__default_stack_size();` |
| `ev_3d1b29823210` | call_site | `third_party/libuv/src/uv-common.c:272` | `addr->sin6_port = htons(port);` |
| `ev_3d4062efcbfd` | call_site | `third_party/libuv/src/unix/stream.c:246` | `assert(events != 0);` |
| `ev_3d4ce73526b1` | call_site | `third_party/libuv/src/unix/stream.c:927` | `req->cb(req, req->error);` |
| `ev_3d58159dc058` | call_site | `third_party/libuv/src/unix/tty.c:227` | `r = fcntl(fd, F_SETFL, saved_flags);` |
| `ev_3d66e371f7c6` | call_site | `third_party/libuv/src/unix/loop.c:108` | `uv_mutex_destroy(&loop->wq_mutex);` |
| `ev_3da88c3fad66` | call_site | `third_party/libuv/src/unix/getnameinfo.c:43` | `abort();` |
| `ev_3dd2da93e6a6` | call_site | `third_party/libuv/src/unix/udp.c:388` | `err = uv__sock_reuseaddr(fd);` |
| `ev_3dddfc2a9563` | call_site | `third_party/libuv/src/unix/fs.c:1728` | `X(LINK, link(req->path, req->new_path));` |
| `ev_3dee9447fffc` | call_site | `third_party/libuv/src/unix/random-devurandom.c:55` | `n = read(fd, (char*) buf + pos, buflen - pos);` |
| `ev_3dfa107301c5` | call_site | `third_party/libuv/src/unix/tcp.c:602` | `err =uv__tcp_keepalive(uv__stream_fd(handle), on, delay);` |
| `ev_3e2c02d281e4` | call_site | `third_party/libuv/src/unix/kqueue.c:198` | `assert(w->pevents != 0);` |
| `ev_3e360726c122` | call_site | `third_party/libuv/src/unix/core.c:1157` | `return UV__ERR(errno);` |
| `ev_3e65cdb3deb6` | assignment | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_3e7d5088375a` | call_site | `third_party/libuv/src/unix/fs.c:1873` | `PATH;` |
| `ev_3e841004bc4a` | call_site | `third_party/libuv/src/uv-common.c:99` | `uv__free(ptr);` |
| `ev_3e89b455f40b` | call_site | `third_party/libuv/src/threadpool.c:160` | `uv_mutex_unlock(&mutex);` |
| `ev_3e9fa5a521d7` | call_site | `third_party/libuv/src/threadpool.c:303` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_3eaad1c48470` | call_site | `third_party/libuv/src/unix/darwin.c:195` | `if (sysctlbyname("machdep.cpu.brand_string", &model, &size, NULL, 0) &&` |
| `ev_3ec3987e5ab7` | call_site | `third_party/libuv/src/unix/fsevents.c:805` | `free(buf); /* _Not_ uv__free. */` |
| `ev_3ec69ea652f1` | call_site | `third_party/libuv/src/unix/core.c:906` | `assert(cb != NULL);` |
| `ev_3ece215cf602` | call_site | `third_party/libuv/src/unix/thread.c:484` | `abort();` |
| `ev_3ed4e1e2e5d6` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:162` | `rc = uv__idna_toascii(hostname,` |
| `ev_3ee889c5830d` | call_site | `third_party/libuv/src/unix/stream.c:224` | `uv_async_send(&s->async);` |
| `ev_3f168bc11f83` | call_site | `third_party/libuv/src/unix/stream.c:997` | `assert(cmsg->cmsg_len >= CMSG_LEN(0));` |
| `ev_3f6e1a4fc9f9` | call_site | `third_party/libuv/src/unix/tcp.c:270` | `freeifaddrs(ifa);` |
| `ev_3f85f47d6b4b` | call_site | `third_party/libuv/src/unix/process.c:383` | `if ((options->flags & UV_PROCESS_SETGID) && setgid(options->gid))` |
| `ev_3f87722c298b` | call_site | `third_party/libuv/src/unix/stream.c:1251` | `assert(stream->type == UV_TCP \|\| stream->type == UV_NAMED_PIPE);` |
| `ev_3f8df32eb85c` | call_site | `third_party/libuv/src/unix/pipe.c:515` | `if ((err = uv__cloexec(temp[0], 1)))` |
| `ev_3fbb0975ce2b` | call_site | `third_party/libuv/src/unix/pipe.c:126` | `memcpy(&saddr.sun_path, name, namelen);` |
| `ev_3fcb548be170` | call_site | `third_party/libuv/src/unix/fs.c:1679` | `req->nbufs = uv__fs_buf_offset(req->bufs, result);` |
| `ev_3fd180cfb651` | call_site | `third_party/libuv/src/unix/fs.c:594` | `free(dents);` |
| `ev_40056aa4b1f0` | call_site | `third_party/libuv/src/unix/tcp.c:602` | `err =uv__tcp_keepalive(uv__stream_fd(handle), on, delay);` |
| `ev_405124f0cf19` | call_site | `third_party/libuv/src/unix/core.c:1284` | `uv__free(buf);` |
| `ev_407963a13616` | call_site | `third_party/libuv/src/idna.c:233` | `assert(c != UINT_MAX);` |
| `ev_4085af6e2b7b` | call_site | `third_party/libuv/src/unix/fs.c:1428` | `err = uv__close_nocheckstdio(dstfd);` |
| `ev_408699e87ca2` | call_site | `third_party/libuv/src/unix/async.c:342` | `uv__queue_remove(q);` |
| `ev_40adfaff942c` | call_site | `third_party/libuv/src/inet.c:80` | `memset(words, '\0', sizeof words);` |
| `ev_40d274cc6eec` | call_site | `third_party/libuv/src/unix/fs.c:777` | `len = readlink(req->path, buf, maxlen);` |
| `ev_40e265cad30c` | call_site | `third_party/libuv/src/unix/async.c:168` | `assert(w == &loop->async_io_watcher);` |
| `ev_40f5fa3e419d` | call_site | `third_party/libuv/src/unix/process.c:265` | `_exit(127);` |
| `ev_40f9f26406f0` | call_site | `third_party/libuv/src/unix/stream.c:1059` | `assert(buf.base != NULL);` |
| `ev_410832dd0f24` | call_site | `third_party/libuv/src/unix/signal.c:531` | `assert(!uv__is_closing(handle));` |
| `ev_4129ae23f459` | call_site | `third_party/libuv/src/unix/stream.c:632` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_41650290dce6` | call_site | `third_party/libuv/src/unix/random-devurandom.c:64` | `uv__close(fd);` |
| `ev_41912e441032` | assignment | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_419354d44a35` | call_site | `third_party/libuv/src/unix/core.c:1303` | `uv__free(buf);` |
| `ev_41a0ad9a2598` | call_site | `third_party/libuv/src/unix/loop.c:184` | `assert(!uv__has_active_reqs(loop));` |
| `ev_41c1b22f91f1` | call_site | `third_party/libuv/src/unix/signal.c:104` | `abort();` |
| `ev_41d4eb66d524` | call_site | `third_party/libuv/src/unix/process.c:934` | `assert(err == *pid);` |
| `ev_41db092268b7` | call_site | `third_party/libuv/src/unix/tcp.c:406` | `if (errno == EINVAL) {` |
| `ev_4223c575da12` | call_site | `third_party/libuv/src/unix/kqueue.c:195` | `uv__queue_init(q);` |
| `ev_42299d1e0e40` | call_site | `third_party/libuv/src/unix/core.c:1414` | `return uv__getpwuid_r(pwd, geteuid());` |
| `ev_422a17a181ac` | call_site | `third_party/libuv/src/unix/udp.c:458` | `assert(0 && "unsupported address family");` |
| `ev_423b65c48d84` | call_site | `third_party/libuv/src/unix/kqueue.c:379` | `w->cb(loop, w, ev->fflags); /* XXX always uv__fs_event() */` |
| `ev_4243945f12c5` | call_site | `third_party/libuv/src/unix/stream.c:1519` | `uv_sem_post(&s->async_sem);` |
| `ev_42463528e0e3` | call_site | `third_party/libuv/src/unix/fs.c:2074` | `PATH;` |
| `ev_4313f69454a6` | call_site | `third_party/libuv/src/unix/fs.c:1743` | `X(STAT, uv__fs_stat(req->path, &req->statbuf));` |
| `ev_4327a4c3a955` | call_site | `third_party/libuv/src/unix/stream.c:916` | `uv__req_unregister(stream->loop);` |
| `ev_432a855eeb80` | call_site | `third_party/libuv/src/unix/kqueue.c:300` | `pthread_sigmask(SIG_UNBLOCK, pset, NULL);` |
| `ev_435c5b108fba` | call_site | `third_party/libuv/src/unix/process.c:925` | `r = read(signal_pipe[0], &exec_errorno, sizeof(exec_errorno));` |
| `ev_436d392d1127` | call_site | `third_party/libuv/src/unix/thread.c:909` | `int err = pthread_setname_np(namebuf);` |
| `ev_4371d63878bf` | call_site | `third_party/libuv/src/unix/process.c:380` | `SAVE_ERRNO(setgroups(0, NULL));` |
| `ev_43add662811b` | call_site | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_43c047acb158` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:243` | `memcpy(buffer, ifname_buf, len);` |
| `ev_43c7ad61028b` | call_site | `third_party/libuv/src/unix/async.c:370` | `q = uv__queue_head(&queue);` |
| `ev_43d30dd38d44` | call_site | `third_party/libuv/src/unix/process.c:219` | `assert(0 && "Unexpected flags");` |
| `ev_43e9cd62ea58` | call_site | `third_party/libuv/src/unix/udp.c:194` | `if (nread == 0 \|\| errno == EAGAIN \|\| errno == EWOULDBLOCK)` |
| `ev_43f1c5da265e` | call_site | `third_party/libuv/src/unix/udp.c:1223` | `if (!uv__io_active(&handle->io_watcher, POLLOUT))` |
| `ev_43f3efbeb7d4` | call_site | `third_party/libuv/src/unix/udp.c:143` | `assert(handle->type == UV_UDP);` |
| `ev_43f5f73c73c9` | call_site | `third_party/libuv/src/unix/core.c:1828` | `if (gettimeofday(&time, NULL) != 0)` |
| `ev_43fa6052808b` | call_site | `third_party/libuv/src/unix/darwin.c:216` | `vm_deallocate(mach_task_self(), (vm_address_t)info, msg_type);` |
| `ev_4400131fe7b3` | call_site | `third_party/libuv/src/fs-poll.c:183` | `if (uv_fs_stat(ctx->loop, &ctx->fs_req, ctx->path, poll_cb))` |
| `ev_440f71fd7cf0` | assignment | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_44318f0bb23a` | call_site | `third_party/libuv/src/uv-common.c:568` | `walk_cb(h, arg);` |
| `ev_443ef202672e` | call_site | `third_party/libuv/src/unix/fs.c:1968` | `PATH2;` |
| `ev_444bcae4650a` | call_site | `third_party/libuv/src/unix/tcp.c:346` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_4457c7c20d40` | call_site | `third_party/libuv/src/unix/core.c:1312` | `memcpy(pwd->homedir, pw.pw_dir, homedir_size);` |
| `ev_4472bb7e6a84` | call_site | `third_party/libuv/src/unix/fsevents.c:882` | `assert(handle != NULL);` |
| `ev_447401d0c835` | call_site | `third_party/libuv/src/unix/loop.c:37` | `memset(loop, 0, sizeof(*loop));` |
| `ev_44a22989e51a` | call_site | `third_party/libuv/src/unix/udp.c:643` | `err = uv__udp_maybe_deferred_bind(handle, addr->sa_family, 0);` |
| `ev_44a9eb2cadec` | call_site | `third_party/libuv/src/unix/thread.c:809` | `if (pthread_cond_broadcast(cond))` |
| `ev_44b72ea3df33` | call_site | `third_party/libuv/src/unix/udp.c:231` | `assert(handle->recv_cb != NULL);` |
| `ev_44c5dcdf2475` | call_site | `third_party/libuv/src/unix/udp.c:621` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_44ddab761f91` | call_site | `third_party/libuv/src/unix/process.c:655` | `if (strncmp(*env_iterator, path_var, sizeof(path_var) - 1) == 0) {` |
| `ev_44ebe9a6e192` | call_site | `third_party/libuv/src/unix/fsevents.c:781` | `pCFRunLoopSourceSignal(state->signal_source);` |
| `ev_450ba561786a` | call_site | `third_party/libuv/src/unix/kqueue.c:378` | `uv__metrics_update_idle_time(loop);` |
| `ev_452a8185aed7` | call_site | `third_party/libuv/src/unix/fsevents.c:543` | `V(core_foundation_handle, CFRelease);` |
| `ev_4537864157be` | call_site | `third_party/libuv/src/unix/fsevents.c:622` | `state->signal_source = pCFRunLoopSourceCreate(NULL, 0, &ctx);` |
| `ev_45a6729b760f` | call_site | `third_party/libuv/src/unix/core.c:1918` | `token = uv__strtok(NULL, ":", &itr);` |
| `ev_45cb9bff4592` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_45fdbbe3c990` | call_site | `third_party/libuv/src/unix/kqueue.c:138` | `return UV__ERR(errno);` |
| `ev_4620534ff25f` | call_site | `third_party/libuv/src/unix/process.c:436` | `if (sysctl(which, ARRAY_SIZE(which), buf, &len, NULL, 0))` |
| `ev_4660a5e441db` | call_site | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_4680b7cc8dd9` | call_site | `third_party/libuv/src/unix/async.c:276` | `uv_once(&kqueue_runtime_detection_guard, uv__kqueue_runtime_detection);` |
| `ev_4697c2148c33` | call_site | `third_party/libuv/src/unix/core.c:1609` | `if (setpriority(PRIO_PROCESS, (int) pid, priority) != 0)` |
| `ev_46bdda91e596` | call_site | `third_party/libuv/src/unix/core.c:1131` | `abort();` |
| `ev_46c001c613d4` | call_site | `third_party/libuv/src/unix/pipe.c:248` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_46e211d4dc45` | call_site | `third_party/libuv/src/unix/thread.c:129` | `return uv_thread_create_ex(tid, &params, entry, arg);` |
| `ev_46f1e541bca9` | call_site | `third_party/libuv/src/unix/poll.c:71` | `if (uv__fd_exists(loop, fd))` |
| `ev_471719867f20` | call_site | `third_party/libuv/src/uv-common.c:746` | `nbufs = uv__get_nbufs(req);` |
| `ev_4742f24d0fbc` | call_site | `third_party/libuv/src/unix/pipe.c:172` | `uv__io_start(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_477038c97627` | call_site | `third_party/libuv/src/unix/stream.c:640` | `assert(req);` |
| `ev_4774e0afabce` | call_site | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_47c82a7acda6` | call_site | `third_party/libuv/src/inet.c:38` | `return (inet_ntop4(src, dst, size));` |
| `ev_480ef7d1478b` | call_site | `third_party/libuv/src/unix/udp.c:713` | `memset(&mreq, 0, sizeof mreq);` |
| `ev_4813a53bc506` | call_site | `third_party/libuv/src/threadpool.c:330` | `w->done(w, err);` |
| `ev_484a3d7c80b8` | call_site | `third_party/libuv/src/unix/fsevents.c:445` | `q = uv__queue_next(q);` |
| `ev_48641e4f806c` | call_site | `third_party/libuv/src/unix/fsevents.c:434` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_488c19f1b6d1` | call_site | `third_party/libuv/src/unix/kqueue.c:377` | `assert(w->pevents == POLLIN);` |
| `ev_4898e3f47d20` | call_site | `third_party/libuv/src/unix/tcp.c:662` | `if ((err = uv__nonblock(temp[1], 1)))` |
| `ev_48a49234f802` | call_site | `third_party/libuv/src/unix/signal.c:238` | `if (sigaction(signum, &sa, NULL))` |
| `ev_48cced63af3e` | call_site | `third_party/libuv/src/unix/process.c:826` | `abort();` |
| `ev_490f82ac4ddf` | call_site | `third_party/libuv/src/unix/process.c:780` | `err = uv__spawn_set_posix_spawn_file_actions(&actions,` |
| `ev_4933bc379533` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_494cd2613af4` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:117` | `memset(&address->netmask, 0, sizeof(address->netmask));` |
| `ev_497444ca5f8b` | call_site | `third_party/libuv/src/unix/core.c:360` | `uv__queue_remove(&handle->handle_queue);` |
| `ev_4979de6306dc` | call_site | `third_party/libuv/src/unix/tty.c:293` | `rc = tcgetattr(fd, &tty->orig_termios);` |
| `ev_497ab9fc8fd0` | call_site | `third_party/libuv/src/unix/signal.c:160` | `if (pthread_sigmask(SIG_SETMASK, saved_sigmask, NULL))` |
| `ev_497f4a4b673d` | assignment | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_498eaf90d8b5` | call_site | `third_party/libuv/src/unix/poll.c:124` | `assert((pevents & ~(UV_READABLE \| UV_WRITABLE \| UV_DISCONNECT \|` |
| `ev_499353c12dbf` | call_site | `third_party/libuv/src/unix/kqueue.c:137` | `if (kevent(loop->backend_fd, ev, 2, NULL, 0, NULL))` |
| `ev_4994604f67d9` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_49b2cd364975` | call_site | `third_party/libuv/src/unix/udp.c:666` | `memset(&mreq, 0, sizeof mreq);` |
| `ev_49bbc66fa565` | call_site | `third_party/libuv/src/timer.c:100` | `heap_remove(timer_heap(handle->loop),` |
| `ev_49be1a3702f3` | call_site | `third_party/libuv/src/unix/tcp.c:410` | `errno = 0;` |
| `ev_49cff6d36c47` | call_site | `third_party/libuv/src/unix/udp.c:243` | `handle->recv_cb(handle, UV_ENOBUFS, &buf, NULL, 0);` |
| `ev_49d4611886a9` | call_site | `third_party/libuv/src/unix/process.c:828` | `*pid = fork();` |
| `ev_49de6b22fe6c` | call_site | `third_party/libuv/src/unix/pipe.c:527` | `if ((err = uv__nonblock(temp[1], 1)))` |
| `ev_4a1049af6085` | call_site | `third_party/libuv/src/unix/async.c:141` | `uv__cpu_relax();` |
| `ev_4a427616726f` | call_site | `third_party/libuv/src/timer.c:149` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_4a54c458effe` | call_site | `third_party/libuv/src/unix/random-devurandom.c:69` | `uv__close(fd);` |
| `ev_4a7178747dc2` | call_site | `third_party/libuv/src/unix/udp.c:1272` | `r = sendmsg(fd, &h, 0);` |
| `ev_4ad4ee7787ef` | call_site | `third_party/libuv/src/unix/fsevents.c:546` | `V(core_foundation_handle, CFRunLoopRemoveSource);` |
| `ev_4af657080f7a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:175` | `buf = uv__malloc(hostname_len + service_len + hints_len);` |
| `ev_4afb722ab47d` | call_site | `third_party/libuv/src/unix/tcp.c:303` | `tmp6.sin6_scope_id = uv__ipv6_link_local_scope_id();` |
| `ev_4b1a4f1e0390` | call_site | `third_party/libuv/src/unix/udp.c:102` | `while (!uv__queue_empty(&handle->write_completed_queue)) {` |
| `ev_4b3607f42daf` | call_site | `third_party/libuv/src/unix/stream.c:166` | `if (uv_sem_trywait(&s->close_sem) == 0)` |
| `ev_4b5a8cb91d04` | call_site | `third_party/libuv/src/unix/udp.c:382` | `err = uv__set_recverr(fd, addr->sa_family);` |
| `ev_4b6f96a92262` | call_site | `third_party/libuv/src/unix/process.c:157` | `q = uv__queue_next(q);` |
| `ev_4b9bf329aa70` | call_site | `third_party/libuv/src/unix/core.c:907` | `assert(fd >= -1);` |
| `ev_4ba518cf5ab4` | call_site | `third_party/libuv/src/unix/stream.c:1059` | `assert(buf.base != NULL);` |
| `ev_4bae0407c446` | call_site | `third_party/libuv/src/unix/thread.c:295` | `return UV__ERR(pthread_join(*tid, NULL));` |
| `ev_4bc3828d6565` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:118` | `uv__free(req->service);` |
| `ev_4bcb8190029f` | call_site | `third_party/libuv/src/unix/async.c:65` | `uv__close(kq);` |
| `ev_4c01dabae99b` | call_site | `third_party/libuv/src/unix/core.c:1784` | `r = uv__strscpy(buffer->machine, buf.machine, sizeof(buffer->machine));` |
| `ev_4c0ca12d187a` | call_site | `third_party/libuv/src/unix/fs.c:767` | `buf = uv__malloc(maxlen);` |
| `ev_4c1f54c951eb` | call_site | `third_party/libuv/src/unix/core.c:1373` | `name_size = strlen(gp.gr_name) + 1;` |
| `ev_4c2d3bc5c155` | call_site | `third_party/libuv/src/uv-common.c:72` | `return memcpy(m, s, len);` |
| `ev_4c335fd37666` | call_site | `third_party/libuv/src/unix/fsevents.c:853` | `uv__free(handle->cf_cb);` |
| `ev_4c35c6d99f34` | call_site | `third_party/libuv/src/unix/stream.c:98` | `uv__queue_init(&stream->write_completed_queue);` |
| `ev_4c3c5e690c47` | call_site | `third_party/libuv/src/uv-common.c:341` | `return uv__tcp_bind(handle, addr, addrlen, flags);` |
| `ev_4c3cfeea5670` | call_site | `third_party/libuv/src/inet.c:296` | `memcpy(dst, tmp, sizeof tmp);` |
| `ev_4c5e05d9a7c9` | call_site | `third_party/libuv/src/unix/process.c:832` | `uv__process_child_init(options, stdio_count, pipes, error_fd);` |
| `ev_4c5e81c9fb3a` | call_site | `third_party/libuv/src/uv-common.c:1003` | `exit_time = uv_hrtime();` |
| `ev_4c6b304b2aac` | call_site | `third_party/libuv/src/threadpool.c:248` | `memcpy(&once, &child_once, sizeof(child_once));` |
| `ev_4c9af180f176` | call_site | `third_party/libuv/src/unix/fs.c:1755` | `req->result = UV__ERR(errno);` |
| `ev_4ca7298a513b` | call_site | `third_party/libuv/src/unix/stream.c:469` | `assert(stream->write_queue_size == 0);` |
| `ev_4ca86b17fc93` | call_site | `third_party/libuv/src/unix/udp.c:1400` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_4cad4aafb048` | call_site | `third_party/libuv/src/unix/stream.c:1197` | `assert(!(stream->flags & UV_HANDLE_CLOSING));` |
| `ev_4caf0c74df12` | call_site | `third_party/libuv/src/unix/process.c:452` | `uv__spawn_init_can_use_setsid();` |
| `ev_4cd9bc4c3b3c` | call_site | `third_party/libuv/src/unix/process.c:298` | `if (SIG_ERR != signal(n, SIG_DFL))` |
| `ev_4d01fb12465f` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:98` | `freeifaddrs(addrs);` |
| `ev_4d0ef7488403` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_4d1131bbe680` | call_site | `third_party/libuv/src/fs-poll.c:75` | `if (uv_is_active((uv_handle_t*)handle))` |
| `ev_4d14652a2e2a` | call_site | `third_party/libuv/src/unix/fs.c:1954` | `PATH;` |
| `ev_4d2d59b148ba` | call_site | `third_party/libuv/src/unix/fs.c:1128` | `errno == EIO \|\|` |
| `ev_4d2e105e2302` | call_site | `third_party/libuv/src/unix/fs.c:1798` | `PATH;` |
| `ev_4d5277e06514` | call_site | `third_party/libuv/src/unix/udp.c:197` | `handle->recv_cb(handle, UV__ERR(errno), buf, NULL, 0);` |
| `ev_4d94708ba07e` | call_site | `third_party/libuv/src/unix/tty.c:159` | `saved_flags = fcntl(fd, F_GETFL);` |
| `ev_4d96ed347579` | call_site | `third_party/libuv/src/unix/udp.c:591` | `memcpy(&req->u.storage, addr, addrlen);` |
| `ev_4dc43affd48c` | call_site | `third_party/libuv/src/unix/fsevents.c:747` | `uv__queue_remove(item);` |
| `ev_4dcb5b6818f2` | call_site | `third_party/libuv/src/unix/udp.c:323` | `return UV__ERR(errno);` |
| `ev_4de397bdc926` | call_site | `third_party/libuv/src/unix/thread.c:181` | `err = pthread_create(tid, attr, f.out, arg);` |
| `ev_4e0450891acb` | call_site | `third_party/libuv/src/fs-poll.c:248` | `uv__make_close_pending((uv_handle_t*)handle);` |
| `ev_4e17d17ade1f` | assignment | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_4e8d75a656fb` | assignment | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_4eb09f591023` | call_site | `third_party/libuv/src/unix/fs.c:184` | `r = fcntl(req->file, 85 /* F_BARRIERFSYNC */);  /* fsync + barrier */` |
| `ev_4ed8d0431328` | call_site | `third_party/libuv/src/unix/stream.c:170` | `memset(s->sread, 0, s->sread_sz);` |
| `ev_4eda124e0e13` | call_site | `third_party/libuv/src/threadpool.c:271` | `uv_once(&once, init_once);` |
| `ev_4ef2aa7dba80` | call_site | `third_party/libuv/src/unix/fs.c:2150` | `PATH;` |
| `ev_4f1e439ac388` | call_site | `third_party/libuv/src/unix/pipe.c:308` | `if (r == -1 && errno != EINPROGRESS) {` |
| `ev_4f228b617626` | call_site | `third_party/libuv/src/unix/core.c:1454` | `ptr = strchr(buf, '=');` |
| `ev_4f3c17d6ab12` | call_site | `third_party/libuv/src/threadpool.c:176` | `post(&exit_message, UV__WORK_CPU);` |
| `ev_4fc575c4e877` | call_site | `third_party/libuv/src/unix/getnameinfo.c:90` | `memcpy(&req->storage,` |
| `ev_4fc9785bf93d` | call_site | `third_party/libuv/src/thread-common.c:79` | `uv__free(b);` |
| `ev_4fcc0b521403` | call_site | `third_party/libuv/src/unix/thread.c:477` | `if (semaphore_destroy(mach_task_self(), *sem))` |
| `ev_4fcf48ade5c6` | call_site | `third_party/libuv/src/unix/fs.c:2150` | `PATH;` |
| `ev_4fe71ee7ac1f` | call_site | `third_party/libuv/src/unix/stream.c:1183` | `uv__io_feed(stream->loop, &stream->io_watcher);` |
| `ev_4ffc29f60334` | call_site | `third_party/libuv/src/unix/fs.c:458` | `return uv__preadv_or_pwritev_emul(fd, bufs, nbufs, off, /*is_pread*/0);` |
| `ev_501470ecaa9e` | call_site | `third_party/libuv/src/unix/darwin.c:174` | `return UV__ERR(errno);` |
| `ev_501af8139273` | assignment | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_502a77f997cd` | call_site | `third_party/libuv/src/unix/stream.c:935` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_506ace48261c` | call_site | `third_party/libuv/src/unix/pipe.c:185` | `unlink(handle->pipe_fname);` |
| `ev_5087f57ad22c` | call_site | `third_party/libuv/src/unix/thread.c:391` | `return UV__ERR(pthread_rwlock_init(rwlock, NULL));` |
| `ev_5092d4aa49e1` | assignment | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_5095876400c4` | call_site | `third_party/libuv/src/unix/tcp.c:584` | `err = uv__tcp_nodelay(uv__stream_fd(handle), on);` |
| `ev_50b6439ff1fa` | call_site | `third_party/libuv/src/unix/pipe.c:411` | `return uv__pipe_getsockpeername(handle, getpeername, buffer, size);` |
| `ev_50b6e91bac57` | call_site | `third_party/libuv/src/uv-common.c:72` | `return memcpy(m, s, len);` |
| `ev_50d9af222527` | call_site | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_50efcb4b3bf7` | call_site | `third_party/libuv/src/unix/pipe.c:454` | `if (handle == NULL \|\| uv__stream_fd(handle) == -1)` |
| `ev_50f1bcb1da8b` | call_site | `third_party/libuv/src/unix/signal.c:256` | `if (sigaction(signum, &sa, NULL))` |
| `ev_50f44f64675e` | call_site | `third_party/libuv/src/fs-poll.c:151` | `assert(ctx != NULL);` |
| `ev_50f623ebdbe0` | call_site | `third_party/libuv/src/unix/udp.c:831` | `memcpy(&mreq.gsr_source, source_addr, sizeof(*source_addr));` |
| `ev_51025a5521ec` | call_site | `third_party/libuv/src/fs-poll.c:99` | `err = uv_fs_stat(loop, &ctx->fs_req, ctx->path, poll_cb);` |
| `ev_510c05e6e0b3` | call_site | `third_party/libuv/src/unix/stream.c:666` | `return writev(fd, vec, n);` |
| `ev_5124df63dfc2` | call_site | `third_party/libuv/src/unix/tcp.c:412` | `return UV__ERR(errno);` |
| `ev_512ae64e62ae` | call_site | `third_party/libuv/src/unix/fs.c:664` | `uv__free((char*) dir->dirents[i].name);` |
| `ev_5133b749df90` | call_site | `third_party/libuv/src/unix/stream.c:915` | `uv__queue_remove(q);` |
| `ev_513e3cadc773` | call_site | `third_party/libuv/src/uv-common.c:860` | `loop = uv__malloc(sizeof(*loop));` |
| `ev_5149297a9ce2` | call_site | `third_party/libuv/src/unix/udp.c:146` | `uv__udp_recvmsg(handle);` |
| `ev_515f624f8add` | call_site | `third_party/libuv/src/unix/fs.c:1823` | `PATH;` |
| `ev_51615468af5f` | call_site | `third_party/libuv/src/unix/core.c:553` | `uv__close(fd);` |
| `ev_5170b36f45dc` | call_site | `third_party/libuv/src/unix/loop.c:69` | `uv__update_time(loop);` |
| `ev_5184c63db79c` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:120` | `uv__free(req->hostname);` |
| `ev_519bf130b762` | call_site | `third_party/libuv/src/unix/core.c:1134` | `return UV__ERR(errno);` |
| `ev_51c88169d0f8` | call_site | `third_party/libuv/src/unix/udp.c:547` | `} while (r == -1 && errno == EINTR);` |
| `ev_51ce14db5db1` | call_site | `third_party/libuv/src/unix/thread.c:396` | `if (pthread_rwlock_destroy(rwlock))` |
| `ev_51e84415b051` | call_site | `third_party/libuv/src/idna.c:408` | `assert(w_target_len == 0);` |
| `ev_51ec4e066304` | call_site | `third_party/libuv/src/unix/darwin.c:43` | `return UV__ERR(errno);` |
| `ev_51f56cb20b31` | call_site | `third_party/libuv/src/threadpool.c:66` | `uv_mutex_lock(&mutex);` |
| `ev_520f44354230` | call_site | `third_party/libuv/src/unix/stream.c:735` | `uv__queue_insert_tail(&stream->write_completed_queue, &req->queue);` |
| `ev_521dbf60ba46` | call_site | `third_party/libuv/src/unix/fsevents.c:899` | `uv__free(handle->realpath);` |
| `ev_52237ffe7746` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:122` | `assert(0);` |
| `ev_5232ee615aad` | call_site | `third_party/libuv/src/unix/pipe.c:236` | `err = uv_pipe_connect2(req, handle, name, strlen(name), 0, cb);` |
| `ev_5239bb731512` | call_site | `third_party/libuv/src/unix/core.c:1829` | `return UV__ERR(errno);` |
| `ev_5242f99b85c5` | call_site | `third_party/libuv/src/unix/pipe.c:512` | `if (pipe(temp))` |
| `ev_52577897d19d` | call_site | `third_party/libuv/src/unix/fsevents.c:437` | `paths = uv__malloc(sizeof(*paths) * path_count);` |
| `ev_5259063e5319` | call_site | `third_party/libuv/src/unix/fs.c:1723` | `X(FSYNC, uv__fs_fsync(req));` |
| `ev_5265c80a4731` | call_site | `third_party/libuv/src/unix/async.c:154` | `uv__async_spin(handle);` |
| `ev_52848d00ed31` | call_site | `third_party/libuv/src/unix/async.c:239` | `abort();` |
| `ev_52a5c033af1e` | call_site | `third_party/libuv/src/unix/fs.c:651` | `dirent->name = uv__strdup(res->d_name);` |
| `ev_52a7281f16ea` | call_site | `third_party/libuv/src/unix/fs.c:620` | `uv__free(dir);` |
| `ev_52ac4599ca7e` | call_site | `third_party/libuv/src/unix/loop.c:52` | `heap_init((struct heap*) &loop->timer_heap);` |
| `ev_52b644e4d1b8` | call_site | `third_party/libuv/src/uv-common.c:236` | `UV_ERRNO_MAP(UV_STRERROR_GEN_R)` |
| `ev_52e5aa51f8d6` | call_site | `third_party/libuv/src/unix/stream.c:813` | `n = uv__writev(uv__stream_fd(stream), iov, iovcnt);` |
| `ev_52fd3aa290e7` | call_site | `third_party/libuv/src/unix/tcp.c:74` | `uv__close(sockfd);` |
| `ev_5307abe95af8` | call_site | `third_party/libuv/src/unix/darwin.c:50` | `uv__fsevents_loop_delete(loop);` |
| `ev_532c486d46cf` | call_site | `third_party/libuv/src/thread-common.c:134` | `assert(b->in == 0);` |
| `ev_534cb57df4a2` | call_site | `third_party/libuv/src/unix/fs.c:1163` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_53777d734369` | call_site | `third_party/libuv/src/unix/darwin.c:56` | `abort();` |
| `ev_53bc2f6bea0c` | call_site | `third_party/libuv/src/unix/udp.c:1402` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_53bfb4a21c78` | call_site | `third_party/libuv/src/unix/fsevents.c:879` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_53db02f942c8` | call_site | `third_party/libuv/src/unix/kqueue.c:562` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_FS_EVENT);` |
| `ev_53debda5b8f2` | call_site | `third_party/libuv/src/unix/fs.c:2022` | `PATH;` |
| `ev_540bbe771510` | call_site | `third_party/libuv/src/unix/kqueue.c:149` | `if (0 == kevent(kqfd, &change, 1, NULL, 0, NULL))` |
| `ev_540e0a218219` | call_site | `third_party/libuv/src/unix/fsevents.c:189` | `handle->cb(handle, event->path[0] ? event->path : NULL, event->events, 0);` |
| `ev_5410c16778b6` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:147` | `pCFBundleGetInfoDictionary(pCFBundleGetMainBundle()));` |
| `ev_54140d67df82` | call_site | `third_party/libuv/src/idna.c:233` | `assert(c != UINT_MAX);` |
| `ev_5425e8e14f2c` | assignment | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_544347c516ac` | call_site | `third_party/libuv/src/unix/stream.c:497` | `uv__close(err);` |
| `ev_5446f71c1fe6` | assignment | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_546cbc781075` | call_site | `third_party/libuv/src/unix/core.c:646` | `assert(fd > STDERR_FILENO);  /* Catch stdio close bugs. */` |
| `ev_5481c624c3b2` | call_site | `third_party/libuv/src/inet.c:209` | `memcpy(dst, tmp, sizeof(struct in_addr));` |
| `ev_5491ee86113d` | call_site | `third_party/libuv/src/unix/fsevents.c:552` | `V(core_foundation_handle, CFStringCreateWithFileSystemRepresentation);` |
| `ev_54968c2ac81c` | call_site | `third_party/libuv/src/inet.c:163` | `memcpy(s, src, len);` |
| `ev_54a84ccd5390` | assignment | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_54fc1fdf3132` | call_site | `third_party/libuv/src/unix/fs.c:1307` | `if (ftruncate(dstfd, 0) != 0) {` |
| `ev_5503b743a615` | call_site | `third_party/libuv/src/unix/udp.c:605` | `memcpy(req->bufs, bufs, nbufs * sizeof(bufs[0]));` |
| `ev_552aa6bee2f5` | call_site | `third_party/libuv/src/inet.c:40` | `return (inet_ntop6(src, dst, size));` |
| `ev_554360576ea4` | call_site | `third_party/libuv/src/unix/tty.c:330` | `rc = uv__tcsetattr(fd, TCSADRAIN, &tmp);` |
| `ev_554dc70a4830` | call_site | `third_party/libuv/src/idna.c:252` | `assert(c != UINT_MAX);` |
| `ev_55577e1bbafb` | call_site | `third_party/libuv/src/unix/pipe.c:57` | `return uv_pipe_bind2(handle, name, strlen(name), 0);` |
| `ev_5598c0090e96` | call_site | `third_party/libuv/src/unix/tty.c:183` | `r = uv__open_cloexec(path, mode \| O_NOCTTY);` |
| `ev_55a83a9faa7e` | call_site | `third_party/libuv/src/unix/thread.c:507` | `err = semaphore_timedwait(*sem, interval);` |
| `ev_55ba9ba8e2f3` | call_site | `third_party/libuv/src/unix/stream.c:1111` | `uv__stream_eof(stream, &buf);` |
| `ev_55bf1551da09` | call_site | `third_party/libuv/src/unix/pipe.c:394` | `memcpy(buffer, sa.sun_path, addrlen);` |
| `ev_55c7f02f05c4` | call_site | `third_party/libuv/src/unix/stream.c:116` | `uv__io_init(&stream->io_watcher, uv__stream_io, -1);` |
| `ev_55dfc4a5d81d` | call_site | `third_party/libuv/src/unix/signal.c:196` | `for (handle = uv__signal_first_handle(signum);` |
| `ev_55f65c923a05` | call_site | `third_party/libuv/src/unix/core.c:1504` | `memcpy(buffer, var, len + 1);` |
| `ev_5619dff01858` | call_site | `third_party/libuv/src/threadpool.c:287` | `uv_mutex_lock(&w->loop->wq_mutex);` |
| `ev_5626f3d79137` | call_site | `third_party/libuv/src/unix/fs.c:1798` | `PATH;` |
| `ev_5631ee89fbf2` | call_site | `third_party/libuv/src/unix/core.c:1815` | `if (func(fd, name, &socklen))` |
| `ev_5649846deaaf` | call_site | `third_party/libuv/src/unix/stream.c:938` | `stream->read_cb(stream, UV_EOF, buf);` |
| `ev_5650a69d222c` | call_site | `third_party/libuv/src/unix/fs.c:1129` | `errno == ENOTSOCK \|\|` |
| `ev_5664b00e3118` | call_site | `third_party/libuv/src/unix/core.c:315` | `assert(!(handle->flags & UV_HANDLE_CLOSED));` |
| `ev_566ec74a2aac` | call_site | `third_party/libuv/src/unix/pipe.c:535` | `uv__close(temp[0]);` |
| `ev_5675ec5f6895` | call_site | `third_party/libuv/src/unix/stream.c:250` | `if ((events & POLLIN) && uv__io_active(&stream->io_watcher, POLLIN))` |
| `ev_56841b856f6a` | call_site | `third_party/libuv/src/unix/core.c:1875` | `abspath_size = strlen(abspath);` |
| `ev_5685aa20daa9` | call_site | `third_party/libuv/src/unix/fsevents.c:646` | `uv_sem_wait(&loop->cf_sem);` |
| `ev_56b5cece58e6` | call_site | `third_party/libuv/src/unix/thread.c:513` | `abort();` |
| `ev_56beef52d14e` | call_site | `third_party/libuv/src/unix/getnameinfo.c:61` | `uv__req_unregister(req->loop);` |
| `ev_56e8bbe5e97f` | call_site | `third_party/libuv/src/uv-common.c:236` | `UV_ERRNO_MAP(UV_STRERROR_GEN_R)` |
| `ev_56e8bf29a78d` | call_site | `third_party/libuv/src/unix/core.c:659` | `while (r == -1 && errno == EINTR);` |
| `ev_56f6f766f2c5` | call_site | `third_party/libuv/src/unix/signal.c:407` | `first_handle = uv__signal_first_handle(signum);` |
| `ev_5701a78a3d4b` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:193` | `req->hints = memcpy(buf + len, hints, sizeof(*hints));` |
| `ev_570bbb436885` | call_site | `third_party/libuv/src/unix/stream.c:1369` | `memcpy(req->bufs, bufs, nbufs * sizeof(bufs[0]));` |
| `ev_574376669a89` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_57500a6c68c1` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_57762273c21d` | call_site | `third_party/libuv/src/unix/udp.c:72` | `assert(handle->io_watcher.fd == -1);` |
| `ev_57bb004e07fc` | call_site | `third_party/libuv/src/unix/fsevents.c:801` | `buf = realpath(handle->path, NULL);` |
| `ev_57c064a797e0` | call_site | `third_party/libuv/src/unix/thread.c:891` | `return pthread_getspecific(*key);` |
| `ev_57cd239836bd` | call_site | `third_party/libuv/src/unix/stream.c:1194` | `assert(stream->type == UV_TCP \|\|` |
| `ev_57f1506dca04` | call_site | `third_party/libuv/src/unix/process.c:944` | `abort();` |
| `ev_57f24e23d254` | call_site | `third_party/libuv/src/inet.c:53` | `l = snprintf(tmp, sizeof(tmp), fmt, src[0], src[1], src[2], src[3]);` |
| `ev_57fd2242d5ec` | call_site | `third_party/libuv/src/unix/core.c:1155` | `r = dup2(oldfd, newfd);  /* Never retry. */` |
| `ev_57fd6d86f8db` | call_site | `third_party/libuv/src/unix/fs.c:1122` | `if (r == 0 \|\| ((errno == EAGAIN \|\| errno == EINTR) && len != 0)) {` |
| `ev_5800769aee24` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:103` | `err = getaddrinfo(req->hostname, req->service, req->hints, &req->addrinfo);` |
| `ev_58059c3c3aae` | call_site | `third_party/libuv/src/unix/kqueue.c:485` | `assert(fd >= 0);` |
| `ev_580809d7174c` | call_site | `third_party/libuv/src/unix/fs.c:494` | `return f(fd, bufs, nbufs, off);` |
| `ev_5819c8b0e611` | call_site | `third_party/libuv/src/unix/process.c:934` | `assert(err == *pid);` |
| `ev_581f346928e6` | assignment | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_582755115ee9` | call_site | `third_party/libuv/src/unix/pipe.c:186` | `uv__free((void*)handle->pipe_fname);` |
| `ev_583ab4f93a99` | call_site | `third_party/libuv/src/unix/loop.c:117` | `uv__platform_loop_delete(loop);` |
| `ev_583cb6605bfb` | call_site | `third_party/libuv/src/unix/async.c:208` | `h->async_cb(h);` |
| `ev_5878e43d4546` | call_site | `third_party/libuv/src/unix/internal.h:426` | `rc = lstat(path, s);` |
| `ev_58d86dc619f7` | call_site | `third_party/libuv/src/unix/stream.c:210` | `abort();` |
| `ev_58ef62acf0eb` | call_site | `third_party/libuv/src/unix/udp.c:256` | `memset(&peer, 0, sizeof(peer));` |
| `ev_58f3dc053f69` | call_site | `third_party/libuv/src/unix/fs.c:656` | `dirent->type = uv__fs_get_dirent_type(res);` |
| `ev_58fe38b49ad4` | call_site | `third_party/libuv/src/thread-common.c:132` | `uv_mutex_lock(&b->mutex);` |
| `ev_590d9da5de83` | call_site | `third_party/libuv/src/unix/fs.c:1608` | `ret = uv__fs_statx(-1, path, /* is_fstat */ 0, /* is_lstat */ 1, buf);` |
| `ev_5927e1aa581c` | call_site | `third_party/libuv/src/unix/thread.c:326` | `if (pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_ERRORCHECK))` |
| `ev_595bfd21b4d8` | call_site | `third_party/libuv/src/unix/core.c:1316` | `memcpy(pwd->shell, pw.pw_shell, shell_size);` |
| `ev_596c1359a89c` | call_site | `third_party/libuv/src/unix/tty.c:493` | `errno = saved_errno;` |
| `ev_597481b20791` | call_site | `third_party/libuv/src/unix/fs.c:1945` | `PATH;` |
| `ev_597b32c514d3` | call_site | `third_party/libuv/src/unix/kqueue.c:192` | `while (!uv__queue_empty(&loop->watcher_queue)) {` |
| `ev_599011f4f1cb` | call_site | `third_party/libuv/src/unix/tcp.c:332` | `return UV__ERR(errno);` |
| `ev_59991a2a699c` | call_site | `third_party/libuv/src/unix/stream.c:736` | `uv__io_feed(stream->loop, &stream->io_watcher);` |
| `ev_59a0fc3ed32f` | call_site | `third_party/libuv/src/unix/signal.c:212` | `assert(r == sizeof msg \|\|` |
| `ev_59ab866064e6` | call_site | `third_party/libuv/src/unix/thread.c:825` | `if (errno == EBUSY)` |
| `ev_59c3e75c12ab` | call_site | `third_party/libuv/src/unix/stream.c:728` | `uv__free(req->bufs);` |
| `ev_59d075a072b3` | call_site | `third_party/libuv/src/unix/pipe.c:285` | `new_sock = (uv__stream_fd(handle) == -1);` |
| `ev_59e3d2f0e493` | call_site | `third_party/libuv/src/unix/process.c:793` | `assert(err != ENOSYS);` |
| `ev_59f60353ca94` | call_site | `third_party/libuv/src/uv-common.c:106` | `newptr = uv__realloc(ptr, size);` |
| `ev_59fb50244220` | call_site | `third_party/libuv/src/idna.c:393` | `code_point = uv__wtf8_decode1(&source_ptr);` |
| `ev_5a16757b7adf` | call_site | `third_party/libuv/src/unix/fs.c:1771` | `uv__req_unregister(req->loop);` |
| `ev_5a18fbb06d02` | call_site | `third_party/libuv/src/unix/tcp.c:125` | `uv__stream_init(loop, (uv_stream_t*)tcp, UV_TCP);` |
| `ev_5a4a88855f09` | call_site | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_5a52e5fdcbdb` | assignment | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_5a821a45bebe` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:148` | `freeifaddrs(addrs);` |
| `ev_5ad38a4dc79c` | call_site | `third_party/libuv/src/unix/tcp.c:659` | `if ((err = uv__nonblock(temp[0], 1)))` |
| `ev_5adadced276d` | call_site | `third_party/libuv/src/unix/udp.c:1094` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_5ae58c42de53` | call_site | `third_party/libuv/src/unix/kqueue.c:185` | `assert(uv__queue_empty(&loop->watcher_queue));` |
| `ev_5af4f57f3ee6` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:84` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFADDR))` |
| `ev_5b099f934fd7` | call_site | `third_party/libuv/src/unix/thread.c:733` | `return UV__ERR(pthread_cond_init(cond, NULL));` |
| `ev_5b390a425a7f` | call_site | `third_party/libuv/src/unix/udp.c:1373` | `n = uv__udp_sendmsgv(handle->io_watcher.fd, n, bufs, nbufs, addrs);` |
| `ev_5b58ef217d45` | call_site | `third_party/libuv/src/unix/fs.c:1402` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_5b6049adef04` | call_site | `third_party/libuv/src/unix/udp.c:545` | `r = connect(handle->io_watcher.fd, (struct sockaddr*) &addr, sizeof(addr));` |
| `ev_5b6b9ad704f2` | call_site | `third_party/libuv/src/unix/kqueue.c:485` | `assert(fd >= 0);` |
| `ev_5b8cd18fc1c7` | call_site | `third_party/libuv/src/unix/process.c:735` | `memcpy(b + (z - p) + (z > p), options->file, k + 1);` |
| `ev_5bdecbd6b74d` | call_site | `third_party/libuv/src/unix/loop.c:45` | `err = uv_mutex_init(&lfields->loop_metrics.lock);` |
| `ev_5be55a6a63f7` | call_site | `third_party/libuv/src/unix/stream.c:1013` | `err = uv__stream_queue_fd(stream, fd);` |
| `ev_5bf8b92b423e` | call_site | `third_party/libuv/src/unix/fsevents.c:542` | `V(core_foundation_handle, CFArrayCreate);` |
| `ev_5bfa883e3ab2` | call_site | `third_party/libuv/src/unix/stream.c:588` | `memmove(queued_fds->fds,` |
| `ev_5c11ce139b5b` | call_site | `third_party/libuv/src/unix/udp.c:1221` | `uv__io_stop(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_5c15eb331bb0` | call_site | `third_party/libuv/src/idna.c:148` | `return uv__utf8_decode1_slow(p, pe, a);` |
| `ev_5c1f5a662016` | call_site | `third_party/libuv/src/unix/random-getentropy.c:35` | `uv__getentropy = (uv__getentropy_cb) dlsym(RTLD_DEFAULT, "getentropy");` |
| `ev_5c284c2bbc65` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:134` | `req->cb(req, req->retcode, req->addrinfo);` |
| `ev_5c29bfee24b1` | call_site | `third_party/libuv/src/unix/fs.c:1656` | `iovmax = uv__getiovmax();` |
| `ev_5c517fed95a7` | call_site | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_5c63af235dec` | call_site | `third_party/libuv/src/unix/core.c:1516` | `return UV__ERR(errno);` |
| `ev_5c65350ffd97` | call_site | `third_party/libuv/src/unix/async.c:183` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK)` |
| `ev_5c8f6805df6e` | call_site | `third_party/libuv/src/unix/tcp.c:389` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_5c91a925fd0b` | call_site | `third_party/libuv/src/uv-common.c:270` | `memset(addr, 0, sizeof(*addr));` |
| `ev_5cc3b05c3da3` | call_site | `third_party/libuv/src/unix/loop.c:98` | `err = uv_async_init(loop, &loop->wq_async, uv__work_done);` |
| `ev_5ce83bb8bc9a` | call_site | `third_party/libuv/src/unix/stream.c:1279` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5d2fac246e05` | call_site | `third_party/libuv/src/unix/core.c:572` | `while (peerfd == -1 && errno == EINTR);` |
| `ev_5d59c515efe5` | call_site | `third_party/libuv/src/unix/udp.c:873` | `uv__queue_init(&handle->write_completed_queue);` |
| `ev_5d6dd8e4fcd0` | assignment | `third_party/libuv/src/unix/udp.c:871` | `uv__io_init(&handle->io_watcher, uv__udp_io, fd);` |
| `ev_5d76cfec820a` | call_site | `third_party/libuv/src/unix/proctitle.c:81` | `memcpy(s, argv[i], size);` |
| `ev_5da0d43629b9` | call_site | `third_party/libuv/src/unix/stream.c:1394` | `uv__io_start(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5dc3a69647f1` | call_site | `third_party/libuv/src/unix/fsevents.c:611` | `err = uv_mutex_init(&state->fsevent_mutex);` |
| `ev_5ddeddfa03c3` | call_site | `third_party/libuv/src/unix/fs.c:1721` | `X(FDATASYNC, uv__fs_fdatasync(req));` |
| `ev_5de8b5cf4f68` | call_site | `third_party/libuv/src/unix/core.c:972` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_5df179cf8486` | call_site | `third_party/libuv/src/unix/stream.c:516` | `assert(!(stream->flags & UV_HANDLE_CLOSING));` |
| `ev_5dfe7ef47841` | call_site | `third_party/libuv/src/unix/fs.c:1748` | `X(WRITE, uv__fs_write_all(req));` |
| `ev_5e0d82a8d673` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_5e184d243f24` | call_site | `third_party/libuv/src/unix/kqueue.c:253` | `assert(timeout >= -1);` |
| `ev_5e29172f460a` | call_site | `third_party/libuv/src/random.c:40` | `rc = uv__random_getentropy(buf, buflen);` |
| `ev_5e3ed8e24910` | call_site | `third_party/libuv/src/unix/darwin.c:91` | `memcpy(buffer, abspath, *size);` |
| `ev_5e51d6a8f660` | call_site | `third_party/libuv/src/unix/stream.c:1227` | `if (uv__stream_fd(stream) == -1)` |
| `ev_5e5a8b04f64f` | call_site | `third_party/libuv/src/unix/dl.c:54` | `dlerror(); /* Reset error status. */` |
| `ev_5e63f2080b13` | call_site | `third_party/libuv/src/uv-common.c:579` | `loop = uv_default_loop();` |
| `ev_5e6f3c1c78bf` | call_site | `third_party/libuv/src/unix/udp.c:394` | `err = uv__sock_reuseport(fd);` |
| `ev_5e9985bf0809` | call_site | `third_party/libuv/src/random.c:85` | `uv__req_unregister(req->loop);` |
| `ev_5e9aef6ce56a` | call_site | `third_party/libuv/src/unix/fs.c:287` | `uv__mkostemp = (int (*)(char*, int)) dlsym(RTLD_DEFAULT, "mkostemp");` |
| `ev_5ee6ca0c3170` | call_site | `third_party/libuv/src/unix/stream.c:1161` | `assert(stream->type == UV_TCP \|\|` |
| `ev_5eeb998d958b` | assignment | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_5f075a82b1f5` | call_site | `third_party/libuv/src/timer.c:108` | `uv__queue_init(&handle->node.queue);` |
| `ev_5f1013b05f10` | call_site | `third_party/libuv/src/unix/stream.c:885` | `uv__io_start(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5f18c7a1b894` | call_site | `third_party/libuv/src/uv-common.c:532` | `return uv__udp_try_send2(handle, count, bufs, nbufs, addrs);` |
| `ev_5f2b8640fe00` | call_site | `third_party/libuv/src/unix/stream.c:897` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_5f31fc43f11c` | call_site | `third_party/libuv/src/unix/core.c:447` | `uv__queue_empty(&loop->pending_queue) &&` |
| `ev_5f7bc69fc1bf` | call_site | `third_party/libuv/src/unix/tcp.c:456` | `return UV__ERR(errno);` |
| `ev_5f7ca3b47966` | call_site | `third_party/libuv/src/unix/fsevents.c:362` | `ref = pFSEventStreamCreate(NULL,` |
| `ev_5f9679f1655b` | call_site | `third_party/libuv/src/unix/pipe.c:383` | `p = memchr(sa.sun_path, '\0', sizeof(sa.sun_path));` |
| `ev_5f9839a1c551` | assignment | `third_party/libuv/src/unix/stream.c:116` | `uv__io_init(&stream->io_watcher, uv__stream_io, -1);` |
| `ev_5fa7748eb3a9` | call_site | `third_party/libuv/src/unix/fs.c:912` | `while (n == -1 && errno == EINTR);` |
| `ev_5fbc3b94e048` | call_site | `third_party/libuv/src/unix/udp.c:1317` | `while (r == -1 && errno == EINTR);` |
| `ev_5fbcf071d1f8` | call_site | `third_party/libuv/src/threadpool.c:157` | `uv__queue_insert_tail(&wq, q);` |
| `ev_5fbfa427a21a` | call_site | `third_party/libuv/src/unix/fs.c:1667` | `result = uv__fs_write(req);` |
| `ev_5fcba15903e8` | call_site | `third_party/libuv/src/unix/stream.c:174` | `FD_SET(fd, s->sread);` |
| `ev_5fd4f228b806` | call_site | `third_party/libuv/src/unix/udp.c:996` | `r = setsockopt(handle->io_watcher.fd,` |
| `ev_5fe6fb05a143` | call_site | `third_party/libuv/src/unix/kqueue.c:152` | `if (errno == EBADF \|\| errno == ENOENT)` |
| `ev_5fef042454c0` | call_site | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_600a26be4c33` | call_site | `third_party/libuv/src/unix/fs.c:257` | `return futimes(req->file, tv);` |
| `ev_600daaf714d9` | call_site | `third_party/libuv/src/unix/thread.c:402` | `if (pthread_rwlock_rdlock(rwlock))` |
| `ev_601a8631134c` | call_site | `third_party/libuv/src/threadpool.c:236` | `abort();` |
| `ev_604e44ac4249` | call_site | `third_party/libuv/src/idna.c:333` | `c = uv__utf8_decode1(&si, se);` |
| `ev_60512eda3418` | call_site | `third_party/libuv/src/unix/kqueue.c:390` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_6057ea19f056` | call_site | `third_party/libuv/src/unix/fsevents.c:777` | `uv__queue_insert_tail(&loop->cf_signals, &item->member);` |
| `ev_6059660fdccc` | call_site | `third_party/libuv/src/unix/fs.c:1438` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_6075033cc0b0` | call_site | `third_party/libuv/src/uv-common.c:237` | `default: snprintf(buf, buflen, "Unknown system error %d", err);` |
| `ev_607b0f3376c6` | call_site | `third_party/libuv/src/fs-poll.c:159` | `memcpy(buffer, ctx->path, required_len);` |
| `ev_60883ffec0b8` | call_site | `third_party/libuv/src/unix/stream.c:491` | `uv__close(loop->emfile_fd);` |
| `ev_608fd58ba2d5` | call_site | `third_party/libuv/src/unix/core.c:1702` | `min = sched_get_priority_min(policy);` |
| `ev_609bc37ebcab` | call_site | `third_party/libuv/src/unix/fsevents.c:688` | `q = uv__queue_head(&loop->cf_signals);` |
| `ev_609be69c6d7c` | call_site | `third_party/libuv/src/unix/kqueue.c:585` | `fd = open(handle->path, O_RDONLY);` |
| `ev_60a8faccdc12` | call_site | `third_party/libuv/src/uv-common.c:56` | `size_t len = strlen(s) + 1;` |
| `ev_60b46f28c250` | call_site | `third_party/libuv/src/unix/tcp.c:358` | `err = uv__nonblock(sock, 1);` |
| `ev_60ded42bf49c` | call_site | `third_party/libuv/src/unix/pipe.c:367` | `memset(&sa, 0, addrlen);` |
| `ev_60e3b9fa3cba` | assignment | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_60f78119b311` | call_site | `third_party/libuv/src/unix/thread.c:173` | `if (pthread_attr_init(attr))` |
| `ev_6130817e9c34` | call_site | `third_party/libuv/src/unix/process.c:1104` | `uv__queue_remove(&handle->queue);` |
| `ev_6130bb3132e7` | call_site | `third_party/libuv/src/unix/fs.c:419` | `r = pwrite(fd, p, n, off);` |
| `ev_613c8798ab98` | call_site | `third_party/libuv/src/unix/kqueue.c:522` | `if (fcntl(handle->event_watcher.fd, F_GETPATH, pathbuf) == 0)` |
| `ev_61422f40698e` | call_site | `third_party/libuv/src/unix/thread.c:134` | `return UV__ERR(pthread_detach(*tid));` |
| `ev_61604e565231` | call_site | `third_party/libuv/src/threadpool.c:318` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_61666d8e2507` | call_site | `third_party/libuv/src/unix/fsevents.c:803` | `return UV__ERR(errno);` |
| `ev_61776a622e07` | assignment | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_61917b99b437` | call_site | `third_party/libuv/src/unix/async.c:368` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_621fff9dc4e8` | call_site | `third_party/libuv/src/unix/signal.c:398` | `uv__signal_stop(handle);` |
| `ev_62435c030a57` | call_site | `third_party/libuv/src/unix/fsevents.c:711` | `state->loop = pCFRunLoopGetCurrent();` |
| `ev_6278eadb198b` | call_site | `third_party/libuv/src/unix/fs.c:1749` | `default: abort();` |
| `ev_629734748466` | call_site | `third_party/libuv/src/unix/udp.c:477` | `err = connect(handle->io_watcher.fd, addr, addrlen);` |
| `ev_62b71d0c2625` | call_site | `third_party/libuv/src/unix/udp.c:898` | `err = uv__nonblock(sock, 1);` |
| `ev_62eafafce89e` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:112` | `uv__req_unregister(req->loop);` |
| `ev_630b9e4a77cd` | call_site | `third_party/libuv/src/unix/stream.c:522` | `err = uv__emfile_trick(loop, fd);  /* Shed load. */` |
| `ev_63386b6d42ea` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:105` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFADDR))` |
| `ev_63663dd071a8` | call_site | `third_party/libuv/src/unix/core.c:690` | `r = fcntl(fd, F_SETFL, flags);` |
| `ev_6374ea66025d` | call_site | `third_party/libuv/src/unix/tcp.c:649` | `if (socketpair(AF_UNIX, type, protocol, temp))` |
| `ev_6380f2d7ec92` | call_site | `third_party/libuv/src/unix/core.c:1007` | `if (getrusage(who, &usage))` |
| `ev_6382d93a875d` | call_site | `third_party/libuv/src/unix/process.c:968` | `assert(options->file != NULL);` |
| `ev_63990f393159` | call_site | `third_party/libuv/src/uv-common.c:60` | `return memcpy(m, s, len);` |
| `ev_6399f23548c6` | call_site | `third_party/libuv/src/unix/udp.c:1134` | `memset(&addr_st, 0, sizeof addr_st);` |
| `ev_63a77851bcd7` | call_site | `third_party/libuv/src/unix/stream.c:1410` | `return uv_write2(req, handle, bufs, nbufs, NULL, cb);` |
| `ev_63bf2d54ddf3` | call_site | `third_party/libuv/src/unix/core.c:630` | `assert(fd > -1);  /* Catch uninitialized io_watcher.fd bugs. */` |
| `ev_63f5f4f4895d` | call_site | `third_party/libuv/src/unix/darwin.c:116` | `if (sysctl(which, ARRAY_SIZE(which), &info, &size, NULL, 0))` |
| `ev_63f7e6500df3` | call_site | `third_party/libuv/src/unix/core.c:1237` | `len = strlen(buf);` |
| `ev_644304a0325d` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_64434f05a208` | call_site | `third_party/libuv/src/unix/fs.c:161` | `rc = uv__close_nocancel(fd);` |
| `ev_64866fa91fcb` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:80` | `return UV__ERR(errno);` |
| `ev_648bf01c3bc5` | assignment | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_648dfb0cd002` | call_site | `third_party/libuv/src/unix/pipe.c:87` | `if (includes_nul(name, namelen))` |
| `ev_648e84c13366` | call_site | `third_party/libuv/src/unix/thread.c:810` | `abort();` |
| `ev_6492225d3615` | call_site | `third_party/libuv/src/unix/pipe.c:226` | `return uv__stream_open((uv_stream_t*)handle, fd, flags);` |
| `ev_649f56ac6cfb` | call_site | `third_party/libuv/src/unix/udp.c:206` | `handle->recv_cb(handle,` |
| `ev_64c2099522fc` | call_site | `third_party/libuv/src/unix/process.c:1058` | `uv__free(pipes);` |
| `ev_64e08799c6b9` | call_site | `third_party/libuv/src/unix/darwin.c:197` | `return UV__ERR(errno);` |
| `ev_6512b9056156` | call_site | `third_party/libuv/src/unix/signal.c:484` | `uv__signal_stop(handle);` |
| `ev_652f38d1da01` | call_site | `third_party/libuv/src/unix/core.c:1911` | `memcpy(buf, abspath, *buflen);` |
| `ev_65367cb4f3b0` | call_site | `third_party/libuv/src/unix/dl.c:56` | `return *ptr ? 0 : uv__dlerror(lib);` |
| `ev_65410c20178b` | call_site | `third_party/libuv/src/unix/fs.c:2243` | `memcpy(req->bufs, bufs, nbufs * sizeof(*bufs));` |
| `ev_6542bbf38418` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:116` | `uv__free(req->hints);` |
| `ev_65452ebb4d25` | call_site | `third_party/libuv/src/unix/core.c:551` | `fp = fdopen(fd, "r");` |
| `ev_6579011471b7` | call_site | `third_party/libuv/src/threadpool.c:224` | `uv__queue_init(&wq);` |
| `ev_65a699b2decf` | call_site | `third_party/libuv/src/unix/thread.c:332` | `abort();` |
| `ev_65bf789059b5` | call_site | `third_party/libuv/src/unix/udp.c:830` | `memcpy(&mreq.gsr_group, multicast_addr, sizeof(*multicast_addr));` |
| `ev_65c480cb5920` | call_site | `third_party/libuv/src/threadpool.c:114` | `uv__queue_insert_tail(&wq, &run_slow_work_message);` |
| `ev_65c87b1335e7` | call_site | `third_party/libuv/src/unix/udp.c:895` | `if (uv__fd_exists(handle->loop, sock))` |
| `ev_662c6abddea5` | call_site | `third_party/libuv/src/unix/fsevents.c:601` | `err = uv_sem_init(&loop->cf_sem, 0);` |
| `ev_663d6e856bed` | call_site | `third_party/libuv/src/unix/stream.c:1369` | `memcpy(req->bufs, bufs, nbufs * sizeof(bufs[0]));` |
| `ev_663e6a2e03bb` | call_site | `third_party/libuv/src/unix/stream.c:1101` | `stream->read_cb(stream, UV__ERR(errno), &buf);` |
| `ev_6654523c6471` | call_site | `third_party/libuv/src/unix/kqueue.c:237` | `if (kevent(loop->backend_fd, events, nevents, NULL, 0, NULL))` |
| `ev_665fade8cc23` | call_site | `third_party/libuv/src/unix/pipe.c:129` | `if (bind(sockfd, (struct sockaddr*)&saddr, addrlen)) {` |
| `ev_666149bc530b` | call_site | `third_party/libuv/src/unix/stream.c:552` | `uv__close(server->accepted_fd);` |
| `ev_667e199b3674` | call_site | `third_party/libuv/src/unix/udp.c:265` | `while (nread == -1 && errno == EINTR);` |
| `ev_667fc01eb30b` | call_site | `third_party/libuv/src/uv-common.c:272` | `addr->sin6_port = htons(port);` |
| `ev_66c7b1623155` | call_site | `third_party/libuv/src/unix/tcp.c:286` | `assert(handle->type == UV_TCP);` |
| `ev_66d0f541d686` | call_site | `third_party/libuv/src/unix/fsevents.c:547` | `V(core_foundation_handle, CFRunLoopRun);` |
| `ev_66ee5271384b` | call_site | `third_party/libuv/src/unix/fsevents.c:198` | `assert(events != NULL \|\| err != 0);` |
| `ev_66f5c673d0ef` | call_site | `third_party/libuv/src/unix/core.c:1632` | `r = pthread_getschedparam(tid, &policy, &param);` |
| `ev_66fd703702e4` | call_site | `third_party/libuv/src/unix/kqueue.c:250` | `sigaddset(pset, SIGPROF);` |
| `ev_67130ff0ac23` | call_site | `third_party/libuv/src/unix/kqueue.c:91` | `uv__free(loop->cf_state);` |
| `ev_671bd90de973` | call_site | `third_party/libuv/src/unix/fs.c:2119` | `PATH;` |
| `ev_671f3fea8617` | call_site | `third_party/libuv/src/unix/fs.c:450` | `return uv__preadv_or_pwritev_emul(fd, bufs, nbufs, off, /*is_pread*/1);` |
| `ev_6729889d71c2` | call_site | `third_party/libuv/src/unix/thread.c:448` | `if (pthread_rwlock_unlock(rwlock))` |
| `ev_6776f5b3d557` | call_site | `third_party/libuv/src/unix/fsevents.c:665` | `uv__free(state);` |
| `ev_67780e7ed116` | call_site | `third_party/libuv/src/unix/core.c:638` | `errno = saved_errno;` |
| `ev_677f6776adf7` | call_site | `third_party/libuv/src/unix/process.c:919` | `uv_rwlock_wrunlock(&loop->cloexec_lock);` |
| `ev_679ff18ca7a2` | call_site | `third_party/libuv/src/unix/udp.c:412` | `if (bind(fd, addr, addrlen)) {` |
| `ev_67a3709e9127` | call_site | `third_party/libuv/src/unix/async.c:354` | `uv__io_stop(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_67d202f6ce51` | call_site | `third_party/libuv/src/unix/pipe.c:486` | `return r != -1 ? 0 : UV__ERR(errno);` |
| `ev_67e182f7a56a` | call_site | `third_party/libuv/src/unix/thread.c:956` | `if (pthread_getname_np(*tid, thread_name, sizeof(thread_name)) != 0)` |
| `ev_68072d3577a9` | call_site | `third_party/libuv/src/unix/fs.c:2008` | `req->path = uv__strdup(tpl);` |
| `ev_680794d40ee9` | call_site | `third_party/libuv/src/unix/process.c:635` | `err = posix_spawn_file_actions_addclose(actions, use_fd);` |
| `ev_680bccec87c6` | call_site | `third_party/libuv/src/unix/kqueue.c:400` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_68104b5d2f94` | call_site | `third_party/libuv/src/unix/kqueue.c:644` | `r = uv__fsevents_close(handle);` |
| `ev_6817b611ee72` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:121` | `*(void **)(&pCFBundleGetInfoDictionary) = dlsym(core_foundation_handle,` |
| `ev_68181212d262` | call_site | `third_party/libuv/src/unix/fs.c:898` | `if (use_pread && nsent == 0 && (errno == EIO \|\| errno == ESPIPE)) {` |
| `ev_682121c9f829` | call_site | `third_party/libuv/src/unix/process.c:733` | `memcpy(b, p, z - p);` |
| `ev_683e274ff5cd` | call_site | `third_party/libuv/src/inet.c:166` | `return inet_pton6(s, dst);` |
| `ev_68419e3b88a3` | call_site | `third_party/libuv/src/unix/fs.c:1612` | `ret = uv__lstat(path, &pbuf);` |
| `ev_68694d8cde28` | call_site | `third_party/libuv/src/unix/stream.c:253` | `if ((events & POLLOUT) && uv__io_active(&stream->io_watcher, POLLOUT))` |
| `ev_686f8a4ddc22` | call_site | `third_party/libuv/src/unix/tcp.c:204` | `tcp->delayed_error = (err == -1) ? UV__ERR(errno) : 0;` |
| `ev_687435e471e9` | call_site | `third_party/libuv/src/unix/kqueue.c:130` | `if (!fcntl(fd, F_GETPATH, path))` |
| `ev_68b4272c6bea` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:251` | `return uv_if_indextoname(ifindex, buffer, size);` |
| `ev_68b9ba41d50f` | call_site | `third_party/libuv/src/unix/tcp.c:448` | `uv__io_start(tcp->loop, &tcp->io_watcher, POLLIN);` |
| `ev_690ddb644850` | call_site | `third_party/libuv/src/unix/process.c:400` | `execvp(options->file, options->args);` |
| `ev_691829d859d4` | call_site | `third_party/libuv/src/unix/stream.c:1304` | `if (uv__stream_fd(stream) < 0)` |
| `ev_6926694be946` | call_site | `third_party/libuv/src/unix/stream.c:217` | `if (FD_ISSET(fd, s->swrite))` |
| `ev_692c27e6fdc7` | call_site | `third_party/libuv/src/unix/stream.c:860` | `assert(req->handle == stream);` |
| `ev_6956cf21b71d` | call_site | `third_party/libuv/src/unix/stream.c:1204` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_696c011320ef` | call_site | `third_party/libuv/src/unix/process.c:147` | `assert(pid == process->pid);` |
| `ev_6985ef7a5f00` | call_site | `third_party/libuv/src/unix/signal.c:268` | `err = uv__make_pipe(loop->signal_pipefd, UV_NONBLOCK_PIPE);` |
| `ev_69ac2d35e2f3` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:234` | `return UV__ERR(errno);` |
| `ev_69b7ab7b9b00` | call_site | `third_party/libuv/src/idna.c:436` | `assert(code_point >= 0);` |
| `ev_69d8860f87b0` | call_site | `third_party/libuv/src/uv-common.c:316` | `return uv_inet_ntop(AF_INET6, &((struct sockaddr_in6 *)src)->sin6_addr,` |
| `ev_69ea19693ec1` | call_site | `third_party/libuv/src/fs-poll.c:60` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_FS_POLL);` |
| `ev_69fe941170d6` | call_site | `third_party/libuv/src/unix/stream.c:420` | `uv__tcp_keepalive(fd, 1, 60)) {` |
| `ev_6a00a584e213` | call_site | `third_party/libuv/src/unix/fs.c:1296` | `err = UV__ERR(errno);` |
| `ev_6a12446c2338` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:122` | `assert(0);` |
| `ev_6a2bcb57421b` | call_site | `third_party/libuv/src/threadpool.c:123` | `w->work(w);` |
| `ev_6a4a8d4ff554` | assignment | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_6a67cb36a710` | call_site | `third_party/libuv/src/unix/stream.c:1289` | `uv__stream_flush_write_queue(stream, UV_ECANCELED);` |
| `ev_6a71039a9ace` | call_site | `third_party/libuv/src/unix/core.c:1634` | `return UV__ERR(errno);` |
| `ev_6a83c8437d0e` | call_site | `third_party/libuv/src/unix/process.c:160` | `uv__queue_init(&process->queue);` |
| `ev_6a943a2da25b` | call_site | `third_party/libuv/src/unix/stream.c:694` | `assert(n <= stream->write_queue_size);` |
| `ev_6aa69d58c468` | call_site | `third_party/libuv/src/unix/fs.c:1734` | `X(SCANDIR, uv__fs_scandir(req));` |
| `ev_6aa8381e2655` | call_site | `third_party/libuv/src/unix/loop.c:56` | `uv__queue_init(&loop->check_handles);` |
| `ev_6aea3e37c1fb` | call_site | `third_party/libuv/src/unix/thread.c:911` | `return UV__ERR(errno);` |
| `ev_6b02388808c9` | call_site | `third_party/libuv/src/unix/fs.c:746` | `maxlen = uv__fs_pathmax_size(req->path);` |
| `ev_6b0c92d92e8e` | call_site | `third_party/libuv/src/unix/stream.c:1081` | `while (nread < 0 && errno == EINTR);` |
| `ev_6b4c09ac33ec` | call_site | `third_party/libuv/src/unix/fs.c:1742` | `X(SENDFILE, uv__fs_sendfile(req));` |
| `ev_6b4cbaa23ab1` | call_site | `third_party/libuv/src/unix/core.c:1597` | `if (r == -1 && errno != 0)` |
| `ev_6b62ec25c94f` | call_site | `third_party/libuv/src/unix/fs.c:826` | `if (realpath(req->path, buf) == NULL) {` |
| `ev_6b8b1f9ce4bb` | call_site | `third_party/libuv/src/unix/stream.c:1079` | `nread = uv__recvmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_6b8ddfde0360` | assignment | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_6b97758595fb` | call_site | `third_party/libuv/src/uv-common.c:550` | `return uv__udp_recv_stop(handle);` |
| `ev_6baf83fb1c9e` | call_site | `third_party/libuv/src/unix/fs.c:1740` | `X(RENAME, rename(req->path, req->new_path));` |
| `ev_6be600edc613` | call_site | `third_party/libuv/src/unix/udp.c:1151` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_6bf8f63b2d2d` | call_site | `third_party/libuv/src/unix/process.c:611` | `err = posix_spawn_file_actions_adddup2(actions, use_fd, fd);` |
| `ev_6c1278f566c1` | call_site | `third_party/libuv/src/unix/loop.c:80` | `err = uv__platform_loop_init(loop);` |
| `ev_6c354a23216b` | call_site | `third_party/libuv/src/unix/udp.c:231` | `assert(handle->recv_cb != NULL);` |
| `ev_6c39df0d2bf4` | call_site | `third_party/libuv/src/unix/fsevents.c:570` | `dlclose(core_foundation_handle);` |
| `ev_6c4817b37dca` | call_site | `third_party/libuv/src/unix/stream.c:138` | `assert(r == 1);` |
| `ev_6c8ebffd1a28` | call_site | `third_party/libuv/src/unix/process.c:131` | `pid = waitpid(process->pid, &status, options);` |
| `ev_6c96f7cd0f70` | call_site | `third_party/libuv/src/unix/tty.c:245` | `assert(tio != NULL);` |
| `ev_6cd88c26ccbe` | call_site | `third_party/libuv/src/unix/udp.c:403` | `err = UV__ERR(errno);` |
| `ev_6cfaf3a19785` | call_site | `third_party/libuv/src/unix/fs.c:1798` | `PATH;` |
| `ev_6cfaf487400b` | call_site | `third_party/libuv/src/unix/proctitle.c:57` | `pt.len = strlen(argv[0]);` |
| `ev_6d00cae2dab6` | call_site | `third_party/libuv/src/unix/pipe.c:126` | `memcpy(&saddr.sun_path, name, namelen);` |
| `ev_6d184f655661` | call_site | `third_party/libuv/src/unix/stream.c:177` | `FD_SET(s->int_fd, s->sread);` |
| `ev_6d3e4f7d0370` | call_site | `third_party/libuv/src/unix/signal.c:565` | `ret = uv__signal_register_handler(handle->signum, 1);` |
| `ev_6d46c3f54d72` | call_site | `third_party/libuv/src/unix/stream.c:306` | `ret = kevent(kq, filter, 1, events, 1, &timeout);` |
| `ev_6d4ae22e552b` | call_site | `third_party/libuv/src/unix/fsevents.c:679` | `if (uv__cf_loop_signal(loop, NULL, kUVCFLoopSignalRegular) != 0)` |
| `ev_6d535b89b2dc` | call_site | `third_party/libuv/src/unix/fs.c:252` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_6d5f4c252e6d` | call_site | `third_party/libuv/src/unix/signal.c:76` | `uv__signal_global_reinit();` |
| `ev_6dacff143424` | call_site | `third_party/libuv/src/unix/tcp.c:310` | `r = connect(uv__stream_fd(handle), addr, addrlen);` |
| `ev_6dad2c55bfa8` | call_site | `third_party/libuv/src/unix/darwin.c:129` | `return uv_get_free_memory();` |
| `ev_6db313507e11` | call_site | `third_party/libuv/src/threadpool.c:203` | `nthreads = atoi(val);` |
| `ev_6de247fe4648` | call_site | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_6e281d6e7a2f` | call_site | `third_party/libuv/src/unix/fsevents.c:746` | `item = uv__queue_head(&split_head);` |
| `ev_6e32e3735838` | call_site | `third_party/libuv/src/unix/loop.c:178` | `uv__close(loop->backend_fd);` |
| `ev_6e456c5123c1` | call_site | `third_party/libuv/src/unix/stream.c:1263` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_6e4e52a19053` | call_site | `third_party/libuv/src/unix/fsevents.c:720` | `pCFRunLoopRemoveSource(state->loop,` |
| `ev_6e565ce2957d` | call_site | `third_party/libuv/src/unix/core.c:1381` | `gr_mem = uv__malloc(name_size + mem_size);` |
| `ev_6e56ba1133e6` | call_site | `third_party/libuv/src/unix/stream.c:97` | `uv__queue_init(&stream->write_queue);` |
| `ev_6ea9d6911f33` | call_site | `third_party/libuv/src/unix/core.c:713` | `return UV__ERR(errno);` |
| `ev_6eb68f006141` | call_site | `third_party/libuv/src/unix/stream.c:1452` | `assert(alloc_cb);` |
| `ev_6ed445745437` | call_site | `third_party/libuv/src/unix/fs.c:2140` | `PATH2;` |
| `ev_6ed754a81fde` | call_site | `third_party/libuv/src/unix/async.c:109` | `uv__async_send(handle->loop);` |
| `ev_6ed962de3c19` | call_site | `third_party/libuv/src/unix/core.c:1161` | `uv__close(newfd);` |
| `ev_6eeb774b2e05` | call_site | `third_party/libuv/src/unix/stream.c:630` | `assert(uv__queue_empty(&stream->write_queue));` |
| `ev_6ef0583df69a` | call_site | `third_party/libuv/src/unix/udp.c:232` | `assert(handle->alloc_cb != NULL);` |
| `ev_6f061adcc953` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:143` | `pLSSetApplicationLaunchServicesServerConnectionStatus(0, NULL);` |
| `ev_6f1d20020c70` | call_site | `third_party/libuv/src/unix/tcp.c:318` | `if (r == -1 && errno != 0) {` |
| `ev_6f1f187a9ac1` | call_site | `third_party/libuv/src/unix/udp.c:673` | `mreq.imr_interface.s_addr = htonl(INADDR_ANY);` |
| `ev_6f38d2fc520c` | call_site | `third_party/libuv/src/uv-common.c:214` | `default: snprintf(buf, buflen, "Unknown system error %d", err);` |
| `ev_6f444a8f22bb` | call_site | `third_party/libuv/src/uv-common.c:109` | `uv__free(ptr);` |
| `ev_6f851eda2d79` | call_site | `third_party/libuv/src/uv-common.c:360` | `rc = uv__udp_init_ex(loop, handle, flags, domain);` |
| `ev_6fb0a35ba2e6` | call_site | `third_party/libuv/src/unix/stream.c:809` | `n = sendmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_6fb80148c529` | call_site | `third_party/libuv/src/unix/process.c:726` | `z = p + strlen(p);` |
| `ev_6fb8ad0f3c81` | call_site | `third_party/libuv/src/uv-common.c:747` | `assert(nbufs);` |
| `ev_7032b2ad9f95` | call_site | `third_party/libuv/src/unix/tty.c:365` | `uv__stream_close((uv_stream_t*) handle);` |
| `ev_703c0b9fc077` | call_site | `third_party/libuv/src/uv-common.c:1029` | `memcpy(metrics,` |
| `ev_704f31501111` | call_site | `third_party/libuv/src/idna.c:395` | `assert(code_point >= 0);` |
| `ev_7063af7e594d` | call_site | `third_party/libuv/src/unix/core.c:363` | `handle->close_cb(handle);` |
| `ev_7069296110df` | call_site | `third_party/libuv/src/unix/signal.c:106` | `if (uv__signal_unlock())` |
| `ev_7081799b83af` | call_site | `third_party/libuv/src/uv-common.c:597` | `fprintf(stream,` |
| `ev_70a6b8ea8954` | call_site | `third_party/libuv/src/unix/tcp.c:58` | `return UV__ERR(errno);` |
| `ev_70ad00ca0156` | call_site | `third_party/libuv/src/unix/tcp.c:652` | `if ((err = uv__cloexec(temp[0], 1)))` |
| `ev_70b2e1a35c4f` | call_site | `third_party/libuv/src/uv-common.c:255` | `memset(addr, 0, sizeof(*addr));` |
| `ev_70b5fd2258d6` | call_site | `third_party/libuv/src/unix/stream.c:1263` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_70bdf8cb6036` | call_site | `third_party/libuv/src/unix/fs.c:2129` | `PATH;` |
| `ev_70f5dc732dff` | call_site | `third_party/libuv/src/unix/kqueue.c:615` | `uv__free(handle->path);` |
| `ev_7159861680a0` | call_site | `third_party/libuv/src/uv-common.c:203` | `copy = uv__strdup(buf);` |
| `ev_716377ec70c2` | call_site | `third_party/libuv/src/unix/internal.h:406` | `s = strrchr(path, '/');` |
| `ev_7170440dd9cb` | call_site | `third_party/libuv/src/unix/udp.c:61` | `uv__close(handle->io_watcher.fd);` |
| `ev_7177d40110a5` | call_site | `third_party/libuv/src/idna.c:397` | `assert(code_point < 0x10FFFF);` |
| `ev_717c1e341227` | call_site | `third_party/libuv/src/unix/stream.c:888` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_71b1d11ab510` | call_site | `third_party/libuv/src/unix/core.c:1456` | `uv__free(buf);` |
| `ev_720266ec755c` | call_site | `third_party/libuv/src/unix/thread.c:113` | `return uv__default_stack_size();` |
| `ev_7249cdfb8c22` | call_site | `third_party/libuv/src/threadpool.c:211` | `threads = uv__malloc(nthreads * sizeof(threads[0]));` |
| `ev_726df6ac9bec` | call_site | `third_party/libuv/src/unix/core.c:1316` | `memcpy(pwd->shell, pw.pw_shell, shell_size);` |
| `ev_727d04330d42` | call_site | `third_party/libuv/src/unix/core.c:807` | `if (uv__cloexec(fd, 1) && fd > 15)` |
| `ev_7294d02f781a` | call_site | `third_party/libuv/src/unix/process.c:612` | `assert(err != ENOSYS);` |
| `ev_729679b71839` | call_site | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_729bb01cf365` | call_site | `third_party/libuv/src/unix/tty.c:396` | `if (isatty(file))` |
| `ev_72adfce66af2` | call_site | `third_party/libuv/src/unix/fs.c:1982` | `PATH;` |
| `ev_72b139e4bf26` | call_site | `third_party/libuv/src/unix/fs.c:770` | `errno = ENOMEM;` |
| `ev_72b324ab06dd` | call_site | `third_party/libuv/src/unix/proctitle.c:42` | `uv_mutex_init(&process_title_mutex);` |
| `ev_72d25a3e450c` | call_site | `third_party/libuv/src/fs-poll.c:221` | `uv_fs_req_cleanup(req);` |
| `ev_7309501b2c39` | call_site | `third_party/libuv/src/idna.c:499` | `assert(code_point >= 0);` |
| `ev_7309a7e5bbd1` | call_site | `third_party/libuv/src/unix/thread.c:454` | `if (pthread_once(guard, callback))` |
| `ev_734814f05104` | call_site | `third_party/libuv/src/unix/process.c:301` | `uv__write_errno(error_fd);` |
| `ev_7355587f6539` | call_site | `third_party/libuv/src/unix/loop.c:84` | `uv__signal_global_once_init();` |
| `ev_735919042c04` | call_site | `third_party/libuv/src/unix/udp.c:86` | `assert(handle->send_queue_count == 0);` |
| `ev_736b9cf12b70` | call_site | `third_party/libuv/src/unix/thread.c:344` | `abort();` |
| `ev_736c6a1ee36d` | call_site | `third_party/libuv/src/unix/pipe.c:469` | `if (uv__stat(name_buffer, &pipe_stat) == -1)` |
| `ev_7389c7f3eade` | call_site | `third_party/libuv/src/fs-poll.c:171` | `uv__make_close_pending((uv_handle_t*)handle);` |
| `ev_7395297c97e5` | call_site | `third_party/libuv/src/unix/core.c:674` | `r = fcntl(fd, F_GETFL);` |
| `ev_739e63d8b500` | call_site | `third_party/libuv/src/unix/signal.c:94` | `uv__close(uv__signal_lock_pipefd[1]);` |
| `ev_73b38530cdae` | call_site | `third_party/libuv/src/unix/process.c:352` | `uv__write_int(error_fd, n);` |
| `ev_73b55b9d0886` | call_site | `third_party/libuv/src/unix/stream.c:1231` | `uv__write(stream);` |
| `ev_73b5d163aa4a` | call_site | `third_party/libuv/src/unix/pipe.c:215` | `err = uv__stream_try_select((uv_stream_t*) handle, &fd);` |
| `ev_73b69d7bbc9d` | call_site | `third_party/libuv/src/unix/udp.c:736` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_73bbc97ad5bc` | call_site | `third_party/libuv/src/unix/fsevents.c:439` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_73c039001c4b` | call_site | `third_party/libuv/src/unix/thread.c:386` | `abort();` |
| `ev_73ca266fd72c` | call_site | `third_party/libuv/src/threadpool.c:324` | `while (!uv__queue_empty(&wq)) {` |
| `ev_73d6a0e24c74` | call_site | `third_party/libuv/src/unix/stream.c:1435` | `return uv__try_write(stream, bufs, nbufs, send_handle);` |
| `ev_7400d8d34315` | call_site | `third_party/libuv/src/unix/fs.c:1420` | `err = uv__close_nocheckstdio(srcfd);` |
| `ev_74049b001659` | call_site | `third_party/libuv/src/unix/core.c:175` | `uv__tcp_close((uv_tcp_t*)handle);` |
| `ev_7405ce9f82b6` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:146` | `pLSApplicationCheckIn(-2,` |
| `ev_740962944152` | call_site | `third_party/libuv/src/uv-common.c:371` | `return uv_udp_init_ex(loop, handle, AF_UNSPEC);` |
| `ev_743f20eb1657` | call_site | `third_party/libuv/src/unix/fsevents.c:550` | `V(core_foundation_handle, CFRunLoopStop);` |
| `ev_74419188bc2f` | call_site | `third_party/libuv/src/unix/fsevents.c:371` | `pFSEventStreamScheduleWithRunLoop(ref, state->loop, *pkCFRunLoopDefaultMode);` |
| `ev_74543600cfb2` | call_site | `third_party/libuv/src/uv-common.c:449` | `if (uv_udp_getpeername(handle, (struct sockaddr*) &addr, &addrlen) != 0)` |
| `ev_7460a5a0ef73` | call_site | `third_party/libuv/src/unix/fs.c:2119` | `PATH;` |
| `ev_7475a9ded8a4` | call_site | `third_party/libuv/src/unix/fs.c:642` | `if (errno != 0)` |
| `ev_7479586a3b40` | call_site | `third_party/libuv/src/fs-poll.c:123` | `assert(ctx != NULL);` |
| `ev_748ab347c266` | call_site | `third_party/libuv/src/threadpool.c:300` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_74a98bfe55ce` | call_site | `third_party/libuv/src/unix/thread.c:313` | `return uv__thread_getname(tid, name, size);` |
| `ev_74ad6f6a43d1` | call_site | `third_party/libuv/src/uv-common.c:237` | `default: snprintf(buf, buflen, "Unknown system error %d", err);` |
| `ev_74b634b3e8ff` | call_site | `third_party/libuv/src/threadpool.c:75` | `slow_io_work_running >= slow_work_thread_threshold())) {` |
| `ev_7522765d1036` | call_site | `third_party/libuv/src/unix/udp.c:872` | `uv__queue_init(&handle->write_queue);` |
| `ev_75392261f203` | call_site | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_75406c8b6161` | call_site | `third_party/libuv/src/unix/process.c:1071` | `uv__close_nocheckstdio(pipes[i][1]);` |
| `ev_7550fe6f4f04` | call_site | `third_party/libuv/src/unix/stream.c:215` | `if (FD_ISSET(fd, s->sread))` |
| `ev_75734426f05a` | call_site | `third_party/libuv/src/unix/fs.c:503` | `return uv__preadv_or_pwritev(fd, bufs, nbufs, off, &cache, /*is_pread*/1);` |
| `ev_7574415cb0ea` | call_site | `third_party/libuv/src/unix/signal.c:158` | `abort();` |
| `ev_757f45674b98` | call_site | `third_party/libuv/src/uv-common.c:77` | `return uv__allocator.local_malloc(size);` |
| `ev_75848779bc85` | call_site | `third_party/libuv/src/threadpool.c:102` | `if (uv__queue_empty(&slow_io_pending_wq))` |
| `ev_75892c995a18` | call_site | `third_party/libuv/src/unix/fs.c:1810` | `PATH;` |
| `ev_75cfe8001256` | call_site | `third_party/libuv/src/uv-common.c:249` | `return uv__unknown_err_code(err);` |
| `ev_7637f38d007a` | call_site | `third_party/libuv/src/unix/kqueue.c:407` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_765cb02c86a1` | call_site | `third_party/libuv/src/unix/udp.c:241` | `handle->alloc_cb((uv_handle_t*) handle, UV__UDP_DGRAM_MAXSIZE, &buf);` |
| `ev_766c7a4d2c9a` | call_site | `third_party/libuv/src/unix/core.c:478` | `uv__run_timers(loop);` |
| `ev_768cf1885315` | call_site | `third_party/libuv/src/unix/thread.c:306` | `return uv__thread_setname(name);` |
| `ev_76b187a2adac` | call_site | `third_party/libuv/src/unix/stream.c:186` | `abort();` |
| `ev_76b88df8c6b7` | call_site | `third_party/libuv/src/unix/process.c:270` | `uv__write_int(error_fd, UV__ERR(errno));` |
| `ev_76bc7b36c4f3` | call_site | `third_party/libuv/src/unix/fs.c:336` | `if (errno != EINVAL)` |
| `ev_770129efb973` | call_site | `third_party/libuv/src/unix/core.c:709` | `r = fcntl(fd, F_SETFD, flags);` |
| `ev_7720e0dff960` | call_site | `third_party/libuv/src/unix/udp.c:527` | `memset(&addr, 0, sizeof(addr));` |
| `ev_77282b3916c2` | call_site | `third_party/libuv/src/fs-poll.c:88` | `ctx->start_time = uv_now(loop);` |
| `ev_773cac45e64e` | assignment | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_773e20d2b029` | call_site | `third_party/libuv/src/unix/stream.c:220` | `assert(events != 0 \|\| FD_ISSET(s->int_fd, s->sread));` |
| `ev_773f11a10c5b` | call_site | `third_party/libuv/src/inet.c:152` | `return (inet_pton4(src, dst));` |
| `ev_77bd32570c37` | call_site | `third_party/libuv/src/unix/process.c:786` | `(void) posix_spawnattr_destroy(&attrs);` |
| `ev_7830144562a8` | call_site | `third_party/libuv/src/unix/kqueue.c:218` | `abort();` |
| `ev_783e86892202` | call_site | `third_party/libuv/src/unix/core.c:314` | `assert(handle->flags & UV_HANDLE_CLOSING);` |
| `ev_7847f76fe069` | call_site | `third_party/libuv/src/unix/process.c:601` | `assert(err != ENOSYS);` |
| `ev_7848589f66bd` | call_site | `third_party/libuv/src/unix/thread.c:410` | `err = pthread_rwlock_tryrdlock(rwlock);` |
| `ev_7863c47a6f03` | call_site | `third_party/libuv/src/unix/fs.c:420` | `while (r == -1 && errno == EINTR);` |
| `ev_787be673cf24` | call_site | `third_party/libuv/src/unix/async.c:193` | `while (!uv__queue_empty(&queue)) {` |
| `ev_7881c8e7a47c` | call_site | `third_party/libuv/src/unix/stream.c:664` | `return write(fd, vec->iov_base, vec->iov_len);` |
| `ev_78ae321be232` | call_site | `third_party/libuv/src/unix/core.c:1060` | `kr = thread_info(thread,` |
| `ev_78e710952dae` | call_site | `third_party/libuv/src/unix/tcp.c:46` | `return UV__ERR(errno);` |
| `ev_791dea3c7743` | call_site | `third_party/libuv/src/unix/stream.c:180` | `r = select(max_fd + 1, s->sread, s->swrite, NULL, NULL);` |
| `ev_791f66959b2c` | assignment | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_797ce2ad40cd` | call_site | `third_party/libuv/src/unix/kqueue.c:106` | `if (uv__fstat(fd, &sb))` |
| `ev_7987974b213e` | call_site | `third_party/libuv/src/unix/stream.c:254` | `uv__stream_io(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_79a966fecc53` | call_site | `third_party/libuv/src/unix/dl.c:42` | `uv__free(lib->errmsg);` |
| `ev_79cad2fd59d2` | call_site | `third_party/libuv/src/unix/loop.c:186` | `uv_mutex_destroy(&loop->wq_mutex);` |
| `ev_7a1766d69d6f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_7a558d821bff` | call_site | `third_party/libuv/src/unix/thread.c:896` | `if (pthread_setspecific(*key, value))` |
| `ev_7a5ac731a67f` | call_site | `third_party/libuv/src/unix/fs.c:1714` | `X(CHMOD, chmod(req->path, req->mode));` |
| `ev_7a6d44c9f586` | call_site | `third_party/libuv/src/unix/signal.c:493` | `memmove(buf, buf + end, bytes);` |
| `ev_7a7d94f2afa6` | call_site | `third_party/libuv/src/unix/core.c:1447` | `if (environ[j] == NULL)` |
| `ev_7a8709e7b264` | call_site | `third_party/libuv/src/unix/thread.c:851` | `r = pthread_cond_timedwait_relative_np(cond, mutex, &ts);` |
| `ev_7a95c9358161` | call_site | `third_party/libuv/src/unix/stream.c:630` | `assert(uv__queue_empty(&stream->write_queue));` |
| `ev_7a9d3b3630aa` | call_site | `third_party/libuv/src/unix/stream.c:1172` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_7ab95b2af00e` | call_site | `third_party/libuv/src/unix/kqueue.c:200` | `assert(w->fd < (int) loop->nwatchers);` |
| `ev_7ad5392ecc96` | call_site | `third_party/libuv/src/unix/process.c:360` | `uv__write_errno(error_fd);` |
| `ev_7adfb00d6fc3` | assignment | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_7ae7c5c539eb` | call_site | `third_party/libuv/src/unix/core.c:1871` | `if (strchr(prog, '/') != NULL) {` |
| `ev_7af27683855d` | call_site | `third_party/libuv/src/unix/core.c:145` | `return UV__ERR(errno);` |
| `ev_7af545e4ff66` | call_site | `third_party/libuv/src/unix/core.c:852` | `uv__queue_init(q);` |
| `ev_7b055d7f58c9` | call_site | `third_party/libuv/src/unix/stream.c:911` | `while (!uv__queue_empty(&pq)) {` |
| `ev_7b1cd0741bcb` | call_site | `third_party/libuv/src/unix/core.c:140` | `r = clock_gettime(CLOCK_REALTIME, &t);` |
| `ev_7b2a27557eaf` | call_site | `third_party/libuv/src/inet.c:222` | `memset((tp = tmp), '\0', sizeof tmp);` |
| `ev_7b2ab2ee5ea1` | call_site | `third_party/libuv/src/unix/core.c:978` | `uv__queue_remove(&w->pending_queue);` |
| `ev_7b3f3b5a9948` | call_site | `third_party/libuv/src/unix/darwin.c:55` | `if (KERN_SUCCESS != mach_timebase_info(&timebase))` |
| `ev_7b49cdbdb717` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_7b66afd68e91` | call_site | `third_party/libuv/src/unix/core.c:1377` | `mem_size += strlen(gp.gr_mem[r]) + 1 + sizeof(char*);` |
| `ev_7b875945d255` | call_site | `third_party/libuv/src/unix/tcp.c:375` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_7ba421a35714` | call_site | `third_party/libuv/src/unix/proctitle.c:121` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_7ba9f2ae53ef` | call_site | `third_party/libuv/src/unix/fs.c:318` | `strcmp(path + path_length - pattern_size, pattern)) {` |
| `ev_7c1946c115dc` | call_site | `third_party/libuv/src/unix/proctitle.c:119` | `uv__set_process_title(pt->str);` |
| `ev_7c30a737a963` | call_site | `third_party/libuv/src/unix/udp.c:150` | `uv__udp_run_completed(handle);` |
| `ev_7c38728fe6ad` | call_site | `third_party/libuv/src/unix/core.c:416` | `return uv__backend_timeout(loop);` |
| `ev_7c453864dec2` | call_site | `third_party/libuv/src/unix/fs.c:1823` | `PATH;` |
| `ev_7c66fd136764` | call_site | `third_party/libuv/src/unix/core.c:396` | `!uv__queue_empty(&loop->pending_queue) \|\|` |
| `ev_7c677d651647` | call_site | `third_party/libuv/src/unix/udp.c:813` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET6, UV_UDP_REUSEADDR);` |
| `ev_7c743d3ea33e` | call_site | `third_party/libuv/src/unix/thread.c:885` | `if (pthread_key_delete(*key))` |
| `ev_7c8564c28616` | call_site | `third_party/libuv/src/unix/signal.c:353` | `uv__signal_stop(handle);` |
| `ev_7ca0a06a6b5b` | assignment | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_7cbe7f5d4fb7` | call_site | `third_party/libuv/src/unix/fsevents.c:484` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_7cc58377c31a` | call_site | `third_party/libuv/src/threadpool.c:148` | `if (!uv__queue_empty(&run_slow_work_message)) {` |
| `ev_7d0fe4fc434a` | call_site | `third_party/libuv/src/unix/stream.c:457` | `assert(stream->flags & UV_HANDLE_CLOSED);` |
| `ev_7d269f408585` | call_site | `third_party/libuv/src/unix/signal.c:191` | `if (uv__signal_lock()) {` |
| `ev_7d27be801e6f` | call_site | `third_party/libuv/src/unix/stream.c:1566` | `return uv__nonblock(uv__stream_fd(handle), !blocking);` |
| `ev_7d2950f4ad14` | call_site | `third_party/libuv/src/unix/udp.c:591` | `memcpy(&req->u.storage, addr, addrlen);` |
| `ev_7d4f0413754a` | call_site | `third_party/libuv/src/unix/async.c:197` | `uv__queue_remove(q);` |
| `ev_7d7a5d572aae` | call_site | `third_party/libuv/src/unix/udp.c:459` | `abort();` |
| `ev_7d90fbb75433` | call_site | `third_party/libuv/src/unix/pipe.c:518` | `if ((err = uv__cloexec(temp[1], 1)))` |
| `ev_7df1be6a60da` | call_site | `third_party/libuv/src/unix/udp.c:1213` | `uv__io_start(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_7e0cf617aab4` | call_site | `third_party/libuv/src/fs-poll.c:233` | `abort();` |
| `ev_7e0dc6f23a1f` | call_site | `third_party/libuv/src/unix/fsevents.c:425` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_7e2a5f76f477` | call_site | `third_party/libuv/src/unix/pipe.c:367` | `memset(&sa, 0, addrlen);` |
| `ev_7e2a9a65b588` | call_site | `third_party/libuv/src/unix/stream.c:1285` | `if (uv__stream_fd(stream) == -1)` |
| `ev_7e2f7ce88e7d` | call_site | `third_party/libuv/src/unix/core.c:819` | `fd_out = uv__stream_fd((uv_stream_t*) handle);` |
| `ev_7e3a29b82180` | call_site | `third_party/libuv/src/unix/dl.c:47` | `dlclose(lib->handle);` |
| `ev_7e4cb252a290` | call_site | `third_party/libuv/src/unix/random-devurandom.c:49` | `uv__close(fd);` |
| `ev_7e4d1b53780f` | call_site | `third_party/libuv/src/unix/fsevents.c:697` | `uv_mutex_destroy(&state->fsevent_mutex);` |
| `ev_7e50f4886f5d` | call_site | `third_party/libuv/src/unix/proctitle.c:107` | `uv_once(&process_title_mutex_once, init_process_title_mutex_once);` |
| `ev_7e5aaa338262` | call_site | `third_party/libuv/src/unix/fs.c:182` | `r = fcntl(req->file, F_FULLFSYNC);` |
| `ev_7e6a3fa339ef` | call_site | `third_party/libuv/src/unix/stream.c:858` | `q = uv__queue_head(&stream->write_queue);` |
| `ev_7e7f6f944a88` | call_site | `third_party/libuv/src/fs-poll.c:119` | `if (!uv_is_active((uv_handle_t*)handle))` |
| `ev_7e979700706c` | call_site | `third_party/libuv/src/unix/fs.c:1718` | `X(FCHMOD, fchmod(req->file, req->mode));` |
| `ev_7eac5862569a` | call_site | `third_party/libuv/src/unix/stream.c:466` | `uv__write_callbacks(stream);` |
| `ev_7eb1da12cae5` | call_site | `third_party/libuv/src/unix/loop.c:184` | `assert(!uv__has_active_reqs(loop));` |
| `ev_7eb6caf3abc1` | call_site | `third_party/libuv/src/unix/core.c:947` | `assert(0 != events);` |
| `ev_7f02ea6496ff` | assignment | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_7f05828baffe` | assignment | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_7f25c54b39ef` | call_site | `third_party/libuv/src/unix/kqueue.c:297` | `assert(timeout != -1);` |
| `ev_7f2edeedc5b0` | call_site | `third_party/libuv/src/unix/kqueue.c:369` | `w->cb(loop, w, w->events);` |
| `ev_7f35d7b5a699` | call_site | `third_party/libuv/src/unix/udp.c:926` | `return uv__udp_set_membership4(handle, &addr4, interface_addr, membership);` |
| `ev_7f3f110e9dfb` | call_site | `third_party/libuv/src/unix/signal.c:532` | `uv__signal_stop(handle);` |
| `ev_7f6793cbc485` | assignment | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_7f8161196394` | call_site | `third_party/libuv/src/unix/fs.c:889` | `nread = pread(in_fd, buf, buflen, offset);` |
| `ev_7f97a20176a3` | call_site | `third_party/libuv/src/unix/fsevents.c:684` | `uv_mutex_destroy(&loop->cf_mutex);` |
| `ev_7f9805d77b81` | call_site | `third_party/libuv/src/unix/stream.c:790` | `memset(&cmsg, 0, sizeof(cmsg));` |
| `ev_7f9991823f2e` | call_site | `third_party/libuv/src/unix/signal.c:219` | `uv__signal_unlock();` |
| `ev_7fc004c222d4` | call_site | `third_party/libuv/src/unix/core.c:1808` | `r = uv_fileno(handle, &fd);` |
| `ev_7fca44d60f49` | call_site | `third_party/libuv/src/timer.c:89` | `heap_insert(timer_heap(handle->loop),` |
| `ev_7fda347c51a3` | call_site | `third_party/libuv/src/unix/stream.c:1521` | `uv_thread_join(&s->thread);` |
| `ev_7ff7eedbe563` | call_site | `third_party/libuv/src/unix/kqueue.c:199` | `assert(w->fd >= 0);` |
| `ev_7ffe0a334d62` | call_site | `third_party/libuv/src/unix/core.c:580` | `err = uv__nonblock(peerfd, 1);` |
| `ev_802e2db1a21a` | call_site | `third_party/libuv/src/unix/stream.c:182` | `if (errno == EINTR)` |
| `ev_803d9fc2e66f` | call_site | `third_party/libuv/src/unix/stream.c:380` | `uv_sem_destroy(&s->async_sem);` |
| `ev_8053cf589106` | call_site | `third_party/libuv/src/unix/fsevents.c:659` | `uv_sem_destroy(&loop->cf_sem);` |
| `ev_80550f065c42` | call_site | `third_party/libuv/src/unix/kqueue.c:367` | `assert(fd == w->fd);` |
| `ev_8069e20e2f49` | call_site | `third_party/libuv/src/unix/tty.c:378` | `return UV__ERR(errno);` |
| `ev_807683da2b22` | call_site | `third_party/libuv/src/unix/tty.c:182` | `if (uv__tty_is_slave(fd) && ttyname_r(fd, path, sizeof(path)) == 0)` |
| `ev_807929ffb79d` | call_site | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_807af17cbd7c` | call_site | `third_party/libuv/src/unix/core.c:1394` | `gr_mem += strlen(gr_mem) + 1;` |
| `ev_807fa680de87` | call_site | `third_party/libuv/src/unix/tcp.c:301` | `memcpy(&tmp6, addr, sizeof(tmp6));` |
| `ev_80caf9cfa23a` | call_site | `third_party/libuv/src/unix/stream.c:1290` | `uv__write_callbacks(stream);` |
| `ev_80ce08357450` | call_site | `third_party/libuv/src/uv-common.c:313` | `return uv_inet_ntop(AF_INET, &((struct sockaddr_in *)src)->sin_addr,` |
| `ev_814facd894f9` | call_site | `third_party/libuv/src/unix/tcp.c:136` | `uv__close(tcp->io_watcher.fd);` |
| `ev_8155b2ad829c` | call_site | `third_party/libuv/src/unix/fsevents.c:527` | `core_services_handle = dlopen("/System/Library/Frameworks/"` |
| `ev_816698ce7e00` | call_site | `third_party/libuv/src/unix/thread.c:429` | `abort();` |
| `ev_81822f939bc1` | call_site | `third_party/libuv/src/threadpool.c:89` | `uv__queue_init(q);  /* Signal uv_cancel() that the work req is executing. */` |
| `ev_819e671c8811` | call_site | `third_party/libuv/src/unix/process.c:95` | `memset(&loop->child_watcher, 0, sizeof(loop->child_watcher));` |
| `ev_81a4233afcb2` | call_site | `third_party/libuv/src/unix/process.c:1029` | `abort();` |
| `ev_81c808a3bc76` | call_site | `third_party/libuv/src/unix/fs.c:2276` | `uv__fs_scandir_cleanup(req);` |
| `ev_81d860abd7b7` | call_site | `third_party/libuv/src/unix/thread.c:880` | `return UV__ERR(pthread_key_create(key, NULL));` |
| `ev_81db7a9d7a79` | call_site | `third_party/libuv/src/unix/fs.c:2188` | `PATH2;` |
| `ev_81ddac4db117` | call_site | `third_party/libuv/src/unix/stream.c:1522` | `uv_sem_destroy(&s->close_sem);` |
| `ev_81f97056b8fd` | call_site | `third_party/libuv/src/timer.c:187` | `queue_node = uv__queue_head(&ready_queue);` |
| `ev_82011c2a41c9` | call_site | `third_party/libuv/src/unix/core.c:1393` | `strcpy(gr_mem, gp.gr_mem[r]);` |
| `ev_820f11433640` | call_site | `third_party/libuv/src/unix/poll.c:84` | `err = uv__nonblock_fcntl(fd, 1);` |
| `ev_8217b34cd8f0` | call_site | `third_party/libuv/src/unix/async.c:245` | `while (r == -1 && errno == EINTR);` |
| `ev_826173396cba` | call_site | `third_party/libuv/src/uv-common.c:301` | `return uv_inet_ntop(AF_INET, &src->sin_addr, dst, size);` |
| `ev_827825785ab4` | call_site | `third_party/libuv/src/thread-common.c:110` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_82872ae21da3` | call_site | `third_party/libuv/src/uv-common.c:89` | `errno = saved_errno;` |
| `ev_8299d963714c` | call_site | `third_party/libuv/src/unix/stream.c:651` | `else if (shutdown(uv__stream_fd(stream), SHUT_WR))` |
| `ev_82c7f16d1e5e` | assignment | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_830154a4c8db` | call_site | `third_party/libuv/src/unix/core.c:195` | `uv__async_close((uv_async_t*)handle);` |
| `ev_832e035d8a9a` | call_site | `third_party/libuv/src/unix/tty.c:374` | `err = ioctl(uv__stream_fd(tty), TIOCGWINSZ, &ws);` |
| `ev_834b0d3a1de5` | call_site | `third_party/libuv/src/unix/stream.c:383` | `uv_sem_destroy(&s->close_sem);` |
| `ev_834e9d8b5921` | call_site | `third_party/libuv/src/unix/stream.c:1204` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_8350b4fa6192` | call_site | `third_party/libuv/src/unix/darwin.c:102` | `if (host_statistics(mach_host_self(), HOST_VM_INFO,` |
| `ev_8351687ab60b` | call_site | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_836c323fa0fe` | call_site | `third_party/libuv/src/unix/kqueue.c:557` | `abort();` |
| `ev_836f4a80e747` | call_site | `third_party/libuv/src/unix/core.c:993` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_8398ce4bdc2f` | call_site | `third_party/libuv/src/threadpool.c:81` | `q = uv__queue_head(&wq);` |
| `ev_839ed4825e5f` | call_site | `third_party/libuv/src/unix/udp.c:1340` | `r = UV__ERR(errno);` |
| `ev_83a41e9ab7a1` | call_site | `third_party/libuv/src/unix/tcp.c:441` | `return UV__ERR(errno);` |
| `ev_83bb25b6b9b4` | call_site | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_840307191aa9` | call_site | `third_party/libuv/src/unix/random-devurandom.c:82` | `status = uv__random_readpath("/dev/random", &c, 1);` |
| `ev_841fbc18151d` | call_site | `third_party/libuv/src/fs-poll.c:90` | `memcpy(ctx->path, path, len + 1);` |
| `ev_8421ff19b86f` | call_site | `third_party/libuv/src/unix/udp.c:125` | `req->send_cb(req, req->status);` |
| `ev_842791aeeedd` | call_site | `third_party/libuv/src/unix/udp.c:716` | `if (uv_ip6_addr(interface_addr, 0, &addr6))` |
| `ev_843ff40b92c5` | call_site | `third_party/libuv/src/unix/random-devurandom.c:56` | `while (n == -1 && errno == EINTR);` |
| `ev_8443df6fae21` | call_site | `third_party/libuv/src/unix/stream.c:595` | `uv__io_start(server->loop, &server->io_watcher, POLLIN);` |
| `ev_84482511256c` | call_site | `third_party/libuv/src/unix/core.c:1497` | `len = strlen(var);` |
| `ev_8451186eb1f3` | call_site | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_845f29d716c9` | call_site | `third_party/libuv/src/unix/process.c:914` | `uv_rwlock_wrlock(&loop->cloexec_lock);` |
| `ev_846820e53f9d` | call_site | `third_party/libuv/src/unix/fs.c:1355` | `err = UV__ERR(errno);` |
| `ev_846bc7c6bca9` | call_site | `third_party/libuv/src/unix/signal.c:477` | `assert(!(handle->flags & UV_HANDLE_CLOSING));` |
| `ev_848e03795dba` | call_site | `third_party/libuv/src/queue.h:66` | `uv__queue_split(h, h->next, n);` |
| `ev_848eec88c44e` | call_site | `third_party/libuv/src/inet.c:53` | `l = snprintf(tmp, sizeof(tmp), fmt, src[0], src[1], src[2], src[3]);` |
| `ev_849396e6cca7` | call_site | `third_party/libuv/src/unix/process.c:936` | `} else if (r == -1 && errno == EPIPE) {` |
| `ev_8499d75c493c` | call_site | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_84b75c9ae774` | call_site | `third_party/libuv/src/unix/process.c:577` | `err = posix_spawn_file_actions_adddup2(` |
| `ev_85036a20bf6b` | call_site | `third_party/libuv/src/unix/signal.c:213` | `(r == -1 && (errno == EAGAIN \|\| errno == EWOULDBLOCK)));` |
| `ev_853fd77ee1a5` | call_site | `third_party/libuv/src/unix/stream.c:1525` | `uv__close(s->int_fd);` |
| `ev_8552f15a2590` | call_site | `third_party/libuv/src/idna.c:178` | `c = uv__utf8_decode1(&s, se);` |
| `ev_8556ed0432de` | call_site | `third_party/libuv/src/threadpool.c:302` | `uv_async_send(&loop->wq_async);` |
| `ev_85717ca19a40` | call_site | `third_party/libuv/src/unix/core.c:988` | `uv__queue_insert_tail(&loop->pending_queue, &w->pending_queue);` |
| `ev_85840402817e` | call_site | `third_party/libuv/src/fs-poll.c:179` | `assert(ctx->parent_handle != NULL);` |
| `ev_859516413ae5` | call_site | `third_party/libuv/src/threadpool.c:50` | `abort();` |
| `ev_85a3a740507a` | call_site | `third_party/libuv/src/unix/fsevents.c:240` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_85a89b637451` | call_site | `third_party/libuv/src/unix/fs.c:2214` | `PATH;` |
| `ev_85dd0d3a7986` | assignment | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_85ec735aee3a` | call_site | `third_party/libuv/src/unix/stream.c:1342` | `err = uv__check_before_write(stream, nbufs, send_handle);` |
| `ev_86009eba06be` | call_site | `third_party/libuv/src/uv-common.c:747` | `assert(nbufs);` |
| `ev_860dd1a2cd6b` | call_site | `third_party/libuv/src/unix/pipe.c:536` | `uv__close(temp[1]);` |
| `ev_86133c1a823d` | call_site | `third_party/libuv/src/unix/core.c:547` | `fd = uv__open_cloexec(path, O_RDONLY);` |
| `ev_861532f4f5e8` | call_site | `third_party/libuv/src/unix/fsevents.c:480` | `pCFRelease(cf_paths);` |
| `ev_863cb0ea432f` | call_site | `third_party/libuv/src/unix/stream.c:1523` | `uv_sem_destroy(&s->async_sem);` |
| `ev_866a9cce71ad` | call_site | `third_party/libuv/src/unix/core.c:849` | `while (!uv__queue_empty(&pq)) {` |
| `ev_867293ea574a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_8673ccdb7fa3` | call_site | `third_party/libuv/src/unix/loop.c:55` | `uv__queue_init(&loop->async_handles);` |
| `ev_867f3bc2bdac` | call_site | `third_party/libuv/src/unix/fsevents.c:559` | `V(core_services_handle, FSEventStreamStop);` |
| `ev_8700275783f6` | call_site | `third_party/libuv/src/idna.c:356` | `rc = uv__idna_toascii_label(s, se, &d, de);` |
| `ev_8729f0989741` | call_site | `third_party/libuv/src/unix/getnameinfo.c:73` | `req->getnameinfo_cb(req, req->retcode, host, service);` |
| `ev_8759c9907e95` | call_site | `third_party/libuv/src/unix/fs.c:1278` | `dstfd = uv_fs_open(NULL,` |
| `ev_87780bd3e380` | call_site | `third_party/libuv/src/unix/async.c:373` | `uv__queue_remove(q);` |
| `ev_8784472b39e8` | call_site | `third_party/libuv/src/unix/poll.c:159` | `uv__poll_stop(handle);` |
| `ev_879b038cf0b3` | call_site | `third_party/libuv/src/threadpool.c:147` | `uv__queue_insert_tail(&slow_io_pending_wq, q);` |
| `ev_87a43b67c216` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:117` | `memset(&address->netmask, 0, sizeof(address->netmask));` |
| `ev_87ae09c864b6` | call_site | `third_party/libuv/src/unix/loop.c:168` | `uv__signal_loop_cleanup(loop);` |
| `ev_87e0b4b4f8e6` | call_site | `third_party/libuv/src/unix/fsevents.c:421` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_87ec923c051a` | call_site | `third_party/libuv/src/unix/pipe.c:338` | `uv__queue_init(&req->queue);` |
| `ev_87f826be3431` | call_site | `third_party/libuv/src/uv-common.c:835` | `va_end(ap);` |
| `ev_88222e2c3fb0` | call_site | `third_party/libuv/src/unix/tcp.c:168` | `return UV__ERR(errno);` |
| `ev_8822dd8ed2e8` | call_site | `third_party/libuv/src/unix/stream.c:107` | `err = uv__open_cloexec("/", O_RDONLY);` |
| `ev_882b5680dbef` | call_site | `third_party/libuv/src/unix/darwin.c:42` | `if (uv__kqueue_init(loop))` |
| `ev_882cc3a75241` | call_site | `third_party/libuv/src/unix/core.c:269` | `assert(handle->flags & UV_HANDLE_CLOSING);` |
| `ev_885f2d8683be` | call_site | `third_party/libuv/src/unix/kqueue.c:227` | `if (kevent(loop->backend_fd, events, nevents, NULL, 0, NULL))` |
| `ev_886ea4c2fdee` | call_site | `third_party/libuv/src/unix/thread.c:796` | `abort();` |
| `ev_888f9cc8daa6` | call_site | `third_party/libuv/src/unix/udp.c:606` | `handle->send_queue_size += uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_888fccbe3315` | call_site | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_889f2f65fab4` | call_site | `third_party/libuv/src/unix/fsevents.c:254` | `len = strlen(path);` |
| `ev_88a2e919b5b4` | call_site | `third_party/libuv/src/unix/dl.c:55` | `*ptr = dlsym(lib->handle, name);` |
| `ev_88cebbc38c3d` | call_site | `third_party/libuv/src/unix/fs.c:1724` | `X(FTRUNCATE, ftruncate(req->file, req->off));` |
| `ev_88d5bb7eae60` | call_site | `third_party/libuv/src/threadpool.c:134` | `uv_mutex_lock(&mutex);` |
| `ev_88f44777a60b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:103` | `S("_LSGetCurrentApplicationASN"));` |
| `ev_8908b0232434` | call_site | `third_party/libuv/src/unix/stream.c:1540` | `uv__close(handle->io_watcher.fd);` |
| `ev_892ce661d115` | call_site | `third_party/libuv/src/unix/fsevents.c:769` | `item = uv__malloc(sizeof(*item));` |
| `ev_8951169c97a8` | call_site | `third_party/libuv/src/timer.c:182` | `uv_timer_stop(handle);` |
| `ev_896d29c2c62f` | call_site | `third_party/libuv/src/fs-poll.c:179` | `assert(ctx->parent_handle != NULL);` |
| `ev_89832f95168f` | call_site | `third_party/libuv/src/unix/stream.c:173` | `if (uv__io_active(&stream->io_watcher, POLLIN))` |
| `ev_89944018e590` | call_site | `third_party/libuv/src/threadpool.c:326` | `uv__queue_remove(q);` |
| `ev_89a5c35c4a43` | call_site | `third_party/libuv/src/unix/udp.c:1022` | `return uv__setsockopt(handle, option4, option6, &arg, sizeof(arg));` |
| `ev_89b22020ea9e` | call_site | `third_party/libuv/src/unix/fsevents.c:890` | `uv_close((uv_handle_t*) handle->cf_cb, (uv_close_cb) uv__free);` |
| `ev_89b800a3da29` | call_site | `third_party/libuv/src/unix/fsevents.c:308` | `memcpy(event->path, path, len + 1);` |
| `ev_89ec81972ffc` | call_site | `third_party/libuv/src/unix/udp.c:322` | `if (setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &yes, sizeof(yes)))` |
| `ev_89ed7f7e890c` | call_site | `third_party/libuv/src/unix/stream.c:461` | `stream->connect_req->cb(stream->connect_req, UV_ECANCELED);` |
| `ev_8a079a656194` | call_site | `third_party/libuv/src/unix/tcp.c:94` | `return new_socket(handle, domain, flags);` |
| `ev_8a098305e9ab` | call_site | `third_party/libuv/src/unix/fs.c:1968` | `PATH2;` |
| `ev_8a0bc26439f6` | call_site | `third_party/libuv/src/unix/kqueue.c:185` | `assert(uv__queue_empty(&loop->watcher_queue));` |
| `ev_8a10c970642d` | call_site | `third_party/libuv/src/uv-common.c:893` | `memset(loop, -1, sizeof(*loop));` |
| `ev_8a1c1d69a022` | call_site | `third_party/libuv/src/unix/core.c:1847` | `assert(rc == 0);` |
| `ev_8a2d2e5b978b` | call_site | `third_party/libuv/src/uv-common.c:495` | `addrlen = uv__udp_check_before_send(handle, addr);` |
| `ev_8a3b2615659b` | call_site | `third_party/libuv/src/unix/core.c:851` | `uv__queue_remove(q);` |
| `ev_8a7645104cfb` | assignment | `third_party/libuv/src/unix/poll.c:91` | `uv__io_init(&handle->io_watcher, uv__poll_io, fd);` |
| `ev_8a8c8d43c608` | call_site | `third_party/libuv/src/unix/thread.c:872` | `abort();` |
| `ev_8a8fef961a5b` | call_site | `third_party/libuv/src/unix/fs.c:353` | `if (r >= 0 && uv__cloexec(r, 1) != 0) {` |
| `ev_8aa5318c12f8` | call_site | `third_party/libuv/src/unix/stream.c:937` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_8ab5cf71b1e1` | call_site | `third_party/libuv/src/thread-common.c:107` | `uv_cond_broadcast((uv_cond_t*) &b->cond);` |
| `ev_8ad099db703f` | call_site | `third_party/libuv/src/unix/pipe.c:112` | `pipe_fname = uv__malloc(namelen + 1);` |
| `ev_8ad24f7111f1` | call_site | `third_party/libuv/src/unix/thread.c:359` | `if (pthread_mutex_destroy(mutex))` |
| `ev_8b09c69fb987` | call_site | `third_party/libuv/src/heap-inl.h:222` | `if (child->left != NULL && less_than(child->left, smallest))` |
| `ev_8b150c03f1d7` | call_site | `third_party/libuv/src/unix/random-getentropy.c:54` | `return UV__ERR(errno);` |
| `ev_8b3fe28acd59` | call_site | `third_party/libuv/src/unix/core.c:1130` | `if (uv__close_nocheckstdio(fd))` |
| `ev_8b45daadca58` | call_site | `third_party/libuv/src/unix/internal.h:416` | `rc = fstat(fd, s);` |
| `ev_8b7f6ffda2d7` | call_site | `third_party/libuv/src/unix/fsevents.c:631` | `if (pthread_attr_setstacksize(&attr, uv__thread_stack_size()))` |
| `ev_8b8b27b45239` | call_site | `third_party/libuv/src/fs-poll.c:253` | `assert(last->previous != NULL);` |
| `ev_8bab69c4e47c` | call_site | `third_party/libuv/src/unix/udp.c:817` | `memset(&mreq, 0, sizeof(mreq));` |
| `ev_8bca323dfdca` | call_site | `third_party/libuv/src/unix/process.c:775` | `err = uv__spawn_set_posix_spawn_attrs(&attrs, posix_spawn_fncs, options);` |
| `ev_8bcba93cfab2` | call_site | `third_party/libuv/src/fs-poll.c:168` | `uv_fs_poll_stop(handle);` |
| `ev_8bfedbad7f45` | call_site | `third_party/libuv/src/unix/signal.c:144` | `abort();` |
| `ev_8c1081a3c5b7` | call_site | `third_party/libuv/src/unix/fs.c:512` | `return uv__preadv_or_pwritev(fd, bufs, nbufs, off, &cache, /*is_pread*/0);` |
| `ev_8c212d16a019` | call_site | `third_party/libuv/src/unix/udp.c:128` | `if (uv__queue_empty(&handle->write_queue)) {` |
| `ev_8c31c88d6d04` | call_site | `third_party/libuv/src/unix/signal.c:189` | `memset(&msg, 0, sizeof msg);` |
| `ev_8c331b54d50a` | call_site | `third_party/libuv/src/unix/thread.c:496` | `abort();` |
| `ev_8c3979abc4b1` | call_site | `third_party/libuv/src/unix/udp.c:1377` | `req->status = uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_8c41ce7011b4` | assignment | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_8c4f424c4e01` | call_site | `third_party/libuv/src/unix/signal.c:74` | `abort();` |
| `ev_8c556db430c1` | call_site | `third_party/libuv/src/unix/core.c:994` | `assert(0 != events);` |
| `ev_8c5939342984` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:84` | `dlsym(core_foundation_handle, "CFBundleGetFunctionPointerForName");` |
| `ev_8c5f4faca50f` | call_site | `third_party/libuv/src/unix/stream.c:1558` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_8c69561c8948` | call_site | `third_party/libuv/src/uv-common.c:614` | `uv__print_handles(loop, 1, stream);` |
| `ev_8c6b6bb04461` | assignment | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_8c8fe0ae3395` | call_site | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_8ca419191127` | call_site | `third_party/libuv/src/fs-poll.c:80` | `ctx = uv__calloc(1, sizeof(*ctx) + len);` |
| `ev_8cbd97a1d7ff` | call_site | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_8d2587913b86` | call_site | `third_party/libuv/src/unix/fsevents.c:548` | `V(core_foundation_handle, CFRunLoopSourceCreate);` |
| `ev_8d5b46240f43` | call_site | `third_party/libuv/src/unix/core.c:966` | `assert(loop->nfds > 0);` |
| `ev_8d5bed6f359b` | call_site | `third_party/libuv/src/unix/udp.c:197` | `handle->recv_cb(handle, UV__ERR(errno), buf, NULL, 0);` |
| `ev_8d7e05f143e1` | call_site | `third_party/libuv/src/unix/stream.c:1385` | `uv__write(stream);` |
| `ev_8d7f73a4cce7` | call_site | `third_party/libuv/src/unix/fs.c:1774` | `assert(req->result == 0);` |
| `ev_8d8e3e7d5ef4` | call_site | `third_party/libuv/src/idna.c:499` | `assert(code_point >= 0);` |
| `ev_8d9e6a8a95c2` | call_site | `third_party/libuv/src/unix/core.c:1070` | `memset(rusage, 0, sizeof(*rusage));` |
| `ev_8da70dae3f9f` | call_site | `third_party/libuv/src/unix/process.c:1028` | `if (errno != ESRCH)` |
| `ev_8db635d437c0` | call_site | `third_party/libuv/src/unix/fsevents.c:565` | `dlclose(core_services_handle);` |
| `ev_8dba8a2cece4` | call_site | `third_party/libuv/src/unix/udp.c:778` | `mreq.imr_interface.s_addr = htonl(INADDR_ANY);` |
| `ev_8dc6560f30db` | call_site | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_8de1db9cb950` | call_site | `third_party/libuv/src/unix/core.c:1128` | `while (n == -1 && errno == EINTR);` |
| `ev_8e0af9132b30` | call_site | `third_party/libuv/src/unix/random-devurandom.c:87` | `uv_once(&once, uv__random_devurandom_init);` |
| `ev_8e0f7f9df419` | call_site | `third_party/libuv/src/unix/process.c:703` | `path = uv__spawn_find_path_in_env(env);` |
| `ev_8e213c87f3a3` | call_site | `third_party/libuv/src/unix/process.c:176` | `assert(uv__queue_empty(&pending));` |
| `ev_8e2a22f18f87` | call_site | `third_party/libuv/src/unix/process.c:932` | `err = waitpid(*pid, &status, 0); /* okay, read errorno */` |
| `ev_8e2afb8db7ba` | call_site | `third_party/libuv/src/unix/core.c:220` | `uv__poll_close((uv_poll_t*)handle);` |
| `ev_8e3d8b6539fb` | call_site | `third_party/libuv/src/unix/udp.c:1399` | `uv__queue_remove(&req->queue);` |
| `ev_8e52d127706f` | call_site | `third_party/libuv/src/unix/udp.c:1375` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_8e72f246673c` | call_site | `third_party/libuv/src/uv-common.c:725` | `uv__fs_scandir_free(dents[i]);` |
| `ev_8e84a5a773e9` | call_site | `third_party/libuv/src/unix/fs.c:1746` | `X(UNLINK, unlink(req->path));` |
| `ev_8e90f2f0061d` | call_site | `third_party/libuv/src/unix/fs.c:1203` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_8eb3e43caf10` | call_site | `third_party/libuv/src/unix/udp.c:451` | `memset(addr, 0, sizeof *addr);` |
| `ev_8eb9f4be2d9f` | call_site | `third_party/libuv/src/uv-common.c:909` | `err = uv_loop_close(loop);` |
| `ev_8ec44eae80d5` | call_site | `third_party/libuv/src/unix/fsevents.c:236` | `assert(state != NULL);` |
| `ev_8ecf7baf4b64` | call_site | `third_party/libuv/src/timer.c:189` | `uv__queue_init(queue_node);` |
| `ev_8ef1bbe13fbb` | call_site | `third_party/libuv/src/unix/dl.c:68` | `uv__free(lib->errmsg);` |
| `ev_8f018f9369dc` | assignment | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_8f26eb811f45` | call_site | `third_party/libuv/src/unix/stream.c:612` | `err = uv__pipe_listen((uv_pipe_t*)stream, backlog, cb);` |
| `ev_8f57ebd5377c` | call_site | `third_party/libuv/src/unix/signal.c:451` | `if (r == -1 && (errno == EAGAIN \|\| errno == EWOULDBLOCK)) {` |
| `ev_8f5ba541b11c` | call_site | `third_party/libuv/src/unix/async.c:345` | `uv__async_spin(h);` |
| `ev_8f6fde152313` | call_site | `third_party/libuv/src/unix/udp.c:1167` | `assert(0 && "unexpected address family");` |
| `ev_8f730bb35ca5` | call_site | `third_party/libuv/src/unix/kqueue.c:55` | `loop->backend_fd = kqueue();` |
| `ev_8f83c2427ef5` | call_site | `third_party/libuv/src/unix/process.c:1047` | `err = uv__process_open_stream(options->stdio + i, pipes[i]);` |
| `ev_8fa7f12fa952` | call_site | `third_party/libuv/src/unix/thread.c:804` | `if (pthread_cond_signal(cond))` |
| `ev_8fab43dca120` | call_site | `third_party/libuv/src/unix/process.c:246` | `return uv__stream_open(container->data.stream, pipefds[0], flags);` |
| `ev_8fb7349469b6` | call_site | `third_party/libuv/src/unix/stream.c:293` | `kq = kqueue();` |
| `ev_8fba5d7ce7d4` | call_site | `third_party/libuv/src/unix/fsevents.c:898` | `uv_mutex_destroy(&handle->cf_mutex);` |
| `ev_8fc0e4559b5a` | call_site | `third_party/libuv/src/unix/core.c:452` | `uv__run_prepare(loop);` |
| `ev_903bee8fb2ff` | call_site | `third_party/libuv/src/unix/poll.c:114` | `uv__poll_stop(handle);` |
| `ev_90507fb3e4a5` | call_site | `third_party/libuv/src/uv-common.c:425` | `return uv__udp_disconnect(handle);` |
| `ev_9050c2d83dea` | call_site | `third_party/libuv/src/unix/core.c:1450` | `buf = uv__strdup(environ[j]);` |
| `ev_906405d3e7d4` | call_site | `third_party/libuv/src/unix/signal.c:103` | `if (uv__make_pipe(uv__signal_lock_pipefd, 0))` |
| `ev_906ee55f80c3` | call_site | `third_party/libuv/src/unix/signal.c:161` | `abort();` |
| `ev_9093aadca805` | call_site | `third_party/libuv/src/unix/fs.c:1705` | `errno = 0;` |
| `ev_90ba0c8ebd79` | call_site | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_90c27b7d36f2` | call_site | `third_party/libuv/src/unix/stream.c:1558` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_90f0cfd2d7f3` | call_site | `third_party/libuv/src/unix/udp.c:619` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_90fc30076d5a` | call_site | `third_party/libuv/src/unix/stream.c:1064` | `nread = read(uv__stream_fd(stream), buf.base, buf.len);` |
| `ev_910f4cab3627` | call_site | `third_party/libuv/src/unix/darwin.c:183` | `unsigned int ticks = (unsigned int)sysconf(_SC_CLK_TCK),` |
| `ev_911509385277` | call_site | `third_party/libuv/src/uv-common.c:60` | `return memcpy(m, s, len);` |
| `ev_912142859eda` | call_site | `third_party/libuv/src/unix/pipe.c:99` | `if (uv__stream_fd(handle) >= 0)` |
| `ev_913d84408ff1` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:136` | `pCFBundleGetFunctionPointerForName(` |
| `ev_9145bd76d762` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_9153b09f77a1` | call_site | `third_party/libuv/src/unix/udp.c:1369` | `q = uv__queue_next(q);` |
| `ev_9162580bf160` | call_site | `third_party/libuv/src/unix/thread.c:327` | `abort();` |
| `ev_9170115c6d6b` | call_site | `third_party/libuv/src/unix/stream.c:220` | `assert(events != 0 \|\| FD_ISSET(s->int_fd, s->sread));` |
| `ev_9187d4cf3774` | call_site | `third_party/libuv/src/unix/loop.c:169` | `uv__platform_loop_delete(loop);` |
| `ev_918f4160003e` | call_site | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_9196265ec309` | call_site | `third_party/libuv/src/unix/proctitle.c:116` | `memcpy(pt->str, title, len);` |
| `ev_919d9de04858` | call_site | `third_party/libuv/src/unix/fsevents.c:419` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_91afe4964a4b` | call_site | `third_party/libuv/src/unix/udp.c:278` | `handle->recv_cb(handle, nread, &buf, (const struct sockaddr*) &peer, flags);` |
| `ev_91e2a35bf663` | call_site | `third_party/libuv/src/unix/process.c:340` | `use_fd = open("/dev/null", fd == 0 ? O_RDONLY : O_RDWR);` |
| `ev_91ecc97a6372` | call_site | `third_party/libuv/src/unix/fsevents.c:453` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_92021d222814` | call_site | `third_party/libuv/src/unix/pipe.c:167` | `if (listen(uv__stream_fd(handle), backlog))` |
| `ev_9211d111f581` | call_site | `third_party/libuv/src/unix/stream.c:1235` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_921f5206c390` | call_site | `third_party/libuv/src/unix/core.c:1546` | `if (gethostname(buf, sizeof(buf)) != 0)` |
| `ev_924d1bbc8b1b` | call_site | `third_party/libuv/src/unix/signal.c:209` | `r = write(handle->loop->signal_pipefd[1], &msg, sizeof msg);` |
| `ev_92527806ab16` | call_site | `third_party/libuv/src/unix/fs.c:1354` | `if (fchmod(dstfd, src_statsbuf.st_mode) == -1) {` |
| `ev_926391b3b2f4` | call_site | `third_party/libuv/src/unix/udp.c:551` | `if (errno != EAFNOSUPPORT && errno != EINVAL)` |
| `ev_92655b3c6378` | call_site | `third_party/libuv/src/unix/udp.c:195` | `handle->recv_cb(handle, 0, buf, NULL, 0);` |
| `ev_926c13c5c85b` | call_site | `third_party/libuv/src/unix/process.c:523` | `(void) posix_spawnattr_destroy(attrs);` |
| `ev_92a32d90b1e1` | call_site | `third_party/libuv/src/unix/fsevents.c:691` | `uv__free(s);` |
| `ev_92b39da3388f` | call_site | `third_party/libuv/src/unix/thread.c:483` | `if (semaphore_signal(*sem))` |
| `ev_92c241a4ff29` | call_site | `third_party/libuv/src/unix/signal.c:149` | `abort();` |
| `ev_92cf37040163` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:116` | `S("_kLSDisplayNameKey"));` |
| `ev_92db1b96584c` | call_site | `third_party/libuv/src/unix/fsevents.c:741` | `uv_mutex_lock(&loop->cf_mutex);` |
| `ev_92e032141a9e` | call_site | `third_party/libuv/src/inet.c:57` | `uv__strscpy(dst, tmp, size);` |
| `ev_92e7619db474` | call_site | `third_party/libuv/src/unix/kqueue.c:589` | `return UV__ERR(errno);` |
| `ev_930ba6539480` | call_site | `third_party/libuv/src/unix/core.c:1687` | `return UV__ERR(errno);` |
| `ev_932ec8b332ff` | call_site | `third_party/libuv/src/unix/darwin.c:160` | `assert(err == KERN_SUCCESS);` |
| `ev_93301b7a3cbf` | call_site | `third_party/libuv/src/unix/loop.c:88` | `uv__queue_init(&loop->process_handles);` |
| `ev_933a7b9157fd` | assignment | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_933abdc79656` | call_site | `third_party/libuv/src/unix/kqueue.c:368` | `uv__metrics_update_idle_time(loop);` |
| `ev_935e212037fb` | call_site | `third_party/libuv/src/unix/udp.c:601` | `uv__req_unregister(handle->loop);` |
| `ev_939cfc2f57d7` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:79` | `if (getifaddrs(&addrs) != 0)` |
| `ev_93b7aa43cdb8` | call_site | `third_party/libuv/src/unix/thread.c:352` | `abort();` |
| `ev_94193e1159f3` | call_site | `third_party/libuv/src/unix/fs.c:1284` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_941cc1bccfd7` | call_site | `third_party/libuv/src/unix/fs.c:2173` | `PATH;` |
| `ev_944a82327899` | call_site | `third_party/libuv/src/unix/core.c:224` | `uv__fs_poll_close((uv_fs_poll_t*)handle);` |
| `ev_944bdd7415ef` | call_site | `third_party/libuv/src/unix/process.c:644` | `(void) posix_spawn_file_actions_destroy(actions);` |
| `ev_945b33e3f6f6` | call_site | `third_party/libuv/src/unix/process.c:636` | `assert(err != ENOSYS);` |
| `ev_945e53dd7399` | call_site | `third_party/libuv/src/unix/process.c:380` | `SAVE_ERRNO(setgroups(0, NULL));` |
| `ev_947227b3b116` | call_site | `third_party/libuv/src/uv-common.c:757` | `uv__fs_scandir_free(dents);` |
| `ev_94a18feeb47e` | call_site | `third_party/libuv/src/unix/thread.c:449` | `abort();` |
| `ev_94a57a363447` | call_site | `third_party/libuv/src/unix/tcp.c:559` | `return UV__ERR(errno);` |
| `ev_94a8fa2b63f7` | call_site | `third_party/libuv/src/unix/stream.c:652` | `err = UV__ERR(errno);` |
| `ev_94be85a7e907` | call_site | `third_party/libuv/src/unix/core.c:924` | `maybe_resize(loop, w->fd + 1);` |
| `ev_94c476b48777` | call_site | `third_party/libuv/src/thread-common.c:61` | `rc = uv_mutex_init(&b->mutex);` |
| `ev_94e1933354c1` | call_site | `third_party/libuv/src/unix/core.c:977` | `uv__io_stop(loop, w, POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI);` |
| `ev_94f64ad7ca60` | call_site | `third_party/libuv/src/random.c:90` | `req->cb(req, status, req->buf, req->buflen);` |
| `ev_9521436d2375` | call_site | `third_party/libuv/src/queue.h:64` | `uv__queue_init(n);` |
| `ev_9532a8692587` | call_site | `third_party/libuv/src/unix/udp.c:1237` | `memset(h, 0, sizeof(*h));` |
| `ev_957e6f6b3269` | call_site | `third_party/libuv/src/unix/pipe.c:342` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_958b3e530e0d` | call_site | `third_party/libuv/src/unix/async.c:311` | `uv__io_init(&loop->async_io_watcher, uv__async_io, pipefd[0]);` |
| `ev_95b5c4d30645` | call_site | `third_party/libuv/src/unix/stream.c:1283` | `req->cb(req, error);` |
| `ev_95ed398e9f04` | call_site | `third_party/libuv/src/unix/process.c:423` | `dlsym(RTLD_DEFAULT, "posix_spawn_file_actions_addchdir_np");` |
| `ev_95f5260e8fa3` | call_site | `third_party/libuv/src/unix/stream.c:788` | `fd_to_send = uv__handle_fd((uv_handle_t*) send_handle);` |
| `ev_96038fc493ba` | call_site | `third_party/libuv/src/unix/stream.c:837` | `return UV__ERR(errno);` |
| `ev_960d6e13976f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_960ecf83810d` | call_site | `third_party/libuv/src/uv-common.c:1043` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_960f995b9028` | call_site | `third_party/libuv/src/unix/signal.c:410` | `err = uv__signal_register_handler(signum, oneshot);` |
| `ev_962199be6dd2` | call_site | `third_party/libuv/src/unix/tcp.c:319` | `if (errno == EINPROGRESS)` |
| `ev_9622376feeb3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_962b51322708` | call_site | `third_party/libuv/src/unix/fs.c:2313` | `PATH;` |
| `ev_963a91257551` | call_site | `third_party/libuv/src/unix/udp.c:414` | `if (errno == EAFNOSUPPORT)` |
| `ev_965951b7fdc7` | call_site | `third_party/libuv/src/unix/core.c:1872` | `if (realpath(prog, abspath) != abspath)` |
| `ev_965a9b083a49` | call_site | `third_party/libuv/src/unix/darwin.c:77` | `if (_NSGetExecutablePath(exepath, &exepath_size))` |
| `ev_96678e28119a` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_96744dc15d31` | call_site | `third_party/libuv/src/unix/udp.c:1032` | `return UV__ERR(errno);` |
| `ev_967d883f0ba8` | call_site | `third_party/libuv/src/unix/tcp.c:45` | `if (getsockname(fd, &s.addr, &slen))` |
| `ev_9685951f020b` | call_site | `third_party/libuv/src/unix/core.c:409` | `return uv__next_timeout(loop);` |
| `ev_96a4a50c7fd7` | call_site | `third_party/libuv/src/unix/fs.c:2058` | `memcpy(req->bufs, bufs, nbufs * sizeof(*bufs));` |
| `ev_96a5baa42977` | call_site | `third_party/libuv/src/unix/fs.c:2302` | `PATH2;` |
| `ev_96bc0c497273` | call_site | `third_party/libuv/src/unix/udp.c:1144` | `} else if (uv_ip6_addr(interface_addr, 0, addr6) == 0) {` |
| `ev_96dcab071dd3` | call_site | `third_party/libuv/src/unix/process.c:821` | `sigdelset(&signewset, SIGBUS);` |
| `ev_96fa53e797d9` | call_site | `third_party/libuv/src/unix/dl.c:73` | `lib->errmsg = uv__strdup(errmsg);` |
| `ev_9707b2acf0f3` | call_site | `third_party/libuv/src/random.c:77` | `req->status = uv__random(req->buf, req->buflen);` |
| `ev_9710e5865b80` | call_site | `third_party/libuv/src/unix/fsevents.c:615` | `uv__queue_init(&state->fsevent_handles);` |
| `ev_973bd7f9ada4` | call_site | `third_party/libuv/src/unix/thread.c:323` | `if (pthread_mutexattr_init(&attr))` |
| `ev_97493536527e` | call_site | `third_party/libuv/src/unix/core.c:1194` | `uv_os_free_passwd(&pwd);` |
| `ev_974d806447a4` | call_site | `third_party/libuv/src/unix/stream.c:1524` | `uv__close(s->fake_fd);` |
| `ev_974fd77dcb16` | call_site | `third_party/libuv/src/unix/core.c:564` | `assert(sockfd >= 0);` |
| `ev_975859089517` | call_site | `third_party/libuv/src/unix/core.c:137` | `r = clock_gettime(CLOCK_MONOTONIC, &t);` |
| `ev_977af2b00faf` | call_site | `third_party/libuv/src/unix/kqueue.c:484` | `assert(loop->watchers != NULL);` |
| `ev_97a752f84ed1` | call_site | `third_party/libuv/src/unix/dl.c:34` | `dlerror(); /* Reset error status. */` |
| `ev_97a8441cfeaf` | call_site | `third_party/libuv/src/unix/kqueue.c:556` | `if (kevent(loop->backend_fd, &ev, 1, NULL, 0, NULL))` |
| `ev_97b855a06eb3` | call_site | `third_party/libuv/src/unix/udp.c:820` | `err = uv_ip6_addr(interface_addr, 0, &addr6);` |
| `ev_97c08b79bdee` | call_site | `third_party/libuv/src/unix/kqueue.c:625` | `uv__io_start(handle->loop, &handle->event_watcher, POLLIN);` |
| `ev_97dbfc748dd8` | call_site | `third_party/libuv/src/unix/thread.c:376` | `abort();` |
| `ev_97f73163ce5b` | call_site | `third_party/libuv/src/unix/udp.c:871` | `uv__io_init(&handle->io_watcher, uv__udp_io, fd);` |
| `ev_981ed43605eb` | call_site | `third_party/libuv/src/uv-common.c:390` | `return uv__udp_bind(handle, addr, addrlen, flags);` |
| `ev_984d48ec7136` | call_site | `third_party/libuv/src/unix/fs.c:1162` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_98781bd3e95c` | call_site | `third_party/libuv/src/fs-poll.c:180` | `assert(ctx->parent_handle->poll_ctx == ctx);` |
| `ev_98997645656c` | call_site | `third_party/libuv/src/unix/signal.c:133` | `r = write(uv__signal_lock_pipefd[1], &data, sizeof data);` |
| `ev_98b503eb2c88` | call_site | `third_party/libuv/src/unix/fsevents.c:780` | `assert(state != NULL);` |
| `ev_9902fe133540` | call_site | `third_party/libuv/src/unix/pipe.c:295` | `memcpy(&saddr.sun_path, name, namelen);` |
| `ev_9917b1319099` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9943a256389b` | call_site | `third_party/libuv/src/unix/pipe.c:208` | `return UV__ERR(errno); /* according to docs, must be EBADF */` |
| `ev_996ae7240809` | call_site | `third_party/libuv/src/unix/thread.c:329` | `err = pthread_mutex_init(mutex, &attr);` |
| `ev_996d49afe4d2` | call_site | `third_party/libuv/src/unix/thread.c:184` | `pthread_attr_destroy(attr);` |
| `ev_9987d16484ee` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_999b93e07d63` | call_site | `third_party/libuv/src/unix/core.c:1249` | `memcpy(buffer, buf, len + 1);` |
| `ev_99a769c4a0c8` | call_site | `third_party/libuv/src/unix/tty.c:160` | `while (saved_flags == -1 && errno == EINTR);` |
| `ev_99b0cec72102` | call_site | `third_party/libuv/src/unix/pipe.c:304` | `r = connect(uv__stream_fd(handle), (struct sockaddr*)&saddr, addrlen);` |
| `ev_99d19f3cf47f` | call_site | `third_party/libuv/src/unix/core.c:1881` | `memcpy(buf, abspath, *buflen);` |
| `ev_99d67296e689` | call_site | `third_party/libuv/src/unix/core.c:691` | `while (r == -1 && errno == EINTR);` |
| `ev_9a000fe9979c` | call_site | `third_party/libuv/src/unix/signal.c:377` | `assert(!uv__is_closing(handle));` |
| `ev_9a0559702f1c` | call_site | `third_party/libuv/src/unix/udp.c:1379` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_9a05a35c399b` | call_site | `third_party/libuv/src/unix/process.c:1097` | `return UV__ERR(errno);` |
| `ev_9a1d24965d95` | call_site | `third_party/libuv/src/unix/darwin.c:234` | `vm_deallocate(mach_task_self(), (vm_address_t)info, msg_type);` |
| `ev_9a23b1a90869` | call_site | `third_party/libuv/src/threadpool.c:72` | `while (uv__queue_empty(&wq) \|\|` |
| `ev_9a2a70fb12d5` | call_site | `third_party/libuv/src/thread-common.c:116` | `uv_cond_broadcast((uv_cond_t*) &b->cond);` |
| `ev_9a415b790894` | call_site | `third_party/libuv/src/unix/signal.c:325` | `uv__close(loop->signal_pipefd[0]);` |
| `ev_9a42f315457a` | call_site | `third_party/libuv/src/unix/fsevents.c:553` | `V(core_foundation_handle, kCFRunLoopDefaultMode);` |
| `ev_9a455b79d1d7` | call_site | `third_party/libuv/src/unix/core.c:269` | `assert(handle->flags & UV_HANDLE_CLOSING);` |
| `ev_9a4ac97c49c8` | call_site | `third_party/libuv/src/unix/core.c:1901` | `snprintf(trypath, sizeof(trypath) - 1, "%s/%s", token, prog);` |
| `ev_9a5679a6a157` | call_site | `third_party/libuv/src/unix/process.c:403` | `uv__write_errno(error_fd);` |
| `ev_9a5e3250e49b` | call_site | `third_party/libuv/src/unix/process.c:369` | `if (options->cwd != NULL && chdir(options->cwd))` |
| `ev_9a5f048e1985` | call_site | `third_party/libuv/src/idna.c:251` | `c = uv__utf8_decode1(&s, se);` |
| `ev_9a81ff5bcbe9` | call_site | `third_party/libuv/src/inet.c:186` | `if ((pch = strchr(digits, ch)) != NULL) {` |
| `ev_9a8af568ba6d` | call_site | `third_party/libuv/src/unix/fsevents.c:392` | `pFSEventStreamInvalidate(state->fsevent_stream);` |
| `ev_9a9474e7673c` | call_site | `third_party/libuv/src/unix/stream.c:676` | `assert(req->handle->write_queue_size >= size);` |
| `ev_9abdcec53521` | call_site | `third_party/libuv/src/unix/fs.c:576` | `return strcmp((*a)->d_name, (*b)->d_name);` |
| `ev_9acfaae91c3f` | call_site | `third_party/libuv/src/unix/kqueue.c:653` | `uv__free(handle->path);` |
| `ev_9b30b0246595` | call_site | `third_party/libuv/src/unix/fs.c:1229` | `r = writev(fd, bufs, nbufs);` |
| `ev_9b5bab4789a4` | call_site | `third_party/libuv/src/unix/core.c:237` | `uv__make_close_pending(handle);` |
| `ev_9b5c1e099e5c` | call_site | `third_party/libuv/src/unix/udp.c:650` | `err = uv__udp_sendmsg1(handle->io_watcher.fd, bufs, nbufs, addr);` |
| `ev_9b63423b5c18` | call_site | `third_party/libuv/src/unix/pipe.c:309` | `err = UV__ERR(errno);` |
| `ev_9b865267da27` | call_site | `third_party/libuv/src/unix/tty.c:245` | `assert(tio != NULL);` |
| `ev_9b89c4efe46f` | call_site | `third_party/libuv/src/unix/core.c:1733` | `r = pthread_setschedparam(tid, policy, &param);` |
| `ev_9b8a29f55da5` | call_site | `third_party/libuv/src/unix/thread.c:300` | `return pthread_equal(*t1, *t2);` |
| `ev_9b8c8d69db30` | call_site | `third_party/libuv/src/unix/tcp.c:261` | `if (uv__is_ipv6_link_local(p->ifa_addr))` |
| `ev_9b94634f5892` | call_site | `third_party/libuv/src/unix/fs.c:1204` | `return lutimes(req->path, tv);` |
| `ev_9ba025374183` | call_site | `third_party/libuv/src/threadpool.c:109` | `uv__queue_remove(q);` |
| `ev_9bb8b32ca5a9` | call_site | `third_party/libuv/src/unix/core.c:1414` | `return uv__getpwuid_r(pwd, geteuid());` |
| `ev_9bfffacd6a23` | call_site | `third_party/libuv/src/timer.c:105` | `uv__queue_remove(&handle->node.queue);` |
| `ev_9c3efc1a4c58` | call_site | `third_party/libuv/src/unix/udp.c:86` | `assert(handle->send_queue_count == 0);` |
| `ev_9c43e65424a9` | call_site | `third_party/libuv/src/unix/core.c:918` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_9c5aa8a79c39` | call_site | `third_party/libuv/src/unix/stream.c:921` | `uv__free(req->bufs);` |
| `ev_9c783d6aa9ce` | call_site | `third_party/libuv/src/unix/fs.c:346` | `uv_rwlock_rdlock(&req->loop->cloexec_lock);` |
| `ev_9c78be2081b9` | call_site | `third_party/libuv/src/threadpool.c:352` | `req->work_cb(req);` |
| `ev_9c7c125833d8` | call_site | `third_party/libuv/src/unix/fs.c:163` | `if (errno == EINTR \|\| errno == EINPROGRESS)` |
| `ev_9ca11e61f466` | call_site | `third_party/libuv/src/unix/stream.c:1431` | `err = uv__check_before_write(stream, nbufs, NULL);` |
| `ev_9ca82e9d4980` | call_site | `third_party/libuv/src/unix/thread.c:805` | `abort();` |
| `ev_9cbc9a4b05fa` | call_site | `third_party/libuv/src/unix/stream.c:813` | `n = uv__writev(uv__stream_fd(stream), iov, iovcnt);` |
| `ev_9d101c05322c` | call_site | `third_party/libuv/src/unix/fs.c:1127` | `if (errno == EINVAL \|\|` |
| `ev_9d1464d2c4ee` | call_site | `third_party/libuv/src/unix/stream.c:1451` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_9d1ca5ca4f5a` | call_site | `third_party/libuv/src/unix/stream.c:673` | `assert(req->bufs != NULL);` |
| `ev_9d2740ba66c2` | call_site | `third_party/libuv/src/thread-common.c:141` | `uv_mutex_unlock(&b->mutex);` |
| `ev_9d2b0c8a16be` | call_site | `third_party/libuv/src/unix/stream.c:246` | `assert(events != 0);` |
| `ev_9d34d39630ee` | call_site | `third_party/libuv/src/uv-common.c:955` | `uv__free(cpu_infos[i].model);` |
| `ev_9d455b09c0a1` | call_site | `third_party/libuv/src/unix/udp.c:246` | `assert(buf.base != NULL);` |
| `ev_9d579686632a` | call_site | `third_party/libuv/src/unix/tty.c:490` | `err = uv__tcsetattr(orig_termios_fd, TCSANOW, &orig_termios);` |
| `ev_9d59dc77cae7` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9d8621a083b6` | call_site | `third_party/libuv/src/unix/loop.c:182` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_9d90a87fafb6` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9d93d0edd9f7` | call_site | `third_party/libuv/src/uv-common.c:270` | `memset(addr, 0, sizeof(*addr));` |
| `ev_9dbad9b909bd` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:149` | `asn = pLSGetCurrentApplicationASN();` |
| `ev_9dc0d3a7be75` | call_site | `third_party/libuv/src/unix/stream.c:896` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_9dd6f384b6a7` | call_site | `third_party/libuv/src/unix/stream.c:862` | `n = uv__try_write(stream,` |
| `ev_9dd74e2753ce` | call_site | `third_party/libuv/src/unix/thread.c:366` | `abort();` |
| `ev_9df55a464661` | call_site | `third_party/libuv/src/unix/fs.c:1713` | `X(ACCESS, access(req->path, req->flags));` |
| `ev_9e113808cf94` | call_site | `third_party/libuv/src/unix/async.c:338` | `while (!uv__queue_empty(&queue)) {` |
| `ev_9e3ce92db5ce` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9e4791014158` | call_site | `third_party/libuv/src/unix/tcp.c:571` | `if (setsockopt(fd, IPPROTO_TCP, TCP_KEEPCNT, &cnt, sizeof(cnt)))` |
| `ev_9e4fb987df49` | call_site | `third_party/libuv/src/unix/stream.c:1104` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_9e5eb687289c` | call_site | `third_party/libuv/src/unix/udp.c:902` | `err = uv__sock_reuseaddr(sock);` |
| `ev_9e707c6ab619` | call_site | `third_party/libuv/src/unix/fsevents.c:639` | `if (pthread_attr_destroy(&attr))` |
| `ev_9e97eff9a9db` | call_site | `third_party/libuv/src/unix/fsevents.c:757` | `uv__free(s);` |
| `ev_9e9f8c359585` | call_site | `third_party/libuv/src/unix/thread.c:365` | `if (pthread_mutex_lock(mutex))` |
| `ev_9eb0271d884f` | call_site | `third_party/libuv/src/unix/core.c:249` | `fd = uv__stream_fd((uv_stream_t*) handle);` |
| `ev_9eb242044998` | call_site | `third_party/libuv/src/unix/stream.c:1452` | `assert(alloc_cb);` |
| `ev_9eb4a9371174` | call_site | `third_party/libuv/src/unix/thread.c:780` | `abort();` |
| `ev_9ebc26732fda` | call_site | `third_party/libuv/src/unix/core.c:894` | `abort();` |
| `ev_9ebd515ba2a1` | call_site | `third_party/libuv/src/unix/stream.c:539` | `assert(server->loop == client->loop);` |
| `ev_9ec7808c31ee` | call_site | `third_party/libuv/src/unix/async.c:297` | `err = kevent(loop->backend_fd, &ev, 1, NULL, 0, NULL);` |
| `ev_9edc75ea9c66` | assignment | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_9ee824a37da7` | call_site | `third_party/libuv/src/unix/stream.c:560` | `uv__close(server->accepted_fd);` |
| `ev_9f206abdf92e` | call_site | `third_party/libuv/src/unix/udp.c:953` | `err = uv_ip4_addr(multicast_addr, 0, &mcast_addr.in);` |
| `ev_9f4405b082a5` | call_site | `third_party/libuv/src/unix/fsevents.c:372` | `if (!pFSEventStreamStart(ref)) {` |
| `ev_9f67531bd193` | call_site | `third_party/libuv/src/uv-common.c:306` | `return uv_inet_ntop(AF_INET6, &src->sin6_addr, dst, size);` |
| `ev_9fe9881bf08e` | call_site | `third_party/libuv/src/unix/fsevents.c:653` | `uv_mutex_destroy(&state->fsevent_mutex);` |
| `ev_9fe9cfc5a18c` | call_site | `third_party/libuv/src/unix/fsevents.c:320` | `if (!uv__queue_empty(&head))` |
| `ev_a01e467af70e` | call_site | `third_party/libuv/src/unix/stream.c:608` | `err = uv__tcp_listen((uv_tcp_t*)stream, backlog, cb);` |
| `ev_a01fb5903d23` | call_site | `third_party/libuv/src/unix/stream.c:1172` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_a04b8c7c756d` | call_site | `third_party/libuv/src/unix/udp.c:817` | `memset(&mreq, 0, sizeof(mreq));` |
| `ev_a04e96e5d89b` | call_site | `third_party/libuv/src/unix/fs.c:638` | `errno = 0;` |
| `ev_a050d4e384bb` | call_site | `third_party/libuv/src/unix/signal.c:152` | `abort();` |
| `ev_a059adb8df13` | call_site | `third_party/libuv/src/unix/fs.c:933` | `errno = EIO;` |
| `ev_a05cb92ccdc8` | call_site | `third_party/libuv/src/unix/stream.c:445` | `uv__queue_remove(q);` |
| `ev_a086780577cf` | call_site | `third_party/libuv/src/unix/stream.c:518` | `fd = uv__stream_fd(stream);` |
| `ev_a08f4b3f95f8` | call_site | `third_party/libuv/src/unix/fsevents.c:835` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_a0bff9dd5a4c` | call_site | `third_party/libuv/src/unix/signal.c:321` | `uv__signal_stop((uv_signal_t*) handle);` |
| `ev_a0c5a6c9fb8e` | call_site | `third_party/libuv/src/unix/fs.c:2129` | `PATH;` |
| `ev_a0f0dbbd85ef` | call_site | `third_party/libuv/src/unix/stream.c:640` | `assert(req);` |
| `ev_a10022f33747` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:198` | `req->service = memcpy(buf + len, service, service_len);` |
| `ev_a1338d057197` | call_site | `third_party/libuv/src/uv-common.c:832` | `va_start(ap, option);` |
| `ev_a13cb798066d` | call_site | `third_party/libuv/src/unix/core.c:763` | `if (errno != ERANGE)` |
| `ev_a14ec4757563` | call_site | `third_party/libuv/src/unix/loop.c:90` | `err = uv_rwlock_init(&loop->cloexec_lock);` |
| `ev_a1520595a761` | call_site | `third_party/libuv/src/unix/stream.c:456` | `assert(!uv__io_active(&stream->io_watcher, POLLIN \| POLLOUT));` |
| `ev_a15a8a935323` | call_site | `third_party/libuv/src/unix/udp.c:269` | `handle->recv_cb(handle, 0, &buf, NULL, 0);` |
| `ev_a177e7089af3` | call_site | `third_party/libuv/src/unix/fs.c:1686` | `uv__free(bufs);` |
| `ev_a180b9c2c133` | call_site | `third_party/libuv/src/unix/udp.c:1341` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK \|\| errno == ENOBUFS)` |
| `ev_a192e8fc92aa` | call_site | `third_party/libuv/src/unix/tcp.c:198` | `if (errno == EAFNOSUPPORT)` |
| `ev_a19e7ff238c4` | call_site | `third_party/libuv/src/unix/tcp.c:171` | `err = uv__sock_reuseport(tcp->io_watcher.fd);` |
| `ev_a1aaa11c0827` | assignment | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_a1b58abb864f` | call_site | `third_party/libuv/src/threadpool.c:219` | `abort();` |
| `ev_a1ccc3eece0a` | call_site | `third_party/libuv/src/unix/thread.c:463` | `err = semaphore_create(mach_task_self(), sem, SYNC_POLICY_FIFO, value);` |
| `ev_a1fcf2e85ad5` | call_site | `third_party/libuv/src/unix/udp.c:1142` | `} else if (uv_ip4_addr(interface_addr, 0, addr4) == 0) {` |
| `ev_a204684749b1` | call_site | `third_party/libuv/src/unix/thread.c:783` | `abort();` |
| `ev_a243a907176c` | call_site | `third_party/libuv/src/unix/fsevents.c:303` | `event = uv__malloc(sizeof(*event) + len);` |
| `ev_a2460f2d58bb` | call_site | `third_party/libuv/src/unix/stream.c:1276` | `uv__req_unregister(stream->loop);` |
| `ev_a2700f9f3dfc` | call_site | `third_party/libuv/src/unix/thread.c:428` | `if (pthread_rwlock_wrlock(rwlock))` |
| `ev_a29b3837ffe5` | call_site | `third_party/libuv/src/unix/process.c:510` | `err = posix_spawnattr_setsigdefault(attrs, &signal_set);` |
| `ev_a2a5e9b49f90` | call_site | `third_party/libuv/src/unix/stream.c:516` | `assert(!(stream->flags & UV_HANDLE_CLOSING));` |
| `ev_a2a7b2ac5fa3` | call_site | `third_party/libuv/src/unix/fsevents.c:850` | `uv_mutex_destroy(&handle->cf_mutex);` |
| `ev_a2b2b8f87cf5` | call_site | `third_party/libuv/src/unix/stream.c:846` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_a2be3695e1c9` | call_site | `third_party/libuv/src/unix/process.c:860` | `uv_once(&posix_spawn_init_once, uv__spawn_init_posix_spawn);` |
| `ev_a2cd9b965dcc` | call_site | `third_party/libuv/src/unix/pipe.c:542` | `return uv_pipe(fds,` |
| `ev_a2d651d9c142` | call_site | `third_party/libuv/src/unix/core.c:764` | `return UV__ERR(errno);` |
| `ev_a2d702ef443b` | call_site | `third_party/libuv/src/unix/process.c:819` | `sigdelset(&signewset, SIGTRAP);` |
| `ev_a2e499120e77` | call_site | `third_party/libuv/src/unix/udp.c:971` | `return uv__udp_set_source_membership4(handle,` |
| `ev_a2e6417d69b2` | call_site | `third_party/libuv/src/unix/fsevents.c:829` | `err = uv_mutex_init(&handle->cf_mutex);` |
| `ev_a2ebd7c9e867` | call_site | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_a306a6c96a6c` | call_site | `third_party/libuv/src/unix/fs.c:1227` | `r = write(fd, bufs->iov_base, bufs->iov_len);` |
| `ev_a30f04123ef0` | call_site | `third_party/libuv/src/unix/thread.c:109` | `if (getrlimit(RLIMIT_STACK, &lim))` |
| `ev_a310bd633352` | call_site | `third_party/libuv/src/uv-common.c:717` | `nbufs = uv__get_nbufs(req);` |
| `ev_a31af428fee4` | call_site | `third_party/libuv/src/unix/process.c:387` | `uv__write_errno(error_fd);` |
| `ev_a33664095464` | call_site | `third_party/libuv/src/heap-inl.h:235` | `while (child->parent != NULL && less_than(child, child->parent))` |
| `ev_a33d34d0e286` | call_site | `third_party/libuv/src/unix/fs.c:536` | `r = read(fd, bufs->iov_base, bufs->iov_len);` |
| `ev_a37904aadb68` | call_site | `third_party/libuv/src/unix/process.c:796` | `(void) posix_spawn_file_actions_destroy(&actions);` |
| `ev_a38146646386` | call_site | `third_party/libuv/src/unix/fs.c:2129` | `PATH;` |
| `ev_a3a05f0bb777` | call_site | `third_party/libuv/src/unix/core.c:355` | `assert(0);` |
| `ev_a3aa80ba6f7d` | call_site | `third_party/libuv/src/unix/core.c:909` | `uv__queue_init(&w->watcher_queue);` |
| `ev_a3bf26147e56` | call_site | `third_party/libuv/src/unix/core.c:770` | `return UV__ERR(errno);` |
| `ev_a3c6b77761ea` | call_site | `third_party/libuv/src/unix/pipe.c:236` | `err = uv_pipe_connect2(req, handle, name, strlen(name), 0, cb);` |
| `ev_a3ca3938a278` | call_site | `third_party/libuv/src/unix/pipe.c:470` | `return UV__ERR(errno);` |
| `ev_a3dcf6ec0abb` | call_site | `third_party/libuv/src/unix/core.c:460` | `uv__io_poll(loop, timeout);` |
| `ev_a3e6d807e9ab` | call_site | `third_party/libuv/src/unix/pipe.c:484` | `r = chmod(name_buffer, pipe_stat.st_mode);` |
| `ev_a4047c2b38aa` | call_site | `third_party/libuv/src/unix/core.c:908` | `uv__queue_init(&w->pending_queue);` |
| `ev_a411363ff68d` | call_site | `third_party/libuv/src/unix/stream.c:992` | `fprintf(stderr, "ignoring non-SCM_RIGHTS ancillary data: %d\n",` |
| `ev_a42333feee1c` | assignment | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_a4247c22e811` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:172` | `dlclose(application_services_handle);` |
| `ev_a42f36eb8f23` | call_site | `third_party/libuv/src/unix/process.c:940` | `while (err == -1 && errno == EINTR);` |
| `ev_a4488dfde8d9` | assignment | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_a464e6686716` | call_site | `third_party/libuv/src/unix/fsevents.c:888` | `uv_sem_wait(&state->fsevent_sem);` |
| `ev_a4694cca16a5` | call_site | `third_party/libuv/src/unix/darwin.c:152` | `err = task_info(mach_task_self(),` |
| `ev_a47f8c0ddb26` | call_site | `third_party/libuv/src/unix/fsevents.c:549` | `V(core_foundation_handle, CFRunLoopSourceSignal);` |
| `ev_a48630075c98` | call_site | `third_party/libuv/src/threadpool.c:218` | `if (uv_cond_init(&cond))` |
| `ev_a49ff7469940` | call_site | `third_party/libuv/src/unix/stream.c:1520` | `uv__stream_osx_interrupt_select(handle);` |
| `ev_a4b02f6a2f18` | call_site | `third_party/libuv/src/unix/udp.c:1156` | `return UV__ERR(errno);` |
| `ev_a4c976d0d41b` | call_site | `third_party/libuv/src/threadpool.c:248` | `memcpy(&once, &child_once, sizeof(child_once));` |
| `ev_a4e9ca5f3658` | call_site | `third_party/libuv/src/unix/fs.c:612` | `dir->dir = opendir(req->path);` |
| `ev_a51acb7598ff` | call_site | `third_party/libuv/src/unix/darwin.c:196` | `sysctlbyname("hw.model", &model, &size, NULL, 0)) {` |
| `ev_a536858e7057` | call_site | `third_party/libuv/src/unix/tcp.c:147` | `return uv_tcp_init_ex(loop, tcp, AF_UNSPEC);` |
| `ev_a55ab0a346df` | call_site | `third_party/libuv/src/unix/core.c:890` | `watchers = uv__reallocf(loop->watchers,` |
| `ev_a56d48f79faf` | call_site | `third_party/libuv/src/threadpool.c:301` | `uv__queue_insert_tail(&loop->wq, &w->wq);` |
| `ev_a588d2bfac42` | call_site | `third_party/libuv/src/threadpool.c:63` | `uv_sem_post((uv_sem_t*) arg);` |
| `ev_a59894688097` | call_site | `third_party/libuv/src/uv-common.c:940` | `uv__free(envitems[i].name);` |
| `ev_a59e80e88a08` | call_site | `third_party/libuv/src/unix/pipe.c:120` | `err = uv__socket(AF_UNIX, SOCK_STREAM, 0);` |
| `ev_a5b47c8f30ff` | call_site | `third_party/libuv/src/unix/udp.c:240` | `buf = uv_buf_init(NULL, 0);` |
| `ev_a5b9a2bcb11b` | call_site | `third_party/libuv/src/unix/udp.c:1384` | `if (uv__queue_empty(&handle->write_queue))` |
| `ev_a5c8ee3f641f` | call_site | `third_party/libuv/src/unix/fsevents.c:308` | `memcpy(event->path, path, len + 1);` |
| `ev_a5d9b8cbddf6` | call_site | `third_party/libuv/src/unix/tcp.c:189` | `return UV__ERR(errno);` |
| `ev_a5dbecdabc93` | call_site | `third_party/libuv/src/unix/stream.c:346` | `err = uv_async_init(stream->loop, &s->async, uv__stream_osx_select_cb);` |
| `ev_a613248534b2` | assignment | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_a62cc61b73fc` | call_site | `third_party/libuv/src/uv-common.c:1022` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_a64251c40505` | call_site | `third_party/libuv/src/unix/getnameinfo.c:45` | `err = getnameinfo((struct sockaddr*) &req->storage,` |
| `ev_a65ffbef2eba` | call_site | `third_party/libuv/src/unix/stream.c:960` | `queued_fds = uv__realloc(queued_fds,` |
| `ev_a695acef6e46` | call_site | `third_party/libuv/src/unix/fsevents.c:555` | `V(core_services_handle, FSEventStreamInvalidate);` |
| `ev_a6b129d96fd3` | call_site | `third_party/libuv/src/timer.c:118` | `uv_timer_stop(handle);` |
| `ev_a6bc978a3d6f` | call_site | `third_party/libuv/src/unix/process.c:233` | `err = uv__close(pipefds[1]);` |
| `ev_a6de376bdefb` | call_site | `third_party/libuv/src/unix/darwin.c:208` | `if (host_processor_info(mach_host_self(), PROCESSOR_CPU_LOAD_INFO, &numcpus,` |
| `ev_a715e2345985` | call_site | `third_party/libuv/src/unix/core.c:947` | `assert(0 != events);` |
| `ev_a730bce52fc1` | call_site | `third_party/libuv/src/unix/signal.c:339` | `err = uv__signal_loop_once_init(loop);` |
| `ev_a73a6b33b2e3` | call_site | `third_party/libuv/src/unix/process.c:947` | `uv__close_nocheckstdio(signal_pipe[0]);` |
| `ev_a74259a51d2e` | call_site | `third_party/libuv/src/unix/core.c:1198` | `memcpy(buffer, pwd.homedir, len + 1);` |
| `ev_a7483ce3c64d` | call_site | `third_party/libuv/src/random.c:85` | `uv__req_unregister(req->loop);` |
| `ev_a74f997bc693` | call_site | `third_party/libuv/src/uv-common.c:1009` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_a7813c766650` | call_site | `third_party/libuv/src/inet.c:141` | `uv__strscpy(dst, tmp, size);` |
| `ev_a7992ce27ded` | call_site | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_a7c0a39f1deb` | call_site | `third_party/libuv/src/unix/udp.c:1417` | `return uv__udp_sendmsgv(fd, count, bufs, nbufs, addrs);` |
| `ev_a7d1ad2faa13` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:193` | `req->hints = memcpy(buf + len, hints, sizeof(*hints));` |
| `ev_a7e15974aa1b` | call_site | `third_party/libuv/src/unix/udp.c:1066` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_a7edebc70b1c` | call_site | `third_party/libuv/src/unix/core.c:1299` | `shell_size = strlen(pw.pw_shell) + 1;` |
| `ev_a7ee3349205e` | call_site | `third_party/libuv/src/unix/core.c:1190` | `len = strlen(pwd.homedir);` |
| `ev_a84da80e0238` | call_site | `third_party/libuv/src/unix/core.c:1419` | `return uv__getpwuid_r(pwd, uid);` |
| `ev_a864febf0ee8` | call_site | `third_party/libuv/src/unix/thread.c:492` | `r = semaphore_wait(*sem);` |
| `ev_a86d202f42f0` | call_site | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_a86f60818c75` | call_site | `third_party/libuv/src/unix/core.c:406` | `uv__queue_empty(&loop->idle_handles) &&` |
| `ev_a89baec5eecf` | call_site | `third_party/libuv/src/unix/tcp.c:670` | `uv__close(temp[0]);` |
| `ev_a8a16ad1cbe6` | call_site | `third_party/libuv/src/unix/udp.c:598` | `req->bufs = uv__malloc(nbufs * sizeof(bufs[0]));` |
| `ev_a8a62afac3b6` | call_site | `third_party/libuv/src/unix/stream.c:809` | `n = sendmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_a8a7e4b4a4c1` | call_site | `third_party/libuv/src/unix/fs.c:827` | `uv__free(buf);` |
| `ev_a8b9edb851da` | call_site | `third_party/libuv/src/unix/core.c:961` | `uv__queue_remove(&w->watcher_queue);` |
| `ev_a8bcad5e62f2` | call_site | `third_party/libuv/src/unix/udp.c:689` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_a8c59432791e` | call_site | `third_party/libuv/src/unix/fsevents.c:836` | `uv__queue_insert_tail(&state->fsevent_handles, &handle->cf_member);` |
| `ev_a8e2a4c6db00` | call_site | `third_party/libuv/src/unix/fs.c:417` | `r = pread(fd, p, n, off);` |
| `ev_a8fc8ccf1dec` | call_site | `third_party/libuv/src/unix/tcp.c:583` | `if (uv__stream_fd(handle) != -1) {` |
| `ev_a90326fd425d` | call_site | `third_party/libuv/src/unix/loop.c:170` | `uv__async_stop(loop);` |
| `ev_a90c2e617c26` | call_site | `third_party/libuv/src/uv-common.c:213` | `UV_ERRNO_MAP(UV_ERR_NAME_GEN_R)` |
| `ev_a91e590cf299` | call_site | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_a93694a5ef5d` | assignment | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_a938ee483119` | call_site | `third_party/libuv/src/unix/thread.c:471` | `abort();` |
| `ev_a94c6c91517a` | call_site | `third_party/libuv/src/unix/async.c:194` | `q = uv__queue_head(&queue);` |
| `ev_a957e6c7b4ac` | call_site | `third_party/libuv/src/threadpool.c:120` | `uv_mutex_unlock(&mutex);` |
| `ev_a96331e551e5` | call_site | `third_party/libuv/src/unix/fs.c:1945` | `PATH;` |
| `ev_a9825cfe39b1` | call_site | `third_party/libuv/src/unix/core.c:850` | `q = uv__queue_head(&pq);` |
| `ev_a9a852da563c` | call_site | `third_party/libuv/src/unix/fsevents.c:369` | `assert(ref != NULL);` |
| `ev_a9ae4d40bcff` | call_site | `third_party/libuv/src/unix/core.c:1899` | `token = uv__strtok(cloned_path, ":", &itr);` |
| `ev_a9bcf8435fed` | call_site | `third_party/libuv/src/unix/process.c:174` | `process->exit_cb(process, exit_status, term_signal);` |
| `ev_a9c8d12a9016` | call_site | `third_party/libuv/src/unix/core.c:1547` | `return UV__ERR(errno);` |
| `ev_aa260097a8d3` | assignment | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_aa749ba6ab8f` | call_site | `third_party/libuv/src/inet.c:157` | `p = strchr(src, '%');` |
| `ev_aa8c6bf6aa6b` | call_site | `third_party/libuv/src/unix/stream.c:846` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_aa9496e87469` | call_site | `third_party/libuv/src/unix/udp.c:840` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_aab818684f01` | call_site | `third_party/libuv/src/unix/signal.c:401` | `uv__signal_block_and_lock(&saved_sigmask);` |
| `ev_aacb2a06a7d9` | call_site | `third_party/libuv/src/unix/async.c:339` | `q = uv__queue_head(&queue);` |
| `ev_aad00c6d2c5b` | call_site | `third_party/libuv/src/unix/poll.c:64` | `handle->poll_cb(handle, 0, pevents);` |
| `ev_aafe66ac5cab` | call_site | `third_party/libuv/src/unix/fsevents.c:337` | `memset(&ctx, 0, sizeof(ctx));` |
| `ev_ab0980935fe6` | call_site | `third_party/libuv/src/unix/fs.c:681` | `uv__free(req->ptr);` |
| `ev_ab1965d3bb82` | call_site | `third_party/libuv/src/unix/async.c:369` | `while (!uv__queue_empty(&queue)) {` |
| `ev_ab19e5c82169` | call_site | `third_party/libuv/src/unix/core.c:179` | `uv__udp_close((uv_udp_t*)handle);` |
| `ev_ab2ba65eeb23` | call_site | `third_party/libuv/src/unix/stream.c:1172` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_ab3c40d25d92` | call_site | `third_party/libuv/src/unix/stream.c:547` | `err = uv__stream_open(client,` |
| `ev_ab54bbdfe8b6` | call_site | `third_party/libuv/src/idna.c:141` | `assert(*p < pe);` |
| `ev_ab60cd87c8b1` | call_site | `third_party/libuv/src/unix/fs.c:275` | `return mkdtemp((char*) req->path) ? 0 : -1;` |
| `ev_ab60d56a63b9` | call_site | `third_party/libuv/src/unix/stream.c:584` | `uv__free(queued_fds);` |
| `ev_aba4efdcae44` | call_site | `third_party/libuv/src/unix/tty.c:228` | `while (r == -1 && errno == EINTR);` |
| `ev_abbfbae38c08` | call_site | `third_party/libuv/src/unix/fs.c:1745` | `X(SYMLINK, symlink(req->path, req->new_path));` |
| `ev_abc59c72416b` | call_site | `third_party/libuv/src/unix/signal.c:192` | `errno = saved_errno;` |
| `ev_abf5b76d041d` | call_site | `third_party/libuv/src/unix/process.c:370` | `uv__write_errno(error_fd);` |
| `ev_abff54541877` | call_site | `third_party/libuv/src/unix/tty.c:224` | `uv__close(newfd);` |
| `ev_ac1d41815025` | call_site | `third_party/libuv/src/unix/stream.c:515` | `assert(stream->accepted_fd == -1);` |
| `ev_ac6554a105ef` | call_site | `third_party/libuv/src/unix/fsevents.c:373` | `pFSEventStreamInvalidate(ref);` |
| `ev_ac6621139824` | call_site | `third_party/libuv/src/unix/core.c:1058` | `thread = mach_thread_self();` |
| `ev_ac8013f80ebb` | call_site | `third_party/libuv/src/unix/loop.c:48` | `memset(&lfields->loop_metrics.metrics,` |
| `ev_acb15c736951` | call_site | `third_party/libuv/src/unix/stream.c:1320` | `if (uv__handle_fd((uv_handle_t*) send_handle) < 0)` |
| `ev_acb247b17f6a` | call_site | `third_party/libuv/src/unix/loop.c:58` | `uv__queue_init(&loop->handle_queue);` |
| `ev_acc9cf94ce9a` | call_site | `third_party/libuv/src/idna.c:485` | `target = uv__malloc(target_len + 1);` |
| `ev_acce12c7d3c3` | call_site | `third_party/libuv/src/timer.c:192` | `uv_timer_again(handle);` |
| `ev_acd28a6f53ea` | call_site | `third_party/libuv/src/unix/udp.c:1268` | `if ((r = uv__udp_prep_pkt(&h, bufs, nbufs, addr)))` |
| `ev_acdc925eeeca` | call_site | `third_party/libuv/src/unix/core.c:747` | `uv__cloexec(*pfd, 1);` |
| `ev_acfde5ccbf3c` | call_site | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_acfeed207e6c` | call_site | `third_party/libuv/src/unix/loop.c:183` | `assert(uv__queue_empty(&loop->wq) && "thread pool work queue not empty!");` |
| `ev_ad0abb363a9e` | call_site | `third_party/libuv/src/unix/signal.c:189` | `memset(&msg, 0, sizeof msg);` |
| `ev_ad0e11307aea` | call_site | `third_party/libuv/src/uv-common.c:865` | `uv__free(loop);` |
| `ev_ad14661bf222` | call_site | `third_party/libuv/src/timer.c:174` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_ad17aaaf780a` | call_site | `third_party/libuv/src/unix/udp.c:413` | `err = UV__ERR(errno);` |
| `ev_ad23f3a12d24` | call_site | `third_party/libuv/src/unix/kqueue.c:523` | `path = uv__basename_r(pathbuf);` |
| `ev_ad2c861dfb3b` | call_site | `third_party/libuv/src/unix/udp.c:1277` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK \|\| errno == ENOBUFS)` |
| `ev_ad31a1e71bc1` | call_site | `third_party/libuv/src/unix/poll.c:131` | `if (uv__fd_exists(handle->loop, w->fd))` |
| `ev_ad42ffea959f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_ad447387dd65` | call_site | `third_party/libuv/src/unix/fs.c:1720` | `X(LCHOWN, lchown(req->path, req->uid, req->gid));` |
| `ev_ad4991b0e5dd` | call_site | `third_party/libuv/src/fs-poll.c:123` | `assert(ctx != NULL);` |
| `ev_ad875c0e8c2b` | call_site | `third_party/libuv/src/uv-common.c:680` | `memcpy(buffer, handle->path, required_len);` |
| `ev_ad9bd4bed3b4` | call_site | `third_party/libuv/src/unix/loop.c:155` | `if (w->pevents != 0 && uv__queue_empty(&w->watcher_queue)) {` |
| `ev_ade1d519f0a3` | call_site | `third_party/libuv/src/unix/stream.c:718` | `uv__queue_remove(&req->queue);` |
| `ev_ae10532d40e8` | call_site | `third_party/libuv/src/unix/fsevents.c:449` | `assert(curr->realpath != NULL);` |
| `ev_ae19b02f127a` | call_site | `third_party/libuv/src/unix/udp.c:255` | `memset(&h, 0, sizeof(h));` |
| `ev_ae21638ab04c` | call_site | `third_party/libuv/src/unix/proctitle.c:148` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_ae22a2e185ab` | call_site | `third_party/libuv/src/fs-poll.c:215` | `ctx->poll_cb(ctx->parent_handle, 0, &ctx->statbuf, statbuf);` |
| `ev_ae2ce7d79969` | assignment | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_ae2d490b6146` | call_site | `third_party/libuv/src/idna.c:397` | `assert(code_point < 0x10FFFF);` |
| `ev_ae35213eb1a0` | call_site | `third_party/libuv/src/heap-inl.h:147` | `heap_node_swap(heap, newnode->parent, newnode);` |
| `ev_ae6dd53571a0` | call_site | `third_party/libuv/src/unix/fs.c:2119` | `PATH;` |
| `ev_ae70e6957faf` | call_site | `third_party/libuv/src/unix/proctitle.c:135` | `uv_once(&process_title_mutex_once, init_process_title_mutex_once);` |
| `ev_ae7921cd1652` | call_site | `third_party/libuv/src/unix/thread.c:422` | `if (pthread_rwlock_unlock(rwlock))` |
| `ev_ae9b50a0f8ab` | call_site | `third_party/libuv/src/unix/thread.c:176` | `if (pthread_attr_setstacksize(attr, stack_size))` |
| `ev_aea39618776b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:110` | `S("_LSSetApplicationInformationItem"));` |
| `ev_aec41cea8269` | call_site | `third_party/libuv/src/fs-poll.c:257` | `uv__free(ctx);` |
| `ev_aecee77afd31` | call_site | `third_party/libuv/src/unix/signal.c:422` | `RB_INSERT(uv__signal_tree_s, &uv__signal_tree, handle);` |
| `ev_aedfadbbe11b` | call_site | `third_party/libuv/src/unix/fsevents.c:545` | `V(core_foundation_handle, CFRunLoopGetCurrent);` |
| `ev_aee85be2bd11` | call_site | `third_party/libuv/src/unix/stream.c:1089` | `uv__io_start(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_aeefeb47cd7c` | call_site | `third_party/libuv/src/unix/udp.c:958` | `err = uv_ip6_addr(source_addr, 0, &src_addr.in6);` |
| `ev_af087f8af8cb` | call_site | `third_party/libuv/src/timer.c:174` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_af110f0f7675` | call_site | `third_party/libuv/src/unix/stream.c:387` | `uv__close(fds[1]);` |
| `ev_af2a7488026e` | call_site | `third_party/libuv/src/unix/async.c:186` | `if (errno == EINTR)` |
| `ev_af32d9ed1243` | call_site | `third_party/libuv/src/unix/fsevents.c:307` | `memset(event, 0, sizeof(*event));` |
| `ev_af3640fdb8e5` | call_site | `third_party/libuv/src/unix/async.c:398` | `return uv__async_start(loop);` |
| `ev_af36b5af30d8` | call_site | `third_party/libuv/src/unix/proctitle.c:116` | `memcpy(pt->str, title, len);` |
| `ev_af6eb270438f` | call_site | `third_party/libuv/src/unix/stream.c:814` | `while (n == -1 && errno == EINTR);` |
| `ev_af82ff27a973` | call_site | `third_party/libuv/src/unix/fsevents.c:574` | `pthread_mutex_unlock(&global_init_mutex);` |
| `ev_af912c87bd1e` | call_site | `third_party/libuv/src/unix/tty.c:217` | `uv__nonblock(fd, 1);` |
| `ev_afab2756c8a0` | call_site | `third_party/libuv/src/unix/async.c:299` | `return UV__ERR(errno);` |
| `ev_afab56ac7dd9` | call_site | `third_party/libuv/src/unix/core.c:987` | `if (uv__queue_empty(&w->pending_queue))` |
| `ev_afbaf1a18ca9` | call_site | `third_party/libuv/src/unix/pipe.c:168` | `return UV__ERR(errno);` |
| `ev_afc686a3a119` | call_site | `third_party/libuv/src/fs-poll.c:129` | `if (uv_is_active((uv_handle_t*)&ctx->timer_handle))` |
| `ev_aff5422d48b8` | call_site | `third_party/libuv/src/unix/core.c:355` | `assert(0);` |
| `ev_b0066fd8bf8f` | call_site | `third_party/libuv/src/unix/core.c:1557` | `memcpy(buffer, buf, len + 1);` |
| `ev_b00a452f52a2` | call_site | `third_party/libuv/src/unix/pipe.c:210` | `err = uv__nonblock(fd, 1);` |
| `ev_b042a5f86ea6` | call_site | `third_party/libuv/src/unix/udp.c:172` | `memset(&msgs[k].msg_hdr, 0, sizeof(msgs[k].msg_hdr));` |
| `ev_b0536e333f74` | call_site | `third_party/libuv/src/unix/process.c:1052` | `uv__process_close_stream(options->stdio + i);` |
| `ev_b0602380f78d` | call_site | `third_party/libuv/src/unix/async.c:244` | `r = write(fd, buf, len);` |
| `ev_b06b26a8fdc7` | call_site | `third_party/libuv/src/unix/core.c:583` | `uv__close(peerfd);` |
| `ev_b07eb122b0b1` | call_site | `third_party/libuv/src/timer.c:188` | `uv__queue_remove(queue_node);` |
| `ev_b09188bc8c9b` | call_site | `third_party/libuv/src/unix/pipe.c:306` | `while (r == -1 && errno == EINTR);` |
| `ev_b09595ea95f9` | call_site | `third_party/libuv/src/uv-common.c:822` | `uv__free((char*) dirents[i].name);` |
| `ev_b0ac79da8f2f` | call_site | `third_party/libuv/src/unix/udp.c:778` | `mreq.imr_interface.s_addr = htonl(INADDR_ANY);` |
| `ev_b0aec13491f7` | call_site | `third_party/libuv/src/unix/async.c:189` | `abort();` |
| `ev_b0e08bae336a` | call_site | `third_party/libuv/src/unix/fsevents.c:477` | `uv__free(paths);` |
| `ev_b0e8907d4d85` | call_site | `third_party/libuv/src/unix/fsevents.c:593` | `state = uv__calloc(1, sizeof(*state));` |
| `ev_b0edcd8c8c37` | call_site | `third_party/libuv/src/unix/fs.c:1729` | `X(MKDIR, mkdir(req->path, req->mode));` |
| `ev_b1101e47316d` | call_site | `third_party/libuv/src/fs-poll.c:202` | `ctx->poll_cb(ctx->parent_handle,` |
| `ev_b1160bb5ffb5` | call_site | `third_party/libuv/src/unix/signal.c:231` | `abort();` |
| `ev_b12e866a5c2a` | call_site | `third_party/libuv/src/unix/process.c:939` | `err = waitpid(*pid, &status, 0); /* okay, got EPIPE */` |
| `ev_b13f8c34eaa7` | call_site | `third_party/libuv/src/unix/fsevents.c:687` | `while (!uv__queue_empty(&loop->cf_signals)) {` |
| `ev_b140cddf0888` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:87` | `case EAI_SYSTEM: return UV__ERR(errno);` |
| `ev_b1592e06f03b` | call_site | `third_party/libuv/src/unix/kqueue.c:314` | `assert((reset_timeout == 0 ? timeout : user_timeout) == 0);` |
| `ev_b19bc573086e` | call_site | `third_party/libuv/src/unix/stream.c:1060` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_b1cdea941118` | call_site | `third_party/libuv/src/inet.c:133` | `tp += snprintf(tp, sizeof tmp - (tp - tmp), "%x", words[i]);` |
| `ev_b1d03e18b3f3` | call_site | `third_party/libuv/src/unix/core.c:936` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_b1d9f14206de` | call_site | `third_party/libuv/src/unix/loop.c:54` | `uv__queue_init(&loop->idle_handles);` |
| `ev_b1e74516d7f4` | call_site | `third_party/libuv/src/unix/pipe.c:190` | `uv__stream_close((uv_stream_t*)handle);` |
| `ev_b2141c8939c6` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:141` | `memcpy(address->phys_addr, LLADDR(sa_addr), sizeof(address->phys_addr));` |
| `ev_b2178f59079d` | call_site | `third_party/libuv/src/unix/signal.c:249` | `memset(&sa, 0, sizeof(sa));` |
| `ev_b295d1c02f2c` | call_site | `third_party/libuv/src/unix/kqueue.c:599` | `if (uv__fstat(fd, &statbuf))` |
| `ev_b296a8d4db33` | call_site | `third_party/libuv/src/unix/loop.c:126` | `uv__free(loop->watchers);` |
| `ev_b2a8a7ea72f0` | call_site | `third_party/libuv/src/uv-common.c:499` | `return uv__udp_send(req, handle, bufs, nbufs, addr, addrlen, send_cb);` |
| `ev_b2ca666143d8` | call_site | `third_party/libuv/src/unix/core.c:521` | `return UV__ERR(errno);` |
| `ev_b2d33c4977d5` | call_site | `third_party/libuv/src/unix/process.c:797` | `(void) posix_spawnattr_destroy(&attrs);` |
| `ev_b2fe7f9b9e33` | call_site | `third_party/libuv/src/unix/kqueue.c:580` | `handle->path = uv__strdup(path);` |
| `ev_b315a82773a2` | call_site | `third_party/libuv/src/uv-common.c:277` | `zone_index = strchr(ip, '%');` |
| `ev_b3318f75c51b` | call_site | `third_party/libuv/src/unix/fs.c:608` | `dir = uv__malloc(sizeof(*dir));` |
| `ev_b3378d680173` | call_site | `third_party/libuv/src/unix/getnameinfo.c:65` | `assert(req->retcode == 0);` |
| `ev_b344b472e541` | call_site | `third_party/libuv/src/unix/dl.c:70` | `errmsg = dlerror();` |
| `ev_b3480e1648db` | call_site | `third_party/libuv/src/unix/thread.c:291` | `return pthread_self();` |
| `ev_b34aecd9cd51` | call_site | `third_party/libuv/src/unix/loop.c:137` | `err = uv__io_fork(loop);` |
| `ev_b3590e089dda` | call_site | `third_party/libuv/src/threadpool.c:221` | `if (uv_mutex_init(&mutex))` |
| `ev_b366963f0cf1` | call_site | `third_party/libuv/src/unix/tty.c:225` | `uv__queue_remove(&tty->handle_queue);` |
| `ev_b36bff74b528` | call_site | `third_party/libuv/src/unix/stream.c:1252` | `assert(req);` |
| `ev_b39f960c4599` | call_site | `third_party/libuv/src/unix/fs.c:561` | `uv__free(req->bufs);` |
| `ev_b3a23a19635e` | call_site | `third_party/libuv/src/unix/core.c:632` | `saved_errno = errno;` |
| `ev_b3bdde9f1264` | call_site | `third_party/libuv/src/unix/fsevents.c:842` | `assert(handle != NULL);` |
| `ev_b3da1033776b` | call_site | `third_party/libuv/src/uv-common.c:1024` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_b3edcccafe46` | call_site | `third_party/libuv/src/unix/tcp.c:584` | `err = uv__tcp_nodelay(uv__stream_fd(handle), on);` |
| `ev_b3f3477d1901` | call_site | `third_party/libuv/src/unix/udp.c:99` | `assert(!(handle->flags & UV_HANDLE_UDP_PROCESSING));` |
| `ev_b4105064da1e` | call_site | `third_party/libuv/src/unix/fs.c:1735` | `X(OPENDIR, uv__fs_opendir(req));` |
| `ev_b41bc47ab162` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:123` | `*(void **)(&pCFBundleGetMainBundle) = dlsym(core_foundation_handle,` |
| `ev_b4346f6cad0c` | call_site | `third_party/libuv/src/unix/stream.c:247` | `assert(events == (events & (POLLIN \| POLLOUT)));` |
| `ev_b44af00b137a` | call_site | `third_party/libuv/src/threadpool.c:235` | `if (uv_thread_create_ex(threads + i, &config, worker, &sem))` |
| `ev_b45b5df7f9eb` | call_site | `third_party/libuv/src/unix/fs.c:1614` | `uv__to_stat(&pbuf, buf);` |
| `ev_b4893b4cee3b` | call_site | `third_party/libuv/src/unix/darwin.c:62` | `return mach_continuous_time() * timebase.numer / timebase.denom;` |
| `ev_b48f965e8c3f` | call_site | `third_party/libuv/src/unix/stream.c:388` | `uv_close((uv_handle_t*) &s->async, uv__stream_osx_cb_close);` |
| `ev_b4a84dd2f171` | call_site | `third_party/libuv/src/unix/udp.c:572` | `assert(nbufs > 0);` |
| `ev_b4b4db014405` | call_site | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_b4b9b07cacda` | call_site | `third_party/libuv/src/unix/fs.c:1295` | `if (uv__fstat(dstfd, &dst_statsbuf)) {` |
| `ev_b4beeab58f50` | call_site | `third_party/libuv/src/unix/loop.c:183` | `assert(uv__queue_empty(&loop->wq) && "thread pool work queue not empty!");` |
| `ev_b4ead329de93` | call_site | `third_party/libuv/src/unix/fsevents.c:796` | `err = uv__fsevents_loop_init(handle->loop);` |
| `ev_b5096daadc0b` | call_site | `third_party/libuv/src/timer.c:149` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_b52013c442d5` | call_site | `third_party/libuv/src/unix/process.c:820` | `sigdelset(&signewset, SIGSEGV);` |
| `ev_b521e4c95996` | call_site | `third_party/libuv/src/unix/fs.c:1267` | `if (uv__fstat(srcfd, &src_statsbuf)) {` |
| `ev_b53d5aed87d7` | call_site | `third_party/libuv/src/unix/udp.c:1164` | `return UV__ERR(errno);` |
| `ev_b569cc0ee623` | call_site | `third_party/libuv/src/unix/stream.c:1451` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_b58f456a8b89` | call_site | `third_party/libuv/src/unix/stream.c:421` | `return UV__ERR(errno);` |
| `ev_b59f0191959a` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_b5e2d9477d90` | call_site | `third_party/libuv/src/unix/tcp.c:72` | `err = uv__stream_open((uv_stream_t*) handle, sockfd, flags);` |
| `ev_b5edf9be7d5d` | call_site | `third_party/libuv/src/unix/core.c:1735` | `return UV__ERR(errno);` |
| `ev_b608025b3064` | call_site | `third_party/libuv/src/unix/async.c:355` | `uv__close(loop->async_io_watcher.fd);` |
| `ev_b60a1c9b57c3` | call_site | `third_party/libuv/src/unix/udp.c:1396` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_b6112e3e2db0` | call_site | `third_party/libuv/src/unix/udp.c:1140` | `addr4->sin_addr.s_addr = htonl(INADDR_ANY);` |
| `ev_b66a27295773` | call_site | `third_party/libuv/src/unix/core.c:496` | `uv__update_time(loop);` |
| `ev_b66d9a2db378` | call_site | `third_party/libuv/src/unix/tcp.c:102` | `err = maybe_bind_socket(sockfd);` |
| `ev_b672e6163356` | call_site | `third_party/libuv/src/unix/thread.c:799` | `if (pthread_cond_destroy(cond))` |
| `ev_b68dee444baa` | call_site | `third_party/libuv/src/unix/udp.c:861` | `fd = uv__socket(domain, SOCK_DGRAM, 0);` |
| `ev_b6c1675e9560` | call_site | `third_party/libuv/src/unix/signal.c:148` | `if (pthread_sigmask(SIG_SETMASK, &new_mask, saved_sigmask))` |
| `ev_b6d80ba09e1a` | call_site | `third_party/libuv/src/unix/core.c:1360` | `uv__free(buf);` |
| `ev_b6e6b50f6c06` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:169` | `dlclose(core_foundation_handle);` |
| `ev_b6f7401f8869` | call_site | `third_party/libuv/src/threadpool.c:285` | `uv_once(&once, init_once);  /* Ensure \|mutex\| is initialized. */` |
| `ev_b6fa66ec36e0` | call_site | `third_party/libuv/src/unix/core.c:1527` | `return UV__ERR(errno);` |
| `ev_b707cec3fa49` | call_site | `third_party/libuv/src/unix/thread.c:423` | `abort();` |
| `ev_b71707dadfdc` | call_site | `third_party/libuv/src/unix/udp.c:552` | `return UV__ERR(errno);` |
| `ev_b732e1e6b2e9` | assignment | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_b73aeaba1a40` | call_site | `third_party/libuv/src/unix/stream.c:138` | `assert(r == 1);` |
| `ev_b745eb2c1aa3` | call_site | `third_party/libuv/src/unix/stream.c:651` | `else if (shutdown(uv__stream_fd(stream), SHUT_WR))` |
| `ev_b749c6ccdaab` | call_site | `third_party/libuv/src/unix/darwin.c:231` | `cpu_info->model = uv__strdup(model);` |
| `ev_b7605aff065c` | call_site | `third_party/libuv/src/unix/fsevents.c:489` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_b765f5b059c7` | call_site | `third_party/libuv/src/unix/fs.c:2074` | `PATH;` |
| `ev_b773d853e86c` | call_site | `third_party/libuv/src/unix/fsevents.c:605` | `uv__queue_init(&loop->cf_signals);` |
| `ev_b7898c619ca0` | call_site | `third_party/libuv/src/unix/async.c:337` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_b78f7dc68c95` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:172` | `hostname_len = hostname ? strlen(hostname) + 1 : 0;` |
| `ev_b79187295b36` | call_site | `third_party/libuv/src/threadpool.c:187` | `uv_cond_destroy(&cond);` |
| `ev_b7a42711f976` | call_site | `third_party/libuv/src/unix/proctitle.c:63` | `size += strlen(argv[i]) + 1;` |
| `ev_b7b65c3847dd` | call_site | `third_party/libuv/src/unix/kqueue.c:423` | `w->cb(loop, w, revents);` |
| `ev_b7bcbd555aad` | call_site | `third_party/libuv/src/unix/udp.c:458` | `assert(0 && "unsupported address family");` |
| `ev_b7c8e5094a23` | call_site | `third_party/libuv/src/unix/fs.c:329` | `r = uv__mkostemp(path, O_CLOEXEC);` |
| `ev_b7cc31f6f70b` | call_site | `third_party/libuv/src/unix/core.c:1350` | `buf = uv__malloc(bufsize);` |
| `ev_b7dffed81e5a` | call_site | `third_party/libuv/src/unix/thread.c:959` | `strncpy(name, thread_name, size - 1);` |
| `ev_b7f1e8920312` | call_site | `third_party/libuv/src/unix/process.c:344` | `uv__write_errno(error_fd);` |
| `ev_b82262930047` | call_site | `third_party/libuv/src/unix/random-getentropy.c:53` | `if (uv__getentropy((char *) buf + pos, buflen - pos))` |
| `ev_b887dd34f8b4` | call_site | `third_party/libuv/src/threadpool.c:275` | `post(&w->wq, kind);` |
| `ev_b88fd9a72864` | call_site | `third_party/libuv/src/unix/tcp.c:311` | `} while (r == -1 && errno == EINTR);` |
| `ev_b897d0abfe07` | call_site | `third_party/libuv/src/unix/stream.c:1554` | `uv__free(handle->queued_fds);` |
| `ev_b8af9b15bfd4` | call_site | `third_party/libuv/src/unix/tcp.c:671` | `uv__close(temp[1]);` |
| `ev_b8b777ec9646` | call_site | `third_party/libuv/src/threadpool.c:229` | `abort();` |
| `ev_b8bf57ea8323` | call_site | `third_party/libuv/src/unix/fs.c:2074` | `PATH;` |
| `ev_b8e79c0313c2` | call_site | `third_party/libuv/src/unix/tty.c:294` | `while (rc == -1 && errno == EINTR);` |
| `ev_b93dfa208408` | call_site | `third_party/libuv/src/unix/fs.c:1737` | `X(CLOSEDIR, uv__fs_closedir(req));` |
| `ev_b93e018b19da` | call_site | `third_party/libuv/src/unix/process.c:612` | `assert(err != ENOSYS);` |
| `ev_b973caa5bfd4` | call_site | `third_party/libuv/src/unix/stream.c:395` | `uv__close(fds[0]);` |
| `ev_b98059aa7171` | call_site | `third_party/libuv/src/unix/darwin.c:91` | `memcpy(buffer, abspath, *size);` |
| `ev_b989201c298c` | call_site | `third_party/libuv/src/uv-common.c:943` | `uv__free(envitems);` |
| `ev_b9bb36ce3f0c` | call_site | `third_party/libuv/src/unix/thread.c:324` | `abort();` |
| `ev_ba0705e7afdf` | call_site | `third_party/libuv/src/unix/fs.c:1400` | `uv_fs_sendfile(NULL, &fs_req, dstfd, srcfd, in_offset, bytes_chunk, NULL);` |
| `ev_ba2b2c51f208` | call_site | `third_party/libuv/src/unix/core.c:1847` | `assert(rc == 0);` |
| `ev_ba31b5a1b27f` | call_site | `third_party/libuv/src/unix/fs.c:2238` | `req->bufs = uv__malloc(nbufs * sizeof(*bufs));` |
| `ev_ba49ffc8131b` | call_site | `third_party/libuv/src/unix/stream.c:207` | `if (errno == EINTR)` |
| `ev_ba5e2d3b1dd4` | call_site | `third_party/libuv/src/uv-common.c:283` | `memcpy(address_part, ip, address_part_size);` |
| `ev_ba652f5cbd24` | call_site | `third_party/libuv/src/unix/async.c:312` | `uv__io_start(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_bab5dbccd29e` | call_site | `third_party/libuv/src/unix/fsevents.c:556` | `V(core_services_handle, FSEventStreamRelease);` |
| `ev_bac54f612905` | call_site | `third_party/libuv/src/unix/random-devurandom.c:92` | `return uv__random_readpath("/dev/urandom", buf, buflen);` |
| `ev_bb20fd100806` | assignment | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_bb321b8aef5b` | call_site | `third_party/libuv/src/unix/signal.c:551` | `removed_handle = RB_REMOVE(uv__signal_tree_s, &uv__signal_tree, handle);` |
| `ev_bb5adcb605d2` | call_site | `third_party/libuv/src/unix/proctitle.c:144` | `memcpy(buffer, process_title.str, process_title.len + 1);` |
| `ev_bb5e75ad809e` | call_site | `third_party/libuv/src/unix/loop.c:141` | `err = uv__async_fork(loop);` |
| `ev_bb64305bd4c7` | assignment | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_bb748193c495` | call_site | `third_party/libuv/src/unix/core.c:1120` | `assert(len > 0);` |
| `ev_bb79ad99c152` | call_site | `third_party/libuv/src/unix/udp.c:931` | `return uv__udp_set_membership6(handle, &addr6, interface_addr, membership);` |
| `ev_bb90e695940f` | call_site | `third_party/libuv/src/unix/core.c:1438` | `*envitems = uv__calloc(i, sizeof(**envitems));` |
| `ev_bb9dc7bb11c4` | call_site | `third_party/libuv/src/unix/process.c:978` | `uv__handle_init(loop, (uv_handle_t*)process, UV_PROCESS);` |
| `ev_bbc21fa1521b` | call_site | `third_party/libuv/src/unix/kqueue.c:609` | `uv__close_nocheckstdio(fd);` |
| `ev_bbc6f4848e6c` | call_site | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_bbcb36b8a439` | call_site | `third_party/libuv/src/uv-common.c:765` | `ent->type = uv__fs_get_dirent_type(dent);` |
| `ev_bbd0e2dfc698` | call_site | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_bbdc1658a0b2` | call_site | `third_party/libuv/src/uv-common.c:57` | `char* m = uv__malloc(len);` |
| `ev_bbefb157b88c` | assignment | `third_party/libuv/src/unix/kqueue.c:624` | `uv__io_init(&handle->event_watcher, uv__fs_event, fd);` |
| `ev_bc141baefdaf` | call_site | `third_party/libuv/src/unix/tcp.c:654` | `if ((err = uv__cloexec(temp[1], 1)))` |
| `ev_bc18e8cd7633` | call_site | `third_party/libuv/src/unix/udp.c:471` | `err = uv__udp_maybe_deferred_bind(handle, addr->sa_family, 0);` |
| `ev_bc40a997f360` | call_site | `third_party/libuv/src/unix/stream.c:416` | `return UV__ERR(errno);` |
| `ev_bc56ba5fb9c2` | call_site | `third_party/libuv/src/unix/darwin.c:176` | `now = time(NULL);` |
| `ev_bc6c69b12c1d` | call_site | `third_party/libuv/src/unix/stream.c:1120` | `stream->read_cb(stream, err, &buf);` |
| `ev_bc6e625fa261` | call_site | `third_party/libuv/src/unix/kqueue.c:155` | `abort();` |
| `ev_bc705a70895f` | call_site | `third_party/libuv/src/unix/fsevents.c:629` | `abort();` |
| `ev_bc92c818788f` | call_site | `third_party/libuv/src/unix/signal.c:330` | `uv__close(loop->signal_pipefd[1]);` |
| `ev_bca1a589e344` | call_site | `third_party/libuv/src/unix/core.c:475` | `uv__run_closing_handles(loop);` |
| `ev_bca53357a316` | call_site | `third_party/libuv/src/unix/udp.c:442` | `memset(addr, 0, sizeof *addr);` |
| `ev_bcaabc955863` | call_site | `third_party/libuv/src/threadpool.c:88` | `uv__queue_remove(q);` |
| `ev_bcb695e64680` | call_site | `third_party/libuv/src/unix/udp.c:99` | `assert(!(handle->flags & UV_HANDLE_UDP_PROCESSING));` |
| `ev_bccc48b6f356` | call_site | `third_party/libuv/src/unix/tcp.c:162` | `err = maybe_new_socket(tcp, addr->sa_family, 0);` |
| `ev_bcd39d25514c` | call_site | `third_party/libuv/src/unix/stream.c:1298` | `assert(nbufs > 0);` |
| `ev_bce0d87f8d38` | call_site | `third_party/libuv/src/unix/process.c:176` | `assert(uv__queue_empty(&pending));` |
| `ev_bce3a72b771e` | call_site | `third_party/libuv/src/unix/fsevents.c:713` | `pCFRunLoopAddSource(state->loop,` |
| `ev_bd12c0f2aae5` | call_site | `third_party/libuv/src/unix/process.c:1089` | `if (kill(pid, signum)) {` |
| `ev_bd406563202e` | call_site | `third_party/libuv/src/unix/loop.c:206` | `uv__free(lfields);` |
| `ev_bd5daafdd6f8` | call_site | `third_party/libuv/src/unix/stream.c:500` | `emfile_fd = uv__open_cloexec("/", O_RDONLY);` |
| `ev_bd662a3ae4eb` | call_site | `third_party/libuv/src/uv-common.c:913` | `uv__free(loop);` |
| `ev_bd6ccc3e596e` | call_site | `third_party/libuv/src/unix/process.c:697` | `err = posix_spawn(pid, options->file, actions, attrs, options->args, env);` |
| `ev_bd8e0aaa10b7` | call_site | `third_party/libuv/src/idna.c:202` | `assert(c != UINT_MAX);` |
| `ev_bd9b2df6d84f` | call_site | `third_party/libuv/src/unix/stream.c:1364` | `req->bufs = uv__malloc(nbufs * sizeof(bufs[0]));` |
| `ev_bd9bac265aaf` | call_site | `third_party/libuv/src/unix/fsevents.c:780` | `assert(state != NULL);` |
| `ev_bdd15c70a5c5` | call_site | `third_party/libuv/src/unix/udp.c:205` | `chunk_buf = uv_buf_init(iov[k].iov_base, iov[k].iov_len);` |
| `ev_bdf93e42ee8b` | call_site | `third_party/libuv/src/unix/stream.c:469` | `assert(stream->write_queue_size == 0);` |
| `ev_be1e9a1af48d` | call_site | `third_party/libuv/src/unix/poll.c:91` | `uv__io_init(&handle->io_watcher, uv__poll_io, fd);` |
| `ev_be39dd23acb8` | call_site | `third_party/libuv/src/uv-common.c:542` | `return uv__udp_recv_start(handle, alloc_cb, recv_cb);` |
| `ev_be43452e9ff8` | call_site | `third_party/libuv/src/unix/udp.c:845` | `return UV__ERR(errno);` |
| `ev_be769cb02784` | call_site | `third_party/libuv/src/unix/udp.c:71` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_be7ebf321f3b` | call_site | `third_party/libuv/src/unix/signal.c:188` | `saved_errno = errno;` |
| `ev_be9938575c50` | call_site | `third_party/libuv/src/unix/core.c:448` | `uv__queue_empty(&loop->idle_handles);` |
| `ev_bea4a62ca126` | call_site | `third_party/libuv/src/unix/core.c:1901` | `snprintf(trypath, sizeof(trypath) - 1, "%s/%s", token, prog);` |
| `ev_bead9a79abf7` | call_site | `third_party/libuv/src/unix/core.c:234` | `assert(0);` |
| `ev_bebe0913debe` | call_site | `third_party/libuv/src/uv-common.c:680` | `memcpy(buffer, handle->path, required_len);` |
| `ev_bece5b64ad2c` | call_site | `third_party/libuv/src/unix/core.c:633` | `rc = uv__close_nocancel(fd);` |
| `ev_becf49d800a5` | call_site | `third_party/libuv/src/unix/tcp.c:479` | `return UV__ERR(errno);` |
| `ev_beddc415fcf0` | call_site | `third_party/libuv/src/unix/kqueue.c:198` | `assert(w->pevents != 0);` |
| `ev_bee1b5ef2f66` | call_site | `third_party/libuv/src/unix/core.c:564` | `assert(sockfd >= 0);` |
| `ev_bf05c39d5412` | call_site | `third_party/libuv/src/unix/getnameinfo.c:52` | `req->retcode = uv__getaddrinfo_translate_error(err);` |
| `ev_bf29d3d68222` | call_site | `third_party/libuv/src/thread-common.c:52` | `b = uv__malloc(sizeof(*b));` |
| `ev_bf2df9173317` | call_site | `third_party/libuv/src/unix/stream.c:465` | `uv__stream_flush_write_queue(stream, UV_ECANCELED);` |
| `ev_bf316242a363` | call_site | `third_party/libuv/src/unix/fs.c:732` | `pathmax = pathconf(path, _PC_PATH_MAX);` |
| `ev_bf48a63262eb` | call_site | `third_party/libuv/src/unix/fsevents.c:637` | `err = UV__ERR(pthread_create(&loop->cf_thread, &attr, uv__cf_loop_runner, loop));` |
| `ev_bf5a53f309f1` | call_site | `third_party/libuv/src/unix/fsevents.c:745` | `while (!uv__queue_empty(&split_head)) {` |
| `ev_bf9c1dcb3830` | call_site | `third_party/libuv/src/unix/signal.c:552` | `assert(removed_handle == handle);` |
| `ev_bff28bab5e2d` | call_site | `third_party/libuv/src/uv-common.c:889` | `uv__loop_close(loop);` |
| `ev_bff722388041` | call_site | `third_party/libuv/src/unix/core.c:1312` | `memcpy(pwd->homedir, pw.pw_dir, homedir_size);` |
| `ev_c025fef04414` | call_site | `third_party/libuv/src/threadpool.c:239` | `uv_sem_wait(&sem);` |
| `ev_c0260d154bc5` | call_site | `third_party/libuv/src/fs-poll.c:159` | `memcpy(buffer, ctx->path, required_len);` |
| `ev_c02b572bcedf` | call_site | `third_party/libuv/src/uv-common.c:849` | `if (uv_loop_init(&default_loop_struct))` |
| `ev_c02f246dbe6d` | call_site | `third_party/libuv/src/unix/pipe.c:115` | `memcpy(pipe_fname, name, namelen);` |
| `ev_c04da2825f29` | call_site | `third_party/libuv/src/unix/udp.c:575` | `err = uv__udp_maybe_deferred_bind(handle, addr->sa_family, 0);` |
| `ev_c05545a8eb37` | call_site | `third_party/libuv/src/unix/async.c:53` | `kq = kqueue();` |
| `ev_c0622aa8aa4c` | assignment | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_c07408c5e319` | call_site | `third_party/libuv/src/idna.c:555` | `*target_len_ptr = target_len + uv_utf16_length_as_wtf8(w_source_ptr, w_source_len);` |
| `ev_c07d8c90d04b` | call_site | `third_party/libuv/src/unix/udp.c:57` | `uv__io_close(handle->loop, &handle->io_watcher);` |
| `ev_c082361de90c` | call_site | `third_party/libuv/src/unix/signal.c:134` | `} while (r < 0 && errno == EINTR);` |
| `ev_c0943253e2da` | assignment | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_c0b363f15438` | call_site | `third_party/libuv/src/unix/fs.c:1352` | `result = fchown(dstfd, src_statsbuf.st_uid, src_statsbuf.st_gid);` |
| `ev_c0b8de5692e8` | call_site | `third_party/libuv/src/unix/tcp.c:134` | `uv__queue_remove(&tcp->handle_queue);` |
| `ev_c0bbe22885b3` | call_site | `third_party/libuv/src/unix/udp.c:922` | `if (uv_ip4_addr(multicast_addr, 0, &addr4) == 0) {` |
| `ev_c0bffae61bd8` | call_site | `third_party/libuv/src/threadpool.c:151` | `uv_mutex_unlock(&mutex);` |
| `ev_c0c79fe65676` | call_site | `third_party/libuv/src/unix/kqueue.c:294` | `assert(errno == EINTR);` |
| `ev_c0e4f394e8e3` | call_site | `third_party/libuv/src/unix/getnameinfo.c:61` | `uv__req_unregister(req->loop);` |
| `ev_c0ebd547cc9c` | call_site | `third_party/libuv/src/unix/kqueue.c:193` | `q = uv__queue_head(&loop->watcher_queue);` |
| `ev_c1134f264544` | call_site | `third_party/libuv/src/unix/udp.c:928` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET6, UV_UDP_REUSEADDR);` |
| `ev_c149f02e1131` | call_site | `third_party/libuv/src/unix/fsevents.c:393` | `pFSEventStreamRelease(state->fsevent_stream);` |
| `ev_c14e3dacde4e` | call_site | `third_party/libuv/src/unix/udp.c:652` | `return uv__count_bufs(bufs, nbufs);` |
| `ev_c14fe7e569b1` | call_site | `third_party/libuv/src/idna.c:141` | `assert(*p < pe);` |
| `ev_c179a331e78d` | call_site | `third_party/libuv/src/unix/fsevents.c:551` | `V(core_foundation_handle, CFRunLoopWakeUp);` |
| `ev_c1aef9f437bf` | call_site | `third_party/libuv/src/unix/loop.c:114` | `uv__signal_loop_cleanup(loop);` |
| `ev_c1bbf875a0ee` | assignment | `third_party/libuv/src/unix/signal.c:272` | `uv__io_init(&loop->signal_io_watcher,` |
| `ev_c1e2bbb5e318` | call_site | `third_party/libuv/src/unix/udp.c:71` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_c1e861b792c5` | call_site | `third_party/libuv/src/unix/thread.c:110` | `return uv__default_stack_size();` |
| `ev_c1e9be4cb3a8` | call_site | `third_party/libuv/src/unix/fs.c:1945` | `PATH;` |
| `ev_c1f935620d26` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:109` | `pCFBundleGetFunctionPointerForName(launch_services_bundle,` |
| `ev_c204604ff085` | call_site | `third_party/libuv/src/unix/core.c:1572` | `return getpid();` |
| `ev_c21082c86542` | call_site | `third_party/libuv/src/unix/random-getentropy.c:43` | `uv_once(&once, uv__random_getentropy_init);` |
| `ev_c27367387ac4` | call_site | `third_party/libuv/src/unix/core.c:339` | `uv__make_close_pending(handle);  /* Back into the queue. */` |
| `ev_c2b6d2820953` | call_site | `third_party/libuv/src/unix/fsevents.c:782` | `pCFRunLoopWakeUp(state->loop);` |
| `ev_c2dde5aaba75` | call_site | `third_party/libuv/src/unix/process.c:305` | `setsid();` |
| `ev_c308cadbf87a` | call_site | `third_party/libuv/src/unix/stream.c:1224` | `uv__stream_eof(stream, &buf);` |
| `ev_c32e1bb18003` | call_site | `third_party/libuv/src/unix/core.c:1280` | `r = getpwuid_r(uid, &pw, buf, bufsize, &result);` |
| `ev_c34c08edf0bb` | call_site | `third_party/libuv/src/timer.c:193` | `handle->timer_cb(handle);` |
| `ev_c395b17befd0` | call_site | `third_party/libuv/src/unix/pipe.c:47` | `uv__stream_init(loop, (uv_stream_t*)handle, UV_NAMED_PIPE);` |
| `ev_c3b096d6d0ee` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:129` | `assert(req->retcode == 0);` |
| `ev_c3c1e93dc781` | call_site | `third_party/libuv/src/unix/core.c:1515` | `if (setenv(name, value, 1) != 0)` |
| `ev_c3c6513a28fe` | call_site | `third_party/libuv/src/unix/process.c:321` | `uv__write_errno(error_fd);` |
| `ev_c3dbba06a609` | call_site | `third_party/libuv/src/unix/fsevents.c:632` | `abort();` |
| `ev_c427326553fc` | call_site | `third_party/libuv/src/unix/fsevents.c:210` | `uv_async_send(handle->cf_cb);` |
| `ev_c42c919e2b1e` | call_site | `third_party/libuv/src/unix/core.c:1685` | `r = pthread_getschedparam(tid, &policy, &param);` |
| `ev_c4396c4709b0` | call_site | `third_party/libuv/src/unix/core.c:525` | `err = uv__cloexec(sockfd, 1);` |
| `ev_c44acd0aa7d1` | call_site | `third_party/libuv/src/inet.c:209` | `memcpy(dst, tmp, sizeof(struct in_addr));` |
| `ev_c45df9a84d5b` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:233` | `if (if_indextoname(ifindex, ifname_buf) == NULL)` |
| `ev_c4600cf17133` | call_site | `third_party/libuv/src/unix/fsevents.c:557` | `V(core_services_handle, FSEventStreamScheduleWithRunLoop);` |
| `ev_c4747b5cf58b` | call_site | `third_party/libuv/src/unix/udp.c:647` | `assert(handle->flags & UV_HANDLE_UDP_CONNECTED);` |
| `ev_c494f7c1f30e` | call_site | `third_party/libuv/src/unix/core.c:519` | `sockfd = socket(domain, type, protocol);` |
| `ev_c4984fea51d7` | call_site | `third_party/libuv/src/unix/stream.c:228` | `assert((s->events == 0) \|\| (stream->flags & UV_HANDLE_CLOSING));` |
| `ev_c4d1e0b5cd0c` | call_site | `third_party/libuv/src/uv-common.c:140` | `uv__free(pwd->username);` |
| `ev_c4f38aca21b8` | call_site | `third_party/libuv/src/unix/udp.c:1276` | `r = UV__ERR(errno);` |
| `ev_c505b01b7556` | call_site | `third_party/libuv/src/unix/process.c:1084` | `return uv_kill(process->pid, signum);` |
| `ev_c516ecd16c03` | call_site | `third_party/libuv/src/unix/fsevents.c:682` | `uv_thread_join(&loop->cf_thread);` |
| `ev_c52c9e1d682b` | call_site | `third_party/libuv/src/unix/core.c:191` | `uv__idle_close((uv_idle_t*)handle);` |
| `ev_c52d264dcd1e` | call_site | `third_party/libuv/src/unix/loop.c:120` | `uv_mutex_destroy(&lfields->loop_metrics.lock);` |
| `ev_c53352447a66` | call_site | `third_party/libuv/src/unix/stream.c:456` | `assert(!uv__io_active(&stream->io_watcher, POLLIN \| POLLOUT));` |
| `ev_c53e0d09dab6` | call_site | `third_party/libuv/src/unix/fs.c:1732` | `X(OPEN, uv__fs_open(req));` |
| `ev_c54b4a9d40e6` | call_site | `third_party/libuv/src/threadpool.c:96` | `uv__queue_insert_tail(&wq, q);` |
| `ev_c54b806a3cd0` | call_site | `third_party/libuv/src/unix/loop.c:48` | `memset(&lfields->loop_metrics.metrics,` |
| `ev_c558acef57eb` | call_site | `third_party/libuv/src/unix/fs.c:482` | `p = dlsym(RTLD_DEFAULT, is_pread ? "preadv" : "pwritev");` |
| `ev_c55cf48c308d` | call_site | `third_party/libuv/src/unix/udp.c:1331` | `if ((r = uv__udp_sendmsg1(fd, bufs[i], nbufs[i], addrs[i])))` |
| `ev_c575b4dcece8` | call_site | `third_party/libuv/src/unix/udp.c:186` | `while (nread == -1 && errno == EINTR);` |
| `ev_c5a25c93b10f` | call_site | `third_party/libuv/src/unix/stream.c:307` | `while (ret == -1 && errno == EINTR);` |
| `ev_c5b3e74bd33e` | call_site | `third_party/libuv/src/unix/fsevents.c:468` | `err = uv__fsevents_create_stream(state, loop, cf_paths);` |
| `ev_c5d6f7ed3be4` | call_site | `third_party/libuv/src/unix/fs.c:1778` | `req->cb(req);` |
| `ev_c5e17e29ee47` | call_site | `third_party/libuv/src/unix/process.c:968` | `assert(options->file != NULL);` |
| `ev_c5e7fc2d64fb` | call_site | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_c5f83192d6e8` | call_site | `third_party/libuv/src/unix/stream.c:519` | `err = uv__accept(fd);` |
| `ev_c60d0a32c382` | call_site | `third_party/libuv/src/unix/stream.c:467` | `uv__drain(stream);` |
| `ev_c6482a526097` | call_site | `third_party/libuv/src/unix/fs.c:1717` | `X(COPYFILE, uv__fs_copyfile(req));` |
| `ev_c65f7ee7ea58` | call_site | `third_party/libuv/src/unix/udp.c:451` | `memset(addr, 0, sizeof *addr);` |
| `ev_c6770fa440f4` | call_site | `third_party/libuv/src/unix/proctitle.c:144` | `memcpy(buffer, process_title.str, process_title.len + 1);` |
| `ev_c677441de6ba` | call_site | `third_party/libuv/src/unix/process.c:824` | `sigdelset(&signewset, SIGABRT);` |
| `ev_c69095c42f12` | call_site | `third_party/libuv/src/unix/fs.c:253` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_c6b1f09993c5` | call_site | `third_party/libuv/src/unix/poll.c:104` | `uv__io_stop(handle->loop,` |
| `ev_c6bc3a570d6e` | call_site | `third_party/libuv/src/unix/pipe.c:324` | `uv__stream_fd(handle),` |
| `ev_c6d0d2c587ea` | call_site | `third_party/libuv/src/unix/fs.c:1741` | `X(RMDIR, rmdir(req->path));` |
| `ev_c6d9b637bb20` | call_site | `third_party/libuv/src/unix/udp.c:1134` | `memset(&addr_st, 0, sizeof addr_st);` |
| `ev_c6e91c01e8e1` | call_site | `third_party/libuv/src/thread-common.c:66` | `rc = uv_cond_init((uv_cond_t*) &b->cond);` |
| `ev_c6ed5938e44d` | call_site | `third_party/libuv/src/unix/fsevents.c:589` | `err = uv__fsevents_global_init();` |
| `ev_c709be5edd28` | assignment | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_c71783f63439` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_c7551b537f72` | call_site | `third_party/libuv/src/unix/stream.c:633` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_c758eb7d965d` | call_site | `third_party/libuv/src/unix/udp.c:232` | `assert(handle->alloc_cb != NULL);` |
| `ev_c78a5316121d` | call_site | `third_party/libuv/src/unix/fs.c:818` | `len = uv__fs_pathmax_size(req->path);` |
| `ev_c7b632466062` | call_site | `third_party/libuv/src/unix/getnameinfo.c:94` | `memcpy(&req->storage,` |
| `ev_c7c00065bf73` | call_site | `third_party/libuv/src/unix/udp.c:481` | `return UV__ERR(errno);` |
| `ev_c7cc9db9467d` | call_site | `third_party/libuv/src/unix/proctitle.c:117` | `memset(pt->str + len, '\0', pt->cap - len);` |
| `ev_c7f9d5275ffb` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:138` | `if (strcmp(address->name, ent->ifa_name) == 0) {` |
| `ev_c81448d99117` | call_site | `third_party/libuv/src/unix/fs.c:1982` | `PATH;` |
| `ev_c8659ac535a4` | call_site | `third_party/libuv/src/unix/core.c:946` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_c8890363ff16` | call_site | `third_party/libuv/src/unix/fs.c:1596` | `ret = uv__stat(path, &pbuf);` |
| `ev_c8949d2ef35a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:112` | `uv__req_unregister(req->loop);` |
| `ev_c8ae8e5897a8` | call_site | `third_party/libuv/src/inet.c:296` | `memcpy(dst, tmp, sizeof tmp);` |
| `ev_c8d34ac33e11` | assignment | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_c8d888c00b2a` | call_site | `third_party/libuv/src/threadpool.c:73` | `(uv__queue_head(&wq) == &run_slow_work_message &&` |
| `ev_c8dc0f955927` | call_site | `third_party/libuv/src/unix/stream.c:1204` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_c8f05efb9dda` | call_site | `third_party/libuv/src/unix/fsevents.c:843` | `err = uv__cf_loop_signal(handle->loop, handle, kUVCFLoopSignalRegular);` |
| `ev_c915d0137653` | call_site | `third_party/libuv/src/fs-poll.c:130` | `uv_close((uv_handle_t*)&ctx->timer_handle, timer_close_cb);` |
| `ev_c95e706f32f8` | call_site | `third_party/libuv/src/unix/fsevents.c:499` | `uv_sem_post(&state->fsevent_sem);` |
| `ev_c972bfdb3eda` | call_site | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_c97b5f85a052` | call_site | `third_party/libuv/src/unix/signal.c:446` | `r = read(loop->signal_pipefd[0], buf + bytes, sizeof(buf) - bytes);` |
| `ev_c99564011fc4` | call_site | `third_party/libuv/src/uv-common.c:911` | `assert(err == 0);` |
| `ev_c9b3a0ee6834` | call_site | `third_party/libuv/src/timer.c:183` | `uv__queue_insert_tail(&ready_queue, &handle->node.queue);` |
| `ev_c9d578b23872` | assignment | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_ca135d58681b` | call_site | `third_party/libuv/src/unix/stream.c:220` | `assert(events != 0 \|\| FD_ISSET(s->int_fd, s->sread));` |
| `ev_ca204fc5311f` | call_site | `third_party/libuv/src/unix/udp.c:143` | `assert(handle->type == UV_UDP);` |
| `ev_ca209b632354` | call_site | `third_party/libuv/src/unix/loop.c:40` | `lfields = (uv__loop_internal_fields_t*) uv__calloc(1, sizeof(*lfields));` |
| `ev_ca40fc49101f` | call_site | `third_party/libuv/src/unix/process.c:140` | `if (errno != ECHILD)` |
| `ev_ca49d7b8c64c` | call_site | `third_party/libuv/src/threadpool.c:320` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_ca4bc4ccb8a5` | call_site | `third_party/libuv/src/unix/core.c:1450` | `buf = uv__strdup(environ[j]);` |
| `ev_ca5151b07b7a` | call_site | `third_party/libuv/src/unix/process.c:504` | `err = posix_spawnattr_setflags(attrs, flags);` |
| `ev_ca5b9c9c8bbd` | call_site | `third_party/libuv/src/unix/process.c:219` | `assert(0 && "Unexpected flags");` |
| `ev_ca88114b76dc` | call_site | `third_party/libuv/src/unix/fs.c:186` | `r = fsync(req->file);` |
| `ev_ca8a5bfa13cd` | call_site | `third_party/libuv/src/unix/stream.c:323` | `if (socketpair(AF_UNIX, SOCK_STREAM, 0, fds))` |
| `ev_ca93d09dfd43` | call_site | `third_party/libuv/src/unix/fs.c:372` | `return open(req->path, req->flags \| O_CLOEXEC, req->mode);` |
| `ev_ca974dd8d956` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:80` | `dlsym(core_foundation_handle, "CFBundleGetBundleWithIdentifier");` |
| `ev_cad3b18749bb` | call_site | `third_party/libuv/src/unix/signal.c:558` | `first_handle = uv__signal_first_handle(handle->signum);` |
| `ev_cae38e8a39ab` | call_site | `third_party/libuv/src/unix/fsevents.c:743` | `uv_mutex_unlock(&loop->cf_mutex);` |
| `ev_cae4056ac64c` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_caeb2eecfeea` | assignment | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_cb3e8930a9fc` | call_site | `third_party/libuv/src/unix/stream.c:532` | `uv__io_stop(loop, &stream->io_watcher, POLLIN);` |
| `ev_cb4a72efb34d` | call_site | `third_party/libuv/src/unix/darwin.c:208` | `if (host_processor_info(mach_host_self(), PROCESSOR_CPU_LOAD_INFO, &numcpus,` |
| `ev_cb57013c10d3` | call_site | `third_party/libuv/src/unix/kqueue.c:238` | `abort();` |
| `ev_cb593684fcb7` | call_site | `third_party/libuv/src/unix/random-devurandom.c:43` | `if (uv__fstat(fd, &s)) {` |
| `ev_cb610ef1657c` | call_site | `third_party/libuv/src/unix/random-devurandom.c:60` | `return UV__ERR(errno);` |
| `ev_cb773ed8c179` | call_site | `third_party/libuv/src/unix/stream.c:999` | `assert(count % sizeof(fd) == 0);` |
| `ev_cb819328308f` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:141` | `memcpy(address->phys_addr, LLADDR(sa_addr), sizeof(address->phys_addr));` |
| `ev_cb901e1d6ca5` | call_site | `third_party/libuv/src/unix/stream.c:204` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK)` |
| `ev_cba33e307b6f` | call_site | `third_party/libuv/src/unix/core.c:405` | `uv__queue_empty(&loop->pending_queue) &&` |
| `ev_cba6dcf89022` | call_site | `third_party/libuv/src/unix/async.c:390` | `uv__close(loop->async_wfd);` |
| `ev_cbc5db67d9b3` | call_site | `third_party/libuv/src/threadpool.c:77` | `uv_cond_wait(&cond, &mutex);` |
| `ev_cbc978a7f813` | call_site | `third_party/libuv/src/unix/fs.c:1719` | `X(FCHOWN, fchown(req->file, req->uid, req->gid));` |
| `ev_cbe490a587ad` | call_site | `third_party/libuv/src/unix/stream.c:270` | `uv__free(s);` |
| `ev_cc272be5085b` | call_site | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_cc28c9c3a683` | call_site | `third_party/libuv/src/unix/stream.c:1236` | `uv__drain(stream);` |
| `ev_cc774e2e8c90` | call_site | `third_party/libuv/src/unix/pipe.c:329` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_cc7cc3445003` | call_site | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_cc7ec98e94a9` | call_site | `third_party/libuv/src/unix/signal.c:566` | `assert(ret == 0);` |
| `ev_cc8c859a34ab` | call_site | `third_party/libuv/src/uv-common.c:728` | `uv__fs_scandir_free(req->ptr);` |
| `ev_cc99a9eccb0e` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:159` | `S(title),` |
| `ev_cceea6215119` | call_site | `third_party/libuv/src/unix/kqueue.c:294` | `assert(errno == EINTR);` |
| `ev_ccfb82ba279a` | call_site | `third_party/libuv/src/unix/fs.c:1132` | `return uv__fs_sendfile_emul(req);` |
| `ev_cd2024463a19` | call_site | `third_party/libuv/src/unix/process.c:1042` | `uv__queue_insert_tail(&loop->process_handles, &process->queue);` |
| `ev_cd55bb8f6565` | call_site | `third_party/libuv/src/unix/udp.c:673` | `mreq.imr_interface.s_addr = htonl(INADDR_ANY);` |
| `ev_cd5b09208f34` | call_site | `third_party/libuv/src/unix/fsevents.c:619` | `memset(&ctx, 0, sizeof(ctx));` |
| `ev_cd7feb5c4c8f` | call_site | `third_party/libuv/src/uv-common.c:561` | `q = uv__queue_head(&queue);` |
| `ev_cd9c06b84f0e` | call_site | `third_party/libuv/src/unix/tty.c:431` | `if (getsockname(file, (struct sockaddr*) &ss, &len)) {` |
| `ev_cdb8bbb079f4` | call_site | `third_party/libuv/src/unix/fsevents.c:449` | `assert(curr->realpath != NULL);` |
| `ev_cdc6246b7ebb` | call_site | `third_party/libuv/src/unix/thread.c:897` | `abort();` |
| `ev_cdd5f5f0d1d2` | call_site | `third_party/libuv/src/unix/tty.c:277` | `cfmakeraw(tio);` |
| `ev_cde8f20c2347` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_cdf1c1a45318` | call_site | `third_party/libuv/src/unix/stream.c:790` | `memset(&cmsg, 0, sizeof(cmsg));` |
| `ev_ce0c728b9496` | call_site | `third_party/libuv/src/unix/fs.c:1771` | `uv__req_unregister(req->loop);` |
| `ev_ce1392d7d3d5` | call_site | `third_party/libuv/src/unix/stream.c:645` | `uv__req_unregister(stream->loop);` |
| `ev_ce157345f7c3` | call_site | `third_party/libuv/src/fs-poll.c:79` | `len = strlen(path);` |
| `ev_ce1e1fb84570` | call_site | `third_party/libuv/src/idna.c:344` | `rc = uv__idna_toascii_label(s, st, &d, de);` |
| `ev_ce3d8061820e` | call_site | `third_party/libuv/src/unix/stream.c:1161` | `assert(stream->type == UV_TCP \|\|` |
| `ev_ce3ea056b547` | call_site | `third_party/libuv/src/unix/loop.c:192` | `uv_rwlock_destroy(&loop->cloexec_lock);` |
| `ev_ce40a7a8e04a` | call_site | `third_party/libuv/src/unix/udp.c:271` | `handle->recv_cb(handle, UV__ERR(errno), &buf, NULL, 0);` |
| `ev_ce8871585522` | call_site | `third_party/libuv/src/uv-common.c:257` | `addr->sin_port = htons(port);` |
| `ev_ce92aaa3e854` | call_site | `third_party/libuv/src/unix/core.c:1308` | `memcpy(pwd->username, pw.pw_name, name_size);` |
| `ev_ce9d66273be0` | call_site | `third_party/libuv/src/fs-poll.c:92` | `err = uv_timer_init(loop, &ctx->timer_handle);` |
| `ev_cecd940b830c` | call_site | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_cee273c5b1f3` | call_site | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_cf0a45869d69` | call_site | `third_party/libuv/src/unix/stream.c:411` | `assert(fd >= 0);` |
| `ev_cf27cbd7b3dd` | call_site | `third_party/libuv/src/unix/fs.c:1130` | `errno == EXDEV) {` |
| `ev_cf3e0faa2dfc` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:65` | `application_services_handle = dlopen("/System/Library/Frameworks/"` |
| `ev_cf5781b7a598` | call_site | `third_party/libuv/src/unix/poll.c:48` | `uv__io_stop(loop, w, POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI);` |
| `ev_cf5f9f05bdf1` | call_site | `third_party/libuv/src/unix/loop.c:183` | `assert(uv__queue_empty(&loop->wq) && "thread pool work queue not empty!");` |
| `ev_cf604ada7d6e` | call_site | `third_party/libuv/src/unix/stream.c:806` | `memcpy(CMSG_DATA(&cmsg.hdr), &fd_to_send, sizeof(fd_to_send));` |
| `ev_cf6c3ad65c9a` | call_site | `third_party/libuv/src/unix/fsevents.c:307` | `memset(event, 0, sizeof(*event));` |
| `ev_cf70faf10b1d` | call_site | `third_party/libuv/src/unix/core.c:1598` | `return UV__ERR(errno);` |
| `ev_cfb534324a96` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:132` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFPHYS))` |
| `ev_d004a6ff2b9c` | call_site | `third_party/libuv/src/unix/fsevents.c:742` | `uv__queue_move(&loop->cf_signals, &split_head);` |
| `ev_d00bce033b87` | call_site | `third_party/libuv/src/unix/stream.c:175` | `if (uv__io_active(&stream->io_watcher, POLLOUT))` |
| `ev_d021882524a2` | call_site | `third_party/libuv/src/unix/process.c:316` | `pipes[fd][1] = fcntl(use_fd, F_DUPFD_CLOEXEC, stdio_count);` |
| `ev_d07ea6f4458d` | assignment | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_d0870b3c94c9` | call_site | `third_party/libuv/src/unix/process.c:724` | `z = strchr(p, ':');` |
| `ev_d0a1b705a388` | call_site | `third_party/libuv/src/unix/fsevents.c:683` | `uv_sem_destroy(&loop->cf_sem);` |
| `ev_d0a1cc5475a1` | call_site | `third_party/libuv/src/unix/stream.c:247` | `assert(events == (events & (POLLIN \| POLLOUT)));` |
| `ev_d0aa403c8561` | call_site | `third_party/libuv/src/unix/core.c:465` | `uv__run_pending(loop);` |
| `ev_d0cf39987f9f` | call_site | `third_party/libuv/src/unix/fs.c:705` | `errno = ENOMEM;` |
| `ev_d0e63f23b3a5` | call_site | `third_party/libuv/src/unix/stream.c:1208` | `uv__read(stream);` |
| `ev_d0fd49a84220` | call_site | `third_party/libuv/src/inet.c:130` | `tp += strlen(tp);` |
| `ev_d118df7d8e6f` | call_site | `third_party/libuv/src/unix/stream.c:674` | `size = uv__count_bufs(req->bufs + req->write_index,` |
| `ev_d11d54d0d19f` | call_site | `third_party/libuv/src/unix/fsevents.c:446` | `assert(q != &state->fsevent_handles);` |
| `ev_d12485c3e5c4` | call_site | `third_party/libuv/src/unix/process.c:841` | `return UV__ERR(errno);` |
| `ev_d151a4d43dce` | call_site | `third_party/libuv/src/unix/signal.c:112` | `uv_once(&uv__signal_global_init_guard, uv__signal_global_init);` |
| `ev_d15b5e000713` | call_site | `third_party/libuv/src/unix/process.c:822` | `sigdelset(&signewset, SIGILL);` |
| `ev_d1735b689509` | call_site | `third_party/libuv/src/unix/process.c:339` | `uv__close_nocheckstdio(fd); /* Free up fd, if it happens to be open. */` |
| `ev_d1904d590835` | call_site | `third_party/libuv/src/uv-common.c:559` | `uv__queue_move(&loop->handle_queue, &queue);` |
| `ev_d1acf83af367` | call_site | `third_party/libuv/src/unix/kqueue.c:587` | `uv__free(handle->path);` |
| `ev_d1c0927bbd6b` | call_site | `third_party/libuv/src/unix/signal.c:229` | `memset(&sa, 0, sizeof(sa));` |
| `ev_d1e5a89d4587` | call_site | `third_party/libuv/src/unix/core.c:1881` | `memcpy(buf, abspath, *buflen);` |
| `ev_d1eb9c76b08d` | call_site | `third_party/libuv/src/unix/core.c:946` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_d1f911907011` | call_site | `third_party/libuv/src/unix/stream.c:676` | `assert(req->handle->write_queue_size >= size);` |
| `ev_d22037b22151` | call_site | `third_party/libuv/src/unix/core.c:451` | `uv__run_idle(loop);` |
| `ev_d2287da16e14` | call_site | `third_party/libuv/src/unix/core.c:760` | `if (getcwd(buffer, *size) != NULL)` |
| `ev_d23022af4326` | call_site | `third_party/libuv/src/unix/core.c:474` | `uv__run_check(loop);` |
| `ev_d236797ac25a` | call_site | `third_party/libuv/src/unix/proctitle.c:108` | `uv_mutex_lock(&process_title_mutex);` |
| `ev_d23d39334710` | call_site | `third_party/libuv/src/threadpool.c:418` | `return uv__work_cancel(loop, req, wreq);` |
| `ev_d246b9d6fc6a` | call_site | `third_party/libuv/src/unix/stream.c:1566` | `return uv__nonblock(uv__stream_fd(handle), !blocking);` |
| `ev_d275eeb625e0` | call_site | `third_party/libuv/src/timer.c:63` | `uv__queue_init(&handle->node.queue);` |
| `ev_d2921f4ca6b9` | call_site | `third_party/libuv/src/idna.c:201` | `c = uv__utf8_decode1(&s, se);` |
| `ev_d2b788a80ee2` | call_site | `third_party/libuv/src/unix/fs.c:2173` | `PATH;` |
| `ev_d2d800a82fff` | call_site | `third_party/libuv/src/unix/loop.c:205` | `uv_mutex_destroy(&lfields->loop_metrics.lock);` |
| `ev_d2dba493dabd` | call_site | `third_party/libuv/src/unix/async.c:350` | `uv__close(loop->async_wfd);` |
| `ev_d2f38ae91781` | call_site | `third_party/libuv/src/unix/proctitle.c:81` | `memcpy(s, argv[i], size);` |
| `ev_d308d52ab182` | call_site | `third_party/libuv/src/unix/kqueue.c:194` | `uv__queue_remove(q);` |
| `ev_d3091cd2fb7f` | call_site | `third_party/libuv/src/unix/stream.c:1518` | `uv_sem_post(&s->close_sem);` |
| `ev_d31236e9b656` | call_site | `third_party/libuv/src/unix/fs.c:493` | `memcpy(&f, &p, sizeof(p));` |
| `ev_d33c72089950` | call_site | `third_party/libuv/src/unix/kqueue.c:611` | `r = uv__fsevents_init(handle);` |
| `ev_d33cd147ff88` | call_site | `third_party/libuv/src/unix/fs.c:2058` | `memcpy(req->bufs, bufs, nbufs * sizeof(*bufs));` |
| `ev_d34367287ed6` | call_site | `third_party/libuv/src/unix/async.c:236` | `r = kevent(loop->backend_fd, &ev, 1, NULL, 0, NULL);` |
| `ev_d344de8eb3fb` | call_site | `third_party/libuv/src/uv-common.c:255` | `memset(addr, 0, sizeof(*addr));` |
| `ev_d35c4d53b2e9` | call_site | `third_party/libuv/src/unix/core.c:1249` | `memcpy(buffer, buf, len + 1);` |
| `ev_d36cd3cd9c47` | call_site | `third_party/libuv/src/unix/stream.c:296` | `return UV__ERR(errno);` |
| `ev_d40c816c3707` | call_site | `third_party/libuv/src/unix/stream.c:1442` | `assert(stream->type == UV_TCP \|\| stream->type == UV_NAMED_PIPE \|\|` |
| `ev_d410cdba5320` | call_site | `third_party/libuv/src/unix/udp.c:85` | `assert(handle->send_queue_size == 0);` |
| `ev_d42a460b97a6` | call_site | `third_party/libuv/src/unix/fs.c:647` | `if (strcmp(res->d_name, ".") == 0 \|\| strcmp(res->d_name, "..") == 0)` |
| `ev_d43e3880e171` | call_site | `third_party/libuv/src/unix/tty.c:74` | `while (rc == -1 && errno == EINTR);` |
| `ev_d441087ab17d` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:69` | `core_foundation_handle = dlopen("/System/Library/Frameworks/"` |
| `ev_d4496da193ab` | call_site | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_d46103bda0bb` | call_site | `third_party/libuv/src/unix/udp.c:72` | `assert(handle->io_watcher.fd == -1);` |
| `ev_d47015d076db` | call_site | `third_party/libuv/src/unix/async.c:155` | `uv__queue_remove(&handle->queue);` |
| `ev_d473f97602c0` | call_site | `third_party/libuv/src/unix/process.c:695` | `if (strchr(options->file, '/') != NULL) {` |
| `ev_d479a038ac24` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_d47a1f5e850a` | assignment | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_d485c564824e` | call_site | `third_party/libuv/src/unix/poll.c:135` | `uv__poll_stop(handle);` |
| `ev_d49198b19d93` | call_site | `third_party/libuv/src/threadpool.c:228` | `if (uv_sem_init(&sem, 0))` |
| `ev_d49b8d363cb4` | call_site | `third_party/libuv/src/unix/signal.c:478` | `handle->signal_cb(handle, handle->signum);` |
| `ev_d49c8b47d3f0` | call_site | `third_party/libuv/src/unix/stream.c:810` | `while (n == -1 && errno == EINTR);` |
| `ev_d4c708994794` | call_site | `third_party/libuv/src/unix/stream.c:386` | `uv__close(fds[0]);` |
| `ev_d50a528d166e` | call_site | `third_party/libuv/src/threadpool.c:201` | `val = getenv("UV_THREADPOOL_SIZE");` |
| `ev_d534de3458da` | call_site | `third_party/libuv/src/fs-poll.c:197` | `if (!uv_is_active((uv_handle_t*)handle) \|\| uv__is_closing(handle))` |
| `ev_d53598a463b9` | call_site | `third_party/libuv/src/unix/udp.c:83` | `uv__udp_run_completed(handle);` |
| `ev_d539e9f39d97` | call_site | `third_party/libuv/src/unix/tty.c:182` | `if (uv__tty_is_slave(fd) && ttyname_r(fd, path, sizeof(path)) == 0)` |
| `ev_d55238e49819` | call_site | `third_party/libuv/src/unix/udp.c:1313` | `r = sendmsg_x(fd, m, n, MSG_DONTWAIT);` |
| `ev_d562fcabe124` | call_site | `third_party/libuv/src/unix/async.c:148` | `sched_yield();` |
| `ev_d574494814cb` | call_site | `third_party/libuv/src/unix/fs.c:2199` | `PATH;` |
| `ev_d57f2ac9f710` | call_site | `third_party/libuv/src/unix/fsevents.c:628` | `if (pthread_attr_init(&attr))` |
| `ev_d5868fb8b040` | call_site | `third_party/libuv/src/unix/signal.c:413` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_d5ae787393b9` | call_site | `third_party/libuv/src/unix/tty.c:196` | `r = uv__dup2_cloexec(newfd, fd);` |
| `ev_d5c23a2f7c40` | call_site | `third_party/libuv/src/unix/stream.c:87` | `uv__handle_init(loop, (uv_handle_t*)stream, type);` |
| `ev_d5fdcab2928b` | call_site | `third_party/libuv/src/unix/core.c:1159` | `err = uv__cloexec(newfd, 1);` |
| `ev_d612ed3a00de` | call_site | `third_party/libuv/src/timer.c:171` | `uv__queue_init(&ready_queue);` |
| `ev_d65b1d798a0a` | call_site | `third_party/libuv/src/unix/poll.c:126` | `assert(!uv__is_closing(handle));` |
| `ev_d6695971175f` | call_site | `third_party/libuv/src/unix/udp.c:666` | `memset(&mreq, 0, sizeof mreq);` |
| `ev_d68b49cbe223` | call_site | `third_party/libuv/src/fs-poll.c:111` | `uv__free(ctx);` |
| `ev_d6954cdf136e` | call_site | `third_party/libuv/src/unix/fsevents.c:719` | `pCFRunLoopRun();` |
| `ev_d69a3c8d4056` | call_site | `third_party/libuv/src/unix/stream.c:1066` | `while (nread < 0 && errno == EINTR);` |
| `ev_d6ae98204bba` | call_site | `third_party/libuv/src/unix/kqueue.c:199` | `assert(w->fd >= 0);` |
| `ev_d6ef2b43e075` | call_site | `third_party/libuv/src/unix/kqueue.c:253` | `assert(timeout >= -1);` |
| `ev_d6fe3495ec3c` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:164` | `uv__thread_setname(title);  /* Don't care if it fails. */` |
| `ev_d70af4f70ff0` | call_site | `third_party/libuv/src/unix/pipe.c:42` | `return NULL != memchr(s, '\0', n);` |
| `ev_d715863dffdf` | call_site | `third_party/libuv/src/unix/stream.c:1017` | `uv__close(fd);` |
| `ev_d72f0beb12e3` | call_site | `third_party/libuv/src/unix/udp.c:955` | `err = uv_ip6_addr(multicast_addr, 0, &mcast_addr.in6);` |
| `ev_d7416e722897` | call_site | `third_party/libuv/src/unix/tty.c:297` | `return UV__ERR(errno);` |
| `ev_d789673fac13` | call_site | `third_party/libuv/src/unix/udp.c:478` | `} while (err == -1 && errno == EINTR);` |
| `ev_d78995402e2b` | call_site | `third_party/libuv/src/unix/fs.c:1996` | `req->path = uv__strdup(tpl);` |
| `ev_d7a51c466740` | call_site | `third_party/libuv/src/uv-common.c:560` | `while (!uv__queue_empty(&queue)) {` |
| `ev_d7b8bce3c1e1` | assignment | `third_party/libuv/src/threadpool.c:299` | `w->work = uv__cancelled;` |
| `ev_d7bc311e09c9` | call_site | `third_party/libuv/src/unix/async.c:251` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK)` |
| `ev_d7d6d231c7cb` | call_site | `third_party/libuv/src/unix/signal.c:477` | `assert(!(handle->flags & UV_HANDLE_CLOSING));` |
| `ev_d7e1459ebd63` | call_site | `third_party/libuv/src/unix/core.c:962` | `uv__queue_init(&w->watcher_queue);` |
| `ev_d7ea4f1875c6` | assignment | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_d7f53099005b` | call_site | `third_party/libuv/src/unix/core.c:1595` | `r = getpriority(PRIO_PROCESS, (int) pid);` |
| `ev_d7fd407ee823` | call_site | `third_party/libuv/src/unix/thread.c:439` | `abort();` |
| `ev_d80a543af3a2` | call_site | `third_party/libuv/src/unix/udp.c:1358` | `if (uv__queue_empty(&handle->write_queue))` |
| `ev_d8190b0a3fa4` | call_site | `third_party/libuv/src/unix/core.c:1707` | `return UV__ERR(errno);` |
| `ev_d8601a909eda` | call_site | `third_party/libuv/src/unix/core.c:1991` | `if (0 == sysctlbyname(mib[i], &nprocs, &len, NULL, 0) &&` |
| `ev_d86096e66b8e` | call_site | `third_party/libuv/src/unix/async.c:254` | `abort();` |
| `ev_d8abfe6e9b3e` | call_site | `third_party/libuv/src/unix/signal.c:566` | `assert(ret == 0);` |
| `ev_d8cc95480d02` | call_site | `third_party/libuv/src/unix/fs.c:1722` | `X(FSTAT, uv__fs_fstat(req->file, &req->statbuf));` |
| `ev_d8df992433b9` | call_site | `third_party/libuv/src/unix/process.c:817` | `sigdelset(&signewset, SIGKILL);` |
| `ev_d8f3da621bae` | call_site | `third_party/libuv/src/unix/thread.c:795` | `if (pthread_mutex_destroy(&mutex))` |
| `ev_d92622f525a0` | call_site | `third_party/libuv/src/unix/fsevents.c:631` | `if (pthread_attr_setstacksize(&attr, uv__thread_stack_size()))` |
| `ev_d92e76f5f045` | call_site | `third_party/libuv/src/unix/core.c:1066` | `mach_port_deallocate(mach_task_self(), thread);` |
| `ev_d96996a4e23e` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:128` | `*(void **)(&pLSApplicationCheckIn) = pCFBundleGetFunctionPointerForName(` |
| `ev_d980178ead5f` | call_site | `third_party/libuv/src/uv-common.c:1046` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_d98c185e6143` | call_site | `third_party/libuv/src/unix/thread.c:165` | `min_stack_size = uv__min_stack_size();` |
| `ev_d991d8e355d5` | call_site | `third_party/libuv/src/unix/fsevents.c:883` | `err = uv__cf_loop_signal(handle->loop, handle, kUVCFLoopSignalClosing);` |
| `ev_d99e3c81372e` | call_site | `third_party/libuv/src/unix/stream.c:1558` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_d9a9fd904f3b` | call_site | `third_party/libuv/src/unix/tcp.c:195` | `errno = 0;` |
| `ev_d9b48b296894` | call_site | `third_party/libuv/src/unix/stream.c:262` | `uv_sem_post(&s->async_sem);` |
| `ev_d9b775c1b739` | call_site | `third_party/libuv/src/uv-common.c:564` | `uv__queue_remove(q);` |
| `ev_d9b8a14b214b` | call_site | `third_party/libuv/src/unix/random-devurandom.c:44` | `uv__close(fd);` |
| `ev_d9c72db34f59` | call_site | `third_party/libuv/src/unix/loop.c:173` | `uv__close(loop->emfile_fd);` |
| `ev_d9f9e99c55da` | call_site | `third_party/libuv/src/unix/core.c:971` | `else if (uv__queue_empty(&w->watcher_queue))` |
| `ev_da01fa43084d` | call_site | `third_party/libuv/src/unix/fs.c:1968` | `PATH2;` |
| `ev_da237cbf0f37` | call_site | `third_party/libuv/src/thread-common.c:134` | `assert(b->in == 0);` |
| `ev_da2ea4bec452` | call_site | `third_party/libuv/src/unix/process.c:176` | `assert(uv__queue_empty(&pending));` |
| `ev_da3813cceef7` | assignment | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_da52e95b1bb8` | call_site | `third_party/libuv/src/unix/loop.c:145` | `err = uv__signal_loop_fork(loop);` |
| `ev_da53b740ac75` | call_site | `third_party/libuv/src/unix/signal.c:174` | `handle = RB_NFIND(uv__signal_tree_s, &uv__signal_tree, &lookup);` |
| `ev_da55ccdc0657` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:102` | `pCFBundleGetFunctionPointerForName(launch_services_bundle,` |
| `ev_da63896531df` | call_site | `third_party/libuv/src/unix/fsevents.c:428` | `uv__fsevents_destroy_stream(state);` |
| `ev_da951e41c57b` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_daaa2020b0fc` | call_site | `third_party/libuv/src/unix/kqueue.c:270` | `uv__metrics_set_provider_entry_time(loop);` |
| `ev_dab34f097b37` | call_site | `third_party/libuv/src/unix/udp.c:1206` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, 0);` |
| `ev_dab5e2f2d7dd` | call_site | `third_party/libuv/src/unix/stream.c:430` | `return UV__ERR(errno);` |
| `ev_dabbca8c91ef` | call_site | `third_party/libuv/src/uv-common.c:893` | `memset(loop, -1, sizeof(*loop));` |
| `ev_dabc52a0c57b` | call_site | `third_party/libuv/src/unix/tcp.c:132` | `err = new_socket(tcp, domain, 0);` |
| `ev_dabc8bf7594d` | call_site | `third_party/libuv/src/unix/loop.c:65` | `uv__queue_init(&loop->pending_queue);` |
| `ev_dabd12372cbc` | call_site | `third_party/libuv/src/fs-poll.c:232` | `if (uv_timer_start(&ctx->timer_handle, timer_cb, interval, 0))` |
| `ev_daf39f5f68c4` | call_site | `third_party/libuv/src/unix/proctitle.c:105` | `len = strlen(title);` |
| `ev_db04d5f16aeb` | call_site | `third_party/libuv/src/unix/process.c:350` | `n = uv__cloexec(use_fd, 0);` |
| `ev_db1b42d2dadc` | call_site | `third_party/libuv/src/unix/process.c:394` | `if (sigprocmask(SIG_SETMASK, &signewset, NULL) != 0)` |
| `ev_db260f3c2fdf` | call_site | `third_party/libuv/src/unix/getnameinfo.c:117` | `uv__getnameinfo_work(&req->work_req);` |
| `ev_db51894a5d1d` | call_site | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_db68e296a675` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:214` | `uv__getaddrinfo_done(&req->work_req, 0);` |
| `ev_db7c97e01602` | call_site | `third_party/libuv/src/unix/fsevents.c:554` | `V(core_services_handle, FSEventStreamCreate);` |
| `ev_db8b7d85c4a3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_db9a1edb20f6` | call_site | `third_party/libuv/src/unix/thread.c:818` | `errno = 0;` |
| `ev_db9b394ad04d` | call_site | `third_party/libuv/src/unix/core.c:1436` | `for (i = 0; environ[i] != NULL; i++);` |
| `ev_dbd96d75b158` | call_site | `third_party/libuv/src/unix/stream.c:1532` | `uv__io_close(handle->loop, &handle->io_watcher);` |
| `ev_dbfcab4bbeda` | call_site | `third_party/libuv/src/unix/fsevents.c:208` | `uv_mutex_unlock(&handle->cf_mutex);` |
| `ev_dc2253994514` | call_site | `third_party/libuv/src/unix/signal.c:61` | `uv__signal_compare)` |
| `ev_dc2430bb0546` | call_site | `third_party/libuv/src/unix/core.c:1594` | `errno = 0;` |
| `ev_dc428e004347` | assignment | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_dc43525b117d` | call_site | `third_party/libuv/src/unix/stream.c:1264` | `getsockopt(uv__stream_fd(stream),` |
| `ev_dc4bcbd12d70` | call_site | `third_party/libuv/src/unix/stream.c:1090` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_dc75e83d673c` | call_site | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_dc76621ba905` | call_site | `third_party/libuv/src/threadpool.c:116` | `uv_cond_signal(&cond);` |
| `ev_dc7cf7fd7b36` | call_site | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_dc87f5ae3010` | assignment | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_dcaa098ad947` | call_site | `third_party/libuv/src/unix/core.c:952` | `assert(w->fd >= 0);` |
| `ev_dcbb581b1c53` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:138` | `S("_LSSetApplicationLaunchServicesServerConnectionStatus"));` |
| `ev_dcd84d97a726` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:95` | `*addresses = uv__calloc(*count, sizeof(**addresses));` |
| `ev_dd04761d29b8` | call_site | `third_party/libuv/src/unix/stream.c:194` | `if (FD_ISSET(s->int_fd, s->sread))` |
| `ev_dd189c9138d2` | call_site | `third_party/libuv/src/fs-poll.c:145` | `if (!uv_is_active((uv_handle_t*)handle)) {` |
| `ev_dd1dcc2f289b` | call_site | `third_party/libuv/src/unix/fs.c:1823` | `PATH;` |
| `ev_dd23fb7e60bf` | call_site | `third_party/libuv/src/unix/core.c:1092` | `fd = open(path, flags \| O_CLOEXEC);` |
| `ev_dd4a9ef4cc5d` | call_site | `third_party/libuv/src/unix/fsevents.c:510` | `pthread_mutex_lock(&global_init_mutex);` |
| `ev_dd5ae7911c0a` | call_site | `third_party/libuv/src/unix/fsevents.c:811` | `uv__queue_init(&handle->cf_events);` |
| `ev_dd626872b911` | call_site | `third_party/libuv/src/unix/udp.c:1378` | `uv__queue_remove(&req->queue);` |
| `ev_dd666cf67398` | call_site | `third_party/libuv/src/unix/tcp.c:300` | `if (uv__is_ipv6_link_local(addr)) {` |
| `ev_ddb5b2e6b65a` | call_site | `third_party/libuv/src/unix/fs.c:1112` | `r = sendfile(in_fd, out_fd, req->off, &len, NULL, 0);` |
| `ev_ddc5cbe49251` | call_site | `third_party/libuv/src/unix/udp.c:185` | `nread = recvmsg_x(handle->io_watcher.fd, msgs, chunks, MSG_DONTWAIT);` |
| `ev_ddf4ae2f1396` | call_site | `third_party/libuv/src/fs-poll.c:124` | `assert(ctx->parent_handle == handle);` |
| `ev_ddfddf517263` | call_site | `third_party/libuv/src/unix/fs.c:585` | `n = scandir(req->path, &dents, uv__fs_scandir_filter, uv__fs_scandir_sort);` |
| `ev_de07f5091653` | call_site | `third_party/libuv/src/idna.c:375` | `code_point = uv__wtf8_decode1(&source_ptr);` |
| `ev_de10b01f8130` | call_site | `third_party/libuv/src/unix/core.c:1816` | `return UV__ERR(errno);` |
| `ev_de1ce1f89058` | call_site | `third_party/libuv/src/threadpool.c:260` | `abort();` |
| `ev_de3a14facd37` | call_site | `third_party/libuv/src/unix/core.c:1308` | `memcpy(pwd->username, pw.pw_name, name_size);` |
| `ev_de4d7aa9f85a` | call_site | `third_party/libuv/src/unix/core.c:480` | `r = uv__loop_alive(loop);` |
| `ev_de76c6d228d4` | call_site | `third_party/libuv/src/unix/signal.c:358` | `return uv__signal_start(handle, signal_cb, signum, 0);` |
| `ev_de941d25ac14` | call_site | `third_party/libuv/src/unix/tcp.c:180` | `if (setsockopt(tcp->io_watcher.fd,` |
| `ev_decace04d316` | call_site | `third_party/libuv/src/unix/core.c:183` | `uv__prepare_close((uv_prepare_t*)handle);` |
| `ev_ded0ab7c4a90` | call_site | `third_party/libuv/src/unix/udp.c:669` | `err = uv_inet_pton(AF_INET, interface_addr, &mreq.imr_interface.s_addr);` |
| `ev_dee20cff60e7` | call_site | `third_party/libuv/src/threadpool.c:110` | `uv__queue_init(q);` |
| `ev_dee784303ee8` | call_site | `third_party/libuv/src/unix/udp.c:767` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, UV_UDP_REUSEADDR);` |
| `ev_dee788a63b0e` | call_site | `third_party/libuv/src/unix/tcp.c:416` | `uv_close((uv_handle_t*) handle, close_cb);` |
| `ev_df005a1d2457` | call_site | `third_party/libuv/src/unix/process.c:154` | `q = uv__queue_head(h);` |
| `ev_df2040900d3d` | call_site | `third_party/libuv/src/unix/fsevents.c:827` | `uv_unref((uv_handle_t*) handle->cf_cb);` |
| `ev_df9758321799` | call_site | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_dfb7c33d0b80` | call_site | `third_party/libuv/src/unix/darwin.c:102` | `if (host_statistics(mach_host_self(), HOST_VM_INFO,` |
| `ev_dfce5deff2e2` | call_site | `third_party/libuv/src/uv-common.c:674` | `required_len = strlen(handle->path);` |
| `ev_dfd30a980cde` | call_site | `third_party/libuv/src/unix/core.c:456` | `timeout = uv__backend_timeout(loop);` |
| `ev_dfdafa4552b5` | call_site | `third_party/libuv/src/unix/fsevents.c:698` | `pCFRelease(state->signal_source);` |
| `ev_dff7b04b3524` | call_site | `third_party/libuv/src/unix/stream.c:582` | `assert(queued_fds->offset > 0);` |
| `ev_dffce2460e6b` | call_site | `third_party/libuv/src/unix/stream.c:1472` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_e010032cdcba` | call_site | `third_party/libuv/src/unix/udp.c:402` | `if (setsockopt(fd, IPPROTO_IPV6, IPV6_V6ONLY, &yes, sizeof yes) == -1) {` |
| `ev_e05e77ba98fc` | call_site | `third_party/libuv/src/unix/core.c:1477` | `uv__free(*envitems);` |
| `ev_e06579cbe923` | call_site | `third_party/libuv/src/unix/core.c:441` | `uv__update_time(loop);` |
| `ev_e07a8584df14` | call_site | `third_party/libuv/src/uv-common.c:1049` | `idle_time += uv_hrtime() - entry_time;` |
| `ev_e08afc74a112` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:173` | `service_len = service ? strlen(service) + 1 : 0;` |
| `ev_e094c3ad9cf7` | call_site | `third_party/libuv/src/unix/tcp.c:650` | `return UV__ERR(errno);` |
| `ev_e0af3a4100a0` | call_site | `third_party/libuv/src/uv-common.c:257` | `addr->sin_port = htons(port);` |
| `ev_e0fee20d38e0` | call_site | `third_party/libuv/src/uv-common.c:98` | `return uv__allocator.local_realloc(ptr, size);` |
| `ev_e119d0a7b836` | call_site | `third_party/libuv/src/unix/stream.c:1118` | `err = uv__stream_recv_cmsg(stream, &msg);` |
| `ev_e12fdcba4223` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_e13efcc4d406` | call_site | `third_party/libuv/src/unix/core.c:1550` | `len = strlen(buf);` |
| `ev_e13f690b8a80` | call_site | `third_party/libuv/src/unix/fs.c:703` | `stat_fs = uv__malloc(sizeof(*stat_fs));` |
| `ev_e1623ccde874` | call_site | `third_party/libuv/src/unix/pipe.c:125` | `memset(&saddr, 0, sizeof saddr);` |
| `ev_e17c426826df` | call_site | `third_party/libuv/src/unix/fs.c:1308` | `err = UV__ERR(errno);` |
| `ev_e1845059efb0` | call_site | `third_party/libuv/src/unix/core.c:2020` | `rc = sysconf(_SC_NPROCESSORS_ONLN);` |
| `ev_e1a0d7948334` | call_site | `third_party/libuv/src/unix/pipe.c:146` | `uv__free(pipe_fname);` |
| `ev_e1d2855e867a` | call_site | `third_party/libuv/src/unix/signal.c:377` | `assert(!uv__is_closing(handle));` |
| `ev_e20f03658f5a` | call_site | `third_party/libuv/src/unix/signal.c:531` | `assert(!uv__is_closing(handle));` |
| `ev_e22a81e77b42` | call_site | `third_party/libuv/src/unix/fsevents.c:558` | `V(core_services_handle, FSEventStreamStart);` |
| `ev_e238f71022b7` | call_site | `third_party/libuv/src/unix/core.c:442` | `uv__run_timers(loop);` |
| `ev_e2416169733b` | call_site | `third_party/libuv/src/unix/async.c:198` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_e246fdedc165` | call_site | `third_party/libuv/src/unix/process.c:941` | `assert(err == *pid);` |
| `ev_e2476d7128eb` | call_site | `third_party/libuv/src/unix/proctitle.c:155` | `uv__free(args_mem);  /* Keep valgrind happy. */` |
| `ev_e24881a2ea4c` | call_site | `third_party/libuv/src/unix/fs.c:2273` | `uv__fs_readdir_cleanup(req);` |
| `ev_e25a6ba620bf` | call_site | `third_party/libuv/src/unix/tty.c:290` | `fd = uv__stream_fd(tty);` |
| `ev_e261bff047ce` | call_site | `third_party/libuv/src/unix/fsevents.c:487` | `uv__fsevents_push_event(curr, NULL, err);` |
| `ev_e28abeefea5b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:130` | `S("_LSApplicationCheckIn"));` |
| `ev_e308d3749e24` | call_site | `third_party/libuv/src/unix/fsevents.c:882` | `assert(handle != NULL);` |
| `ev_e309ebfd33e4` | call_site | `third_party/libuv/src/unix/fsevents.c:298` | `pos = strchr(path + 1, '/');` |
| `ev_e34d2661654d` | call_site | `third_party/libuv/src/unix/stream.c:1553` | `uv__close(queued_fds->fds[i]);` |
| `ev_e3543af49f75` | call_site | `third_party/libuv/src/unix/signal.c:275` | `uv__io_start(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_e3559fad69eb` | call_site | `third_party/libuv/src/unix/fs.c:2313` | `PATH;` |
| `ev_e3622bace295` | call_site | `third_party/libuv/src/unix/thread.c:373` | `err = pthread_mutex_trylock(mutex);` |
| `ev_e375559df85a` | call_site | `third_party/libuv/src/unix/poll.c:50` | `handle->poll_cb(handle, UV_EBADF, 0);` |
| `ev_e37a559f3603` | call_site | `third_party/libuv/src/unix/thread.c:116` | `lim.rlim_cur -= lim.rlim_cur % (rlim_t) getpagesize();` |
| `ev_e39b436dd838` | call_site | `third_party/libuv/src/unix/fsevents.c:317` | `uv__queue_insert_tail(&head, &event->member);` |
| `ev_e3ae11ec3a59` | call_site | `third_party/libuv/src/unix/darwin.c:61` | `uv_once(&once, uv__hrtime_init_once);` |
| `ev_e3b1fc76bcfc` | call_site | `third_party/libuv/src/unix/core.c:1008` | `return UV__ERR(errno);` |
| `ev_e3bca43bbc2d` | call_site | `third_party/libuv/src/unix/fs.c:2283` | `uv__free(req->ptr);` |
| `ev_e40155d4eb70` | call_site | `third_party/libuv/src/unix/core.c:1225` | `CHECK_ENV_VAR("TEMPDIR");` |
| `ev_e42091574791` | call_site | `third_party/libuv/src/unix/tty.c:374` | `err = ioctl(uv__stream_fd(tty), TIOCGWINSZ, &ws);` |
| `ev_e48d006f50da` | call_site | `third_party/libuv/src/unix/process.c:793` | `assert(err != ENOSYS);` |
| `ev_e4ac5b38f4be` | call_site | `third_party/libuv/src/unix/fsevents.c:198` | `assert(events != NULL \|\| err != 0);` |
| `ev_e4c24b643b61` | call_site | `third_party/libuv/src/unix/core.c:919` | `assert(0 != events);` |
| `ev_e4c4b5c0b227` | call_site | `third_party/libuv/src/unix/udp.c:796` | `return UV__ERR(errno);` |
| `ev_e4c9dc60e008` | call_site | `third_party/libuv/src/unix/signal.c:465` | `abort();` |
| `ev_e4cafe2eebda` | call_site | `third_party/libuv/src/unix/stream.c:909` | `uv__queue_move(&stream->write_completed_queue, &pq);` |
| `ev_e4d0c8d90256` | call_site | `third_party/libuv/src/unix/udp.c:527` | `memset(&addr, 0, sizeof(addr));` |
| `ev_e4edc448ccac` | call_site | `third_party/libuv/src/unix/darwin.c:83` | `abspath_size = strlen(abspath);` |
| `ev_e4fdef658627` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:78` | `dlsym(core_foundation_handle, "CFStringCreateWithCString");` |
| `ev_e536beb3b044` | call_site | `third_party/libuv/src/uv-common.c:88` | `uv__allocator.local_free(ptr);` |
| `ev_e539607ea3c4` | call_site | `third_party/libuv/src/threadpool.c:325` | `q = uv__queue_head(&wq);` |
| `ev_e56ad485e290` | call_site | `third_party/libuv/src/unix/udp.c:131` | `if (!uv__io_active(&handle->io_watcher, POLLIN))` |
| `ev_e572759def4a` | call_site | `third_party/libuv/src/unix/pipe.c:304` | `r = connect(uv__stream_fd(handle), (struct sockaddr*)&saddr, addrlen);` |
| `ev_e5736bdf88e3` | call_site | `third_party/libuv/src/uv-common.c:513` | `return uv__udp_try_send(handle, bufs, nbufs, addr, addrlen);` |
| `ev_e57715436254` | call_site | `third_party/libuv/src/unix/stream.c:1494` | `assert(handle->type == UV_TCP \|\|` |
| `ev_e5c6797d395a` | call_site | `third_party/libuv/src/unix/stream.c:457` | `assert(stream->flags & UV_HANDLE_CLOSED);` |
| `ev_e5d92615b65f` | call_site | `third_party/libuv/src/unix/fs.c:1261` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_e600382b122b` | call_site | `third_party/libuv/src/unix/async.c:168` | `assert(w == &loop->async_io_watcher);` |
| `ev_e6039e9e0b66` | call_site | `third_party/libuv/src/uv-common.c:214` | `default: snprintf(buf, buflen, "Unknown system error %d", err);` |
| `ev_e60690493e4f` | call_site | `third_party/libuv/src/threadpool.c:130` | `uv_mutex_unlock(&w->loop->wq_mutex);` |
| `ev_e62a5d70cd10` | call_site | `third_party/libuv/src/unix/fsevents.c:458` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_e6472c7d418c` | assignment | `third_party/libuv/src/unix/tcp.c:447` | `tcp->io_watcher.cb = uv__server_io;` |
| `ev_e65471c64fc6` | assignment | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_e68d0644ff36` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:129` | `assert(req->retcode == 0);` |
| `ev_e699bd5397f4` | call_site | `third_party/libuv/src/unix/kqueue.c:59` | `uv__cloexec(loop->backend_fd, 1);` |
| `ev_e6bb8533cb11` | call_site | `third_party/libuv/src/unix/stream.c:1006` | `memcpy(&fd, p, sizeof(fd));` |
| `ev_e6d0259e7006` | call_site | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_e6e427366243` | call_site | `third_party/libuv/src/unix/thread.c:160` | `stack_size = uv__thread_stack_size();` |
| `ev_e6e4340ec169` | call_site | `third_party/libuv/src/unix/fsevents.c:243` | `uv__queue_init(&head);` |
| `ev_e6f42e853812` | call_site | `third_party/libuv/src/unix/process.c:989` | `pipes = uv__malloc(stdio_count * sizeof(*pipes));` |
| `ev_e70c838ebb27` | call_site | `third_party/libuv/src/unix/tcp.c:601` | `if (uv__stream_fd(handle) != -1) {` |
| `ev_e717033a79f7` | call_site | `third_party/libuv/src/unix/process.c:552` | `err = posix_spawn_fncs->file_actions.addchdir_np(actions, options->cwd);` |
| `ev_e74876777124` | call_site | `third_party/libuv/src/unix/udp.c:923` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, UV_UDP_REUSEADDR);` |
| `ev_e75627e716d7` | call_site | `third_party/libuv/src/unix/darwin.c:173` | `if (sysctl(which, ARRAY_SIZE(which), &info, &size, NULL, 0))` |
| `ev_e75d69e30220` | call_site | `third_party/libuv/src/unix/core.c:258` | `r = getsockopt(fd, SOL_SOCKET, optname, value, &len);` |
| `ev_e768d308c774` | call_site | `third_party/libuv/src/unix/process.c:238` | `uv__nonblock(pipefds[0], 1);` |
| `ev_e77f14d51879` | call_site | `third_party/libuv/src/unix/stream.c:906` | `if (uv__queue_empty(&stream->write_completed_queue))` |
| `ev_e7ad50b09c69` | call_site | `third_party/libuv/src/idna.c:434` | `code_point = uv__get_surrogate_value(w_source_ptr, w_source_len);` |
| `ev_e7ade02159ec` | call_site | `third_party/libuv/src/unix/kqueue.c:649` | `uv__close(handle->event_watcher.fd);` |
| `ev_e7b285aadff2` | call_site | `third_party/libuv/src/unix/udp.c:774` | `err = uv_inet_pton(AF_INET, interface_addr, &mreq.imr_interface.s_addr);` |
| `ev_e7b5999f13d5` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:90` | `assert(!"unknown EAI_* error code");` |
| `ev_e7bca5df2fd0` | call_site | `third_party/libuv/src/uv-common.c:1020` | `now = uv_hrtime();` |
| `ev_e7bed57bb6ec` | call_site | `third_party/libuv/src/unix/tcp.c:478` | `if (setsockopt(fd, SOL_SOCKET, SO_KEEPALIVE, &on, sizeof(on)))` |
| `ev_e7c93fafb96c` | call_site | `third_party/libuv/src/threadpool.c:225` | `uv__queue_init(&slow_io_pending_wq);` |
| `ev_e7f42bdec3e0` | call_site | `third_party/libuv/src/unix/poll.c:81` | `err = uv__nonblock(fd, 1);` |
| `ev_e80a281682d1` | call_site | `third_party/libuv/src/unix/fs.c:2199` | `PATH;` |
| `ev_e83b58191254` | call_site | `third_party/libuv/src/unix/tcp.c:455` | `if (setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &on, sizeof(on)))` |
| `ev_e8484abefa64` | call_site | `third_party/libuv/src/threadpool.c:360` | `uv__req_unregister(req->loop);` |
| `ev_e84ff2638b56` | call_site | `third_party/libuv/src/unix/udp.c:1002` | `return UV__ERR(errno);` |
| `ev_e864892a0d91` | call_site | `third_party/libuv/src/unix/stream.c:428` | `errno != ENOTSOCK &&` |
| `ev_e88d9afa7f1e` | call_site | `third_party/libuv/src/threadpool.c:144` | `uv_mutex_lock(&mutex);` |
| `ev_e8a0eb28563a` | call_site | `third_party/libuv/src/unix/udp.c:107` | `uv__req_unregister(handle->loop);` |
| `ev_e8de2944e3c7` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:162` | `uv__free(addresses);` |
| `ev_e8e2376e295b` | call_site | `third_party/libuv/src/unix/fs.c:2313` | `PATH;` |
| `ev_e8f51a24747f` | call_site | `third_party/libuv/src/unix/core.c:1911` | `memcpy(buf, abspath, *buflen);` |
| `ev_e8f65fd2bb12` | call_site | `third_party/libuv/src/unix/core.c:662` | `return UV__ERR(errno);` |
| `ev_e8f7befb4b22` | call_site | `third_party/libuv/src/unix/core.c:1475` | `uv__free(envitem->name);` |
| `ev_e8fb6ae744c8` | call_site | `third_party/libuv/src/unix/fs.c:2084` | `PATH;` |
| `ev_e91ed7bc9a81` | call_site | `third_party/libuv/src/unix/core.c:1224` | `CHECK_ENV_VAR("TEMP");` |
| `ev_e929c5af5f49` | call_site | `third_party/libuv/src/unix/udp.c:172` | `memset(&msgs[k].msg_hdr, 0, sizeof(msgs[k].msg_hdr));` |
| `ev_e938e6848aa3` | call_site | `third_party/libuv/src/unix/fsevents.c:680` | `abort();` |
| `ev_e9763bab607f` | call_site | `third_party/libuv/src/unix/fs.c:1968` | `PATH2;` |
| `ev_e985f0370341` | call_site | `third_party/libuv/src/unix/udp.c:968` | `err = uv_ip4_addr(source_addr, 0, &src_addr.in);` |
| `ev_e9921f6a963f` | call_site | `third_party/libuv/src/unix/stream.c:460` | `uv__req_unregister(stream->loop);` |
| `ev_e9ac4dbaf0c8` | call_site | `third_party/libuv/src/unix/core.c:270` | `assert(!(handle->flags & UV_HANDLE_CLOSED));` |
| `ev_e9b3073756a2` | call_site | `third_party/libuv/src/unix/process.c:356` | `fd = dup2(use_fd, fd);` |
| `ev_e9f83b888ca3` | call_site | `third_party/libuv/src/unix/signal.c:89` | `uv__close(uv__signal_lock_pipefd[0]);` |
| `ev_ea1ce297616f` | assignment | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_ea1e7036fb81` | call_site | `third_party/libuv/src/unix/stream.c:1278` | `if (error < 0 \|\| uv__queue_empty(&stream->write_queue)) {` |
| `ev_ea3df173b246` | call_site | `third_party/libuv/src/unix/process.c:159` | `uv__queue_remove(&process->queue);` |
| `ev_ea55b7d1dd22` | call_site | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_ea6049b9893c` | call_site | `third_party/libuv/src/unix/process.c:210` | `fd = uv__stream_fd(container->data.stream);` |
| `ev_ea716ea2ec06` | assignment | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_ea82f8dc73cd` | call_site | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_ea91f24c2a91` | call_site | `third_party/libuv/src/unix/core.c:575` | `return UV__ERR(errno);` |
| `ev_eab3a763ae82` | call_site | `third_party/libuv/src/unix/fs.c:571` | `return strcmp(dent->d_name, ".") != 0 && strcmp(dent->d_name, "..") != 0;` |
| `ev_eac021df7f14` | call_site | `third_party/libuv/src/unix/stream.c:1086` | `if (errno == EAGAIN \|\| errno == EWOULDBLOCK) {` |
| `ev_eac65dad1a55` | call_site | `third_party/libuv/src/unix/udp.c:255` | `memset(&h, 0, sizeof(h));` |
| `ev_ead793d1052c` | call_site | `third_party/libuv/src/unix/stream.c:1101` | `stream->read_cb(stream, UV__ERR(errno), &buf);` |
| `ev_ead7a451be87` | call_site | `third_party/libuv/src/unix/udp.c:1167` | `assert(0 && "unexpected address family");` |
| `ev_eaede467bfd9` | call_site | `third_party/libuv/src/unix/fs.c:2084` | `PATH;` |
| `ev_eb09084eed64` | assignment | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_eb16e34c0c31` | call_site | `third_party/libuv/src/unix/stream.c:251` | `uv__stream_io(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_eb17e2273625` | call_site | `third_party/libuv/src/threadpool.c:95` | `if (slow_io_work_running >= slow_work_thread_threshold()) {` |
| `ev_eb2068a865ca` | call_site | `third_party/libuv/src/unix/fs.c:1628` | `ret = uv__fstat(fd, &pbuf);` |
| `ev_eb46ba8a9e94` | call_site | `third_party/libuv/src/unix/core.c:847` | `uv__queue_move(&loop->pending_queue, &pq);` |
| `ev_eb5516713c27` | call_site | `third_party/libuv/src/unix/thread.c:907` | `strncpy(namebuf, name, sizeof(namebuf) - 1);` |
| `ev_eb5c515c4f3d` | call_site | `third_party/libuv/src/unix/process.c:440` | `if (3 != sscanf_l(buf, NULL, "%u.%u.%u", &major, &minor, &patch))` |
| `ev_eb71c046c68d` | call_site | `third_party/libuv/src/unix/tcp.c:256` | `if (getifaddrs(&ifa))` |
| `ev_eb75bd037683` | call_site | `third_party/libuv/src/unix/udp.c:1027` | `if (setsockopt(handle->io_watcher.fd,` |
| `ev_eb8ef49dfd38` | call_site | `third_party/libuv/src/unix/stream.c:792` | `assert(fd_to_send >= 0);` |
| `ev_ebf6d5a889f1` | call_site | `third_party/libuv/src/unix/fsevents.c:619` | `memset(&ctx, 0, sizeof(ctx));` |
| `ev_ebf6dd43e814` | call_site | `third_party/libuv/src/unix/fsevents.c:717` | `uv_sem_post(&loop->cf_sem);` |
| `ev_ebfb552afe5a` | call_site | `third_party/libuv/src/unix/core.c:1120` | `assert(len > 0);` |
| `ev_ec06fd9d8252` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:82` | `dlsym(core_foundation_handle, "CFBundleGetDataPointerForName");` |
| `ev_ec1e3539f6bb` | call_site | `third_party/libuv/src/unix/kqueue.c:468` | `assert(timeout > 0);` |
| `ev_ec209930b389` | call_site | `third_party/libuv/src/unix/stream.c:1251` | `assert(stream->type == UV_TCP \|\| stream->type == UV_NAMED_PIPE);` |
| `ev_ec5038cf9114` | call_site | `third_party/libuv/src/unix/core.c:1396` | `assert(gr_mem == (char*)grp->members + mem_size);` |
| `ev_ec6d52a9c2a8` | call_site | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_ec9679f03cf1` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_ecaf00635ad9` | call_site | `third_party/libuv/src/unix/kqueue.c:332` | `assert(loop->watchers != NULL);` |
| `ev_ecc849e922a7` | call_site | `third_party/libuv/src/unix/fsevents.c:374` | `pFSEventStreamRelease(ref);` |
| `ev_ecc8fcb91523` | call_site | `third_party/libuv/src/threadpool.c:286` | `uv_mutex_lock(&mutex);` |
| `ev_ecde99fe2d17` | call_site | `third_party/libuv/src/unix/signal.c:424` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_ece7d55feb91` | call_site | `third_party/libuv/src/unix/fsevents.c:656` | `uv_sem_destroy(&state->fsevent_sem);` |
| `ev_ecf6dfb44c04` | call_site | `third_party/libuv/src/uv-common.c:65` | `size_t len = strlen(s);` |
| `ev_ed20342e7851` | call_site | `third_party/libuv/src/unix/udp.c:605` | `memcpy(req->bufs, bufs, nbufs * sizeof(bufs[0]));` |
| `ev_ed2ae77589b1` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_ed2b2e4c111d` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:108` | `address->name = uv__strdup(ent->ifa_name);` |
| `ev_ed37ad6ff868` | call_site | `third_party/libuv/src/unix/udp.c:1308` | `if ((r = uv__udp_prep_pkt(&m[n].msg_hdr, bufs[i], nbufs[i], addrs[i])))` |
| `ev_ed4ec597b507` | call_site | `third_party/libuv/src/unix/fs.c:1954` | `PATH;` |
| `ev_ed577decb294` | call_site | `third_party/libuv/src/unix/core.c:1122` | `fd = uv__open_cloexec(filename, O_RDONLY);` |
| `ev_ed60072d3f15` | call_site | `third_party/libuv/src/unix/stream.c:1079` | `nread = uv__recvmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_ed6cc76faf4f` | call_site | `third_party/libuv/src/unix/core.c:1223` | `CHECK_ENV_VAR("TMP");` |
| `ev_ed97b73719aa` | call_site | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_edacc1e1a7eb` | call_site | `third_party/libuv/src/unix/core.c:234` | `assert(0);` |
| `ev_edbe7aea1182` | call_site | `third_party/libuv/src/idna.c:436` | `assert(code_point >= 0);` |
| `ev_edfae655fde1` | call_site | `third_party/libuv/src/unix/udp.c:612` | `uv__udp_sendmsg(handle);` |
| `ev_ee01d26241df` | call_site | `third_party/libuv/src/unix/fs.c:1341` | `if (futimens(dstfd, times) == -1) {` |
| `ev_ee643cd7f570` | call_site | `third_party/libuv/src/unix/stream.c:895` | `uv__write_req_finish(req);` |
| `ev_ee6977999ce1` | call_site | `third_party/libuv/src/unix/udp.c:75` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_ee6f2cd4b61a` | call_site | `third_party/libuv/src/unix/core.c:738` | `return UV__ERR(errno);` |
| `ev_ee9bda9780d6` | call_site | `third_party/libuv/src/unix/udp.c:1140` | `addr4->sin_addr.s_addr = htonl(INADDR_ANY);` |
| `ev_eec7a4d037bc` | call_site | `third_party/libuv/src/threadpool.c:360` | `uv__req_unregister(req->loop);` |
| `ev_eee9634e0e53` | call_site | `third_party/libuv/src/unix/tcp.c:404` | `fd = uv__stream_fd(handle);` |
| `ev_eef18fd70443` | call_site | `third_party/libuv/src/unix/signal.c:220` | `errno = saved_errno;` |
| `ev_eef34aa93d07` | call_site | `third_party/libuv/src/unix/udp.c:271` | `handle->recv_cb(handle, UV__ERR(errno), &buf, NULL, 0);` |
| `ev_eef9d262f023` | call_site | `third_party/libuv/src/unix/fs.c:1445` | `errno = UV__ERR(result);` |
| `ev_ef0cd92bfb10` | call_site | `third_party/libuv/src/unix/core.c:675` | `while (r == -1 && errno == EINTR);` |
| `ev_ef175a01b7ed` | call_site | `third_party/libuv/src/unix/stream.c:415` | `if ((stream->flags & UV_HANDLE_TCP_NODELAY) && uv__tcp_nodelay(fd, 1))` |
| `ev_ef1e693826f1` | call_site | `third_party/libuv/src/unix/udp.c:476` | `errno = 0;` |
| `ev_ef1e7852ba07` | call_site | `third_party/libuv/src/unix/poll.c:108` | `uv__platform_invalidate_fd(handle->loop, handle->io_watcher.fd);` |
| `ev_ef306b3e2ee3` | call_site | `third_party/libuv/src/unix/fs.c:541` | `r = pread(fd, bufs->iov_base, bufs->iov_len, off);` |
| `ev_ef4a3223c50e` | call_site | `third_party/libuv/src/unix/fs.c:677` | `closedir(dir->dir);` |
| `ev_ef772a45bb21` | call_site | `third_party/libuv/src/unix/process.c:833` | `abort();` |
| `ev_ef8b4633bd50` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:147` | `pCFBundleGetInfoDictionary(pCFBundleGetMainBundle()));` |
| `ev_efa3bfa7a254` | call_site | `third_party/libuv/src/unix/process.c:270` | `uv__write_int(error_fd, UV__ERR(errno));` |
| `ev_efa92a12b85b` | call_site | `third_party/libuv/src/unix/core.c:794` | `return UV__ERR(errno);` |
| `ev_f0064fb17c18` | call_site | `third_party/libuv/src/unix/tcp.c:196` | `err = bind(tcp->io_watcher.fd, addr, addrlen);` |
| `ev_f01a219794e0` | call_site | `third_party/libuv/src/unix/fsevents.c:337` | `memset(&ctx, 0, sizeof(ctx));` |
| `ev_f060d986633d` | call_site | `third_party/libuv/src/unix/fs.c:1630` | `uv__to_stat(&pbuf, buf);` |
| `ev_f0ac2565abe9` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:156` | `if (pLSSetApplicationInformationItem(-2,  /* Magic value. */` |
| `ev_f0b98c2ab90a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:236` | `len = strnlen(ifname_buf, sizeof(ifname_buf));` |
| `ev_f0d30f8823e8` | call_site | `third_party/libuv/src/unix/stream.c:514` | `assert(events & POLLIN);` |
| `ev_f1022ea4fc65` | call_site | `third_party/libuv/src/unix/core.c:1184` | `r = uv_os_get_passwd(&pwd);` |
| `ev_f108cfae6524` | call_site | `third_party/libuv/src/uv-common.c:932` | `return uv__read_start(stream, alloc_cb, read_cb);` |
| `ev_f10b82fa09d9` | call_site | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_f116ee8ed548` | call_site | `third_party/libuv/src/unix/process.c:203` | `return uv_socketpair(SOCK_STREAM, 0, fds, 0, 0);` |
| `ev_f1219b043d46` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:159` | `uv__free(addresses[i].name);` |
| `ev_f128ef1e0779` | call_site | `third_party/libuv/src/unix/stream.c:1395` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_f1551ded3ff7` | call_site | `third_party/libuv/src/unix/kqueue.c:306` | `uv__update_time(loop);` |
| `ev_f1571593e266` | assignment | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_f1662de62aaa` | call_site | `third_party/libuv/src/unix/stream.c:357` | `err = uv_sem_init(&s->async_sem, 0);` |
| `ev_f1a6d7e777ea` | call_site | `third_party/libuv/src/unix/fs.c:2140` | `PATH2;` |
| `ev_f1c7b45e077d` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:222` | `freeaddrinfo(ai);` |
| `ev_f1d2097e7253` | call_site | `third_party/libuv/src/unix/udp.c:601` | `uv__req_unregister(handle->loop);` |
| `ev_f2195fdd62fb` | call_site | `third_party/libuv/src/unix/core.c:1845` | `while (rc == -1 && errno == EINTR);` |
| `ev_f22623d5590c` | call_site | `third_party/libuv/src/unix/signal.c:288` | `uv__close(loop->signal_pipefd[1]);` |
| `ev_f27ea6337e6f` | call_site | `third_party/libuv/src/uv-common.c:410` | `return uv__tcp_connect(req, handle, addr, addrlen, cb);` |
| `ev_f302624036a5` | call_site | `third_party/libuv/src/unix/udp.c:771` | `memset(&mreq, 0, sizeof(mreq));` |
| `ev_f32eac08d2bc` | call_site | `third_party/libuv/src/unix/process.c:1075` | `uv__free(pipes);` |
| `ev_f3480debb9b7` | call_site | `third_party/libuv/src/unix/udp.c:1188` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_f355b4f31eac` | call_site | `third_party/libuv/src/unix/process.c:875` | `err = uv__spawn_and_init_child_posix_spawn(options,` |
| `ev_f36a74a9caef` | call_site | `third_party/libuv/src/unix/pipe.c:294` | `memset(&saddr, 0, sizeof saddr);` |
| `ev_f37958c3a5a4` | call_site | `third_party/libuv/src/unix/core.c:423` | `return uv__loop_alive(loop);` |
| `ev_f3832ed1291f` | call_site | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_f3aa3a485991` | call_site | `third_party/libuv/src/threadpool.c:241` | `uv_sem_destroy(&sem);` |
| `ev_f3aaefe6c567` | call_site | `third_party/libuv/src/unix/signal.c:122` | `} while (r < 0 && errno == EINTR);` |
| `ev_f3b589da3099` | call_site | `third_party/libuv/src/unix/dl.c:37` | `return lib->handle ? 0 : uv__dlerror(lib);` |
| `ev_f3deb2934d98` | call_site | `third_party/libuv/src/unix/core.c:155` | `return uv__hrtime(UV_CLOCK_PRECISE);` |
| `ev_f3faef45b6cb` | call_site | `third_party/libuv/src/unix/pipe.c:274` | `if (includes_nul(name, namelen))` |
| `ev_f422b02efc6f` | call_site | `third_party/libuv/src/unix/udp.c:831` | `memcpy(&mreq.gsr_source, source_addr, sizeof(*source_addr));` |
| `ev_f451aaf7215d` | call_site | `third_party/libuv/src/unix/fsevents.c:839` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_f4812cf235d3` | call_site | `third_party/libuv/src/unix/stream.c:645` | `uv__req_unregister(stream->loop);` |
| `ev_f4a034728a90` | call_site | `third_party/libuv/src/threadpool.c:222` | `abort();` |
| `ev_f4be40e427a0` | call_site | `third_party/libuv/src/unix/core.c:736` | `rc = recvmsg(fd, msg, flags);` |
| `ev_f4dca1629118` | call_site | `third_party/libuv/src/unix/udp.c:107` | `uv__req_unregister(handle->loop);` |
| `ev_f501081cc60b` | call_site | `third_party/libuv/src/unix/stream.c:1182` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_f5634bb23ca0` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:213` | `uv__getaddrinfo_work(&req->work_req);` |
| `ev_f563ea107417` | call_site | `third_party/libuv/src/unix/fsevents.c:607` | `err = uv_sem_init(&state->fsevent_sem, 0);` |
| `ev_f58a5cd461d9` | call_site | `third_party/libuv/src/threadpool.c:319` | `uv__queue_move(&loop->wq, &wq);` |
| `ev_f5af8d523511` | assignment | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_f5c6198d991e` | call_site | `third_party/libuv/src/unix/fs.c:1131` | `errno = 0;` |
| `ev_f5da7c8542e9` | call_site | `third_party/libuv/src/unix/stream.c:1210` | `if (uv__stream_fd(stream) == -1)` |
| `ev_f5e6e0cd8e7b` | call_site | `third_party/libuv/src/unix/pipe.c:513` | `return UV__ERR(errno);` |
| `ev_f5f546380dc5` | call_site | `third_party/libuv/src/unix/tty.c:325` | `uv__tty_make_raw(&tmp);` |
| `ev_f6007ff33c79` | call_site | `third_party/libuv/src/uv-common.c:1029` | `memcpy(metrics,` |
| `ev_f61ceabe42fc` | call_site | `third_party/libuv/src/unix/thread.c:118` | `if (lim.rlim_cur >= (rlim_t) uv__min_stack_size())` |
| `ev_f62987fb7631` | call_site | `third_party/libuv/src/unix/darwin.c:80` | `if (realpath(exepath, abspath) != abspath)` |
| `ev_f6395d2a38b4` | call_site | `third_party/libuv/src/unix/tcp.c:355` | `if (uv__fd_exists(handle->loop, sock))` |
| `ev_f692596f7f95` | call_site | `third_party/libuv/src/unix/process.c:1010` | `exec_errorno = uv__spawn_and_init_child(loop, options, stdio_count, pipes, &pid);` |
| `ev_f697f0d480ca` | call_site | `third_party/libuv/src/unix/fsevents.c:875` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_f6a91cbf90c4` | call_site | `third_party/libuv/src/thread-common.c:139` | `abort();` |
| `ev_f6ca9cfda7f1` | call_site | `third_party/libuv/src/unix/tty.c:375` | `while (err == -1 && errno == EINTR);` |
| `ev_f6d0541719e7` | call_site | `third_party/libuv/src/inet.c:80` | `memset(words, '\0', sizeof words);` |
| `ev_f6ff14192a47` | call_site | `third_party/libuv/src/fs-poll.c:180` | `assert(ctx->parent_handle->poll_ctx == ctx);` |
| `ev_f7156c120f5a` | call_site | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_f719aa8bf1da` | call_site | `third_party/libuv/src/fs-poll.c:151` | `assert(ctx != NULL);` |
| `ev_f7227be16b08` | call_site | `third_party/libuv/src/unix/stream.c:1060` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_f73853ec687d` | call_site | `third_party/libuv/src/idna.c:395` | `assert(code_point >= 0);` |
| `ev_f73e5cc77b90` | call_site | `third_party/libuv/src/unix/udp.c:572` | `assert(nbufs > 0);` |
| `ev_f753391cdac5` | call_site | `third_party/libuv/src/unix/tcp.c:286` | `assert(handle->type == UV_TCP);` |
| `ev_f7822d5cd1de` | call_site | `third_party/libuv/src/unix/thread.c:346` | `if (pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE))` |
| `ev_f79e414930c4` | call_site | `third_party/libuv/src/unix/pipe.c:523` | `if ((err = uv__nonblock(temp[0], 1)))` |
| `ev_f7b579a18d9c` | call_site | `third_party/libuv/src/unix/core.c:1047` | `return uv__getrusage(RUSAGE_SELF, rusage);` |
| `ev_f7b6e217c75e` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_f7e698584085` | call_site | `third_party/libuv/src/unix/stream.c:353` | `err = uv_sem_init(&s->close_sem, 0);` |
| `ev_f7fd900cabe3` | call_site | `third_party/libuv/src/unix/core.c:528` | `uv__close(sockfd);` |
| `ev_f80093ab98fd` | call_site | `third_party/libuv/src/threadpool.c:74` | `uv__queue_next(&run_slow_work_message) == &wq &&` |
| `ev_f8059c4eb9dc` | call_site | `third_party/libuv/src/unix/fs.c:1592` | `ret = uv__fs_statx(-1, path, /* is_fstat */ 0, /* is_lstat */ 0, buf);` |
| `ev_f81411d0e702` | call_site | `third_party/libuv/src/unix/signal.c:212` | `assert(r == sizeof msg \|\|` |
| `ev_f817b7ad2b3e` | call_site | `third_party/libuv/src/unix/stream.c:514` | `assert(events & POLLIN);` |
| `ev_f8253cf22497` | call_site | `third_party/libuv/src/unix/stream.c:949` | `queued_fds = uv__malloc((queue_size - 1) * sizeof(*queued_fds->fds) +` |
| `ev_f85910885849` | assignment | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_f86c50bae908` | call_site | `third_party/libuv/src/unix/thread.c:957` | `return UV__ERR(errno);` |
| `ev_f87e32bcc811` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_f88597e32012` | call_site | `third_party/libuv/src/unix/stream.c:1049` | `assert(stream->alloc_cb != NULL);` |
| `ev_f889621f4f32` | call_site | `third_party/libuv/src/unix/fsevents.c:520` | `core_foundation_handle = dlopen("/System/Library/Frameworks/"` |
| `ev_f898006d43d2` | call_site | `third_party/libuv/src/unix/kqueue.c:200` | `assert(w->fd < (int) loop->nwatchers);` |
| `ev_f89cbb31f8a7` | call_site | `third_party/libuv/src/unix/fsevents.c:446` | `assert(q != &state->fsevent_handles);` |
| `ev_f89d7ab6ff3a` | call_site | `third_party/libuv/src/fs-poll.c:90` | `memcpy(ctx->path, path, len + 1);` |
| `ev_f8a1ad912e91` | call_site | `third_party/libuv/src/unix/thread.c:385` | `if (pthread_mutex_unlock(mutex))` |
| `ev_f8a5f2b68799` | call_site | `third_party/libuv/src/thread-common.c:118` | `uv_mutex_unlock(&b->mutex);` |
| `ev_f8ddfd55deff` | assignment | `third_party/libuv/src/unix/async.c:311` | `uv__io_init(&loop->async_io_watcher, uv__async_io, pipefd[0]);` |
| `ev_f9156dd747cb` | call_site | `third_party/libuv/src/unix/stream.c:171` | `memset(s->swrite, 0, s->swrite_sz);` |
| `ev_f925858582af` | call_site | `third_party/libuv/src/unix/thread.c:790` | `abort();` |
| `ev_f92cba05b32c` | call_site | `third_party/libuv/src/queue.h:63` | `if (uv__queue_empty(h))` |
| `ev_f93cafdce75b` | call_site | `third_party/libuv/src/unix/thread.c:436` | `err = pthread_rwlock_trywrlock(rwlock);` |
| `ev_f93d256542e1` | call_site | `third_party/libuv/src/unix/udp.c:113` | `uv__free(req->bufs);` |
| `ev_f97f0d23a079` | call_site | `third_party/libuv/src/unix/stream.c:1533` | `uv_read_stop(handle);` |
| `ev_f9a124e2e788` | call_site | `third_party/libuv/src/unix/stream.c:196` | `r = read(s->int_fd, buf, sizeof(buf));` |
| `ev_f9b645bbed9f` | call_site | `third_party/libuv/src/unix/core.c:889` | `nwatchers = next_power_of_two(len + 2) - 2;` |
| `ev_f9c5acb6eb23` | call_site | `third_party/libuv/src/unix/process.c:609` | `err = posix_spawn_file_actions_addinherit_np(actions, fd);` |
| `ev_f9f790410cf0` | call_site | `third_party/libuv/src/unix/fs.c:2267` | `uv__free((void*) req->path);  /* Memory is shared with req->new_path. */` |
| `ev_f9fd744d1594` | call_site | `third_party/libuv/src/unix/stream.c:913` | `q = uv__queue_head(&pq);` |
| `ev_fa0e91092281` | call_site | `third_party/libuv/src/unix/udp.c:745` | `return UV__ERR(errno);` |
| `ev_fa284476d33b` | call_site | `third_party/libuv/src/unix/thread.c:360` | `abort();` |
| `ev_fa334f184c7d` | call_site | `third_party/libuv/src/unix/tty.c:210` | `uv__stream_init(loop, (uv_stream_t*) tty, UV_TTY);` |
| `ev_fa392fbeccaf` | call_site | `third_party/libuv/src/unix/fs.c:929` | `n = poll(&pfd, 1, -1);` |
| `ev_faa6357cd96c` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:198` | `req->service = memcpy(buf + len, service, service_len);` |
| `ev_fabdb1932e37` | call_site | `third_party/libuv/src/unix/core.c:918` | `assert(0 == (events & ~(POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI)));` |
| `ev_fac95b3c91e9` | call_site | `third_party/libuv/src/unix/kqueue.c:314` | `assert((reset_timeout == 0 ? timeout : user_timeout) == 0);` |
| `ev_faccc2a91a90` | call_site | `third_party/libuv/src/unix/thread.c:162` | `pagesize = (size_t)getpagesize();` |
| `ev_facf1520fd2a` | call_site | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_fae537fac9c4` | call_site | `third_party/libuv/src/unix/fs.c:1668` | `while (result < 0 && errno == EINTR);` |
| `ev_faebca96799f` | call_site | `third_party/libuv/src/unix/signal.c:210` | `} while (r == -1 && errno == EINTR);` |
| `ev_fb04137a2540` | call_site | `third_party/libuv/src/unix/process.c:618` | `uv__nonblock_fcntl(use_fd, 0);` |
| `ev_fb145fdadf7c` | call_site | `third_party/libuv/src/unix/process.c:260` | `n = write(fd, &val, sizeof(val));` |
| `ev_fb29196e82fd` | call_site | `third_party/libuv/src/unix/thread.c:886` | `abort();` |
| `ev_fb51f19781e9` | call_site | `third_party/libuv/src/unix/stream.c:916` | `uv__req_unregister(stream->loop);` |
| `ev_fb547ffabf46` | call_site | `third_party/libuv/src/unix/core.c:578` | `err = uv__cloexec(peerfd, 1);` |
| `ev_fb5abf04e33d` | call_site | `third_party/libuv/src/unix/thread.c:907` | `strncpy(namebuf, name, sizeof(namebuf) - 1);` |
| `ev_fba2c202e38f` | call_site | `third_party/libuv/src/unix/fs.c:1715` | `X(CHOWN, chown(req->path, req->uid, req->gid));` |
| `ev_fbb40e372bcd` | call_site | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_fbdab1c688e3` | assignment | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_fbf3059a3c9e` | call_site | `third_party/libuv/src/unix/tty.c:483` | `saved_errno = errno;` |
| `ev_fc16d83d15da` | call_site | `third_party/libuv/src/unix/kqueue.c:484` | `assert(loop->watchers != NULL);` |
| `ev_fc1a250252c7` | call_site | `third_party/libuv/src/unix/tcp.c:301` | `memcpy(&tmp6, addr, sizeof(tmp6));` |
| `ev_fc5635c5b5d0` | call_site | `third_party/libuv/src/unix/stream.c:1052` | `stream->alloc_cb((uv_handle_t*)stream, 64 * 1024, &buf);` |
| `ev_fc6251443018` | call_site | `third_party/libuv/src/unix/fs.c:1202` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_fc75b96e58bf` | call_site | `third_party/libuv/src/unix/fs.c:1982` | `PATH;` |
| `ev_fc9c201f311f` | call_site | `third_party/libuv/src/unix/poll.c:74` | `err = uv__io_check_fd(loop, fd);` |
| `ev_fc9d7369f5fb` | call_site | `third_party/libuv/src/fs-poll.c:184` | `abort();` |
| `ev_fcd5f4f38ae4` | call_site | `third_party/libuv/src/unix/fs.c:2302` | `PATH2;` |
| `ev_fcdf392d2591` | call_site | `third_party/libuv/src/unix/signal.c:552` | `assert(removed_handle == handle);` |
| `ev_fd0fe73b6c39` | call_site | `third_party/libuv/src/threadpool.c:291` | `uv__queue_remove(&w->wq);` |
| `ev_fd15943cce66` | call_site | `third_party/libuv/src/unix/process.c:926` | `while (r == -1 && errno == EINTR);` |
| `ev_fd40b04980f7` | assignment | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_fd4278805330` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_fd83b0b24448` | call_site | `third_party/libuv/src/unix/signal.c:286` | `uv__io_stop(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_fd8677621322` | call_site | `third_party/libuv/src/unix/core.c:351` | `uv__udp_finish_close((uv_udp_t*)handle);` |
| `ev_fd9ce8da62a2` | call_site | `third_party/libuv/src/unix/fs.c:1727` | `X(LSTAT, uv__fs_lstat(req->path, &req->statbuf));` |
| `ev_fdc759489a88` | call_site | `third_party/libuv/src/unix/fs.c:2150` | `PATH;` |
| `ev_fe1cee440e9e` | call_site | `third_party/libuv/src/unix/async.c:394` | `uv__io_stop(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_fe26acb7066c` | call_site | `third_party/libuv/src/idna.c:232` | `c = uv__utf8_decode1(&s, se);` |
| `ev_fe3fd10cd5e0` | call_site | `third_party/libuv/src/unix/process.c:199` | `assert(container->data.stream != NULL);` |
| `ev_fe4c236904c0` | call_site | `third_party/libuv/src/unix/kqueue.c:376` | `assert(w->events == POLLIN);` |
| `ev_fe6137adc778` | call_site | `third_party/libuv/src/unix/core.c:1777` | `r = uv__strscpy(buffer->version, buf.version, sizeof(buffer->version));` |
| `ev_fe6b3fbeb2f8` | call_site | `third_party/libuv/src/unix/kqueue.c:360` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_fe911d56467a` | call_site | `third_party/libuv/src/unix/udp.c:1273` | `while (r == -1 && errno == EINTR);` |
| `ev_feb4676dfae8` | call_site | `third_party/libuv/src/unix/stream.c:1006` | `memcpy(&fd, p, sizeof(fd));` |
| `ev_fec163fa5680` | call_site | `third_party/libuv/src/unix/kqueue.c:72` | `err = uv__kqueue_init(loop);` |
| `ev_fee781bf7238` | assignment | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_ff11ea804f9b` | call_site | `third_party/libuv/src/unix/stream.c:135` | `r = write(s->fake_fd, "x", 1);` |
| `ev_ff1ce1bcf754` | call_site | `third_party/libuv/src/unix/core.c:921` | `assert(w->fd < INT_MAX);` |
| `ev_ff24e18349a9` | call_site | `third_party/libuv/src/unix/fs.c:319` | `errno = EINVAL;` |
| `ev_ff2c1feaef16` | call_site | `third_party/libuv/src/unix/pipe.c:125` | `memset(&saddr, 0, sizeof saddr);` |
| `ev_ff3a4f0d97bf` | call_site | `third_party/libuv/src/unix/stream.c:460` | `uv__req_unregister(stream->loop);` |
| `ev_ff728f86ed86` | call_site | `third_party/libuv/src/unix/core.c:377` | `uv__finish_close(p);` |
| `ev_ff77cbfb84ff` | call_site | `third_party/libuv/src/unix/core.c:1890` | `path_env = getenv("PATH");` |
| `ev_ff7e59f3db4f` | call_site | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_ffa07e66dc9b` | call_site | `third_party/libuv/src/unix/random-devurandom.c:38` | `fd = uv__open_cloexec(path, O_RDONLY);` |
| `ev_ffd42790c7d3` | call_site | `third_party/libuv/src/unix/core.c:160` | `assert(!uv__is_closing(handle));` |
| `ev_ffe2a3be3446` | call_site | `third_party/libuv/src/unix/fs.c:1731` | `X(MKSTEMP, uv__fs_mkstemp(req));` |
