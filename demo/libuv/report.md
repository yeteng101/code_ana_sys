# 代码逆向分析 Demo

- Run: `run_libuv_1.50.0`
- Build profile: `libuv-macos-clang`
- Analyzer: `clang++ -Xclang -ast-dump=json`
- Nodes: 633 / Edges: 1481
- Verification: 79%

## 模块架构

- **core**: 事件循环驱动、停止循环、核心逻辑
  - Files: ``
  - Symbols: `f、func、less_than、pCFArrayCreate、pCFBundleGetBundleWithIdentifier、pCFBundleGetDataPointerForName、pCFBundleGetFunctionPointerForName、pCFBundleGetInfoDictionary、pCFBundleGetMainBundle、pCFRelease、pCFRunLoopAddSource、pCFRunLoopGetCurrent、pCFRunLoopRemoveSource、pCFRunLoopRun、pCFRunLoopSourceCreate、pCFRunLoopSourceSignal、pCFRunLoopStop、pCFRunLoopWakeUp、pCFStringCreateWithCString、pCFStringCreateWithFileSystemRepresentation、pFSEventStreamCreate、pFSEventStreamInvalidate、pFSEventStreamRelease、pFSEventStreamScheduleWithRunLoop、pFSEventStreamStart、pFSEventStreamStop、pLSApplicationCheckIn、pLSGetCurrentApplicationASN、pLSSetApplicationInformationItem、pLSSetApplicationLaunchServicesServerConnectionStatus、uv__getentropy、uv__mkostemp、walk_cb`
- **include**: 事件等待、核心逻辑
  - Files: `third_party/libuv/include/uv.h`
  - Symbols: `uv_async_s::async_cb、uv_check_s::check_cb、uv_connect_s::cb、uv_fs_event_s::cb、uv_fs_s::cb、uv_getaddrinfo_s::cb、uv_getnameinfo_s::getnameinfo_cb、uv_handle_s::close_cb、uv_idle_s::idle_cb、uv_poll_s::poll_cb、uv_prepare_s::prepare_cb、uv_process_s::exit_cb、uv_random_s::cb、uv_shutdown_s::cb、uv_signal_s::signal_cb、uv_stream_s::alloc_cb、uv_stream_s::connection_cb、uv_stream_s::read_cb、uv_timer_s::timer_cb、uv_udp_s::alloc_cb、uv_udp_s::recv_cb、uv_udp_send_s::send_cb、uv_work_s::after_work_cb、uv_work_s::work_cb、uv_write_s::cb`
- **src**: 事件循环驱动、事件等待、停止循环、初始化、核心逻辑
  - Files: `third_party/libuv/src/fs-poll.c`, `third_party/libuv/src/heap-inl.h`, `third_party/libuv/src/idna.c`, `third_party/libuv/src/inet.c`, `third_party/libuv/src/queue.h`, `third_party/libuv/src/random.c`, `third_party/libuv/src/strscpy.c`, `third_party/libuv/src/strtok.c`, `third_party/libuv/src/thread-common.c`, `third_party/libuv/src/threadpool.c`, `third_party/libuv/src/timer.c`, `third_party/libuv/src/uv-common.c`
  - Symbols: `poll_ctx::poll_cb、uv__allocator_t::local_calloc、uv__allocator_t::local_free、uv__allocator_t::local_malloc、uv__allocator_t::local_realloc、heap_dequeue、heap_init、heap_insert、heap_min、heap_node_swap、heap_remove、inet_ntop4、inet_ntop6、inet_pton4、inet_pton6、init_once、init_threads、poll_cb、post、slow_work_thread_threshold、statbuf_eq、timer_cb、timer_close_cb、timer_heap、uv__calloc、uv__cancelled、uv__count_bufs、uv__free、uv__fs_get_dirent_type、uv__fs_poll_close、uv__fs_readdir_cleanup、uv__fs_scandir_cleanup、uv__get_nbufs、uv__get_surrogate_value、uv__idna_toascii、uv__idna_toascii_label、uv__malloc、uv__metrics_set_provider_entry_time、uv__metrics_update_idle_time、uv__next_timeout、uv__print_handles、uv__queue_add、uv__queue_done、uv__queue_empty、uv__queue_head、uv__queue_init、uv__queue_insert_head、uv__queue_insert_tail、uv__queue_move、uv__queue_next、uv__queue_remove、uv__queue_split、uv__queue_work、uv__random、uv__random_done、uv__random_work、uv__realloc、uv__reallocf、uv__run_timers、uv__strdup、uv__strndup、uv__strscpy、uv__strtok、uv__threadpool_cleanup、uv__timer_close、uv__udp_check_before_send、uv__udp_is_connected、uv__unknown_err_code、uv__utf8_decode1、uv__utf8_decode1_slow、uv__work_cancel、uv__work_done、uv__work_submit、uv__wtf8_decode1、uv_barrier_destroy、uv_barrier_init、uv_barrier_wait、uv_buf_init、uv_cancel、uv_default_loop、uv_err_name、uv_err_name_r、uv_free_cpu_info、uv_fs_poll_getpath、uv_fs_poll_init、uv_fs_poll_start、uv_fs_poll_stop、uv_fs_scandir_next、uv_inet_ntop、uv_inet_pton、uv_ip4_addr、uv_ip4_name、uv_ip6_addr、uv_ip6_name、uv_ip_name、uv_library_shutdown、uv_loop_close、uv_loop_configure、uv_loop_delete、uv_loop_new、uv_metrics_idle_time、uv_now、uv_os_free_environ、uv_os_free_group、uv_os_free_passwd、uv_print_active_handles、uv_print_all_handles、uv_queue_work、uv_random、uv_read_start、uv_recv_buffer_size、uv_send_buffer_size、uv_strerror、uv_tcp_bind、uv_tcp_connect、uv_timer_again、uv_timer_init、uv_timer_start、uv_timer_stop、uv_udp_bind、uv_udp_connect、uv_udp_init、uv_udp_init_ex、uv_udp_recv_start、uv_udp_recv_stop、uv_udp_send、uv_udp_try_send、uv_udp_try_send2、uv_unref、uv_utf16_length_as_wtf8、uv_utf16_to_wtf8、uv_walk、uv_wtf8_length_as_utf16、uv_wtf8_to_utf16、worker`
- **unix**: 事件循环驱动、事件等待、停止循环、初始化、回调注册、核心逻辑
  - Files: `third_party/libuv/src/unix/async.c`, `third_party/libuv/src/unix/bsd-ifaddrs.c`, `third_party/libuv/src/unix/core.c`, `third_party/libuv/src/unix/darwin-proctitle.c`, `third_party/libuv/src/unix/darwin-syscalls.h`, `third_party/libuv/src/unix/darwin.c`, `third_party/libuv/src/unix/dl.c`, `third_party/libuv/src/unix/fs.c`, `third_party/libuv/src/unix/fsevents.c`, `third_party/libuv/src/unix/getaddrinfo.c`, `third_party/libuv/src/unix/getnameinfo.c`, `third_party/libuv/src/unix/internal.h`, `third_party/libuv/src/unix/kqueue.c`, `third_party/libuv/src/unix/loop-watcher.c`, `third_party/libuv/src/unix/loop.c`, `third_party/libuv/src/unix/pipe.c`, `third_party/libuv/src/unix/poll.c`, `third_party/libuv/src/unix/process.c`, `third_party/libuv/src/unix/proctitle.c`, `third_party/libuv/src/unix/random-devurandom.c`, `third_party/libuv/src/unix/random-getentropy.c`, `third_party/libuv/src/unix/signal.c`, `third_party/libuv/src/unix/stream.c`, `third_party/libuv/src/unix/tcp.c`, `third_party/libuv/src/unix/thread.c`, `third_party/libuv/src/unix/tty.c`, `third_party/libuv/src/unix/udp.c`
  - Symbols: `uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np、close$NOCANCEL、includes_nul、init_process_title_mutex_once、maybe_bind_socket、maybe_new_socket、maybe_resize、new_socket、next_power_of_two、recvmsg_x、sendmsg_x、uv___stream_fd、uv__accept、uv__async_close、uv__async_fork、uv__async_io、uv__async_send、uv__async_spin、uv__async_start、uv__async_stop、uv__backend_timeout、uv__basename_r、uv__cf_loop_cb、uv__cf_loop_runner、uv__cf_loop_signal、uv__check_before_write、uv__check_close、uv__cloexec、uv__close、uv__close_nocancel、uv__close_nocheckstdio、uv__cpu_relax、uv__default_stack_size、uv__dlerror、uv__drain、uv__dup2_cloexec、uv__emfile_trick、uv__fd_exists、uv__finish_close、uv__fs_buf_offset、uv__fs_close、uv__fs_closedir、uv__fs_copyfile、uv__fs_done、uv__fs_event、uv__fs_event_close、uv__fs_fdatasync、uv__fs_fstat、uv__fs_fsync、uv__fs_futime、uv__fs_lstat、uv__fs_lutime、uv__fs_mkdtemp、uv__fs_mkstemp、uv__fs_open、uv__fs_opendir、uv__fs_pathmax_size、uv__fs_post、uv__fs_read、uv__fs_readdir、uv__fs_readlink、uv__fs_realpath、uv__fs_scandir、uv__fs_sendfile、uv__fs_sendfile_emul、uv__fs_stat、uv__fs_statfs、uv__fs_statx、uv__fs_to_timeval、uv__fs_utime、uv__fs_work、uv__fs_write、uv__fs_write_all、uv__fsevents_cb、uv__fsevents_close、uv__fsevents_create_stream、uv__fsevents_destroy_stream、uv__fsevents_event_cb、uv__fsevents_global_init、uv__fsevents_init、uv__fsevents_loop_delete、uv__fsevents_loop_init、uv__fsevents_push_event、uv__fsevents_reschedule、uv__fstat、uv__getaddrinfo_done、uv__getaddrinfo_translate_error、uv__getaddrinfo_work、uv__getiovmax、uv__getnameinfo_done、uv__getnameinfo_work、uv__getpwuid_r、uv__getrusage、uv__getsockpeername、uv__handle_fd、uv__hrtime、uv__idle_close、uv__ifaddr_exclude、uv__io_active、uv__io_check_fd、uv__io_close、uv__io_feed、uv__io_fork、uv__io_init、uv__io_poll、uv__io_start、uv__io_stop、uv__ipv6_link_local_scope_id、uv__is_ipv6_link_local、uv__kqueue_delete、uv__kqueue_init、uv__kqueue_runtime_detection、uv__loop_alive、uv__loop_close、uv__loop_configure、uv__lstat、uv__make_close_pending、uv__make_pipe、uv__min_stack_size、uv__nonblock_fcntl、uv__nonblock_ioctl、uv__open_cloexec、uv__open_file、uv__pipe_close、uv__pipe_getsockpeername、uv__pipe_listen、uv__platform_invalidate_fd、uv__platform_loop_delete、uv__platform_loop_init、uv__poll_close、uv__poll_io、uv__poll_stop、uv__preadv、uv__preadv_emul、uv__preadv_or_pwritev、uv__preadv_or_pwritev_emul、uv__prepare_close、uv__process_child_init、uv__process_close、uv__process_close_stream、uv__process_init、uv__process_init_stdio、uv__process_open_stream、uv__process_title_cleanup、uv__pwritev、uv__pwritev_emul、uv__random_devurandom、uv__random_devurandom_init、uv__random_getentropy、uv__random_readpath、uv__read、uv__read_start、uv__recvmsg、uv__run_check、uv__run_closing_handles、uv__run_idle、uv__run_pending、uv__run_prepare、uv__search_path、uv__server_io、uv__set_process_title、uv__set_recverr、uv__setsockopt、uv__setsockopt_maybe_char、uv__signal_block_and_lock、uv__signal_cleanup、uv__signal_close、uv__signal_compare、uv__signal_event、uv__signal_first_handle、uv__signal_global_init、uv__signal_global_once_init、uv__signal_global_reinit、uv__signal_handler、uv__signal_lock、uv__signal_loop_cleanup、uv__signal_loop_fork、uv__signal_loop_once_init、uv__signal_register_handler、uv__signal_start、uv__signal_stop、uv__signal_tree_s_RB_FIND、uv__signal_tree_s_RB_INSERT、uv__signal_tree_s_RB_INSERT_COLOR、uv__signal_tree_s_RB_NEXT、uv__signal_tree_s_RB_NFIND、uv__signal_tree_s_RB_REMOVE、uv__signal_tree_s_RB_REMOVE_COLOR、uv__signal_unlock、uv__signal_unlock_and_unblock、uv__signal_unregister_handler、uv__slurp、uv__sock_reuseaddr、uv__sock_reuseport、uv__socket、uv__socket_sockopt、uv__spawn_and_init_child、uv__spawn_and_init_child_fork、uv__spawn_and_init_child_posix_spawn、uv__spawn_find_path_in_env、uv__spawn_init_can_use_setsid、uv__spawn_init_posix_spawn、uv__spawn_init_posix_spawn_fncs、uv__spawn_resolve_and_spawn、uv__spawn_set_posix_spawn_attrs、uv__spawn_set_posix_spawn_file_actions、uv__stat、uv__stream_close、uv__stream_connect、uv__stream_destroy、uv__stream_eof、uv__stream_flush_write_queue、uv__stream_init、uv__stream_io、uv__stream_open、uv__stream_osx_cb_close、uv__stream_osx_interrupt_select、uv__stream_osx_select、uv__stream_osx_select_cb、uv__stream_queue_fd、uv__stream_recv_cmsg、uv__stream_try_select、uv__tcp_bind、uv__tcp_close、uv__tcp_connect、uv__tcp_keepalive、uv__tcp_listen、uv__tcp_nodelay、uv__tcsetattr、uv__thread_getname、uv__thread_setname、uv__thread_stack_size、uv__to_stat、uv__try_write、uv__tty_close、uv__tty_is_slave、uv__tty_make_raw、uv__udp_bind、uv__udp_close、uv__udp_connect、uv__udp_disconnect、uv__udp_finish_close、uv__udp_init_ex、uv__udp_io、uv__udp_maybe_deferred_bind、uv__udp_prep_pkt、uv__udp_recv_start、uv__udp_recv_stop、uv__udp_recvmmsg、uv__udp_recvmsg、uv__udp_run_completed、uv__udp_send、uv__udp_sendmsg、uv__udp_sendmsg1、uv__udp_sendmsgv、uv__udp_set_membership4、uv__udp_set_membership6、uv__udp_set_source_membership4、uv__udp_set_source_membership6、uv__udp_try_send、uv__udp_try_send2、uv__update_time、uv__wait_children、uv__write、uv__write_callbacks、uv__write_errno、uv__write_int、uv__write_req_finish、uv__write_req_size、uv__write_req_update、uv__writev、uv_accept、uv_async_init、uv_async_send、uv_backend_timeout、uv_check_init、uv_check_start、uv_check_stop、uv_close、uv_cond_broadcast、uv_cond_destroy、uv_cond_init、uv_cond_signal、uv_cond_wait、uv_cpu_info、uv_disable_stdio_inheritance、uv_dlclose、uv_dlopen、uv_dlsym、uv_fileno、uv_free_interface_addresses、uv_fs_access、uv_fs_chmod、uv_fs_chown、uv_fs_close、uv_fs_closedir、uv_fs_copyfile、uv_fs_event_init、uv_fs_event_start、uv_fs_event_stop、uv_fs_fchmod、uv_fs_fchown、uv_fs_fdatasync、uv_fs_fstat、uv_fs_fsync、uv_fs_ftruncate、uv_fs_futime、uv_fs_lchown、uv_fs_link、uv_fs_lstat、uv_fs_lutime、uv_fs_mkdir、uv_fs_mkdtemp、uv_fs_mkstemp、uv_fs_open、uv_fs_opendir、uv_fs_read、uv_fs_readdir、uv_fs_readlink、uv_fs_realpath、uv_fs_rename、uv_fs_req_cleanup、uv_fs_rmdir、uv_fs_scandir、uv_fs_sendfile、uv_fs_stat、uv_fs_statfs、uv_fs_symlink、uv_fs_unlink、uv_fs_utime、uv_fs_write、uv_get_available_memory、uv_get_free_memory、uv_get_process_title、uv_getaddrinfo、uv_getnameinfo、uv_getrusage、uv_guess_handle、uv_hrtime、uv_idle_init、uv_idle_start、uv_idle_stop、uv_if_indextoiid、uv_if_indextoname、uv_interface_addresses、uv_is_active、uv_kill、uv_listen、uv_loop_alive、uv_loop_fork、uv_loop_init、uv_mutex_destroy、uv_mutex_init、uv_mutex_lock、uv_mutex_unlock、uv_once、uv_os_environ、uv_os_get_group、uv_os_get_passwd、uv_os_get_passwd2、uv_os_getenv、uv_os_homedir、uv_os_uname、uv_pipe、uv_pipe_bind、uv_pipe_bind2、uv_pipe_chmod、uv_pipe_connect、uv_pipe_connect2、uv_pipe_getpeername、uv_pipe_getsockname、uv_pipe_init、uv_pipe_open、uv_pipe_pending_type、uv_poll_init、uv_poll_init_socket、uv_poll_start、uv_poll_stop、uv_prepare_init、uv_prepare_start、uv_prepare_stop、uv_process_kill、uv_read_stop、uv_run、uv_rwlock_destroy、uv_rwlock_init、uv_rwlock_rdlock、uv_rwlock_rdunlock、uv_rwlock_wrlock、uv_rwlock_wrunlock、uv_sem_destroy、uv_sem_init、uv_sem_post、uv_sem_trywait、uv_sem_wait、uv_set_process_title、uv_setup_args、uv_shutdown、uv_signal_init、uv_signal_start、uv_signal_start_oneshot、uv_signal_stop、uv_socketpair、uv_spawn、uv_stream_set_blocking、uv_tcp_close_reset、uv_tcp_getpeername、uv_tcp_getsockname、uv_tcp_init、uv_tcp_init_ex、uv_tcp_keepalive、uv_tcp_nodelay、uv_tcp_open、uv_thread_create、uv_thread_create_ex、uv_thread_getname、uv_thread_join、uv_thread_setname、uv_try_write、uv_try_write2、uv_tty_get_winsize、uv_tty_init、uv_tty_reset_mode、uv_tty_set_mode、uv_udp_getpeername、uv_udp_getsockname、uv_udp_open、uv_udp_set_membership、uv_udp_set_multicast_interface、uv_udp_set_multicast_loop、uv_udp_set_multicast_ttl、uv_udp_set_source_membership、uv_udp_set_ttl、uv_udp_using_recvmmsg、uv_update_time、uv_write、uv_write2`
- **uv**: 核心逻辑
  - Files: `third_party/libuv/include/uv/threadpool.h`, `third_party/libuv/include/uv/unix.h`
  - Symbols: `uv__io_s::cb、uv__work::done、uv__work::work`

Dependencies: `src -> core`, `src -> include`, `src -> unix`, `src -> uv`, `unix -> core`, `unix -> include`, `unix -> src`, `unix -> uv`, `uv -> src`, `uv -> unix`

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
  subgraph sg_include["include"]
    N34["uv_async_s::async_cb"]
    N35["uv_check_s::check_cb"]
    N36["uv_connect_s::cb"]
    N37["uv_fs_event_s::cb"]
    N38["uv_fs_s::cb"]
    N39["uv_getaddrinfo_s::cb"]
    N40["uv_getnameinfo_s::getnameinfo_cb"]
    N41["uv_handle_s::close_cb"]
    N42["uv_idle_s::idle_cb"]
    N43["uv_poll_s::poll_cb"]
    N44["uv_prepare_s::prepare_cb"]
    N45["uv_process_s::exit_cb"]
    N46["uv_random_s::cb"]
    N47["uv_shutdown_s::cb"]
    N48["uv_signal_s::signal_cb"]
    N49["uv_stream_s::alloc_cb"]
    N50["uv_stream_s::connection_cb"]
    N51["uv_stream_s::read_cb"]
    N52["uv_timer_s::timer_cb"]
    N53["uv_udp_s::alloc_cb"]
    N54["uv_udp_s::recv_cb"]
    N55["uv_udp_send_s::send_cb"]
    N56["uv_work_s::after_work_cb"]
    N57["uv_work_s::work_cb"]
    N58["uv_write_s::cb"]
  end
  subgraph sg_src["src"]
    N59["poll_ctx::poll_cb"]
    N60["uv__allocator_t::local_calloc"]
    N61["uv__allocator_t::local_free"]
    N62["uv__allocator_t::local_malloc"]
    N63["uv__allocator_t::local_realloc"]
    N64["heap_dequeue"]
    N65["heap_init"]
    N66["heap_insert"]
    N67["heap_min"]
    N68["heap_node_swap"]
    N69["heap_remove"]
    N70["inet_ntop4"]
    N71["inet_ntop6"]
    N72["inet_pton4"]
    N73["inet_pton6"]
    N74["init_once"]
    N75["init_threads"]
    N76["poll_cb"]
    N77["post"]
    N78["slow_work_thread_threshold"]
    N79["statbuf_eq"]
    N80["timer_cb"]
    N81["timer_close_cb"]
    N82["timer_heap"]
    N83["uv__calloc"]
    N84["uv__cancelled"]
    N85["uv__count_bufs"]
    N86["uv__free"]
    N87["uv__fs_get_dirent_type"]
    N88["uv__fs_poll_close"]
    N89["uv__fs_readdir_cleanup"]
    N90["uv__fs_scandir_cleanup"]
    N91["uv__get_nbufs"]
    N92["uv__get_surrogate_value"]
    N93["uv__idna_toascii"]
    N94["uv__idna_toascii_label"]
    N95["uv__malloc"]
    N96["uv__metrics_set_provider_entry_time"]
    N97["uv__metrics_update_idle_time"]
    N98["uv__next_timeout"]
    N99["uv__print_handles"]
    N100["uv__queue_add"]
    N101["uv__queue_done"]
    N102["uv__queue_empty"]
    N103["uv__queue_head"]
    N104["uv__queue_init"]
    N105["uv__queue_insert_head"]
    N106["uv__queue_insert_tail"]
    N107["uv__queue_move"]
    N108["uv__queue_next"]
    N109["uv__queue_remove"]
    N110["uv__queue_split"]
    N111["uv__queue_work"]
    N112["uv__random"]
    N113["uv__random_done"]
    N114["uv__random_work"]
    N115["uv__realloc"]
    N116["uv__reallocf"]
    N117["uv__run_timers"]
    N118["uv__strdup"]
    N119["uv__strndup"]
    N120["uv__strscpy"]
    N121["uv__strtok"]
    N122["uv__threadpool_cleanup"]
    N123["uv__timer_close"]
    N124["uv__udp_check_before_send"]
    N125["uv__udp_is_connected"]
    N126["uv__unknown_err_code"]
    N127["uv__utf8_decode1"]
    N128["uv__utf8_decode1_slow"]
    N129["uv__work_cancel"]
    N130["uv__work_done"]
    N131["uv__work_submit"]
    N132["uv__wtf8_decode1"]
    N133["uv_barrier_destroy"]
    N134["uv_barrier_init"]
    N135["uv_barrier_wait"]
    N136["uv_buf_init"]
    N137["uv_cancel"]
    N138["uv_default_loop"]
    N139["uv_err_name"]
    N140["uv_err_name_r"]
    N141["uv_free_cpu_info"]
    N142["uv_fs_poll_getpath"]
    N143["uv_fs_poll_init"]
    N144["uv_fs_poll_start"]
    N145["uv_fs_poll_stop"]
    N146["uv_fs_scandir_next"]
    N147["uv_inet_ntop"]
    N148["uv_inet_pton"]
    N149["uv_ip4_addr"]
    N150["uv_ip4_name"]
    N151["uv_ip6_addr"]
    N152["uv_ip6_name"]
    N153["uv_ip_name"]
    N154["uv_library_shutdown"]
    N155["uv_loop_close"]
    N156["uv_loop_configure"]
    N157["uv_loop_delete"]
    N158["uv_loop_new"]
    N159["uv_metrics_idle_time"]
    N160["uv_now"]
    N161["uv_os_free_environ"]
    N162["uv_os_free_group"]
    N163["uv_os_free_passwd"]
    N164["uv_print_active_handles"]
    N165["uv_print_all_handles"]
    N166["uv_queue_work"]
    N167["uv_random"]
    N168["uv_read_start"]
    N169["uv_recv_buffer_size"]
    N170["uv_send_buffer_size"]
    N171["uv_strerror"]
    N172["uv_tcp_bind"]
    N173["uv_tcp_connect"]
    N174["uv_timer_again"]
    N175["uv_timer_init"]
    N176["uv_timer_start"]
    N177["uv_timer_stop"]
    N178["uv_udp_bind"]
    N179["uv_udp_connect"]
    N180["uv_udp_init"]
    N181["uv_udp_init_ex"]
    N182["uv_udp_recv_start"]
    N183["uv_udp_recv_stop"]
    N184["uv_udp_send"]
    N185["uv_udp_try_send"]
    N186["uv_udp_try_send2"]
    N187["uv_unref"]
    N188["uv_utf16_length_as_wtf8"]
    N189["uv_utf16_to_wtf8"]
    N190["uv_walk"]
    N191["uv_wtf8_length_as_utf16"]
    N192["uv_wtf8_to_utf16"]
    N193["worker"]
  end
  subgraph sg_unix["unix"]
    N194["uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np"]
    N195["close$NOCANCEL"]
    N196["includes_nul"]
    N197["init_process_title_mutex_once"]
    N198["maybe_bind_socket"]
    N199["maybe_new_socket"]
    N200["maybe_resize"]
    N201["new_socket"]
    N202["next_power_of_two"]
    N203["recvmsg_x"]
    N204["sendmsg_x"]
    N205["uv___stream_fd"]
    N206["uv__accept"]
    N207["uv__async_close"]
    N208["uv__async_fork"]
    N209["uv__async_io"]
    N210["uv__async_send"]
    N211["uv__async_spin"]
    N212["uv__async_start"]
    N213["uv__async_stop"]
    N214["uv__backend_timeout"]
    N215["uv__basename_r"]
    N216["uv__cf_loop_cb"]
    N217["uv__cf_loop_runner"]
    N218["uv__cf_loop_signal"]
    N219["uv__check_before_write"]
    N220["uv__check_close"]
    N221["uv__cloexec"]
    N222["uv__close"]
    N223["uv__close_nocancel"]
    N224["uv__close_nocheckstdio"]
    N225["uv__cpu_relax"]
    N226["uv__default_stack_size"]
    N227["uv__dlerror"]
    N228["uv__drain"]
    N229["uv__dup2_cloexec"]
    N230["uv__emfile_trick"]
    N231["uv__fd_exists"]
    N232["uv__finish_close"]
    N233["uv__fs_buf_offset"]
    N234["uv__fs_close"]
    N235["uv__fs_closedir"]
    N236["uv__fs_copyfile"]
    N237["uv__fs_done"]
    N238["uv__fs_event"]
    N239["uv__fs_event_close"]
    N240["uv__fs_fdatasync"]
    N241["uv__fs_fstat"]
    N242["uv__fs_fsync"]
    N243["uv__fs_futime"]
    N244["uv__fs_lstat"]
    N245["uv__fs_lutime"]
    N246["uv__fs_mkdtemp"]
    N247["uv__fs_mkstemp"]
    N248["uv__fs_open"]
    N249["uv__fs_opendir"]
    N250["uv__fs_pathmax_size"]
    N251["uv__fs_post"]
    N252["uv__fs_read"]
    N253["uv__fs_readdir"]
    N254["uv__fs_readlink"]
    N255["uv__fs_realpath"]
    N256["uv__fs_scandir"]
    N257["uv__fs_sendfile"]
    N258["uv__fs_sendfile_emul"]
    N259["uv__fs_stat"]
    N260["uv__fs_statfs"]
    N261["uv__fs_statx"]
    N262["uv__fs_to_timeval"]
    N263["uv__fs_utime"]
    N264["uv__fs_work"]
    N265["uv__fs_write"]
    N266["uv__fs_write_all"]
    N267["uv__fsevents_cb"]
    N268["uv__fsevents_close"]
    N269["uv__fsevents_create_stream"]
    N270["uv__fsevents_destroy_stream"]
    N271["uv__fsevents_event_cb"]
    N272["uv__fsevents_global_init"]
    N273["uv__fsevents_init"]
    N274["uv__fsevents_loop_delete"]
    N275["uv__fsevents_loop_init"]
    N276["uv__fsevents_push_event"]
    N277["uv__fsevents_reschedule"]
    N278["uv__fstat"]
    N279["uv__getaddrinfo_done"]
    N280["uv__getaddrinfo_translate_error"]
    N281["uv__getaddrinfo_work"]
    N282["uv__getiovmax"]
    N283["uv__getnameinfo_done"]
    N284["uv__getnameinfo_work"]
    N285["uv__getpwuid_r"]
    N286["uv__getrusage"]
    N287["uv__getsockpeername"]
    N288["uv__handle_fd"]
    N289["uv__hrtime"]
    N290["uv__idle_close"]
    N291["uv__ifaddr_exclude"]
    N292["uv__io_active"]
    N293["uv__io_check_fd"]
    N294["uv__io_close"]
    N295["uv__io_feed"]
    N296["uv__io_fork"]
    N297["uv__io_init"]
    N298["uv__io_poll"]
    N299["uv__io_start"]
    N300["uv__io_stop"]
    N301["uv__ipv6_link_local_scope_id"]
    N302["uv__is_ipv6_link_local"]
    N303["uv__kqueue_delete"]
    N304["uv__kqueue_init"]
    N305["uv__kqueue_runtime_detection"]
    N306["uv__loop_alive"]
    N307["uv__loop_close"]
    N308["uv__loop_configure"]
    N309["uv__lstat"]
    N310["uv__make_close_pending"]
    N311["uv__make_pipe"]
    N312["uv__min_stack_size"]
    N313["uv__nonblock_fcntl"]
    N314["uv__nonblock_ioctl"]
    N315["uv__open_cloexec"]
    N316["uv__open_file"]
    N317["uv__pipe_close"]
    N318["uv__pipe_getsockpeername"]
    N319["uv__pipe_listen"]
    N320["uv__platform_invalidate_fd"]
    N321["uv__platform_loop_delete"]
    N322["uv__platform_loop_init"]
    N323["uv__poll_close"]
    N324["uv__poll_io"]
    N325["uv__poll_stop"]
    N326["uv__preadv"]
    N327["uv__preadv_emul"]
    N328["uv__preadv_or_pwritev"]
    N329["uv__preadv_or_pwritev_emul"]
    N330["uv__prepare_close"]
    N331["uv__process_child_init"]
    N332["uv__process_close"]
    N333["uv__process_close_stream"]
    N334["uv__process_init"]
    N335["uv__process_init_stdio"]
    N336["uv__process_open_stream"]
    N337["uv__process_title_cleanup"]
    N338["uv__pwritev"]
    N339["uv__pwritev_emul"]
    N340["uv__random_devurandom"]
    N341["uv__random_devurandom_init"]
    N342["uv__random_getentropy"]
    N343["uv__random_readpath"]
    N344["uv__read"]
    N345["uv__read_start"]
    N346["uv__recvmsg"]
    N347["uv__run_check"]
    N348["uv__run_closing_handles"]
    N349["uv__run_idle"]
    N350["uv__run_pending"]
    N351["uv__run_prepare"]
    N352["uv__search_path"]
    N353["uv__server_io"]
    N354["uv__set_process_title"]
    N355["uv__set_recverr"]
    N356["uv__setsockopt"]
    N357["uv__setsockopt_maybe_char"]
    N358["uv__signal_block_and_lock"]
    N359["uv__signal_cleanup"]
    N360["uv__signal_close"]
    N361["uv__signal_compare"]
    N362["uv__signal_event"]
    N363["uv__signal_first_handle"]
    N364["uv__signal_global_init"]
    N365["uv__signal_global_once_init"]
    N366["uv__signal_global_reinit"]
    N367["uv__signal_handler"]
    N368["uv__signal_lock"]
    N369["uv__signal_loop_cleanup"]
    N370["uv__signal_loop_fork"]
    N371["uv__signal_loop_once_init"]
    N372["uv__signal_register_handler"]
    N373["uv__signal_start"]
    N374["uv__signal_stop"]
    N375["uv__signal_tree_s_RB_FIND"]
    N376["uv__signal_tree_s_RB_INSERT"]
    N377["uv__signal_tree_s_RB_INSERT_COLOR"]
    N378["uv__signal_tree_s_RB_NEXT"]
    N379["uv__signal_tree_s_RB_NFIND"]
    N380["uv__signal_tree_s_RB_REMOVE"]
    N381["uv__signal_tree_s_RB_REMOVE_COLOR"]
    N382["uv__signal_unlock"]
    N383["uv__signal_unlock_and_unblock"]
    N384["uv__signal_unregister_handler"]
    N385["uv__slurp"]
    N386["uv__sock_reuseaddr"]
    N387["uv__sock_reuseport"]
    N388["uv__socket"]
    N389["uv__socket_sockopt"]
    N390["uv__spawn_and_init_child"]
    N391["uv__spawn_and_init_child_fork"]
    N392["uv__spawn_and_init_child_posix_spawn"]
    N393["uv__spawn_find_path_in_env"]
    N394["uv__spawn_init_can_use_setsid"]
    N395["uv__spawn_init_posix_spawn"]
    N396["uv__spawn_init_posix_spawn_fncs"]
    N397["uv__spawn_resolve_and_spawn"]
    N398["uv__spawn_set_posix_spawn_attrs"]
    N399["uv__spawn_set_posix_spawn_file_actions"]
    N400["uv__stat"]
    N401["uv__stream_close"]
    N402["uv__stream_connect"]
    N403["uv__stream_destroy"]
    N404["uv__stream_eof"]
    N405["uv__stream_flush_write_queue"]
    N406["uv__stream_init"]
    N407["uv__stream_io"]
    N408["uv__stream_open"]
    N409["uv__stream_osx_cb_close"]
    N410["uv__stream_osx_interrupt_select"]
    N411["uv__stream_osx_select"]
    N412["uv__stream_osx_select_cb"]
    N413["uv__stream_queue_fd"]
    N414["uv__stream_recv_cmsg"]
    N415["uv__stream_try_select"]
    N416["uv__tcp_bind"]
    N417["uv__tcp_close"]
    N418["uv__tcp_connect"]
    N419["uv__tcp_keepalive"]
    N420["uv__tcp_listen"]
    N421["uv__tcp_nodelay"]
    N422["uv__tcsetattr"]
    N423["uv__thread_getname"]
    N424["uv__thread_setname"]
    N425["uv__thread_stack_size"]
    N426["uv__to_stat"]
    N427["uv__try_write"]
    N428["uv__tty_close"]
    N429["uv__tty_is_slave"]
    N430["uv__tty_make_raw"]
    N431["uv__udp_bind"]
    N432["uv__udp_close"]
    N433["uv__udp_connect"]
    N434["uv__udp_disconnect"]
    N435["uv__udp_finish_close"]
    N436["uv__udp_init_ex"]
    N437["uv__udp_io"]
    N438["uv__udp_maybe_deferred_bind"]
    N439["uv__udp_prep_pkt"]
    N440["uv__udp_recv_start"]
    N441["uv__udp_recv_stop"]
    N442["uv__udp_recvmmsg"]
    N443["uv__udp_recvmsg"]
    N444["uv__udp_run_completed"]
    N445["uv__udp_send"]
    N446["uv__udp_sendmsg"]
    N447["uv__udp_sendmsg1"]
    N448["uv__udp_sendmsgv"]
    N449["uv__udp_set_membership4"]
    N450["uv__udp_set_membership6"]
    N451["uv__udp_set_source_membership4"]
    N452["uv__udp_set_source_membership6"]
    N453["uv__udp_try_send"]
    N454["uv__udp_try_send2"]
    N455["uv__update_time"]
    N456["uv__wait_children"]
    N457["uv__write"]
    N458["uv__write_callbacks"]
    N459["uv__write_errno"]
    N460["uv__write_int"]
    N461["uv__write_req_finish"]
    N462["uv__write_req_size"]
    N463["uv__write_req_update"]
    N464["uv__writev"]
    N465["uv_accept"]
    N466["uv_async_init"]
    N467["uv_async_send"]
    N468["uv_backend_timeout"]
    N469["uv_check_init"]
    N470["uv_check_start"]
    N471["uv_check_stop"]
    N472["uv_close"]
    N473["uv_cond_broadcast"]
    N474["uv_cond_destroy"]
    N475["uv_cond_init"]
    N476["uv_cond_signal"]
    N477["uv_cond_wait"]
    N478["uv_cpu_info"]
    N479["uv_disable_stdio_inheritance"]
    N480["uv_dlclose"]
    N481["uv_dlopen"]
    N482["uv_dlsym"]
    N483["uv_fileno"]
    N484["uv_free_interface_addresses"]
    N485["uv_fs_access"]
    N486["uv_fs_chmod"]
    N487["uv_fs_chown"]
    N488["uv_fs_close"]
    N489["uv_fs_closedir"]
    N490["uv_fs_copyfile"]
    N491["uv_fs_event_init"]
    N492["uv_fs_event_start"]
    N493["uv_fs_event_stop"]
    N494["uv_fs_fchmod"]
    N495["uv_fs_fchown"]
    N496["uv_fs_fdatasync"]
    N497["uv_fs_fstat"]
    N498["uv_fs_fsync"]
    N499["uv_fs_ftruncate"]
    N500["uv_fs_futime"]
    N501["uv_fs_lchown"]
    N502["uv_fs_link"]
    N503["uv_fs_lstat"]
    N504["uv_fs_lutime"]
    N505["uv_fs_mkdir"]
    N506["uv_fs_mkdtemp"]
    N507["uv_fs_mkstemp"]
    N508["uv_fs_open"]
    N509["uv_fs_opendir"]
    N510["uv_fs_read"]
    N511["uv_fs_readdir"]
    N512["uv_fs_readlink"]
    N513["uv_fs_realpath"]
    N514["uv_fs_rename"]
    N515["uv_fs_req_cleanup"]
    N516["uv_fs_rmdir"]
    N517["uv_fs_scandir"]
    N518["uv_fs_sendfile"]
    N519["uv_fs_stat"]
    N520["uv_fs_statfs"]
    N521["uv_fs_symlink"]
    N522["uv_fs_unlink"]
    N523["uv_fs_utime"]
    N524["uv_fs_write"]
    N525["uv_get_available_memory"]
    N526["uv_get_free_memory"]
    N527["uv_get_process_title"]
    N528["uv_getaddrinfo"]
    N529["uv_getnameinfo"]
    N530["uv_getrusage"]
    N531["uv_guess_handle"]
    N532["uv_hrtime"]
    N533["uv_idle_init"]
    N534["uv_idle_start"]
    N535["uv_idle_stop"]
    N536["uv_if_indextoiid"]
    N537["uv_if_indextoname"]
    N538["uv_interface_addresses"]
    N539["uv_is_active"]
    N540["uv_kill"]
    N541["uv_listen"]
    N542["uv_loop_alive"]
    N543["uv_loop_fork"]
    N544["uv_loop_init"]
    N545["uv_mutex_destroy"]
    N546["uv_mutex_init"]
    N547["uv_mutex_lock"]
    N548["uv_mutex_unlock"]
    N549["uv_once"]
    N550["uv_os_environ"]
    N551["uv_os_get_group"]
    N552["uv_os_get_passwd"]
    N553["uv_os_get_passwd2"]
    N554["uv_os_getenv"]
    N555["uv_os_homedir"]
    N556["uv_os_uname"]
    N557["uv_pipe"]
    N558["uv_pipe_bind"]
    N559["uv_pipe_bind2"]
    N560["uv_pipe_chmod"]
    N561["uv_pipe_connect"]
    N562["uv_pipe_connect2"]
    N563["uv_pipe_getpeername"]
    N564["uv_pipe_getsockname"]
    N565["uv_pipe_init"]
    N566["uv_pipe_open"]
    N567["uv_pipe_pending_type"]
    N568["uv_poll_init"]
    N569["uv_poll_init_socket"]
    N570["uv_poll_start"]
    N571["uv_poll_stop"]
    N572["uv_prepare_init"]
    N573["uv_prepare_start"]
    N574["uv_prepare_stop"]
    N575["uv_process_kill"]
    N576["uv_read_stop"]
    N577["uv_run"]
    N578["uv_rwlock_destroy"]
    N579["uv_rwlock_init"]
    N580["uv_rwlock_rdlock"]
    N581["uv_rwlock_rdunlock"]
    N582["uv_rwlock_wrlock"]
    N583["uv_rwlock_wrunlock"]
    N584["uv_sem_destroy"]
    N585["uv_sem_init"]
    N586["uv_sem_post"]
    N587["uv_sem_trywait"]
    N588["uv_sem_wait"]
    N589["uv_set_process_title"]
    N590["uv_setup_args"]
    N591["uv_shutdown"]
    N592["uv_signal_init"]
    N593["uv_signal_start"]
    N594["uv_signal_start_oneshot"]
    N595["uv_signal_stop"]
    N596["uv_socketpair"]
    N597["uv_spawn"]
    N598["uv_stream_set_blocking"]
    N599["uv_tcp_close_reset"]
    N600["uv_tcp_getpeername"]
    N601["uv_tcp_getsockname"]
    N602["uv_tcp_init"]
    N603["uv_tcp_init_ex"]
    N604["uv_tcp_keepalive"]
    N605["uv_tcp_nodelay"]
    N606["uv_tcp_open"]
    N607["uv_thread_create"]
    N608["uv_thread_create_ex"]
    N609["uv_thread_getname"]
    N610["uv_thread_join"]
    N611["uv_thread_setname"]
    N612["uv_try_write"]
    N613["uv_try_write2"]
    N614["uv_tty_get_winsize"]
    N615["uv_tty_init"]
    N616["uv_tty_reset_mode"]
    N617["uv_tty_set_mode"]
    N618["uv_udp_getpeername"]
    N619["uv_udp_getsockname"]
    N620["uv_udp_open"]
    N621["uv_udp_set_membership"]
    N622["uv_udp_set_multicast_interface"]
    N623["uv_udp_set_multicast_loop"]
    N624["uv_udp_set_multicast_ttl"]
    N625["uv_udp_set_source_membership"]
    N626["uv_udp_set_ttl"]
    N627["uv_udp_using_recvmmsg"]
    N628["uv_update_time"]
    N629["uv_write"]
    N630["uv_write2"]
  end
  subgraph sg_uv["uv"]
    N631["uv__io_s::cb"]
    N632["uv__work::done"]
    N633["uv__work::work"]
  end
  N324 -. fd_ready .-> N43
  N267 --> N103
  N472 --> N428
  N401 --> N584
  N336 --> N408
  N180 --> N181
  N209 -. fd_ready .-> N34
  N557 --> N221
  N277 -. fd_ready .-> N4
  N486 --> N118
  N277 --> N548
  N130 -. fd_ready .-> N632
  N544 --> N466
  N561 --> N562
  N216 --> N103
  N266 --> N265
  N345 --> N205
  N285 --> N95
  N503 --> N118
  N335 --> N596
  N267 --> N107
  N273 --> N546
  N264 --> N252
  N213 --> N300
  N193 -. fd_ready .-> N633
  N390 --> N582
  N273 --> N275
  N595 --> N374
  N559 --> N86
  N515 --> N86
  N193 --> N106
  N485 --> N118
  N437 --> N444
  N190 --> N102
  N353 --> N300
  N591 --> N102
  N418 --> N299
  N193 --> N547
  N544 --> N322
  N193 --> N103
  N99 --> N138
  N237 -. fd_ready .-> N38
  N597 --> N335
  N559 --> N196
  N193 --> N102
  N511 --> N131
  N559 --> N205
  N209 --> N102
  N373 --> N383
  N367 --> N363
  N214 --> N102
  N570 --> N325
  N343 --> N222
  N425 --> N226
  N555 --> N163
  N287 --> N483
  N331 --> N459
  N351 --> N103
  N457 --> N410
  N621 --> N149
  N75 --> N588
  N448 --> N439
  N403 -. fd_ready .-> N36
  N443 -. fd_ready .-> N54
  N189 --> N188
  N402 --> N458
  N630 --> N104
  N201 --> N198
  N457 --> N461
  N544 --> N104
  N239 --> N493
  N589 --> N354
  N209 --> N109
  N158 --> N86
  N444 -. fd_ready .-> N55
  N304 --> N221
  N318 --> N287
  N458 --> N102
  N324 -. fd_ready .-> N43
  N458 -. fd_ready .-> N58
  N364 --> N366
  N267 --> N86
  N442 -. fd_ready .-> N54
  N354 -. fd_ready .-> N27
  N323 --> N325
  N465 --> N620
  N486 --> N131
  N77 --> N548
  N444 --> N103
  N596 --> N222
  N265 --> N338
  N277 --> N548
  N275 --> N272
  N129 --> N547
  N436 --> N104
  N112 --> N342
  N411 --> N588
  N415 --> N95
  N134 --> N86
  N273 --> N218
  N193 --> N106
  N208 --> N107
  N354 -. fd_ready .-> N19
  N122 --> N545
  N415 --> N472
  N117 --> N109
  N275 --> N545
  N527 --> N548
  N472 --> N220
  N577 --> N117
  N415 --> N222
  N135 --> N473
  N307 --> N321
  N274 --> N584
  N427 --> N282
  N117 --> N104
  N298 --> N103
  N401 --> N222
  N70 --> N120
  N77 --> N102
  N307 --> N86
  N510 --> N264
  N219 --> N205
  N81 --> N86
  N516 --> N131
  N406 --> N315
  N544 --> N546
  N350 --> N102
  N528 --> N281
  N259 --> N261
  N358 --> N368
  N352 --> N86
  N347 --> N109
  N330 --> N574
  N77 --> N548
  N270 -. fd_ready .-> N23
  N275 -. fd_ready .-> N15
  N184 --> N445
  N307 --> N545
  N277 --> N86
  N442 --> N136
  N435 --> N109
  N277 --> N586
  N277 --> N269
  N484 --> N86
  N606 --> N231
  N275 --> N83
  N440 --> N292
  N597 --> N106
  N456 --> N103
  N544 --> N579
  N145 --> N539
  N468 --> N214
  N592 --> N106
  N268 --> N547
  N216 --> N107
  N298 --> N102
  N415 --> N584
  N193 --> N548
  N380 --> N381
  N486 --> N264
  N69 --> N68
  N101 -. fd_ready .-> N56
  N492 --> N299
  N451 --> N148
  N556 --> N120
  N344 --> N410
  N369 --> N222
  N274 --> N584
  N478 --> N118
  N392 --> N398
  N615 --> N408
  N289 --> N549
  N513 --> N118
  N294 --> N300
  N418 --> N104
  N298 --> N97
  N564 --> N318
  N446 --> N85
  N457 --> N205
  N213 --> N109
  N501 --> N131
  N497 --> N131
  N264 --> N240
  N521 --> N95
  N317 --> N86
  N293 --> N278
  N404 -. fd_ready .-> N51
  N468 --> N102
  N354 -. fd_ready .-> N8
  N456 --> N104
  N352 --> N118
  N442 -. fd_ready .-> N54
  N177 --> N82
  N390 --> N549
  N472 --> N317
  N427 --> N288
  N269 -. fd_ready .-> N24
  N145 --> N539
  N326 --> N328
  N515 --> N90
  N465 --> N86
  N443 -. fd_ready .-> N54
  N193 --> N467
  N243 --> N262
  N445 --> N106
  N275 --> N545
  N236 --> N508
  N375 --> N361
  N75 --> N608
  N487 --> N118
  N185 --> N453
  N316 --> N315
  N294 --> N109
  N148 --> N72
  N541 --> N420
  N277 --> N548
  N350 --> N107
  N347 --> N102
  N577 --> N455
  N597 --> N224
  N544 --> N321
  N71 --> N70
  N350 -. fd_ready .-> N631
  N228 --> N410
  N442 -. fd_ready .-> N54
  N354 -. fd_ready .-> N19
  N614 --> N205
  N88 --> N310
  N122 --> N86
  N401 --> N222
  N418 --> N295
  N208 --> N103
  N352 --> N86
  N116 --> N115
  N416 --> N387
  N144 --> N86
  N596 --> N314
  N193 --> N476
  N209 --> N103
  N268 --> N103
  N577 --> N102
  N279 -. fd_ready .-> N39
  N266 --> N86
  N495 --> N264
  N133 --> N86
  N97 --> N548
  N183 --> N441
  N234 --> N223
  N130 --> N548
  N524 --> N131
  N83 -. fd_ready .-> N60
  N95 -. fd_ready .-> N62
  N319 --> N299
  N328 -. fd_ready .-> N1
  N406 --> N104
  N466 --> N106
  N305 --> N222
  N344 --> N205
  N374 --> N383
  N69 -. fd_ready .-> N3
  N470 --> N105
  N489 --> N131
  N446 --> N108
  N529 --> N284
  N404 --> N410
  N117 --> N104
  N279 --> N86
  N133 --> N474
  N216 --> N86
  N443 -. fd_ready .-> N53
  N542 --> N306
  N596 --> N222
  N373 --> N376
  N271 --> N104
  N405 --> N102
  N457 --> N299
  N222 --> N224
  N418 --> N205
  N251 --> N131
  N366 --> N311
  N568 --> N106
  N403 --> N458
  N347 --> N107
  N94 --> N127
  N603 --> N406
  N77 --> N106
  N510 --> N95
  N298 --> N97
  N269 -. fd_ready .-> N25
  N268 --> N102
  N133 --> N477
  N208 --> N102
  N445 --> N299
  N469 --> N106
  N456 --> N104
  N370 --> N371
  N443 -. fd_ready .-> N54
  N499 --> N264
  N406 --> N315
  N162 --> N86
  N597 --> N336
  N147 --> N71
  N274 -. fd_ready .-> N10
  N596 --> N221
  N268 --> N545
  N264 --> N249
  N123 --> N177
  N555 --> N552
  N412 --> N407
  N301 --> N302
  N367 --> N368
  N630 --> N219
  N362 -. fd_ready .-> N48
  N445 --> N446
  N268 --> N109
  N446 --> N109
  N307 --> N578
  N268 --> N547
  N98 --> N82
  N536 --> N537
  N349 --> N109
  N275 --> N588
  N267 -. fd_ready .-> N37
  N218 -. fd_ready .-> N18
  N521 --> N264
  N456 -. fd_ready .-> N45
  N415 --> N584
  N506 --> N131
  N354 --> N424
  N553 --> N285
  N267 -. fd_ready .-> N37
  N354 -. fd_ready .-> N19
  N213 --> N106
  N277 -. fd_ready .-> N10
  N257 --> N258
  N543 --> N208
  N111 -. fd_ready .-> N57
  N216 --> N277
  N510 --> N131
  N342 -. fd_ready .-> N31
  N274 --> N86
  N383 --> N382
  N577 --> N349
  N458 --> N86
  N275 --> N584
  N247 --> N222
  N232 -. fd_ready .-> N41
  N64 --> N69
  N560 --> N400
  N625 --> N151
  N390 --> N224
  N616 --> N422
  N529 --> N283
  N255 --> N95
  N277 --> N95
  N618 --> N287
  N206 --> N222
  N130 --> N103
  N457 --> N103
  N218 --> N547
  N457 --> N463
  N96 --> N532
  N466 --> N106
  N425 --> N312
  N97 --> N547
  N515 --> N86
  N528 --> N131
  N90 --> N91
  N351 --> N102
  N568 --> N313
  N442 -. fd_ready .-> N54
  N436 --> N106
  N236 --> N522
  N407 --> N402
  N411 --> N587
  N190 --> N109
  N263 --> N262
  N374 --> N358
  N605 --> N421
  N331 --> N459
  N445 --> N85
  N228 --> N300
  N86 -. fd_ready .-> N61
  N525 --> N526
  N399 -. fd_ready .-> N194
  N630 --> N410
  N414 --> N413
  N273 --> N466
  N307 --> N548
  N521 --> N131
  N331 --> N459
  N608 --> N312
  N428 --> N422
  N190 --> N103
  N407 --> N344
  N442 --> N203
  N543 --> N296
  N415 --> N585
  N401 --> N610
  N599 --> N205
  N487 --> N264
  N260 --> N95
  N247 --> N221
  N557 --> N314
  N544 --> N578
  N244 --> N309
  N279 --> N86
  N598 --> N314
  N354 -. fd_ready .-> N28
  N144 --> N83
  N604 --> N205
  N620 --> N125
  N598 --> N205
  N401 --> N222
  N299 --> N200
  N615 --> N315
  N353 --> N230
  N453 --> N85
  N76 -. fd_ready .-> N59
  N351 -. fd_ready .-> N44
  N144 --> N160
  N268 --> N588
  N271 --> N102
  N217 -. fd_ready .-> N13
  N193 --> N586
  N569 --> N568
  N200 --> N202
  N217 --> N586
  N273 --> N95
  N343 --> N222
  N427 --> N205
  N401 --> N222
  N544 --> N104
  N113 -. fd_ready .-> N46
  N602 --> N603
  N597 --> N333
  N178 --> N431
  N277 --> N547
  N331 --> N224
  N556 --> N120
  N247 --> N549
  N455 --> N289
  N154 --> N122
  N193 --> N102
  N325 --> N300
  N253 --> N87
  N193 --> N78
  N129 --> N547
  N492 --> N224
  N366 --> N359
  N589 --> N548
  N127 --> N128
  N213 --> N211
  N527 --> N548
  N207 --> N109
  N465 --> N408
  N409 --> N86
  N511 --> N264
  N151 --> N148
  N441 --> N300
  N557 --> N221
  N206 --> N314
  N401 --> N576
  N349 -. fd_ready .-> N42
  N247 -. fd_ready .-> N32
  N190 -. fd_ready .-> N33
  N201 --> N408
  N374 --> N363
  N502 --> N264
  N129 --> N102
  N345 --> N410
  N156 --> N308
  N264 --> N241
  N534 --> N105
  N344 --> N414
  N283 -. fd_ready .-> N40
  N96 --> N547
  N415 --> N466
  N577 --> N350
  N264 --> N242
  N158 --> N544
  N191 --> N132
  N466 --> N212
  N176 --> N82
  N236 --> N515
  N359 --> N222
  N264 --> N256
  N615 --> N222
  N279 --> N86
  N268 -. fd_ready .-> N37
  N274 --> N102
  N452 --> N151
  N324 --> N300
  N461 --> N86
  N448 --> N447
  N450 --> N151
  N462 --> N85
  N566 --> N231
  N445 --> N95
  N264 --> N236
  N344 --> N299
  N344 --> N205
  N218 --> N548
  N362 --> N374
  N298 --> N456
  N591 --> N205
  N298 --> N97
  N512 --> N264
  N509 --> N118
  N71 --> N120
  N331 --> N459
  N497 --> N264
  N446 --> N109
  N255 --> N86
  N575 --> N540
  N299 --> N106
  N402 -. fd_ready .-> N36
  N135 --> N547
  N193 --> N104
  N498 --> N264
  N285 --> N86
  N446 --> N103
  N80 --> N519
  N300 --> N102
  N185 --> N124
  N192 --> N132
  N75 --> N104
  N529 --> N131
  N472 --> N123
  N271 --> N106
  N96 --> N548
  N562 --> N299
  N117 --> N67
  N401 --> N292
  N118 --> N95
  N406 --> N104
  N524 --> N95
  N597 --> N86
  N97 --> N532
  N395 --> N394
  N117 --> N82
  N159 --> N532
  N146 --> N91
  N89 --> N86
  N157 --> N155
  N145 --> N472
  N143 --> N106
  N428 --> N401
  N517 --> N131
  N630 --> N95
  N594 --> N373
  N606 --> N314
  N562 --> N196
  N193 --> N102
  N568 --> N231
  N359 --> N222
  N472 --> N239
  N493 --> N222
  N264 --> N253
  N264 --> N235
  N229 --> N221
  N412 --> N586
  N307 --> N102
  N403 --> N292
  N155 --> N307
  N418 --> N302
  N77 --> N547
  N294 --> N320
  N212 --> N315
  N351 --> N109
  N80 --> N160
  N117 --> N174
  N472 --> N88
  N456 --> N108
  N134 --> N475
  N577 --> N347
  N213 --> N102
  N425 --> N226
  N431 --> N355
  N284 --> N280
  N307 --> N547
  N75 --> N475
  N485 --> N264
  N273 --> N86
  N535 --> N109
  N544 --> N104
  N275 --> N584
  N444 --> N86
  N319 --> N205
  N77 --> N106
  N144 --> N175
  N344 --> N410
  N577 --> N97
  N436 --> N297
  N193 --> N108
  N472 --> N432
  N415 --> N222
  N411 --> N467
  N298 -. fd_ready .-> N631
  N213 --> N222
  N544 --> N369
  N432 --> N294
  N492 --> N278
  N560 --> N205
  N235 --> N86
  N266 --> N233
  N514 --> N264
  N166 --> N131
  N522 --> N264
  N93 --> N94
  N514 --> N131
  N528 --> N93
  N186 --> N454
  N472 --> N330
  N501 --> N264
  N129 --> N547
  N445 --> N299
  N390 --> N222
  N484 --> N86
  N264 --> N247
  N452 --> N438
  N353 --> N206
  N552 --> N285
  N342 -. fd_ready .-> N31
  N69 -. fd_ready .-> N3
  N296 --> N304
  N620 --> N314
  N457 --> N102
  N507 --> N264
  N354 -. fd_ready .-> N5
  N327 --> N329
  N603 --> N222
  N129 --> N106
  N174 --> N177
  N252 --> N86
  N81 --> N310
  N597 --> N104
  N411 --> N292
  N435 --> N103
  N415 --> N222
  N307 --> N222
  N264 --> N246
  N154 --> N359
  N551 --> N95
  N306 --> N102
  N300 --> N109
  N508 --> N118
  N562 --> N408
  N264 --> N255
  N367 --> N378
  N363 --> N379
  N413 --> N95
  N297 --> N104
  N254 --> N95
  N197 --> N546
  N373 --> N383
  N223 --> N195
  N371 --> N299
  N612 --> N613
  N244 --> N261
  N112 --> N340
  N76 --> N79
  N331 --> N222
  N577 --> N306
  N489 --> N264
  N236 --> N278
  N274 --> N218
  N134 --> N95
  N458 --> N103
  N336 --> N222
  N458 --> N107
  N144 --> N519
  N298 --> N96
  N184 --> N124
  N541 --> N319
  N344 --> N404
  N129 --> N548
  N407 --> N458
  N344 --> N346
  N472 --> N360
  N201 --> N222
  N296 --> N86
  N75 --> N104
  N367 --> N382
  N369 --> N374
  N130 --> N107
  N199 --> N205
  N617 --> N430
  N621 --> N449
  N451 --> N438
  N461 --> N109
  N135 --> N477
  N351 --> N107
  N543 --> N102
  N500 --> N264
  N189 --> N188
  N357 --> N356
  N605 --> N205
  N271 --> N276
  N538 --> N118
  N236 --> N515
  N406 --> N106
  N93 --> N94
  N512 --> N131
  N267 --> N109
  N236 --> N515
  N597 --> N106
  N273 --> N187
  N445 --> N438
  N274 --> N103
  N443 --> N627
  N275 --> N585
  N307 --> N86
  N524 --> N264
  N348 --> N232
  N412 --> N292
  N167 --> N112
  N354 -. fd_ready .-> N19
  N490 --> N131
  N492 --> N86
  N617 --> N422
  N603 --> N201
  N344 -. fd_ready .-> N49
  N403 --> N228
  N446 --> N102
  N457 --> N410
  N167 --> N131
  N245 --> N262
  N395 --> N396
  N523 --> N131
  N146 --> N87
  N107 --> N102
  N457 --> N427
  N76 --> N472
  N407 --> N228
  N597 --> N86
  N401 --> N586
  N457 --> N461
  N332 --> N109
  N456 --> N109
  N506 --> N118
  N401 --> N410
  N402 --> N102
  N508 --> N131
  N544 --> N104
  N495 --> N131
  N228 -. fd_ready .-> N47
  N274 --> N545
  N229 --> N222
  N456 --> N106
  N551 --> N86
  N550 --> N86
  N617 --> N205
  N344 -. fd_ready .-> N51
  N568 --> N293
  N199 --> N198
  N544 --> N104
  N354 -. fd_ready .-> N19
  N274 --> N109
  N193 --> N104
  N373 --> N372
  N295 --> N102
  N494 --> N264
  N608 --> N425
  N245 --> N262
  N454 --> N448
  N459 --> N460
  N133 --> N545
  N75 --> N104
  N444 --> N85
  N502 --> N131
  N446 --> N448
  N388 --> N314
  N343 --> N222
  N577 --> N298
  N471 --> N109
  N555 --> N163
  N352 --> N121
  N268 --> N109
  N615 --> N109
  N182 --> N440
  N208 --> N222
  N370 --> N222
  N417 --> N401
  N208 --> N222
  N131 --> N77
  N388 --> N222
  N568 --> N314
  N169 --> N389
  N266 --> N282
  N161 --> N86
  N158 --> N95
  N551 --> N95
  N556 --> N120
  N461 --> N106
  N444 --> N300
  N438 --> N431
  N443 -. fd_ready .-> N54
  N445 --> N102
  N264 --> N257
  N624 --> N357
  N159 --> N548
  N630 --> N106
  N354 -. fd_ready .-> N7
  N343 --> N315
  N559 --> N95
  N268 --> N86
  N298 -. fd_ready .-> N631
  N129 --> N548
  N412 --> N407
  N300 --> N106
  N285 --> N86
  N307 --> N545
  N379 --> N361
  N277 -. fd_ready .-> N20
  N538 --> N83
  N408 --> N421
  N66 --> N68
  N344 -. fd_ready .-> N51
  N506 --> N264
  N425 --> N226
  N135 --> N548
  N238 --> N215
  N415 --> N222
  N373 --> N374
  N504 --> N264
  N273 --> N106
  N499 --> N131
  N520 --> N131
  N271 --> N547
  N453 --> N447
  N219 --> N288
  N75 --> N95
  N268 --> N548
  N544 --> N86
  N427 --> N205
  N273 --> N104
  N591 --> N295
  N431 --> N386
  N117 --> N102
  N354 -. fd_ready .-> N7
  N200 --> N116
  N488 --> N264
  N270 -. fd_ready .-> N26
  N523 --> N264
  N224 --> N223
  N538 --> N291
  N76 -. fd_ready .-> N59
  N621 --> N151
  N391 --> N331
  N275 --> N104
  N354 -. fd_ready .-> N7
  N472 --> N207
  N488 --> N131
  N630 --> N457
  N354 -. fd_ready .-> N29
  N240 --> N242
  N435 --> N102
  N625 --> N452
  N444 --> N102
  N589 --> N547
  N281 --> N280
  N117 --> N106
  N601 --> N287
  N268 --> N472
  N331 --> N459
  N339 --> N329
  N411 --> N292
  N523 --> N118
  N345 --> N299
  N230 --> N315
  N232 --> N310
  N374 --> N372
  N259 --> N400
  N504 --> N131
  N404 --> N300
  N199 --> N201
  N173 --> N418
  N456 --> N102
  N76 --> N176
  N503 --> N131
  N216 --> N109
  N264 --> N266
  N527 --> N547
  N212 --> N549
  N336 --> N314
  N566 --> N408
  N401 --> N584
  N213 --> N107
  N213 --> N103
  N341 --> N343
  N550 --> N118
  N483 --> N205
  N209 --> N107
  N277 --> N276
  N344 --> N136
  N349 --> N107
  N504 --> N118
  N513 --> N264
  N212 --> N297
  N249 --> N86
  N343 --> N222
  N405 --> N106
  N528 --> N95
  N353 -. fd_ready .-> N50
  N347 -. fd_ready .-> N35
  N563 --> N318
  N401 --> N472
  N317 --> N401
  N567 --> N531
  N441 --> N292
  N298 --> N303
  N496 --> N131
  N480 --> N86
  N576 --> N300
  N273 --> N118
  N557 --> N314
  N388 --> N221
  N615 --> N222
  N369 --> N222
  N267 --> N548
  N370 --> N300
  N565 --> N406
  N444 -. fd_ready .-> N55
  N532 --> N289
  N568 --> N297
  N76 --> N515
  N218 -. fd_ready .-> N16
  N142 --> N539
  N544 --> N65
  N465 --> N222
  N218 --> N95
  N236 --> N278
  N570 --> N299
  N193 --> N548
  N371 --> N297
  N164 --> N99
  N271 --> N548
  N74 --> N75
  N447 --> N439
  N446 --> N106
  N216 --> N547
  N122 --> N77
  N401 --> N294
  N236 --> N515
  N407 --> N102
  N538 --> N291
  N193 --> N547
  N117 -. fd_ready .-> N52
  N298 --> N455
  N531 --> N278
  N615 --> N406
  N505 --> N264
  N420 --> N299
  N217 -. fd_ready .-> N12
  N458 --> N462
  N347 --> N106
  N277 --> N548
  N600 --> N287
  N443 --> N442
  N264 --> N254
  N622 --> N151
  N431 --> N387
  N138 --> N544
  N509 --> N131
  N620 --> N231
  N322 --> N304
  N550 --> N86
  N141 --> N86
  N122 --> N474
  N228 --> N102
  N562 --> N205
  N444 --> N109
  N577 --> N455
  N621 --> N438
  N290 --> N535
  N402 --> N405
  N574 --> N109
  N206 --> N221
  N273 --> N548
  N538 --> N291
  N407 --> N205
  N446 --> N103
  N94 --> N127
  N472 --> N332
  N513 --> N131
  N544 --> N83
  N559 --> N388
  N316 --> N222
  N436 --> N388
  N175 --> N104
  N493 --> N294
  N407 --> N205
  N298 --> N303
  N325 --> N320
  N628 --> N455
  N416 --> N199
  N492 --> N297
  N298 --> N97
  N557 --> N222
  N577 --> N102
  N311 --> N557
  N615 --> N429
  N254 --> N250
  N354 -. fd_ready .-> N6
  N227 --> N118
  N558 --> N559
  N114 --> N112
  N253 --> N118
  N491 --> N106
  N625 --> N149
  N390 --> N311
  N75 --> N585
  N247 --> N581
  N402 --> N205
  N492 --> N86
  N267 --> N547
  N331 --> N313
  N604 --> N419
  N543 --> N106
  N130 --> N102
  N571 --> N325
  N401 --> N222
  N577 --> N306
  N275 --> N585
  N307 --> N369
  N366 --> N382
  N559 --> N222
  N544 --> N104
  N344 -. fd_ready .-> N51
  N344 --> N300
  N140 --> N120
  N277 --> N108
  N472 --> N417
  N220 --> N471
  N492 --> N273
  N230 --> N206
  N154 --> N337
  N76 --> N539
  N354 -. fd_ready .-> N30
  N338 --> N328
  N93 --> N127
  N370 --> N222
  N592 --> N371
  N273 --> N545
  N360 --> N374
  N298 --> N104
  N615 --> N415
  N597 --> N390
  N407 --> N404
  N273 --> N86
  N435 --> N444
  N589 --> N549
  N623 --> N357
  N168 --> N345
  N621 --> N438
  N179 --> N434
  N159 --> N547
  N560 --> N564
  N590 --> N95
  N458 --> N109
  N503 --> N264
  N116 --> N86
  N150 --> N147
  N354 -. fd_ready .-> N9
  N556 --> N120
  N482 --> N227
  N130 --> N109
  N208 --> N300
  N519 --> N118
  N331 --> N459
  N522 --> N118
  N507 --> N118
  N412 --> N292
  N275 --> N425
  N277 --> N548
  N599 --> N472
  N440 --> N299
  N630 --> N299
  N75 --> N546
  N139 --> N126
  N193 --> N109
  N232 --> N403
  N402 --> N205
  N344 -. fd_ready .-> N51
  N161 --> N86
  N193 --> N476
  N472 --> N323
  N613 --> N427
  N270 -. fd_ready .-> N22
  N437 --> N446
  N557 --> N222
  N530 --> N286
  N211 --> N225
  N137 --> N129
  N212 --> N311
  N533 --> N106
  N461 --> N295
  N134 --> N546
  N147 --> N70
  N350 --> N104
  N298 --> N456
  N625 --> N149
  N625 --> N151
  N522 --> N131
  N622 --> N149
  N365 --> N549
  N295 --> N106
  N572 --> N106
  N77 --> N476
  N193 --> N103
  N321 --> N274
  N307 --> N222
  N353 --> N205
  N349 --> N102
  N264 --> N243
  N544 --> N455
  N544 --> N104
  N298 --> N303
  N544 --> N86
  N241 --> N426
  N176 --> N66
  N277 --> N547
  N236 --> N224
  N276 --> N467
  N298 -. fd_ready .-> N631
  N148 --> N73
  N94 --> N127
  N492 --> N118
  N413 --> N115
  N276 --> N548
  N276 --> N100
  N189 --> N95
  N298 --> N303
  N436 --> N104
  N252 --> N282
  N544 --> N365
  N609 --> N423
  N352 --> N121
  N630 --> N85
  N456 --> N103
  N212 --> N299
  N349 --> N103
  N181 --> N436
  N94 --> N127
  N277 --> N547
  N516 --> N264
  N490 --> N95
  N502 --> N95
  N193 --> N477
  N566 --> N415
  N373 --> N358
  N440 --> N438
  N216 -. fd_ready .-> N17
  N117 --> N177
  N264 --> N263
  N76 --> N539
  N551 --> N86
  N615 --> N229
  N573 --> N105
  N493 --> N86
  N427 --> N464
  N376 --> N377
  N446 --> N102
  N385 --> N315
  N354 -. fd_ready .-> N19
  N69 --> N68
  N263 --> N262
  N561 --> N104
  N516 --> N118
  N390 --> N391
  N490 --> N264
  N420 --> N199
  N487 --> N131
  N190 --> N106
  N125 --> N618
  N129 --> N548
  N626 --> N357
  N415 --> N607
  N397 --> N393
  N448 --> N204
  N213 --> N222
  N402 --> N205
  N264 --> N248
  N129 --> N467
  N443 --> N136
  N562 --> N205
  N134 --> N545
  N431 --> N388
  N337 --> N86
  N446 --> N295
  N498 --> N131
  N415 --> N585
  N457 --> N300
  N629 --> N630
  N117 --> N103
  N277 --> N270
  N374 --> N384
  N122 --> N610
  N170 --> N389
  N512 --> N118
  N543 --> N370
  N343 --> N222
  N298 --> N109
  N432 --> N222
  N577 --> N102
  N209 --> N106
  N517 --> N118
  N401 --> N586
  N340 --> N343
  N275 --> N104
  N193 --> N103
  N577 --> N350
  N562 --> N104
  N130 --> N547
  N175 --> N106
  N597 --> N95
  N133 --> N548
  N604 --> N205
  N494 --> N131
  N189 --> N92
  N201 --> N388
  N405 --> N109
  N481 --> N227
  N465 --> N299
  N544 --> N545
  N519 --> N264
  N566 --> N314
  N444 --> N292
  N268 --> N107
  N254 --> N116
  N264 --> N245
  N252 --> N326
  N401 --> N86
  N244 --> N426
  N603 --> N109
  N500 --> N131
  N297 --> N104
  N126 --> N118
  N350 --> N103
  N107 --> N110
  N230 --> N222
  N269 -. fd_ready .-> N21
  N331 --> N221
  N236 --> N518
  N307 --> N213
  N418 --> N199
  N269 -. fd_ready .-> N22
  N544 --> N104
  N193 --> N109
  N515 --> N86
  N344 -. fd_ready .-> N51
  N551 --> N86
  N408 --> N419
  N298 -. fd_ready .-> N631
  N335 --> N205
  N236 --> N224
  N406 --> N297
  N493 --> N268
  N98 --> N67
  N163 --> N86
  N236 --> N508
  N177 --> N69
  N613 --> N219
  N520 --> N118
  N544 --> N545
  N374 --> N380
  N577 --> N351
  N274 --> N610
  N550 --> N86
  N255 --> N250
  N179 --> N433
  N349 --> N106
  N298 --> N102
  N216 --> N548
  N444 --> N102
  N544 --> N546
  N576 --> N410
  N275 --> N546
  N577 --> N455
  N76 --> N160
  N274 --> N545
  N501 --> N118
  N390 --> N392
  N509 --> N264
  N208 --> N212
  N485 --> N131
  N176 --> N177
  N115 -. fd_ready .-> N63
  N193 --> N611
  N129 --> N549
  N518 --> N131
  N407 --> N457
  N437 --> N443
  N458 --> N102
  N399 --> N313
  N259 --> N426
  N207 --> N211
  N149 --> N148
  N227 --> N86
  N247 --> N580
  N373 --> N363
  N267 --> N102
  N611 --> N424
  N621 --> N450
  N344 --> N205
  N264 --> N244
  N518 --> N264
  N264 --> N260
  N354 -. fd_ready .-> N19
  N331 --> N460
  N268 --> N86
  N376 --> N361
  N216 --> N102
  N264 --> N234
  N347 --> N103
  N275 --> N86
  N135 --> N473
  N218 --> N106
  N354 -. fd_ready .-> N7
  N264 --> N259
  N402 --> N300
  N496 --> N264
  N456 --> N108
  N561 --> N295
  N520 --> N264
  N465 --> N222
  N319 --> N205
  N615 --> N531
  N478 --> N95
  N371 --> N311
  N544 --> N104
  N342 --> N549
  N129 --> N109
  N403 --> N405
  N550 --> N83
  N340 --> N549
  N392 --> N397
  N577 --> N117
  N625 --> N451
  N241 --> N278
  N528 --> N279
  N517 --> N264
  N619 --> N287
  N596 --> N314
  N507 --> N131
  N415 --> N86
  N562 --> N295
  N346 --> N221
  N269 -. fd_ready .-> N23
  N287 -. fd_ready .-> N2
  N131 --> N549
  N435 --> N106
  N228 --> N205
  N333 --> N401
  N505 --> N131
  N133 --> N547
  N193 --> N78
  N435 --> N292
  N597 --> N224
  N433 --> N438
  N274 --> N86
  N514 --> N95
  N193 --> N547
  N73 --> N72
  N277 -. fd_ready .-> N10
  N107 --> N104
  N88 --> N145
  N177 --> N104
  N208 --> N106
  N515 --> N89
  N562 --> N388
  N453 --> N438
  N570 --> N231
  N577 --> N214
  N243 --> N262
  N620 --> N386
  N165 --> N99
  N174 --> N176
  N152 --> N147
  N115 --> N86
  N285 --> N95
  N414 --> N222
  N135 --> N477
  N190 --> N107
  N275 --> N546
  N66 -. fd_ready .-> N3
  N249 --> N95
  N472 --> N290
  N607 --> N608
  N596 --> N221
  N390 --> N583
  N271 --> N95
  N472 --> N310
  N606 --> N408
  N615 --> N314
  N418 --> N301
  N300 --> N104
  N254 --> N86
  N593 --> N373
  N519 --> N131
  N232 --> N435
  N268 --> N218
  N193 --> N548
  N253 --> N86
  N214 --> N102
  N217 -. fd_ready .-> N11
  N508 --> N264
  N238 -. fd_ready .-> N37
  N273 --> N547
  N389 --> N205
  N331 --> N459
  N479 --> N221
  N467 --> N210
  N193 --> N106
  N350 --> N109
  N577 --> N348
  N230 --> N222
  N277 --> N548
  N407 --> N205
  N268 --> N548
  N392 --> N399
  N449 --> N148
  N171 --> N126
  N214 --> N98
  N119 --> N95
  N527 --> N549
  N188 --> N92
  N456 --> N109
  N172 --> N416
  N505 --> N118
  N75 --> N584
  N217 -. fd_ready .-> N14
  N285 --> N86
  N241 --> N261
  N232 --> N109
  N144 --> N539
  N544 --> N334
  N141 --> N86
  N415 --> N222
  N276 --> N547
  N157 --> N86
  N446 --> N103
  N351 --> N106
  N331 --> N459
  N153 --> N147
  N208 --> N109
  N446 --> N106
  N299 --> N102
  N605 --> N205
  N405 --> N103
  N343 --> N278
  N562 --> N205
  N153 --> N147
  N177 --> N109
  N69 -. fd_ready .-> N3
  N555 --> N554
  N385 --> N224
  N632 -. fd_ready .-> N237
  N632 -. fd_ready .-> N279
  N632 -. fd_ready .-> N283
  N632 -. fd_ready .-> N101
  N632 -. fd_ready .-> N113
  N633 -. fd_ready .-> N84
  N633 -. fd_ready .-> N264
  N633 -. fd_ready .-> N281
  N633 -. fd_ready .-> N284
  N633 -. fd_ready .-> N111
  N633 -. fd_ready .-> N114
  N631 -. fd_ready .-> N209
  N631 -. fd_ready .-> N238
  N631 -. fd_ready .-> N324
  N631 -. fd_ready .-> N353
  N631 -. fd_ready .-> N362
  N631 -. fd_ready .-> N407
  N631 -. fd_ready .-> N437
  N631 -. fd_ready .-> N362
  N631 -. fd_ready .-> N362
  N631 -. fd_ready .-> N362
  N631 -. fd_ready .-> N362
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
仓库由 core、include、src、unix、uv 组成。入口负责初始化运行时、注册回调并驱动主循环；事件循环组件负责等待就绪事件、遍历句柄并分发回调。

## 关键调用链
入口 `uv_run` 的关键路径是：`uv_run -> uv__io_poll`。

## 异步回调链
fd_ready 事件在 third_party/libuv/src/heap-inl.h:222 触发回调，但候选为空，需要进一步分析。

## 函数指针
静态分析发现回调字段存在多个候选：`uv__async_io、uv__cancelled、uv__fs_done、uv__fs_event、uv__fs_work、uv__getaddrinfo_done、uv__getaddrinfo_work、uv__getnameinfo_done、uv__getnameinfo_work、uv__poll_io、uv__queue_done、uv__queue_work、uv__random_done、uv__random_work、uv__server_io、uv__signal_event、uv__stream_io、uv__udp_io`，无法唯一确定目标，置信度为 0.30。

## 复杂宏
本次分析覆盖：ACCESS_ONCE (third_party/libuv/test/benchmark-async-pummel.c:29)、ARRAY_END (third_party/libuv/src/uv-common.h:55)、ARRAY_SIZE (third_party/libuv/src/uv-common.h:54)、EV_OOBAND (third_party/libuv/src/unix/kqueue.c:48)、F_OK (third_party/libuv/include/uv/win.h:659)、INIT (third_party/libuv/src/unix/fs.c:90)、UV_EXTERN (third_party/libuv/include/uv.h:39)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 79%，报告状态为 not ready；所有结论均引用源码文件、行号和原始代码片段。

## 异步回调链

- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/poll.c:64` -> `third_party/libuv/src/unix/poll.c:64` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/async.c:208` -> `third_party/libuv/src/unix/async.c:208` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:463` -> `third_party/libuv/src/unix/fsevents.c:463` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/random.c:116` -> `third_party/libuv/src/threadpool.c:330` -> callbacks: uv__fs_done, uv__getaddrinfo_done, uv__getnameinfo_done, uv__queue_done, uv__random_done
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:299` -> `third_party/libuv/src/threadpool.c:123` -> callbacks: uv__cancelled, uv__fs_work, uv__getaddrinfo_work, uv__getnameinfo_work, uv__queue_work, uv__random_work
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:1778` -> `third_party/libuv/src/unix/fs.c:1778` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:461` -> `third_party/libuv/src/unix/stream.c:461` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:269` -> `third_party/libuv/src/unix/udp.c:269` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:125` -> `third_party/libuv/src/unix/udp.c:125` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/poll.c:50` -> `third_party/libuv/src/unix/poll.c:50` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:927` -> `third_party/libuv/src/unix/stream.c:927` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:206` -> `third_party/libuv/src/unix/udp.c:206` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:146` -> `third_party/libuv/src/unix/darwin-proctitle.c:146` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:393` -> `third_party/libuv/src/unix/fsevents.c:393` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:622` -> `third_party/libuv/src/unix/fsevents.c:622` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:365` -> `third_party/libuv/src/threadpool.c:365` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:938` -> `third_party/libuv/src/unix/stream.c:938` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:195` -> `third_party/libuv/src/unix/udp.c:195` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:371` -> `third_party/libuv/src/unix/fsevents.c:371` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:271` -> `third_party/libuv/src/unix/udp.c:271` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/core.c:854` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:215` -> `third_party/libuv/src/unix/udp.c:215` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:159` -> `third_party/libuv/src/unix/darwin-proctitle.c:159` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/getaddrinfo.c:134` -> `third_party/libuv/src/unix/getaddrinfo.c:134` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:93` -> `third_party/libuv/src/uv-common.c:93` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:77` -> `third_party/libuv/src/uv-common.c:77` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:494` -> `third_party/libuv/src/unix/fs.c:494` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:224` -> `third_party/libuv/src/heap-inl.h:224` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:241` -> `third_party/libuv/src/unix/udp.c:241` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:372` -> `third_party/libuv/src/unix/fsevents.c:372` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:278` -> `third_party/libuv/src/unix/udp.c:278` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:698` -> `third_party/libuv/src/unix/fsevents.c:698` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/signal.c:478` -> `third_party/libuv/src/unix/signal.c:478` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:188` -> `third_party/libuv/src/unix/fsevents.c:188` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:782` -> `third_party/libuv/src/unix/fsevents.c:782` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/process.c:174` -> `third_party/libuv/src/unix/process.c:174` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:189` -> `third_party/libuv/src/unix/fsevents.c:189` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:130` -> `third_party/libuv/src/unix/darwin-proctitle.c:130` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:476` -> `third_party/libuv/src/unix/fsevents.c:476` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/threadpool.c:352` -> `third_party/libuv/src/threadpool.c:352` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/random-getentropy.c:53` -> `third_party/libuv/src/unix/random-getentropy.c:53` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/core.c:363` -> `third_party/libuv/src/unix/core.c:363` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:197` -> `third_party/libuv/src/unix/udp.c:197` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:88` -> `third_party/libuv/src/uv-common.c:88` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/process.c:552` -> `third_party/libuv/src/unix/process.c:552` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:149` -> `third_party/libuv/src/unix/darwin-proctitle.c:149` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/fs-poll.c:202` -> `third_party/libuv/src/fs-poll.c:202` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:66` -> `third_party/libuv/src/unix/loop-watcher.c:66` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:720` -> `third_party/libuv/src/unix/fsevents.c:720` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/random.c:90` -> `third_party/libuv/src/random.c:90` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:68` -> `third_party/libuv/src/unix/loop-watcher.c:68` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fs.c:329` -> `third_party/libuv/src/unix/fs.c:329` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:568` -> `third_party/libuv/src/uv-common.c:568` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/getnameinfo.c:73` -> `third_party/libuv/src/unix/getnameinfo.c:73` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:894` -> `third_party/libuv/src/unix/fsevents.c:894` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1283` -> `third_party/libuv/src/unix/stream.c:1283` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:379` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/random-getentropy.c:50` -> `third_party/libuv/src/unix/random-getentropy.c:50` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:235` -> `third_party/libuv/src/heap-inl.h:235` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> `third_party/libuv/src/unix/darwin-proctitle.c:96` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:138` -> `third_party/libuv/src/unix/darwin-proctitle.c:138` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1052` -> `third_party/libuv/src/unix/stream.c:1052` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:657` -> `third_party/libuv/src/unix/stream.c:657` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1055` -> `third_party/libuv/src/unix/stream.c:1055` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:110` -> `third_party/libuv/src/unix/darwin-proctitle.c:110` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:243` -> `third_party/libuv/src/unix/udp.c:243` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:128` -> `third_party/libuv/src/unix/darwin-proctitle.c:128` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:443` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:451` -> `third_party/libuv/src/unix/fsevents.c:451` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1092` -> `third_party/libuv/src/unix/stream.c:1092` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:109` -> `third_party/libuv/src/unix/darwin-proctitle.c:109` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:389` -> `third_party/libuv/src/unix/fsevents.c:389` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/fs-poll.c:215` -> `third_party/libuv/src/fs-poll.c:215` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:102` -> `third_party/libuv/src/unix/darwin-proctitle.c:102` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:156` -> `third_party/libuv/src/unix/darwin-proctitle.c:156` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:528` -> `third_party/libuv/src/unix/stream.c:528` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/loop-watcher.c:67` -> `third_party/libuv/src/unix/loop-watcher.c:67` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/udp.c:123` -> `third_party/libuv/src/unix/udp.c:123` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:781` -> `third_party/libuv/src/unix/fsevents.c:781` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/timer.c:193` -> `third_party/libuv/src/timer.c:193` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:711` -> `third_party/libuv/src/unix/fsevents.c:711` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:115` -> `third_party/libuv/src/unix/darwin-proctitle.c:115` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1120` -> `third_party/libuv/src/unix/stream.c:1120` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:143` -> `third_party/libuv/src/unix/darwin-proctitle.c:143` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> `third_party/libuv/src/unix/darwin-proctitle.c:147` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1148` -> `third_party/libuv/src/unix/stream.c:1148` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:392` -> `third_party/libuv/src/unix/fsevents.c:392` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:369` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:753` -> `third_party/libuv/src/unix/fsevents.c:753` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:103` -> `third_party/libuv/src/unix/darwin-proctitle.c:103` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:362` -> `third_party/libuv/src/unix/fsevents.c:362` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:373` -> `third_party/libuv/src/unix/fsevents.c:373` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/stream.c:1101` -> `third_party/libuv/src/unix/stream.c:1101` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/pipe.c:171` -> `third_party/libuv/src/unix/kqueue.c:423` -> callbacks: uv__async_io, uv__fs_event, uv__poll_io, uv__server_io, uv__signal_event, uv__stream_io, uv__udp_io
  - Confidence: 0.60, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/uv-common.c:98` -> `third_party/libuv/src/uv-common.c:98` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:116` -> `third_party/libuv/src/unix/darwin-proctitle.c:116` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/darwin-proctitle.c:136` -> `third_party/libuv/src/unix/darwin-proctitle.c:136` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:374` -> `third_party/libuv/src/unix/fsevents.c:374` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/core.c:1815` -> `third_party/libuv/src/unix/core.c:1815` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:480` -> `third_party/libuv/src/unix/fsevents.c:480` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:146` -> `third_party/libuv/src/heap-inl.h:146` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:713` -> `third_party/libuv/src/unix/fsevents.c:713` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/kqueue.c:545` -> `third_party/libuv/src/unix/kqueue.c:545` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/unix/fsevents.c:719` -> `third_party/libuv/src/unix/fsevents.c:719` -> callbacks: 
  - Confidence: 0.30, loop back: True
- `third_party/libuv/src/fs-poll.c:43` `fd_ready` -> `third_party/libuv/src/heap-inl.h:222` -> `third_party/libuv/src/heap-inl.h:222` -> callbacks: 
  - Confidence: 0.30, loop back: True

## 函数指针候选

- `uv_poll_s::poll_cb` @ `third_party/libuv/src/unix/poll.c:64`
  - Candidates: 
  - Confidence: 0.30
- `uv_async_s::async_cb` @ `third_party/libuv/src/unix/async.c:208`
  - Candidates: 
  - Confidence: 0.30
- `pCFArrayCreate` @ `third_party/libuv/src/unix/fsevents.c:463`
  - Candidates: 
  - Confidence: 0.30
- `uv__work::done` @ `third_party/libuv/src/threadpool.c:330`
  - Candidates: `uv__fs_done` (third_party/libuv/src/unix/fs.c:1767), `uv__getaddrinfo_done` (third_party/libuv/src/unix/getaddrinfo.c:108), `uv__getnameinfo_done` (third_party/libuv/src/unix/getnameinfo.c:55), `uv__queue_done` (third_party/libuv/src/threadpool.c:356), `uv__random_done` (third_party/libuv/src/random.c:81)
  - Confidence: 0.60
- `uv__work::work` @ `third_party/libuv/src/threadpool.c:123`
  - Candidates: `uv__cancelled` (third_party/libuv/src/threadpool.c:49), `uv__fs_work` (third_party/libuv/src/unix/fs.c:1695), `uv__getaddrinfo_work` (third_party/libuv/src/unix/getaddrinfo.c:98), `uv__getnameinfo_work` (third_party/libuv/src/unix/getnameinfo.c:31), `uv__queue_work` (third_party/libuv/src/threadpool.c:349), `uv__random_work` (third_party/libuv/src/random.c:73)
  - Confidence: 0.60
- `uv_fs_s::cb` @ `third_party/libuv/src/unix/fs.c:1778`
  - Candidates: 
  - Confidence: 0.30
- `uv_connect_s::cb` @ `third_party/libuv/src/unix/stream.c:461`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:269`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_send_s::send_cb` @ `third_party/libuv/src/unix/udp.c:125`
  - Candidates: 
  - Confidence: 0.30
- `uv_poll_s::poll_cb` @ `third_party/libuv/src/unix/poll.c:50`
  - Candidates: 
  - Confidence: 0.30
- `uv_write_s::cb` @ `third_party/libuv/src/unix/stream.c:927`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:206`
  - Candidates: 
  - Confidence: 0.30
- `pLSApplicationCheckIn` @ `third_party/libuv/src/unix/darwin-proctitle.c:146`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:96`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamRelease` @ `third_party/libuv/src/unix/fsevents.c:393`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopSourceCreate` @ `third_party/libuv/src/unix/fsevents.c:622`
  - Candidates: 
  - Confidence: 0.30
- `uv_work_s::after_work_cb` @ `third_party/libuv/src/threadpool.c:365`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:938`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetInfoDictionary` @ `third_party/libuv/src/unix/darwin-proctitle.c:147`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:195`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamScheduleWithRunLoop` @ `third_party/libuv/src/unix/fsevents.c:371`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:271`
  - Candidates: 
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/core.c:854`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:215`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:159`
  - Candidates: 
  - Confidence: 0.30
- `uv_getaddrinfo_s::cb` @ `third_party/libuv/src/unix/getaddrinfo.c:134`
  - Candidates: 
  - Confidence: 0.30
- `uv__allocator_t::local_calloc` @ `third_party/libuv/src/uv-common.c:93`
  - Candidates: 
  - Confidence: 0.30
- `uv__allocator_t::local_malloc` @ `third_party/libuv/src/uv-common.c:77`
  - Candidates: 
  - Confidence: 0.30
- `f` @ `third_party/libuv/src/unix/fs.c:494`
  - Candidates: 
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:224`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::alloc_cb` @ `third_party/libuv/src/unix/udp.c:241`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamStart` @ `third_party/libuv/src/unix/fsevents.c:372`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:278`
  - Candidates: 
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:698`
  - Candidates: 
  - Confidence: 0.30
- `uv_signal_s::signal_cb` @ `third_party/libuv/src/unix/signal.c:478`
  - Candidates: 
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:188`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopWakeUp` @ `third_party/libuv/src/unix/fsevents.c:782`
  - Candidates: 
  - Confidence: 0.30
- `uv_process_s::exit_cb` @ `third_party/libuv/src/unix/process.c:174`
  - Candidates: 
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:189`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:130`
  - Candidates: 
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:476`
  - Candidates: 
  - Confidence: 0.30
- `uv_work_s::work_cb` @ `third_party/libuv/src/threadpool.c:352`
  - Candidates: 
  - Confidence: 0.30
- `uv__getentropy` @ `third_party/libuv/src/unix/random-getentropy.c:53`
  - Candidates: 
  - Confidence: 0.30
- `uv_handle_s::close_cb` @ `third_party/libuv/src/unix/core.c:363`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:197`
  - Candidates: 
  - Confidence: 0.30
- `uv__allocator_t::local_free` @ `third_party/libuv/src/uv-common.c:88`
  - Candidates: 
  - Confidence: 0.30
- `uv__posix_spawn_fncs_tag::struct (unnamed at /Users/andye/Documents/ChatGPT/8.18huawei/third_party/libuv/src/unix/process.c:409:3)::addchdir_np` @ `third_party/libuv/src/unix/process.c:552`
  - Candidates: 
  - Confidence: 0.30
- `pLSGetCurrentApplicationASN` @ `third_party/libuv/src/unix/darwin-proctitle.c:149`
  - Candidates: 
  - Confidence: 0.30
- `poll_ctx::poll_cb` @ `third_party/libuv/src/fs-poll.c:202`
  - Candidates: 
  - Confidence: 0.30
- `uv_prepare_s::prepare_cb` @ `third_party/libuv/src/unix/loop-watcher.c:66`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopRemoveSource` @ `third_party/libuv/src/unix/fsevents.c:720`
  - Candidates: 
  - Confidence: 0.30
- `uv_random_s::cb` @ `third_party/libuv/src/random.c:90`
  - Candidates: 
  - Confidence: 0.30
- `uv_idle_s::idle_cb` @ `third_party/libuv/src/unix/loop-watcher.c:68`
  - Candidates: 
  - Confidence: 0.30
- `uv__mkostemp` @ `third_party/libuv/src/unix/fs.c:329`
  - Candidates: 
  - Confidence: 0.30
- `walk_cb` @ `third_party/libuv/src/uv-common.c:568`
  - Candidates: 
  - Confidence: 0.30
- `uv_getnameinfo_s::getnameinfo_cb` @ `third_party/libuv/src/unix/getnameinfo.c:73`
  - Candidates: 
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/fsevents.c:894`
  - Candidates: 
  - Confidence: 0.30
- `uv_connect_s::cb` @ `third_party/libuv/src/unix/stream.c:1283`
  - Candidates: 
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:379`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv__getentropy` @ `third_party/libuv/src/unix/random-getentropy.c:50`
  - Candidates: 
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:235`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetBundleWithIdentifier` @ `third_party/libuv/src/unix/darwin-proctitle.c:96`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:138`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::alloc_cb` @ `third_party/libuv/src/unix/stream.c:1052`
  - Candidates: 
  - Confidence: 0.30
- `uv_shutdown_s::cb` @ `third_party/libuv/src/unix/stream.c:657`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1055`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:110`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_s::recv_cb` @ `third_party/libuv/src/unix/udp.c:243`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:128`
  - Candidates: 
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:443`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `pCFStringCreateWithFileSystemRepresentation` @ `third_party/libuv/src/unix/fsevents.c:451`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1092`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:109`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamStop` @ `third_party/libuv/src/unix/fsevents.c:389`
  - Candidates: 
  - Confidence: 0.30
- `poll_ctx::poll_cb` @ `third_party/libuv/src/fs-poll.c:215`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:102`
  - Candidates: 
  - Confidence: 0.30
- `pLSSetApplicationInformationItem` @ `third_party/libuv/src/unix/darwin-proctitle.c:156`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::connection_cb` @ `third_party/libuv/src/unix/stream.c:528`
  - Candidates: 
  - Confidence: 0.30
- `uv_check_s::check_cb` @ `third_party/libuv/src/unix/loop-watcher.c:67`
  - Candidates: 
  - Confidence: 0.30
- `uv_udp_send_s::send_cb` @ `third_party/libuv/src/unix/udp.c:123`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopSourceSignal` @ `third_party/libuv/src/unix/fsevents.c:781`
  - Candidates: 
  - Confidence: 0.30
- `uv_timer_s::timer_cb` @ `third_party/libuv/src/timer.c:193`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopGetCurrent` @ `third_party/libuv/src/unix/fsevents.c:711`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetDataPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:115`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1120`
  - Candidates: 
  - Confidence: 0.30
- `pLSSetApplicationLaunchServicesServerConnectionStatus` @ `third_party/libuv/src/unix/darwin-proctitle.c:143`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetMainBundle` @ `third_party/libuv/src/unix/darwin-proctitle.c:147`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1148`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamInvalidate` @ `third_party/libuv/src/unix/fsevents.c:392`
  - Candidates: 
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:369`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `pCFRunLoopStop` @ `third_party/libuv/src/unix/fsevents.c:753`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:103`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamCreate` @ `third_party/libuv/src/unix/fsevents.c:362`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamInvalidate` @ `third_party/libuv/src/unix/fsevents.c:373`
  - Candidates: 
  - Confidence: 0.30
- `uv_stream_s::read_cb` @ `third_party/libuv/src/unix/stream.c:1101`
  - Candidates: 
  - Confidence: 0.30
- `uv__io_s::cb` @ `third_party/libuv/src/unix/kqueue.c:423`
  - Candidates: `uv__async_io` (third_party/libuv/src/unix/async.c:160), `uv__fs_event` (third_party/libuv/src/unix/kqueue.c:499), `uv__poll_io` (third_party/libuv/src/unix/poll.c:30), `uv__server_io` (third_party/libuv/src/unix/stream.c:508), `uv__signal_event` (third_party/libuv/src/unix/signal.c:433), `uv__stream_io` (third_party/libuv/src/unix/stream.c:1189), `uv__udp_io` (third_party/libuv/src/unix/udp.c:139)
  - Confidence: 0.60
- `uv__allocator_t::local_realloc` @ `third_party/libuv/src/uv-common.c:98`
  - Candidates: 
  - Confidence: 0.30
- `pCFStringCreateWithCString` @ `third_party/libuv/src/unix/darwin-proctitle.c:116`
  - Candidates: 
  - Confidence: 0.30
- `pCFBundleGetFunctionPointerForName` @ `third_party/libuv/src/unix/darwin-proctitle.c:136`
  - Candidates: 
  - Confidence: 0.30
- `pFSEventStreamRelease` @ `third_party/libuv/src/unix/fsevents.c:374`
  - Candidates: 
  - Confidence: 0.30
- `func` @ `third_party/libuv/src/unix/core.c:1815`
  - Candidates: 
  - Confidence: 0.30
- `pCFRelease` @ `third_party/libuv/src/unix/fsevents.c:480`
  - Candidates: 
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:146`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopAddSource` @ `third_party/libuv/src/unix/fsevents.c:713`
  - Candidates: 
  - Confidence: 0.30
- `uv_fs_event_s::cb` @ `third_party/libuv/src/unix/kqueue.c:545`
  - Candidates: 
  - Confidence: 0.30
- `pCFRunLoopRun` @ `third_party/libuv/src/unix/fsevents.c:719`
  - Candidates: 
  - Confidence: 0.30
- `less_than` @ `third_party/libuv/src/heap-inl.h:222`
  - Candidates: 
  - Confidence: 0.30

## 宏分析

| macro | file:line | definition | call sites |
| --- | --- | --- | --- |

## Evidence

| id | kind | file:line | snippet |
| --- | --- | --- | --- |
| `ev_0099a80275c3` | call_site | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_00e9ac8a4910` | call_site | `third_party/libuv/src/unix/core.c:982` | `uv__platform_invalidate_fd(loop, w->fd);` |
| `ev_00f2122909b4` | call_site | `third_party/libuv/src/unix/udp.c:71` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_00f7eb56e9b1` | call_site | `third_party/libuv/src/unix/signal.c:549` | `uv__signal_block_and_lock(&saved_sigmask);` |
| `ev_01191424f420` | call_site | `third_party/libuv/src/unix/async.c:395` | `uv__close(loop->async_io_watcher.fd);` |
| `ev_012033a59c71` | call_site | `third_party/libuv/src/unix/core.c:207` | `uv__fs_event_close((uv_fs_event_t*)handle);` |
| `ev_0146c582c419` | call_site | `third_party/libuv/src/unix/signal.c:304` | `return uv__signal_loop_once_init(loop);` |
| `ev_01aff5894276` | call_site | `third_party/libuv/src/unix/kqueue.c:648` | `uv__io_close(handle->loop, &handle->event_watcher);` |
| `ev_01d3a88243c6` | call_site | `third_party/libuv/src/unix/pipe.c:464` | `r = uv_pipe_getsockname(handle, name_buffer, &name_len);` |
| `ev_01e85e2afc3f` | call_site | `third_party/libuv/src/unix/core.c:1300` | `pwd->username = uv__malloc(name_size + homedir_size + shell_size);` |
| `ev_02531d0740c8` | call_site | `third_party/libuv/src/unix/tcp.c:626` | `uv__stream_close((uv_stream_t*)handle);` |
| `ev_0279a97cd469` | call_site | `third_party/libuv/src/unix/fs.c:324` | `uv_once(&once, uv__mkostemp_initonce);` |
| `ev_02985e12ffba` | call_site | `third_party/libuv/src/unix/udp.c:618` | `if (!uv__queue_empty(&handle->write_queue))` |
| `ev_02b7456f70d9` | call_site | `third_party/libuv/src/unix/random-getentropy.c:50` | `if (uv__getentropy((char *) buf + pos, stride))` |
| `ev_02c74b2207ca` | call_site | `third_party/libuv/src/heap-inl.h:240` | `heap_remove(heap, heap->min, less_than);` |
| `ev_02ea4b5938e9` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_0314cf1dc8db` | call_site | `third_party/libuv/src/unix/fs.c:781` | `uv__free(buf);` |
| `ev_035fa2815964` | call_site | `third_party/libuv/src/unix/stream.c:630` | `assert(uv__queue_empty(&stream->write_queue));` |
| `ev_0364e38a089a` | call_site | `third_party/libuv/src/unix/kqueue.c:624` | `uv__io_init(&handle->event_watcher, uv__fs_event, fd);` |
| `ev_036f33a2ad9c` | call_site | `third_party/libuv/src/unix/stream.c:1060` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_03874c5ae3f7` | call_site | `third_party/libuv/src/unix/async.c:301` | `err = uv__make_pipe(pipefd, UV_NONBLOCK_PIPE);` |
| `ev_03906ae61fe0` | call_site | `third_party/libuv/src/unix/stream.c:855` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_0393d9427046` | call_site | `third_party/libuv/src/unix/stream.c:1200` | `uv__stream_connect(stream);` |
| `ev_04087c5005c8` | call_site | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_0427e78eb346` | call_site | `third_party/libuv/src/unix/core.c:1322` | `uv__free(buf);` |
| `ev_042b369b6a2c` | call_site | `third_party/libuv/src/unix/process.c:792` | `err = uv__spawn_resolve_and_spawn(options, &attrs, &actions, pid);` |
| `ev_043a1f8589cf` | call_site | `third_party/libuv/src/threadpool.c:125` | `uv_mutex_lock(&w->loop->wq_mutex);` |
| `ev_048840dd2d4c` | call_site | `third_party/libuv/src/unix/udp.c:608` | `uv__queue_insert_tail(&handle->write_queue, &req->queue);` |
| `ev_04b38854c433` | call_site | `third_party/libuv/src/unix/stream.c:444` | `q = uv__queue_head(&stream->write_queue);` |
| `ev_04f9e46838a6` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_051b2ccc6da3` | call_site | `third_party/libuv/src/unix/process.c:1069` | `uv__close_nocheckstdio(pipes[i][0]);` |
| `ev_052fa201b701` | call_site | `third_party/libuv/src/unix/udp.c:80` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_0599dac89e4b` | call_site | `third_party/libuv/src/unix/udp.c:249` | `nread = uv__udp_recvmmsg(handle, &buf);` |
| `ev_06390490032e` | call_site | `third_party/libuv/src/unix/fsevents.c:784` | `uv_mutex_unlock(&loop->cf_mutex);` |
| `ev_069cf24160a2` | call_site | `third_party/libuv/src/unix/udp.c:1203` | `if (uv__io_active(&handle->io_watcher, POLLIN))` |
| `ev_069ecdbb3330` | call_site | `third_party/libuv/src/thread-common.c:76` | `uv_mutex_destroy(&b->mutex);` |
| `ev_06c512c5551c` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_06d4479a269e` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_06fccd917d92` | call_site | `third_party/libuv/src/unix/stream.c:1417` | `return uv_try_write2(stream, bufs, nbufs, NULL);` |
| `ev_070f7f7cab78` | call_site | `third_party/libuv/src/unix/core.c:203` | `uv__process_close((uv_process_t*)handle);` |
| `ev_071e3c08967f` | call_site | `third_party/libuv/src/unix/core.c:1200` | `uv_os_free_passwd(&pwd);` |
| `ev_0765f48cee8c` | call_site | `third_party/libuv/src/thread-common.c:146` | `uv__free(barrier->b);` |
| `ev_078c1e540b51` | call_site | `third_party/libuv/src/unix/process.c:979` | `uv__queue_init(&process->queue);` |
| `ev_07b965b1f445` | call_site | `third_party/libuv/src/unix/process.c:149` | `uv__queue_remove(&process->queue);` |
| `ev_07f77952c987` | call_site | `third_party/libuv/src/unix/async.c:81` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_ASYNC);` |
| `ev_08156833025e` | call_site | `third_party/libuv/src/uv-common.c:296` | `return uv_inet_pton(AF_INET6, ip, &addr->sin6_addr);` |
| `ev_0821a6ac16cc` | call_site | `third_party/libuv/src/thread-common.c:99` | `uv_mutex_lock(&b->mutex);` |
| `ev_08567c743fbb` | call_site | `third_party/libuv/src/unix/tcp.c:343` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_0875828abb2f` | call_site | `third_party/libuv/src/unix/process.c:1000` | `err = uv__process_init_stdio(options->stdio + i, pipes[i]);` |
| `ev_087672101eb1` | call_site | `third_party/libuv/src/unix/fsevents.c:857` | `uv__free(handle->realpath);` |
| `ev_088b3589a37e` | call_site | `third_party/libuv/src/unix/fsevents.c:463` | `cf_paths = pCFArrayCreate(NULL, (const void**) paths, path_count, NULL);` |
| `ev_08973798df7c` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:104` | `req->retcode = uv__getaddrinfo_translate_error(err);` |
| `ev_08d113fd8759` | call_site | `third_party/libuv/src/threadpool.c:180` | `if (uv_thread_join(threads + i))` |
| `ev_08d9b95f8371` | call_site | `third_party/libuv/src/unix/stream.c:450` | `uv__queue_insert_tail(&stream->write_completed_queue, &req->queue);` |
| `ev_08ebbe24d60d` | call_site | `third_party/libuv/src/threadpool.c:83` | `uv_cond_signal(&cond);` |
| `ev_0914e47376ef` | call_site | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_09154c6d60e1` | call_site | `third_party/libuv/src/unix/core.c:935` | `if (uv__queue_empty(&w->watcher_queue))` |
| `ev_093829324527` | call_site | `third_party/libuv/src/unix/fs.c:2279` | `uv__free(req->bufs);` |
| `ev_097ed80f1651` | call_site | `third_party/libuv/src/unix/udp.c:149` | `uv__udp_sendmsg(handle);` |
| `ev_09b661c71631` | call_site | `third_party/libuv/src/unix/core.c:1178` | `r = uv_os_getenv("HOME", buffer, size);` |
| `ev_09d049855a37` | call_site | `third_party/libuv/src/unix/stream.c:871` | `uv__write_req_finish(req);` |
| `ev_09e35b70d7ff` | call_site | `third_party/libuv/src/unix/kqueue.c:442` | `uv__metrics_update_idle_time(loop);` |
| `ev_0a02e3d53aed` | call_site | `third_party/libuv/src/unix/fsevents.c:753` | `pCFRunLoopStop(state->loop);` |
| `ev_0a723121eb46` | call_site | `third_party/libuv/src/unix/pipe.c:152` | `if (uv__stream_fd(handle) == -1)` |
| `ev_0ac74bc0d37b` | call_site | `third_party/libuv/src/unix/fs.c:2173` | `PATH;` |
| `ev_0add7b33578b` | call_site | `third_party/libuv/src/uv-common.c:660` | `return uv__socket_sockopt(handle, SO_SNDBUF, value);` |
| `ev_0ae131588cf4` | call_site | `third_party/libuv/src/unix/udp.c:374` | `err = uv__socket(addr->sa_family, SOCK_DGRAM, 0);` |
| `ev_0ae206425830` | call_site | `third_party/libuv/src/unix/core.c:477` | `uv__update_time(loop);` |
| `ev_0aed3132411a` | call_site | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_0b32440d409b` | call_site | `third_party/libuv/src/unix/stream.c:1360` | `uv__queue_init(&req->queue);` |
| `ev_0b850cbf1e7c` | call_site | `third_party/libuv/src/unix/fs.c:1736` | `X(READDIR, uv__fs_readdir(req));` |
| `ev_0ba616e1022a` | call_site | `third_party/libuv/src/unix/loop.c:123` | `uv__free(lfields);` |
| `ev_0c3d62e20202` | call_site | `third_party/libuv/src/unix/stream.c:770` | `iovmax = uv__getiovmax();` |
| `ev_0c52da5265f1` | assignment | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_0c807921a91f` | call_site | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_0cad6778fed2` | call_site | `third_party/libuv/src/unix/proctitle.c:139` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_0ccc461ace9e` | call_site | `third_party/libuv/src/threadpool.c:294` | `uv_mutex_unlock(&mutex);` |
| `ev_0d62d8f5e472` | call_site | `third_party/libuv/src/unix/fs.c:361` | `uv_rwlock_rdunlock(&req->loop->cloexec_lock);` |
| `ev_0d7e53814be3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_0da8802e9929` | call_site | `third_party/libuv/src/unix/stream.c:396` | `uv__close(fds[1]);` |
| `ev_0dc2ddae96f7` | call_site | `third_party/libuv/src/unix/kqueue.c:661` | `uv_fs_event_stop(handle);` |
| `ev_0dc31ccdc432` | call_site | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_0dd7009b3894` | call_site | `third_party/libuv/src/uv-common.c:981` | `uv__threadpool_cleanup();` |
| `ev_0de39aac0beb` | call_site | `third_party/libuv/src/unix/process.c:150` | `uv__queue_insert_tail(&pending, &process->queue);` |
| `ev_0e410bb4266d` | call_site | `third_party/libuv/src/unix/stream.c:309` | `uv__close(kq);` |
| `ev_0e54f9990020` | call_site | `third_party/libuv/src/timer.c:100` | `heap_remove(timer_heap(handle->loop),` |
| `ev_0e731eb327a2` | call_site | `third_party/libuv/src/unix/kqueue.c:545` | `handle->cb(handle, path, events, 0);` |
| `ev_0e7f5d7e79fe` | call_site | `third_party/libuv/src/thread-common.c:142` | `uv_mutex_destroy(&b->mutex);` |
| `ev_0e9038561362` | call_site | `third_party/libuv/src/unix/poll.c:99` | `return uv_poll_init(loop, handle, socket);` |
| `ev_0efc91732fce` | call_site | `third_party/libuv/src/unix/fs.c:199` | `return uv__fs_fsync(req);` |
| `ev_0f2dc5cbb7f1` | call_site | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_0f3c91f9fb8a` | call_site | `third_party/libuv/src/unix/core.c:1920` | `uv__free(cloned_path);` |
| `ev_0f57ac66b50d` | call_site | `third_party/libuv/src/unix/fsevents.c:825` | `uv_async_init(handle->loop, handle->cf_cb, uv__fsevents_cb);` |
| `ev_0f5d759ead61` | call_site | `third_party/libuv/src/uv-common.c:834` | `err = uv__loop_configure(loop, option, ap);` |
| `ev_0f5fafde2d68` | call_site | `third_party/libuv/src/unix/stream.c:1459` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_0f84d8f546f4` | call_site | `third_party/libuv/src/unix/fsevents.c:690` | `uv__queue_remove(q);` |
| `ev_100056da66f7` | call_site | `third_party/libuv/src/unix/signal.c:560` | `uv__signal_unregister_handler(handle->signum);` |
| `ev_1001cb55f96d` | call_site | `third_party/libuv/src/unix/core.c:167` | `uv__pipe_close((uv_pipe_t*)handle);` |
| `ev_101b07054235` | call_site | `third_party/libuv/src/unix/stream.c:1055` | `stream->read_cb(stream, UV_ENOBUFS, &buf);` |
| `ev_10338a425d04` | call_site | `third_party/libuv/src/unix/fs.c:2053` | `req->bufs = uv__malloc(nbufs * sizeof(*bufs));` |
| `ev_10739f1bfcae` | call_site | `third_party/libuv/src/unix/udp.c:927` | `} else if (uv_ip6_addr(multicast_addr, 0, &addr6) == 0) {` |
| `ev_10a4f102c0a2` | call_site | `third_party/libuv/src/unix/process.c:118` | `q = uv__queue_next(q);` |
| `ev_11b2b673095b` | call_site | `third_party/libuv/src/unix/loop.c:94` | `err = uv_mutex_init(&loop->wq_mutex);` |
| `ev_11c0728870bb` | call_site | `third_party/libuv/src/unix/pipe.c:135` | `uv__close(sockfd);` |
| `ev_11cd93e668d8` | call_site | `third_party/libuv/src/unix/async.c:86` | `uv__queue_insert_tail(&loop->async_handles, &handle->queue);` |
| `ev_11e0852d6f59` | call_site | `third_party/libuv/src/unix/core.c:1274` | `buf = uv__malloc(bufsize);` |
| `ev_11edff8b9729` | call_site | `third_party/libuv/src/unix/signal.c:198` | `handle = RB_NEXT(uv__signal_tree_s, handle)) {` |
| `ev_11fda6899df4` | call_site | `third_party/libuv/src/threadpool.c:113` | `if (!uv__queue_empty(&slow_io_pending_wq)) {` |
| `ev_12184091e12a` | call_site | `third_party/libuv/src/unix/stream.c:1064` | `nread = read(uv__stream_fd(stream), buf.base, buf.len);` |
| `ev_1234eba3e0db` | call_site | `third_party/libuv/src/unix/process.c:252` | `uv__stream_close(container->data.stream);` |
| `ev_123f68ab8359` | call_site | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_124c685c2158` | assignment | `third_party/libuv/src/unix/pipe.c:171` | `handle->io_watcher.cb = uv__server_io;` |
| `ev_1277a4f1694e` | call_site | `third_party/libuv/src/unix/core.c:854` | `w->cb(loop, w, POLLOUT);` |
| `ev_12fb150da2f1` | call_site | `third_party/libuv/src/unix/stream.c:1372` | `stream->write_queue_size += uv__count_bufs(bufs, nbufs);` |
| `ev_12fb7ada444f` | call_site | `third_party/libuv/src/threadpool.c:84` | `uv_mutex_unlock(&mutex);` |
| `ev_1320b044b486` | call_site | `third_party/libuv/src/unix/kqueue.c:422` | `uv__metrics_update_idle_time(loop);` |
| `ev_13668eda86db` | call_site | `third_party/libuv/src/unix/stream.c:102` | `err = uv__open_cloexec("/dev/null", O_RDONLY);` |
| `ev_13917c12f56a` | call_site | `third_party/libuv/src/uv-common.c:1005` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_13a15aaa8721` | call_site | `third_party/libuv/src/unix/poll.c:150` | `uv__io_start(handle->loop, &handle->io_watcher, events);` |
| `ev_13e5b7b7d213` | call_site | `third_party/libuv/src/unix/fs.c:1234` | `r = uv__pwritev(fd, bufs, nbufs, off);` |
| `ev_13f8c58fad47` | call_site | `third_party/libuv/src/fs-poll.c:224` | `uv_close((uv_handle_t*)&ctx->timer_handle, timer_close_cb);` |
| `ev_143e69c8c53b` | call_site | `third_party/libuv/src/uv-common.c:438` | `return uv__udp_connect(handle, addr, addrlen);` |
| `ev_146e0ed4d5a7` | call_site | `third_party/libuv/src/inet.c:127` | `int err = inet_ntop4(src+12, tp, sizeof tmp - (tp - tmp));` |
| `ev_14b6e48c7c1b` | call_site | `third_party/libuv/src/unix/fsevents.c:203` | `uv__queue_add(&handle->cf_events, events);` |
| `ev_14bba1929b2d` | call_site | `third_party/libuv/src/unix/core.c:347` | `uv__stream_destroy((uv_stream_t*)handle);` |
| `ev_150365d5d208` | call_site | `third_party/libuv/src/unix/random-devurandom.c:59` | `uv__close(fd);` |
| `ev_15138841a177` | call_site | `third_party/libuv/src/unix/process.c:112` | `uv__queue_init(&pending);` |
| `ev_152d208c9f6a` | call_site | `third_party/libuv/src/unix/process.c:366` | `uv__close(close_fd);` |
| `ev_158456aaded4` | call_site | `third_party/libuv/src/heap-inl.h:236` | `heap_node_swap(heap, child->parent, child);` |
| `ev_159dde9488ae` | call_site | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_15a979b79734` | assignment | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_15c81bcc736a` | call_site | `third_party/libuv/src/unix/signal.c:272` | `uv__io_init(&loop->signal_io_watcher,` |
| `ev_15d65074e759` | call_site | `third_party/libuv/src/unix/core.c:606` | `return close$NOCANCEL(fd);` |
| `ev_15e8a9868f48` | call_site | `third_party/libuv/src/timer.c:77` | `uv_timer_stop(handle);` |
| `ev_15fdf97bfacf` | call_site | `third_party/libuv/src/heap-inl.h:228` | `heap_node_swap(heap, child, smallest);` |
| `ev_1651cc5b3538` | call_site | `third_party/libuv/src/unix/core.c:187` | `uv__check_close((uv_check_t*)handle);` |
| `ev_16ab7a80375d` | call_site | `third_party/libuv/src/unix/fsevents.c:199` | `uv_mutex_lock(&handle->cf_mutex);` |
| `ev_16b0f25d0fc4` | call_site | `third_party/libuv/src/unix/core.c:650` | `return uv__close_nocheckstdio(fd);` |
| `ev_174a5e7a8a0d` | call_site | `third_party/libuv/src/unix/stream.c:1106` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_176a1561fc32` | call_site | `third_party/libuv/src/unix/fs.c:1436` | `uv_fs_unlink(NULL, &fs_req, req->new_path, NULL);` |
| `ev_17730c09a72c` | call_site | `third_party/libuv/src/unix/stream.c:1526` | `uv_close((uv_handle_t*) &s->async, uv__stream_osx_cb_close);` |
| `ev_17828bd372ad` | call_site | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_179df896b056` | call_site | `third_party/libuv/src/unix/core.c:1914` | `uv__free(cloned_path);` |
| `ev_17c4f6dfe095` | call_site | `third_party/libuv/src/unix/pipe.c:288` | `err = uv__socket(AF_UNIX, SOCK_STREAM, 0);` |
| `ev_17ef84923eda` | call_site | `third_party/libuv/src/unix/pipe.c:200` | `if (uv__fd_exists(handle->loop, fd))` |
| `ev_1812f2811ac8` | call_site | `third_party/libuv/src/timer.c:199` | `uv_timer_stop(handle);` |
| `ev_182a9947b2ac` | call_site | `third_party/libuv/src/unix/process.c:916` | `err = uv__spawn_and_init_child_fork(options, stdio_count, pipes, signal_pipe[1], pid);` |
| `ev_185b8efc41eb` | call_site | `third_party/libuv/src/unix/fs.c:1716` | `X(CLOSE, uv__fs_close(req->file));` |
| `ev_185ee6e42be8` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_186a53e8ac1c` | call_site | `third_party/libuv/src/uv-common.c:609` | `uv__print_handles(loop, 0, stream);` |
| `ev_18762baaeb2f` | call_site | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_18887fab6fc1` | call_site | `third_party/libuv/src/threadpool.c:226` | `uv__queue_init(&run_slow_work_message);` |
| `ev_188e05cab09e` | call_site | `third_party/libuv/src/unix/udp.c:130` | `uv__io_stop(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_189d9ca7af89` | assignment | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_18f01deeaf81` | call_site | `third_party/libuv/src/unix/async.c:283` | `err = uv__open_cloexec("/dev/null", O_RDONLY);` |
| `ev_191c8adc3c04` | call_site | `third_party/libuv/src/unix/stream.c:870` | `if (uv__write_req_update(stream, req, n)) {` |
| `ev_1922842120f4` | call_site | `third_party/libuv/src/unix/loop.c:85` | `err = uv__process_init(loop);` |
| `ev_192eb781235e` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_1950ee129b80` | call_site | `third_party/libuv/src/unix/udp.c:866` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_UDP);` |
| `ev_195f897256f3` | call_site | `third_party/libuv/src/unix/loop.c:57` | `uv__queue_init(&loop->prepare_handles);` |
| `ev_1961fbcd972a` | call_site | `third_party/libuv/src/unix/fsevents.c:876` | `uv__queue_remove(&handle->cf_member);` |
| `ev_196f2a5f3c08` | call_site | `third_party/libuv/src/threadpool.c:129` | `uv_async_send(&w->loop->wq_async);` |
| `ev_19eb78f41da1` | call_site | `third_party/libuv/src/unix/getnameinfo.c:118` | `uv__getnameinfo_done(&req->work_req, 0);` |
| `ev_1a365af838f0` | call_site | `third_party/libuv/src/unix/fs.c:1747` | `X(UTIME, uv__fs_utime(req));` |
| `ev_1affd60a4a39` | call_site | `third_party/libuv/src/unix/kqueue.c:185` | `assert(uv__queue_empty(&loop->watcher_queue));` |
| `ev_1b39518b0531` | call_site | `third_party/libuv/src/unix/fsevents.c:451` | `pCFStringCreateWithFileSystemRepresentation(NULL, curr->realpath);` |
| `ev_1b40786835df` | call_site | `third_party/libuv/src/threadpool.c:62` | `uv_thread_setname("libuv-worker");` |
| `ev_1b588ed3faec` | call_site | `third_party/libuv/src/threadpool.c:365` | `req->after_work_cb(req, err);` |
| `ev_1b6e96eff7fe` | call_site | `third_party/libuv/src/unix/fs.c:1733` | `X(READ, uv__fs_read(req));` |
| `ev_1b7d50ad29e9` | call_site | `third_party/libuv/src/unix/tty.c:150` | `type = uv_guess_handle(fd);` |
| `ev_1bad3006cd6a` | call_site | `third_party/libuv/src/unix/fsevents.c:321` | `uv__fsevents_push_event(handle, &head, 0);` |
| `ev_1bbfcc053b16` | call_site | `third_party/libuv/src/random.c:107` | `return uv__random(buf, buflen);` |
| `ev_1befa26dc27e` | assignment | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_1c17689a22fb` | call_site | `third_party/libuv/src/timer.c:186` | `while (!uv__queue_empty(&ready_queue)) {` |
| `ev_1c2251217b59` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_1c69a1a72174` | call_site | `third_party/libuv/src/threadpool.c:186` | `uv_mutex_destroy(&mutex);` |
| `ev_1c824f8b9990` | call_site | `third_party/libuv/src/uv-common.c:656` | `return uv__socket_sockopt(handle, SO_RCVBUF, value);` |
| `ev_1c91c7033e3c` | call_site | `third_party/libuv/src/unix/udp.c:74` | `while (!uv__queue_empty(&handle->write_queue)) {` |
| `ev_1c9f7c728bcf` | call_site | `third_party/libuv/src/unix/stream.c:1051` | `buf = uv_buf_init(NULL, 0);` |
| `ev_1cf43bc2d4aa` | call_site | `third_party/libuv/src/unix/stream.c:1375` | `uv__queue_insert_tail(&stream->write_queue, &req->queue);` |
| `ev_1d044a6853e0` | call_site | `third_party/libuv/src/threadpool.c:293` | `uv_mutex_unlock(&w->loop->wq_mutex);` |
| `ev_1df22000481a` | call_site | `third_party/libuv/src/threadpool.c:128` | `uv__queue_insert_tail(&w->loop->wq, &w->wq);` |
| `ev_1e1df29d03f3` | call_site | `third_party/libuv/src/fs-poll.c:181` | `ctx->start_time = uv_now(ctx->loop);` |
| `ev_1e2691eede8e` | call_site | `third_party/libuv/src/unix/core.c:1383` | `uv__free(buf);` |
| `ev_1e46d8ab3b13` | call_site | `third_party/libuv/src/unix/stream.c:919` | `stream->write_queue_size -= uv__write_req_size(req);` |
| `ev_1e486deaf79a` | call_site | `third_party/libuv/src/unix/stream.c:1148` | `stream->read_cb(stream, nread, &buf);` |
| `ev_1e963594aac4` | assignment | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_1ec7a13834f3` | call_site | `third_party/libuv/src/unix/signal.c:151` | `if (uv__signal_lock())` |
| `ev_1ed3b77b8bc6` | call_site | `third_party/libuv/src/unix/fsevents.c:323` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_1ef966f004d1` | call_site | `third_party/libuv/src/unix/pipe.c:323` | `err = uv__stream_open((uv_stream_t*)handle,` |
| `ev_1efd46fbd09f` | call_site | `third_party/libuv/src/unix/fs.c:819` | `buf = uv__malloc(len + 1);` |
| `ev_1f144a4c3ef4` | call_site | `third_party/libuv/src/unix/fsevents.c:476` | `pCFRelease(paths[--i]);` |
| `ev_1f36ebffd4fa` | call_site | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_1f8cdd8237be` | call_site | `third_party/libuv/src/unix/poll.c:90` | `uv__handle_init(loop, (uv_handle_t*) handle, UV_POLL);` |
| `ev_1f965ef19eb1` | call_site | `third_party/libuv/src/unix/stream.c:369` | `err = uv_thread_create(&s->thread, uv__stream_osx_select, stream);` |
| `ev_1fe6fd14bac4` | call_site | `third_party/libuv/src/unix/internal.h:400` | `loop->time = uv__hrtime(UV_CLOCK_FAST) / 1000000;` |
| `ev_1ffb25112b0b` | call_site | `third_party/libuv/src/unix/signal.c:157` | `if (uv__signal_unlock())` |
| `ev_2031de935e23` | call_site | `third_party/libuv/src/idna.c:474` | `target_len = uv_utf16_length_as_wtf8(w_source_ptr, w_source_len);` |
| `ev_20e4abf5aeff` | call_site | `third_party/libuv/src/unix/udp.c:1119` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_20f84a920a0a` | call_site | `third_party/libuv/src/uv-common.c:976` | `uv__signal_cleanup();` |
| `ev_211bf80d72e4` | call_site | `third_party/libuv/src/unix/fs.c:1873` | `PATH;` |
| `ev_214a0dca31d2` | call_site | `third_party/libuv/src/unix/stream.c:495` | `err = uv__accept(accept_fd);` |
| `ev_2186a4128abe` | call_site | `third_party/libuv/src/unix/core.c:523` | `err = uv__nonblock(sockfd, 1);` |
| `ev_21c1a60dfc72` | call_site | `third_party/libuv/src/thread-common.c:136` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_21c5e01aaae6` | assignment | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_21d6d0fd92de` | call_site | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_2229444bffa6` | call_site | `third_party/libuv/src/unix/udp.c:1178` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_22514685a0b0` | call_site | `third_party/libuv/src/unix/stream.c:1092` | `stream->read_cb(stream, 0, &buf);` |
| `ev_22785e8672f9` | call_site | `third_party/libuv/src/unix/signal.c:365` | `return uv__signal_start(handle, signal_cb, signum, 1);` |
| `ev_2295b201528b` | call_site | `third_party/libuv/src/unix/kqueue.c:313` | `uv__wait_children(loop);` |
| `ev_2309c0efb781` | call_site | `third_party/libuv/src/unix/core.c:450` | `uv__run_pending(loop);` |
| `ev_237b1c56f72f` | call_site | `third_party/libuv/src/unix/core.c:1895` | `cloned_path = uv__strdup(path_env);` |
| `ev_2443cbbb6d83` | call_site | `third_party/libuv/src/unix/async.c:77` | `err = uv__async_start(loop);` |
| `ev_244a73c75855` | assignment | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_247397b03ad3` | call_site | `third_party/libuv/src/unix/async.c:343` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_247de283aa35` | call_site | `third_party/libuv/src/unix/core.c:1757` | `r = uv__strscpy(buffer->sysname, buf.sysname, sizeof(buffer->sysname));` |
| `ev_247e633779b6` | call_site | `third_party/libuv/src/unix/pipe.c:406` | `return uv__pipe_getsockpeername(handle, getsockname, buffer, size);` |
| `ev_24c4d3d07a71` | call_site | `third_party/libuv/src/unix/core.c:434` | `uv__update_time(loop);` |
| `ev_24c9fde5800e` | call_site | `third_party/libuv/src/unix/stream.c:558` | `err = uv_udp_open((uv_udp_t*) client, server->accepted_fd);` |
| `ev_2564d14b945f` | call_site | `third_party/libuv/src/unix/loop.c:200` | `uv__free(loop->watchers);` |
| `ev_259947cdf592` | assignment | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_25ccb94fcece` | call_site | `third_party/libuv/src/unix/core.c:1406` | `uv__free(buf);` |
| `ev_25f435432947` | call_site | `third_party/libuv/src/unix/signal.c:101` | `uv__signal_cleanup();` |
| `ev_2641405cd83f` | call_site | `third_party/libuv/src/unix/udp.c:76` | `uv__queue_remove(q);` |
| `ev_266842e5e212` | call_site | `third_party/libuv/src/unix/udp.c:961` | `return uv__udp_set_source_membership6(handle,` |
| `ev_26743a85708e` | call_site | `third_party/libuv/src/unix/fs.c:1744` | `X(STATFS, uv__fs_statfs(req));` |
| `ev_267697074afc` | call_site | `third_party/libuv/src/unix/tcp.c:436` | `err = maybe_new_socket(tcp, AF_INET, flags);` |
| `ev_26e2518d5997` | call_site | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_26e7d1fa12de` | call_site | `third_party/libuv/src/unix/loop.c:53` | `uv__queue_init(&loop->wq);` |
| `ev_26ed9ad222f8` | call_site | `third_party/libuv/src/unix/tty.c:238` | `uv__stream_open((uv_stream_t*) tty, fd, flags);` |
| `ev_2780cc7f6233` | call_site | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_282a09a82bd0` | call_site | `third_party/libuv/src/unix/stream.c:657` | `req->cb(req, err);` |
| `ev_28c7c6f6ac33` | call_site | `third_party/libuv/src/uv-common.c:975` | `uv__process_title_cleanup();` |
| `ev_28e43f0eba1c` | call_site | `third_party/libuv/src/unix/async.c:374` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_28edb14e9754` | call_site | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_28f24dfaf31b` | call_site | `third_party/libuv/src/unix/loop.c:66` | `uv__queue_init(&loop->watcher_queue);` |
| `ev_295073cc0f70` | call_site | `third_party/libuv/src/unix/core.c:415` | `if (uv__queue_empty(&loop->watcher_queue))` |
| `ev_2a2f0293c273` | call_site | `third_party/libuv/src/unix/stream.c:443` | `while (!uv__queue_empty(&stream->write_queue)) {` |
| `ev_2a453d775952` | call_site | `third_party/libuv/src/unix/tcp.c:340` | `uv__queue_init(&req->queue);` |
| `ev_2a6570dc3adc` | call_site | `third_party/libuv/src/random.c:42` | `rc = uv__random_devurandom(buf, buflen);` |
| `ev_2a75d7d985ea` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_2ab12d34bb84` | call_site | `third_party/libuv/src/unix/tty.c:202` | `uv__close(newfd);` |
| `ev_2ab4a7c580e9` | call_site | `third_party/libuv/src/inet.c:263` | `int err = inet_pton4(curtok, tp);` |
| `ev_2ab7f36c505f` | call_site | `third_party/libuv/src/unix/loop.c:111` | `uv_rwlock_destroy(&loop->cloexec_lock);` |
| `ev_2abedf8382bd` | call_site | `third_party/libuv/src/unix/core.c:464` | `for (r = 0; r < 8 && !uv__queue_empty(&loop->pending_queue); r++)` |
| `ev_2ae01ea483ec` | call_site | `third_party/libuv/src/threadpool.c:159` | `uv_cond_signal(&cond);` |
| `ev_2afded09a586` | call_site | `third_party/libuv/src/unix/core.c:199` | `uv__timer_close((uv_timer_t*)handle);` |
| `ev_2b0f4c1dc954` | call_site | `third_party/libuv/src/unix/fs.c:1624` | `ret = uv__fs_statx(fd, "", /* is_fstat */ 1, /* is_lstat */ 0, buf);` |
| `ev_2b195d2040ab` | call_site | `third_party/libuv/src/unix/fs.c:1260` | `srcfd = uv_fs_open(NULL, &fs_req, req->path, O_RDONLY, 0, NULL);` |
| `ev_2b82d8a51685` | call_site | `third_party/libuv/src/unix/process.c:921` | `uv__close(signal_pipe[1]);` |
| `ev_2b9f9acc3278` | call_site | `third_party/libuv/src/unix/tty.c:399` | `if (uv__fstat(file, &s)) {` |
| `ev_2bf0e24e4dd5` | call_site | `third_party/libuv/src/unix/core.c:171` | `uv__tty_close((uv_tty_t*)handle);` |
| `ev_2bf4506213f8` | call_site | `third_party/libuv/src/threadpool.c:184` | `uv__free(threads);` |
| `ev_2bf92316f70d` | call_site | `third_party/libuv/src/unix/fsevents.c:755` | `uv__fsevents_reschedule(state, loop, s->type);` |
| `ev_2c08727cb225` | call_site | `third_party/libuv/src/unix/stream.c:528` | `stream->connection_cb(stream, 0);` |
| `ev_2c198a0c4899` | assignment | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_2cfb4e3abba1` | call_site | `third_party/libuv/src/heap-inl.h:224` | `if (child->right != NULL && less_than(child->right, smallest))` |
| `ev_2d1d72224d5d` | call_site | `third_party/libuv/src/threadpool.c:262` | `init_threads();` |
| `ev_2d3756c7b8da` | call_site | `third_party/libuv/src/unix/tty.c:220` | `r = uv__stream_try_select((uv_stream_t*) tty, &fd);` |
| `ev_2d5b243aca20` | call_site | `third_party/libuv/src/unix/tcp.c:68` | `sockfd = uv__socket(domain, SOCK_STREAM, 0);` |
| `ev_2d74c1b81633` | call_site | `third_party/libuv/src/unix/tcp.c:362` | `return uv__stream_open((uv_stream_t*)handle,` |
| `ev_2d8a74aae8b0` | call_site | `third_party/libuv/src/unix/fsevents.c:776` | `uv_mutex_lock(&loop->cf_mutex);` |
| `ev_2d9486c581f5` | call_site | `third_party/libuv/src/uv-common.c:565` | `uv__queue_insert_tail(&loop->handle_queue, q);` |
| `ev_2d9cf9a4d8fb` | call_site | `third_party/libuv/src/unix/tcp.c:79` | `return maybe_bind_socket(sockfd);` |
| `ev_2dd96e0feb4c` | call_site | `third_party/libuv/src/unix/udp.c:123` | `req->send_cb(req, 0);` |
| `ev_2e0cf5832e86` | call_site | `third_party/libuv/src/fs-poll.c:223` | `if (!uv_is_active((uv_handle_t*)handle) \|\| uv__is_closing(handle)) {` |
| `ev_2e585bcf4e2e` | call_site | `third_party/libuv/src/unix/pipe.c:245` | `uv__queue_init(&req->queue);` |
| `ev_2e5c5fbf900f` | call_site | `third_party/libuv/src/unix/stream.c:1545` | `uv__close(handle->accepted_fd);` |
| `ev_2e8143da6e14` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:96` | `pCFBundleGetBundleWithIdentifier(S("com.apple.LaunchServices"));` |
| `ev_2ea8082ed409` | call_site | `third_party/libuv/src/unix/process.c:449` | `uv__spawn_init_posix_spawn_fncs();` |
| `ev_2ee575ffd2de` | call_site | `third_party/libuv/src/unix/udp.c:1363` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_2f2b06fe242a` | call_site | `third_party/libuv/src/unix/fs.c:787` | `buf = uv__reallocf(buf, len + 1);` |
| `ev_2f3f4db09079` | call_site | `third_party/libuv/src/threadpool.c:289` | `cancelled = !uv__queue_empty(&w->wq) && w->work != NULL;` |
| `ev_2f7dda6bfb75` | call_site | `third_party/libuv/src/unix/udp.c:248` | `if (uv_udp_using_recvmmsg(handle)) {` |
| `ev_2f806e37dde4` | call_site | `third_party/libuv/src/uv-common.c:261` | `return uv_inet_pton(AF_INET, ip, &(addr->sin_addr.s_addr));` |
| `ev_2fde093c255a` | call_site | `third_party/libuv/src/unix/async.c:192` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_2fe623fc68af` | call_site | `third_party/libuv/src/uv-common.c:68` | `m = uv__malloc(len + 1);` |
| `ev_30225b99c9f1` | call_site | `third_party/libuv/src/uv-common.c:957` | `uv__free(cpu_infos);` |
| `ev_3069032b5070` | call_site | `third_party/libuv/src/unix/udp.c:907` | `if (uv__udp_is_connected(handle))` |
| `ev_306b6ec05335` | call_site | `third_party/libuv/src/fs-poll.c:230` | `interval -= (uv_now(ctx->loop) - ctx->start_time) % interval;` |
| `ev_309729e6dad5` | call_site | `third_party/libuv/src/thread-common.c:143` | `uv_cond_destroy((uv_cond_t*) &b->cond);` |
| `ev_30a606aa4ca3` | assignment | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_30c77f45b00f` | call_site | `third_party/libuv/src/unix/process.c:363` | `uv__nonblock_fcntl(fd, 0);` |
| `ev_30ed22223da6` | call_site | `third_party/libuv/src/unix/fsevents.c:818` | `handle->cf_cb = uv__malloc(sizeof(*handle->cf_cb));` |
| `ev_30ff8b024343` | call_site | `third_party/libuv/src/unix/proctitle.c:136` | `uv_mutex_lock(&process_title_mutex);` |
| `ev_3104aee8ac8b` | call_site | `third_party/libuv/src/unix/pipe.c:443` | `return uv_guess_handle(handle->accepted_fd);` |
| `ev_31214efee850` | call_site | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_314bdfa42d7d` | call_site | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_316a0f657bdf` | call_site | `third_party/libuv/src/heap-inl.h:146` | `while (newnode->parent != NULL && less_than(newnode, newnode->parent))` |
| `ev_316e1ab00ed3` | call_site | `third_party/libuv/src/unix/fs.c:1598` | `uv__to_stat(&pbuf, buf);` |
| `ev_3170248b77e9` | call_site | `third_party/libuv/src/unix/proctitle.c:68` | `new_argv = uv__malloc(size);` |
| `ev_31b23c175816` | call_site | `third_party/libuv/src/unix/fsevents.c:699` | `uv__free(state);` |
| `ev_31b8a4b1cb83` | assignment | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_31d9e33334d7` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:96` | `pCFBundleGetBundleWithIdentifier(S("com.apple.LaunchServices"));` |
| `ev_328342f2c2e0` | call_site | `third_party/libuv/src/unix/core.c:230` | `uv__signal_close((uv_signal_t*) handle);` |
| `ev_32ba635dd96b` | call_site | `third_party/libuv/src/unix/fs.c:1810` | `PATH;` |
| `ev_32ca5944a889` | call_site | `third_party/libuv/src/unix/process.c:384` | `uv__write_errno(error_fd);` |
| `ev_32d7ade0bfa5` | call_site | `third_party/libuv/src/unix/kqueue.c:431` | `uv__wait_children(loop);` |
| `ev_32feed37e13f` | call_site | `third_party/libuv/src/unix/fsevents.c:696` | `uv_sem_destroy(&state->fsevent_sem);` |
| `ev_334d13d28e80` | call_site | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_337c398f9950` | assignment | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_33d410574c08` | assignment | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_34265ee6c4b8` | call_site | `third_party/libuv/src/unix/core.c:1772` | `r = uv__strscpy(buffer->release, buf.release, sizeof(buffer->release));` |
| `ev_353c4309676a` | call_site | `third_party/libuv/src/unix/fsevents.c:597` | `err = uv_mutex_init(&loop->cf_mutex);` |
| `ev_354f7f3ab324` | call_site | `third_party/libuv/src/threadpool.c:108` | `q = uv__queue_head(&slow_io_pending_wq);` |
| `ev_357d3ffb0b75` | call_site | `third_party/libuv/src/unix/process.c:909` | `err = uv__make_pipe(signal_pipe, 0);` |
| `ev_358cd53fc2e2` | call_site | `third_party/libuv/src/unix/core.c:432` | `r = uv__loop_alive(loop);` |
| `ev_35a5f978caed` | call_site | `third_party/libuv/src/timer.c:89` | `heap_insert(timer_heap(handle->loop),` |
| `ev_35f8f6d9850e` | call_site | `third_party/libuv/src/uv-common.c:509` | `addrlen = uv__udp_check_before_send(handle, addr);` |
| `ev_35f9b6b78ec3` | call_site | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_36290f58d893` | assignment | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_3640a16324bc` | assignment | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_368533d26e47` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:115` | `display_name_key = pCFBundleGetDataPointerForName(launch_services_bundle,` |
| `ev_368e6ff64468` | call_site | `third_party/libuv/src/unix/fs.c:2199` | `PATH;` |
| `ev_369c941d05b6` | call_site | `third_party/libuv/src/fs-poll.c:214` | `if (ctx->busy_polling < 0 \|\| !statbuf_eq(&ctx->statbuf, statbuf))` |
| `ev_36a318f0ce85` | call_site | `third_party/libuv/src/idna.c:497` | `code_point = uv__get_surrogate_value(w_source_ptr, w_source_len);` |
| `ev_36b1f9ed36cc` | call_site | `third_party/libuv/src/unix/fs.c:543` | `r = uv__preadv(fd, bufs, nbufs, off);` |
| `ev_36cb5c78883d` | call_site | `third_party/libuv/src/thread-common.c:102` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_36dae95e80b3` | call_site | `third_party/libuv/src/unix/stream.c:333` | `s = uv__malloc(sizeof(*s) + sread_sz + swrite_sz);` |
| `ev_3713a9c8fb51` | call_site | `third_party/libuv/src/uv-common.c:93` | `return uv__allocator.local_calloc(count, size);` |
| `ev_3717f5d00c57` | call_site | `third_party/libuv/src/unix/tty.c:358` | `uv__tcsetattr(fd, TCSANOW, &orig_termios);` |
| `ev_374464ee690c` | call_site | `third_party/libuv/src/unix/loop.c:185` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_374b3592f790` | call_site | `third_party/libuv/src/unix/udp.c:103` | `q = uv__queue_head(&handle->write_completed_queue);` |
| `ev_377b1f8429df` | call_site | `third_party/libuv/src/unix/signal.c:287` | `uv__close(loop->signal_pipefd[0]);` |
| `ev_37960dbc90d3` | call_site | `third_party/libuv/src/unix/fs.c:1730` | `X(MKDTEMP, uv__fs_mkdtemp(req));` |
| `ev_37dc1b8a6d6f` | call_site | `third_party/libuv/src/unix/udp.c:104` | `uv__queue_remove(q);` |
| `ev_3800f3cbc795` | call_site | `third_party/libuv/src/unix/fs.c:1726` | `X(LUTIME, uv__fs_lutime(req));` |
| `ev_381f3f57f54d` | call_site | `third_party/libuv/src/unix/fsevents.c:662` | `uv_mutex_destroy(&loop->cf_mutex);` |
| `ev_384a5d3ba77e` | call_site | `third_party/libuv/src/unix/signal.c:343` | `uv__handle_init(loop, (uv_handle_t*) handle, UV_SIGNAL);` |
| `ev_385254c7e5ac` | call_site | `third_party/libuv/src/unix/core.c:472` | `uv__metrics_update_idle_time(loop);` |
| `ev_388ae875a13e` | assignment | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_3895519364a0` | call_site | `third_party/libuv/src/timer.c:59` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_TIMER);` |
| `ev_38a3cb2ec3da` | call_site | `third_party/libuv/src/unix/loop.c:157` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_38a67460302e` | call_site | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_391541eec937` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_391e69ab4864` | call_site | `third_party/libuv/src/unix/fs.c:1725` | `X(FUTIME, uv__fs_futime(req));` |
| `ev_391f7b5ae52c` | assignment | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_396feb52b102` | call_site | `third_party/libuv/src/unix/stream.c:456` | `assert(!uv__io_active(&stream->io_watcher, POLLIN \| POLLOUT));` |
| `ev_3972ff248a0c` | call_site | `third_party/libuv/src/unix/stream.c:1470` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_39930c549419` | call_site | `third_party/libuv/src/unix/fs.c:529` | `iovmax = uv__getiovmax();` |
| `ev_39e03bfc37c1` | call_site | `third_party/libuv/src/unix/tcp.c:294` | `err = maybe_new_socket(handle,` |
| `ev_3aa416f9ff63` | call_site | `third_party/libuv/src/unix/udp.c:215` | `handle->recv_cb(handle, 0, buf, NULL, UV_UDP_MMSG_FREE);` |
| `ev_3aa9d5228b9d` | call_site | `third_party/libuv/src/unix/fsevents.c:804` | `handle->realpath = uv__strdup(buf);` |
| `ev_3aeb1da5f61d` | call_site | `third_party/libuv/src/uv-common.c:158` | `uv__free(grp->members);` |
| `ev_3afdccaa2f17` | call_site | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_3b15b85ef85e` | call_site | `third_party/libuv/src/uv-common.c:864` | `if (uv_loop_init(loop)) {` |
| `ev_3b2af92d9b76` | call_site | `third_party/libuv/src/unix/tcp.c:92` | `sockfd = uv__stream_fd(handle);` |
| `ev_3b3d6976360e` | call_site | `third_party/libuv/src/uv-common.c:226` | `return uv__unknown_err_code(err);` |
| `ev_3b53fab5959e` | call_site | `third_party/libuv/src/unix/fs.c:1739` | `X(REALPATH, uv__fs_realpath(req));` |
| `ev_3b55cb8f7ccb` | call_site | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_3b8099a64d27` | call_site | `third_party/libuv/src/unix/fs.c:354` | `r = uv__close(r);` |
| `ev_3baa270ceee6` | call_site | `third_party/libuv/src/unix/kqueue.c:443` | `loop->signal_io_watcher.cb(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_3bafd2a27c12` | call_site | `third_party/libuv/src/unix/udp.c:109` | `handle->send_queue_size -= uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_3bd42f44be98` | call_site | `third_party/libuv/src/unix/process.c:115` | `q = uv__queue_head(h);` |
| `ev_3bd7043bc67f` | call_site | `third_party/libuv/src/unix/fsevents.c:389` | `pFSEventStreamStop(state->fsevent_stream);` |
| `ev_3beb65947784` | call_site | `third_party/libuv/src/unix/stream.c:225` | `uv_sem_wait(&s->async_sem);` |
| `ev_3c01b7fc8ace` | call_site | `third_party/libuv/src/unix/fs.c:1738` | `X(READLINK, uv__fs_readlink(req));` |
| `ev_3c1ae8f72bdf` | call_site | `third_party/libuv/src/unix/signal.c:571` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_3c46f0034804` | call_site | `third_party/libuv/src/unix/darwin.c:214` | `*cpu_infos = uv__malloc(numcpus * sizeof(**cpu_infos));` |
| `ev_3c55aae9ae85` | call_site | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_3c9a9e112c0f` | call_site | `third_party/libuv/src/unix/udp.c:462` | `return uv__udp_bind(handle, &taddr.addr, addrlen, flags);` |
| `ev_3ca7ab3b4a85` | call_site | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_3ca994e340f6` | call_site | `third_party/libuv/src/unix/stream.c:1457` | `uv__io_start(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_3cbf38ed895b` | call_site | `third_party/libuv/src/unix/pipe.c:368` | `err = uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_3cbf6f2943ac` | call_site | `third_party/libuv/src/unix/stream.c:392` | `uv__free(s);` |
| `ev_3cd8f67d62ee` | call_site | `third_party/libuv/src/timer.c:119` | `uv_timer_start(handle, handle->timer_cb, handle->repeat, handle->repeat);` |
| `ev_3d08a523a678` | call_site | `third_party/libuv/src/unix/stream.c:1232` | `uv__write_callbacks(stream);` |
| `ev_3d0a8c7b247e` | call_site | `third_party/libuv/src/unix/thread.c:122` | `return uv__default_stack_size();` |
| `ev_3d4ce73526b1` | call_site | `third_party/libuv/src/unix/stream.c:927` | `req->cb(req, req->error);` |
| `ev_3d66e371f7c6` | call_site | `third_party/libuv/src/unix/loop.c:108` | `uv_mutex_destroy(&loop->wq_mutex);` |
| `ev_3dd2da93e6a6` | call_site | `third_party/libuv/src/unix/udp.c:388` | `err = uv__sock_reuseaddr(fd);` |
| `ev_3dfa107301c5` | call_site | `third_party/libuv/src/unix/tcp.c:602` | `err =uv__tcp_keepalive(uv__stream_fd(handle), on, delay);` |
| `ev_3e65cdb3deb6` | assignment | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_3e841004bc4a` | call_site | `third_party/libuv/src/uv-common.c:99` | `uv__free(ptr);` |
| `ev_3e89b455f40b` | call_site | `third_party/libuv/src/threadpool.c:160` | `uv_mutex_unlock(&mutex);` |
| `ev_3e9fa5a521d7` | call_site | `third_party/libuv/src/threadpool.c:303` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_3ed4e1e2e5d6` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:162` | `rc = uv__idna_toascii(hostname,` |
| `ev_3ee889c5830d` | call_site | `third_party/libuv/src/unix/stream.c:224` | `uv_async_send(&s->async);` |
| `ev_3f8df32eb85c` | call_site | `third_party/libuv/src/unix/pipe.c:515` | `if ((err = uv__cloexec(temp[0], 1)))` |
| `ev_3fcb548be170` | call_site | `third_party/libuv/src/unix/fs.c:1679` | `req->nbufs = uv__fs_buf_offset(req->bufs, result);` |
| `ev_40056aa4b1f0` | call_site | `third_party/libuv/src/unix/tcp.c:602` | `err =uv__tcp_keepalive(uv__stream_fd(handle), on, delay);` |
| `ev_405124f0cf19` | call_site | `third_party/libuv/src/unix/core.c:1284` | `uv__free(buf);` |
| `ev_4085af6e2b7b` | call_site | `third_party/libuv/src/unix/fs.c:1428` | `err = uv__close_nocheckstdio(dstfd);` |
| `ev_408699e87ca2` | call_site | `third_party/libuv/src/unix/async.c:342` | `uv__queue_remove(q);` |
| `ev_4129ae23f459` | call_site | `third_party/libuv/src/unix/stream.c:632` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_41650290dce6` | call_site | `third_party/libuv/src/unix/random-devurandom.c:64` | `uv__close(fd);` |
| `ev_41912e441032` | assignment | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_419354d44a35` | call_site | `third_party/libuv/src/unix/core.c:1303` | `uv__free(buf);` |
| `ev_4223c575da12` | call_site | `third_party/libuv/src/unix/kqueue.c:195` | `uv__queue_init(q);` |
| `ev_42299d1e0e40` | call_site | `third_party/libuv/src/unix/core.c:1414` | `return uv__getpwuid_r(pwd, geteuid());` |
| `ev_423b65c48d84` | call_site | `third_party/libuv/src/unix/kqueue.c:379` | `w->cb(loop, w, ev->fflags); /* XXX always uv__fs_event() */` |
| `ev_4243945f12c5` | call_site | `third_party/libuv/src/unix/stream.c:1519` | `uv_sem_post(&s->async_sem);` |
| `ev_42463528e0e3` | call_site | `third_party/libuv/src/unix/fs.c:2074` | `PATH;` |
| `ev_4313f69454a6` | call_site | `third_party/libuv/src/unix/fs.c:1743` | `X(STAT, uv__fs_stat(req->path, &req->statbuf));` |
| `ev_43add662811b` | call_site | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_43c7ad61028b` | call_site | `third_party/libuv/src/unix/async.c:370` | `q = uv__queue_head(&queue);` |
| `ev_43f1c5da265e` | call_site | `third_party/libuv/src/unix/udp.c:1223` | `if (!uv__io_active(&handle->io_watcher, POLLOUT))` |
| `ev_4400131fe7b3` | call_site | `third_party/libuv/src/fs-poll.c:183` | `if (uv_fs_stat(ctx->loop, &ctx->fs_req, ctx->path, poll_cb))` |
| `ev_440f71fd7cf0` | assignment | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_44318f0bb23a` | call_site | `third_party/libuv/src/uv-common.c:568` | `walk_cb(h, arg);` |
| `ev_443ef202672e` | call_site | `third_party/libuv/src/unix/fs.c:1968` | `PATH2;` |
| `ev_444bcae4650a` | call_site | `third_party/libuv/src/unix/tcp.c:346` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_44a22989e51a` | call_site | `third_party/libuv/src/unix/udp.c:643` | `err = uv__udp_maybe_deferred_bind(handle, addr->sa_family, 0);` |
| `ev_44c5dcdf2475` | call_site | `third_party/libuv/src/unix/udp.c:621` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_44ebe9a6e192` | call_site | `third_party/libuv/src/unix/fsevents.c:781` | `pCFRunLoopSourceSignal(state->signal_source);` |
| `ev_450ba561786a` | call_site | `third_party/libuv/src/unix/kqueue.c:378` | `uv__metrics_update_idle_time(loop);` |
| `ev_4537864157be` | call_site | `third_party/libuv/src/unix/fsevents.c:622` | `state->signal_source = pCFRunLoopSourceCreate(NULL, 0, &ctx);` |
| `ev_45a6729b760f` | call_site | `third_party/libuv/src/unix/core.c:1918` | `token = uv__strtok(NULL, ":", &itr);` |
| `ev_45cb9bff4592` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_4660a5e441db` | call_site | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_4680b7cc8dd9` | call_site | `third_party/libuv/src/unix/async.c:276` | `uv_once(&kqueue_runtime_detection_guard, uv__kqueue_runtime_detection);` |
| `ev_46c001c613d4` | call_site | `third_party/libuv/src/unix/pipe.c:248` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_46e211d4dc45` | call_site | `third_party/libuv/src/unix/thread.c:129` | `return uv_thread_create_ex(tid, &params, entry, arg);` |
| `ev_46f1e541bca9` | call_site | `third_party/libuv/src/unix/poll.c:71` | `if (uv__fd_exists(loop, fd))` |
| `ev_471719867f20` | call_site | `third_party/libuv/src/uv-common.c:746` | `nbufs = uv__get_nbufs(req);` |
| `ev_4742f24d0fbc` | call_site | `third_party/libuv/src/unix/pipe.c:172` | `uv__io_start(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_4774e0afabce` | call_site | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_47c82a7acda6` | call_site | `third_party/libuv/src/inet.c:38` | `return (inet_ntop4(src, dst, size));` |
| `ev_4813a53bc506` | call_site | `third_party/libuv/src/threadpool.c:330` | `w->done(w, err);` |
| `ev_484a3d7c80b8` | call_site | `third_party/libuv/src/unix/fsevents.c:445` | `q = uv__queue_next(q);` |
| `ev_48641e4f806c` | call_site | `third_party/libuv/src/unix/fsevents.c:434` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_4898e3f47d20` | call_site | `third_party/libuv/src/unix/tcp.c:662` | `if ((err = uv__nonblock(temp[1], 1)))` |
| `ev_490f82ac4ddf` | call_site | `third_party/libuv/src/unix/process.c:780` | `err = uv__spawn_set_posix_spawn_file_actions(&actions,` |
| `ev_4933bc379533` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_497444ca5f8b` | call_site | `third_party/libuv/src/unix/core.c:360` | `uv__queue_remove(&handle->handle_queue);` |
| `ev_497f4a4b673d` | assignment | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_4994604f67d9` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_49bbc66fa565` | call_site | `third_party/libuv/src/timer.c:100` | `heap_remove(timer_heap(handle->loop),` |
| `ev_49cff6d36c47` | call_site | `third_party/libuv/src/unix/udp.c:243` | `handle->recv_cb(handle, UV_ENOBUFS, &buf, NULL, 0);` |
| `ev_49de6b22fe6c` | call_site | `third_party/libuv/src/unix/pipe.c:527` | `if ((err = uv__nonblock(temp[1], 1)))` |
| `ev_4a1049af6085` | call_site | `third_party/libuv/src/unix/async.c:141` | `uv__cpu_relax();` |
| `ev_4a427616726f` | call_site | `third_party/libuv/src/timer.c:149` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_4a54c458effe` | call_site | `third_party/libuv/src/unix/random-devurandom.c:69` | `uv__close(fd);` |
| `ev_4af657080f7a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:175` | `buf = uv__malloc(hostname_len + service_len + hints_len);` |
| `ev_4afb722ab47d` | call_site | `third_party/libuv/src/unix/tcp.c:303` | `tmp6.sin6_scope_id = uv__ipv6_link_local_scope_id();` |
| `ev_4b1a4f1e0390` | call_site | `third_party/libuv/src/unix/udp.c:102` | `while (!uv__queue_empty(&handle->write_completed_queue)) {` |
| `ev_4b3607f42daf` | call_site | `third_party/libuv/src/unix/stream.c:166` | `if (uv_sem_trywait(&s->close_sem) == 0)` |
| `ev_4b5a8cb91d04` | call_site | `third_party/libuv/src/unix/udp.c:382` | `err = uv__set_recverr(fd, addr->sa_family);` |
| `ev_4b6f96a92262` | call_site | `third_party/libuv/src/unix/process.c:157` | `q = uv__queue_next(q);` |
| `ev_4bc3828d6565` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:118` | `uv__free(req->service);` |
| `ev_4bcb8190029f` | call_site | `third_party/libuv/src/unix/async.c:65` | `uv__close(kq);` |
| `ev_4c01dabae99b` | call_site | `third_party/libuv/src/unix/core.c:1784` | `r = uv__strscpy(buffer->machine, buf.machine, sizeof(buffer->machine));` |
| `ev_4c0ca12d187a` | call_site | `third_party/libuv/src/unix/fs.c:767` | `buf = uv__malloc(maxlen);` |
| `ev_4c335fd37666` | call_site | `third_party/libuv/src/unix/fsevents.c:853` | `uv__free(handle->cf_cb);` |
| `ev_4c35c6d99f34` | call_site | `third_party/libuv/src/unix/stream.c:98` | `uv__queue_init(&stream->write_completed_queue);` |
| `ev_4c3c5e690c47` | call_site | `third_party/libuv/src/uv-common.c:341` | `return uv__tcp_bind(handle, addr, addrlen, flags);` |
| `ev_4c5e05d9a7c9` | call_site | `third_party/libuv/src/unix/process.c:832` | `uv__process_child_init(options, stdio_count, pipes, error_fd);` |
| `ev_4c5e81c9fb3a` | call_site | `third_party/libuv/src/uv-common.c:1003` | `exit_time = uv_hrtime();` |
| `ev_4ca86b17fc93` | call_site | `third_party/libuv/src/unix/udp.c:1400` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_4caf0c74df12` | call_site | `third_party/libuv/src/unix/process.c:452` | `uv__spawn_init_can_use_setsid();` |
| `ev_4d0ef7488403` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_4d1131bbe680` | call_site | `third_party/libuv/src/fs-poll.c:75` | `if (uv_is_active((uv_handle_t*)handle))` |
| `ev_4d2e105e2302` | call_site | `third_party/libuv/src/unix/fs.c:1798` | `PATH;` |
| `ev_4dc43affd48c` | call_site | `third_party/libuv/src/unix/fsevents.c:747` | `uv__queue_remove(item);` |
| `ev_4e0450891acb` | call_site | `third_party/libuv/src/fs-poll.c:248` | `uv__make_close_pending((uv_handle_t*)handle);` |
| `ev_4e17d17ade1f` | assignment | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_4e8d75a656fb` | assignment | `third_party/libuv/src/unix/fs.c:2304` | `POST;` |
| `ev_4eda124e0e13` | call_site | `third_party/libuv/src/threadpool.c:271` | `uv_once(&once, init_once);` |
| `ev_4f3c17d6ab12` | call_site | `third_party/libuv/src/threadpool.c:176` | `post(&exit_message, UV__WORK_CPU);` |
| `ev_4fc9785bf93d` | call_site | `third_party/libuv/src/thread-common.c:79` | `uv__free(b);` |
| `ev_4fcf48ade5c6` | call_site | `third_party/libuv/src/unix/fs.c:2150` | `PATH;` |
| `ev_4fe71ee7ac1f` | call_site | `third_party/libuv/src/unix/stream.c:1183` | `uv__io_feed(stream->loop, &stream->io_watcher);` |
| `ev_4ffc29f60334` | call_site | `third_party/libuv/src/unix/fs.c:458` | `return uv__preadv_or_pwritev_emul(fd, bufs, nbufs, off, /*is_pread*/0);` |
| `ev_501af8139273` | assignment | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_502a77f997cd` | call_site | `third_party/libuv/src/unix/stream.c:935` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_5092d4aa49e1` | assignment | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_5095876400c4` | call_site | `third_party/libuv/src/unix/tcp.c:584` | `err = uv__tcp_nodelay(uv__stream_fd(handle), on);` |
| `ev_50b6439ff1fa` | call_site | `third_party/libuv/src/unix/pipe.c:411` | `return uv__pipe_getsockpeername(handle, getpeername, buffer, size);` |
| `ev_50d9af222527` | call_site | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_50efcb4b3bf7` | call_site | `third_party/libuv/src/unix/pipe.c:454` | `if (handle == NULL \|\| uv__stream_fd(handle) == -1)` |
| `ev_51025a5521ec` | call_site | `third_party/libuv/src/fs-poll.c:99` | `err = uv_fs_stat(loop, &ctx->fs_req, ctx->path, poll_cb);` |
| `ev_512ae64e62ae` | call_site | `third_party/libuv/src/unix/fs.c:664` | `uv__free((char*) dir->dirents[i].name);` |
| `ev_5133b749df90` | call_site | `third_party/libuv/src/unix/stream.c:915` | `uv__queue_remove(q);` |
| `ev_513e3cadc773` | call_site | `third_party/libuv/src/uv-common.c:860` | `loop = uv__malloc(sizeof(*loop));` |
| `ev_5149297a9ce2` | call_site | `third_party/libuv/src/unix/udp.c:146` | `uv__udp_recvmsg(handle);` |
| `ev_51615468af5f` | call_site | `third_party/libuv/src/unix/core.c:553` | `uv__close(fd);` |
| `ev_5170b36f45dc` | call_site | `third_party/libuv/src/unix/loop.c:69` | `uv__update_time(loop);` |
| `ev_5184c63db79c` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:120` | `uv__free(req->hostname);` |
| `ev_51f56cb20b31` | call_site | `third_party/libuv/src/threadpool.c:66` | `uv_mutex_lock(&mutex);` |
| `ev_520f44354230` | call_site | `third_party/libuv/src/unix/stream.c:735` | `uv__queue_insert_tail(&stream->write_completed_queue, &req->queue);` |
| `ev_521dbf60ba46` | call_site | `third_party/libuv/src/unix/fsevents.c:899` | `uv__free(handle->realpath);` |
| `ev_52577897d19d` | call_site | `third_party/libuv/src/unix/fsevents.c:437` | `paths = uv__malloc(sizeof(*paths) * path_count);` |
| `ev_5259063e5319` | call_site | `third_party/libuv/src/unix/fs.c:1723` | `X(FSYNC, uv__fs_fsync(req));` |
| `ev_5265c80a4731` | call_site | `third_party/libuv/src/unix/async.c:154` | `uv__async_spin(handle);` |
| `ev_52a5c033af1e` | call_site | `third_party/libuv/src/unix/fs.c:651` | `dirent->name = uv__strdup(res->d_name);` |
| `ev_52a7281f16ea` | call_site | `third_party/libuv/src/unix/fs.c:620` | `uv__free(dir);` |
| `ev_52ac4599ca7e` | call_site | `third_party/libuv/src/unix/loop.c:52` | `heap_init((struct heap*) &loop->timer_heap);` |
| `ev_52e5aa51f8d6` | call_site | `third_party/libuv/src/unix/stream.c:813` | `n = uv__writev(uv__stream_fd(stream), iov, iovcnt);` |
| `ev_52fd3aa290e7` | call_site | `third_party/libuv/src/unix/tcp.c:74` | `uv__close(sockfd);` |
| `ev_5307abe95af8` | call_site | `third_party/libuv/src/unix/darwin.c:50` | `uv__fsevents_loop_delete(loop);` |
| `ev_534cb57df4a2` | call_site | `third_party/libuv/src/unix/fs.c:1163` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_53bc2f6bea0c` | call_site | `third_party/libuv/src/unix/udp.c:1402` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_53bfb4a21c78` | call_site | `third_party/libuv/src/unix/fsevents.c:879` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_53db02f942c8` | call_site | `third_party/libuv/src/unix/kqueue.c:562` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_FS_EVENT);` |
| `ev_53debda5b8f2` | call_site | `third_party/libuv/src/unix/fs.c:2022` | `PATH;` |
| `ev_540e0a218219` | call_site | `third_party/libuv/src/unix/fsevents.c:189` | `handle->cb(handle, event->path[0] ? event->path : NULL, event->events, 0);` |
| `ev_5410c16778b6` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:147` | `pCFBundleGetInfoDictionary(pCFBundleGetMainBundle()));` |
| `ev_5425e8e14f2c` | assignment | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_544347c516ac` | call_site | `third_party/libuv/src/unix/stream.c:497` | `uv__close(err);` |
| `ev_5446f71c1fe6` | assignment | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_54a84ccd5390` | assignment | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_552aa6bee2f5` | call_site | `third_party/libuv/src/inet.c:40` | `return (inet_ntop6(src, dst, size));` |
| `ev_554360576ea4` | call_site | `third_party/libuv/src/unix/tty.c:330` | `rc = uv__tcsetattr(fd, TCSADRAIN, &tmp);` |
| `ev_55577e1bbafb` | call_site | `third_party/libuv/src/unix/pipe.c:57` | `return uv_pipe_bind2(handle, name, strlen(name), 0);` |
| `ev_5598c0090e96` | call_site | `third_party/libuv/src/unix/tty.c:183` | `r = uv__open_cloexec(path, mode \| O_NOCTTY);` |
| `ev_55ba9ba8e2f3` | call_site | `third_party/libuv/src/unix/stream.c:1111` | `uv__stream_eof(stream, &buf);` |
| `ev_55c7f02f05c4` | call_site | `third_party/libuv/src/unix/stream.c:116` | `uv__io_init(&stream->io_watcher, uv__stream_io, -1);` |
| `ev_55dfc4a5d81d` | call_site | `third_party/libuv/src/unix/signal.c:196` | `for (handle = uv__signal_first_handle(signum);` |
| `ev_5619dff01858` | call_site | `third_party/libuv/src/threadpool.c:287` | `uv_mutex_lock(&w->loop->wq_mutex);` |
| `ev_5631ee89fbf2` | call_site | `third_party/libuv/src/unix/core.c:1815` | `if (func(fd, name, &socklen))` |
| `ev_5649846deaaf` | call_site | `third_party/libuv/src/unix/stream.c:938` | `stream->read_cb(stream, UV_EOF, buf);` |
| `ev_566ec74a2aac` | call_site | `third_party/libuv/src/unix/pipe.c:535` | `uv__close(temp[0]);` |
| `ev_5675ec5f6895` | call_site | `third_party/libuv/src/unix/stream.c:250` | `if ((events & POLLIN) && uv__io_active(&stream->io_watcher, POLLIN))` |
| `ev_5685aa20daa9` | call_site | `third_party/libuv/src/unix/fsevents.c:646` | `uv_sem_wait(&loop->cf_sem);` |
| `ev_56f6f766f2c5` | call_site | `third_party/libuv/src/unix/signal.c:407` | `first_handle = uv__signal_first_handle(signum);` |
| `ev_574376669a89` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_57500a6c68c1` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_580809d7174c` | call_site | `third_party/libuv/src/unix/fs.c:494` | `return f(fd, bufs, nbufs, off);` |
| `ev_581f346928e6` | assignment | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_582755115ee9` | call_site | `third_party/libuv/src/unix/pipe.c:186` | `uv__free((void*)handle->pipe_fname);` |
| `ev_583ab4f93a99` | call_site | `third_party/libuv/src/unix/loop.c:117` | `uv__platform_loop_delete(loop);` |
| `ev_583cb6605bfb` | call_site | `third_party/libuv/src/unix/async.c:208` | `h->async_cb(h);` |
| `ev_58f3dc053f69` | call_site | `third_party/libuv/src/unix/fs.c:656` | `dirent->type = uv__fs_get_dirent_type(res);` |
| `ev_58fe38b49ad4` | call_site | `third_party/libuv/src/thread-common.c:132` | `uv_mutex_lock(&b->mutex);` |
| `ev_590d9da5de83` | call_site | `third_party/libuv/src/unix/fs.c:1608` | `ret = uv__fs_statx(-1, path, /* is_fstat */ 0, /* is_lstat */ 1, buf);` |
| `ev_597b32c514d3` | call_site | `third_party/libuv/src/unix/kqueue.c:192` | `while (!uv__queue_empty(&loop->watcher_queue)) {` |
| `ev_59991a2a699c` | call_site | `third_party/libuv/src/unix/stream.c:736` | `uv__io_feed(stream->loop, &stream->io_watcher);` |
| `ev_59c3e75c12ab` | call_site | `third_party/libuv/src/unix/stream.c:728` | `uv__free(req->bufs);` |
| `ev_59d075a072b3` | call_site | `third_party/libuv/src/unix/pipe.c:285` | `new_sock = (uv__stream_fd(handle) == -1);` |
| `ev_59f60353ca94` | call_site | `third_party/libuv/src/uv-common.c:106` | `newptr = uv__realloc(ptr, size);` |
| `ev_59fb50244220` | call_site | `third_party/libuv/src/idna.c:393` | `code_point = uv__wtf8_decode1(&source_ptr);` |
| `ev_5a18fbb06d02` | call_site | `third_party/libuv/src/unix/tcp.c:125` | `uv__stream_init(loop, (uv_stream_t*)tcp, UV_TCP);` |
| `ev_5a4a88855f09` | call_site | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_5a52e5fdcbdb` | assignment | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_5ad38a4dc79c` | call_site | `third_party/libuv/src/unix/tcp.c:659` | `if ((err = uv__nonblock(temp[0], 1)))` |
| `ev_5adadced276d` | call_site | `third_party/libuv/src/unix/udp.c:1094` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_5af4f57f3ee6` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:84` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFADDR))` |
| `ev_5b390a425a7f` | call_site | `third_party/libuv/src/unix/udp.c:1373` | `n = uv__udp_sendmsgv(handle->io_watcher.fd, n, bufs, nbufs, addrs);` |
| `ev_5b58ef217d45` | call_site | `third_party/libuv/src/unix/fs.c:1402` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_5bdecbd6b74d` | call_site | `third_party/libuv/src/unix/loop.c:45` | `err = uv_mutex_init(&lfields->loop_metrics.lock);` |
| `ev_5be55a6a63f7` | call_site | `third_party/libuv/src/unix/stream.c:1013` | `err = uv__stream_queue_fd(stream, fd);` |
| `ev_5c11ce139b5b` | call_site | `third_party/libuv/src/unix/udp.c:1221` | `uv__io_stop(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_5c15eb331bb0` | call_site | `third_party/libuv/src/idna.c:148` | `return uv__utf8_decode1_slow(p, pe, a);` |
| `ev_5c284c2bbc65` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:134` | `req->cb(req, req->retcode, req->addrinfo);` |
| `ev_5c29bfee24b1` | call_site | `third_party/libuv/src/unix/fs.c:1656` | `iovmax = uv__getiovmax();` |
| `ev_5c517fed95a7` | call_site | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_5c8f6805df6e` | call_site | `third_party/libuv/src/unix/tcp.c:389` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_5cc3b05c3da3` | call_site | `third_party/libuv/src/unix/loop.c:98` | `err = uv_async_init(loop, &loop->wq_async, uv__work_done);` |
| `ev_5ce83bb8bc9a` | call_site | `third_party/libuv/src/unix/stream.c:1279` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5d59c515efe5` | call_site | `third_party/libuv/src/unix/udp.c:873` | `uv__queue_init(&handle->write_completed_queue);` |
| `ev_5d6dd8e4fcd0` | assignment | `third_party/libuv/src/unix/udp.c:871` | `uv__io_init(&handle->io_watcher, uv__udp_io, fd);` |
| `ev_5da0d43629b9` | call_site | `third_party/libuv/src/unix/stream.c:1394` | `uv__io_start(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5dc3a69647f1` | call_site | `third_party/libuv/src/unix/fsevents.c:611` | `err = uv_mutex_init(&state->fsevent_mutex);` |
| `ev_5ddeddfa03c3` | call_site | `third_party/libuv/src/unix/fs.c:1721` | `X(FDATASYNC, uv__fs_fdatasync(req));` |
| `ev_5de8b5cf4f68` | call_site | `third_party/libuv/src/unix/core.c:972` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_5dfe7ef47841` | call_site | `third_party/libuv/src/unix/fs.c:1748` | `X(WRITE, uv__fs_write_all(req));` |
| `ev_5e0d82a8d673` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_5e29172f460a` | call_site | `third_party/libuv/src/random.c:40` | `rc = uv__random_getentropy(buf, buflen);` |
| `ev_5e51d6a8f660` | call_site | `third_party/libuv/src/unix/stream.c:1227` | `if (uv__stream_fd(stream) == -1)` |
| `ev_5e63f2080b13` | call_site | `third_party/libuv/src/uv-common.c:579` | `loop = uv_default_loop();` |
| `ev_5e6f3c1c78bf` | call_site | `third_party/libuv/src/unix/udp.c:394` | `err = uv__sock_reuseport(fd);` |
| `ev_5eeb998d958b` | assignment | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_5f075a82b1f5` | call_site | `third_party/libuv/src/timer.c:108` | `uv__queue_init(&handle->node.queue);` |
| `ev_5f1013b05f10` | call_site | `third_party/libuv/src/unix/stream.c:885` | `uv__io_start(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_5f18c7a1b894` | call_site | `third_party/libuv/src/uv-common.c:532` | `return uv__udp_try_send2(handle, count, bufs, nbufs, addrs);` |
| `ev_5f2b8640fe00` | call_site | `third_party/libuv/src/unix/stream.c:897` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_5f31fc43f11c` | call_site | `third_party/libuv/src/unix/core.c:447` | `uv__queue_empty(&loop->pending_queue) &&` |
| `ev_5f7ca3b47966` | call_site | `third_party/libuv/src/unix/fsevents.c:362` | `ref = pFSEventStreamCreate(NULL,` |
| `ev_5f9839a1c551` | assignment | `third_party/libuv/src/unix/stream.c:116` | `uv__io_init(&stream->io_watcher, uv__stream_io, -1);` |
| `ev_5fbcf071d1f8` | call_site | `third_party/libuv/src/threadpool.c:157` | `uv__queue_insert_tail(&wq, q);` |
| `ev_5fbfa427a21a` | call_site | `third_party/libuv/src/unix/fs.c:1667` | `result = uv__fs_write(req);` |
| `ev_5fef042454c0` | call_site | `third_party/libuv/src/unix/fs.c:1921` | `POST;` |
| `ev_604e44ac4249` | call_site | `third_party/libuv/src/idna.c:333` | `c = uv__utf8_decode1(&si, se);` |
| `ev_60512eda3418` | call_site | `third_party/libuv/src/unix/kqueue.c:390` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_6057ea19f056` | call_site | `third_party/libuv/src/unix/fsevents.c:777` | `uv__queue_insert_tail(&loop->cf_signals, &item->member);` |
| `ev_6059660fdccc` | call_site | `third_party/libuv/src/unix/fs.c:1438` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_60883ffec0b8` | call_site | `third_party/libuv/src/unix/stream.c:491` | `uv__close(loop->emfile_fd);` |
| `ev_609bc37ebcab` | call_site | `third_party/libuv/src/unix/fsevents.c:688` | `q = uv__queue_head(&loop->cf_signals);` |
| `ev_60b46f28c250` | call_site | `third_party/libuv/src/unix/tcp.c:358` | `err = uv__nonblock(sock, 1);` |
| `ev_60e3b9fa3cba` | assignment | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_6130817e9c34` | call_site | `third_party/libuv/src/unix/process.c:1104` | `uv__queue_remove(&handle->queue);` |
| `ev_61604e565231` | call_site | `third_party/libuv/src/threadpool.c:318` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_61776a622e07` | assignment | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_61917b99b437` | call_site | `third_party/libuv/src/unix/async.c:368` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_621fff9dc4e8` | call_site | `third_party/libuv/src/unix/signal.c:398` | `uv__signal_stop(handle);` |
| `ev_62435c030a57` | call_site | `third_party/libuv/src/unix/fsevents.c:711` | `state->loop = pCFRunLoopGetCurrent();` |
| `ev_62b71d0c2625` | call_site | `third_party/libuv/src/unix/udp.c:898` | `err = uv__nonblock(sock, 1);` |
| `ev_630b9e4a77cd` | call_site | `third_party/libuv/src/unix/stream.c:522` | `err = uv__emfile_trick(loop, fd);  /* Shed load. */` |
| `ev_63386b6d42ea` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:105` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFADDR))` |
| `ev_63a77851bcd7` | call_site | `third_party/libuv/src/unix/stream.c:1410` | `return uv_write2(req, handle, bufs, nbufs, NULL, cb);` |
| `ev_644304a0325d` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_64434f05a208` | call_site | `third_party/libuv/src/unix/fs.c:161` | `rc = uv__close_nocancel(fd);` |
| `ev_648bf01c3bc5` | assignment | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_648dfb0cd002` | call_site | `third_party/libuv/src/unix/pipe.c:87` | `if (includes_nul(name, namelen))` |
| `ev_6492225d3615` | call_site | `third_party/libuv/src/unix/pipe.c:226` | `return uv__stream_open((uv_stream_t*)handle, fd, flags);` |
| `ev_649f56ac6cfb` | call_site | `third_party/libuv/src/unix/udp.c:206` | `handle->recv_cb(handle,` |
| `ev_64c2099522fc` | call_site | `third_party/libuv/src/unix/process.c:1058` | `uv__free(pipes);` |
| `ev_6512b9056156` | call_site | `third_party/libuv/src/unix/signal.c:484` | `uv__signal_stop(handle);` |
| `ev_65367cb4f3b0` | call_site | `third_party/libuv/src/unix/dl.c:56` | `return *ptr ? 0 : uv__dlerror(lib);` |
| `ev_6542bbf38418` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:116` | `uv__free(req->hints);` |
| `ev_6579011471b7` | call_site | `third_party/libuv/src/threadpool.c:224` | `uv__queue_init(&wq);` |
| `ev_65c480cb5920` | call_site | `third_party/libuv/src/threadpool.c:114` | `uv__queue_insert_tail(&wq, &run_slow_work_message);` |
| `ev_65c87b1335e7` | call_site | `third_party/libuv/src/unix/udp.c:895` | `if (uv__fd_exists(handle->loop, sock))` |
| `ev_662c6abddea5` | call_site | `third_party/libuv/src/unix/fsevents.c:601` | `err = uv_sem_init(&loop->cf_sem, 0);` |
| `ev_666149bc530b` | call_site | `third_party/libuv/src/unix/stream.c:552` | `uv__close(server->accepted_fd);` |
| `ev_67130ff0ac23` | call_site | `third_party/libuv/src/unix/kqueue.c:91` | `uv__free(loop->cf_state);` |
| `ev_671bd90de973` | call_site | `third_party/libuv/src/unix/fs.c:2119` | `PATH;` |
| `ev_671f3fea8617` | call_site | `third_party/libuv/src/unix/fs.c:450` | `return uv__preadv_or_pwritev_emul(fd, bufs, nbufs, off, /*is_pread*/1);` |
| `ev_6776f5b3d557` | call_site | `third_party/libuv/src/unix/fsevents.c:665` | `uv__free(state);` |
| `ev_677f6776adf7` | call_site | `third_party/libuv/src/unix/process.c:919` | `uv_rwlock_wrunlock(&loop->cloexec_lock);` |
| `ev_67a3709e9127` | call_site | `third_party/libuv/src/unix/async.c:354` | `uv__io_stop(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_68072d3577a9` | call_site | `third_party/libuv/src/unix/fs.c:2008` | `req->path = uv__strdup(tpl);` |
| `ev_680bccec87c6` | call_site | `third_party/libuv/src/unix/kqueue.c:400` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_68104b5d2f94` | call_site | `third_party/libuv/src/unix/kqueue.c:644` | `r = uv__fsevents_close(handle);` |
| `ev_683e274ff5cd` | call_site | `third_party/libuv/src/inet.c:166` | `return inet_pton6(s, dst);` |
| `ev_68419e3b88a3` | call_site | `third_party/libuv/src/unix/fs.c:1612` | `ret = uv__lstat(path, &pbuf);` |
| `ev_68694d8cde28` | call_site | `third_party/libuv/src/unix/stream.c:253` | `if ((events & POLLOUT) && uv__io_active(&stream->io_watcher, POLLOUT))` |
| `ev_68b4272c6bea` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:251` | `return uv_if_indextoname(ifindex, buffer, size);` |
| `ev_68b9ba41d50f` | call_site | `third_party/libuv/src/unix/tcp.c:448` | `uv__io_start(tcp->loop, &tcp->io_watcher, POLLIN);` |
| `ev_691829d859d4` | call_site | `third_party/libuv/src/unix/stream.c:1304` | `if (uv__stream_fd(stream) < 0)` |
| `ev_6985ef7a5f00` | call_site | `third_party/libuv/src/unix/signal.c:268` | `err = uv__make_pipe(loop->signal_pipefd, UV_NONBLOCK_PIPE);` |
| `ev_69d8860f87b0` | call_site | `third_party/libuv/src/uv-common.c:316` | `return uv_inet_ntop(AF_INET6, &((struct sockaddr_in6 *)src)->sin6_addr,` |
| `ev_69ea19693ec1` | call_site | `third_party/libuv/src/fs-poll.c:60` | `uv__handle_init(loop, (uv_handle_t*)handle, UV_FS_POLL);` |
| `ev_69fe941170d6` | call_site | `third_party/libuv/src/unix/stream.c:420` | `uv__tcp_keepalive(fd, 1, 60)) {` |
| `ev_6a2bcb57421b` | call_site | `third_party/libuv/src/threadpool.c:123` | `w->work(w);` |
| `ev_6a4a8d4ff554` | assignment | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_6a67cb36a710` | call_site | `third_party/libuv/src/unix/stream.c:1289` | `uv__stream_flush_write_queue(stream, UV_ECANCELED);` |
| `ev_6a83c8437d0e` | call_site | `third_party/libuv/src/unix/process.c:160` | `uv__queue_init(&process->queue);` |
| `ev_6aa69d58c468` | call_site | `third_party/libuv/src/unix/fs.c:1734` | `X(SCANDIR, uv__fs_scandir(req));` |
| `ev_6aa8381e2655` | call_site | `third_party/libuv/src/unix/loop.c:56` | `uv__queue_init(&loop->check_handles);` |
| `ev_6b02388808c9` | call_site | `third_party/libuv/src/unix/fs.c:746` | `maxlen = uv__fs_pathmax_size(req->path);` |
| `ev_6b4c09ac33ec` | call_site | `third_party/libuv/src/unix/fs.c:1742` | `X(SENDFILE, uv__fs_sendfile(req));` |
| `ev_6b8b1f9ce4bb` | call_site | `third_party/libuv/src/unix/stream.c:1079` | `nread = uv__recvmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_6b8ddfde0360` | assignment | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_6b97758595fb` | call_site | `third_party/libuv/src/uv-common.c:550` | `return uv__udp_recv_stop(handle);` |
| `ev_6c1278f566c1` | call_site | `third_party/libuv/src/unix/loop.c:80` | `err = uv__platform_loop_init(loop);` |
| `ev_6d3e4f7d0370` | call_site | `third_party/libuv/src/unix/signal.c:565` | `ret = uv__signal_register_handler(handle->signum, 1);` |
| `ev_6d4ae22e552b` | call_site | `third_party/libuv/src/unix/fsevents.c:679` | `if (uv__cf_loop_signal(loop, NULL, kUVCFLoopSignalRegular) != 0)` |
| `ev_6d535b89b2dc` | call_site | `third_party/libuv/src/unix/fs.c:252` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_6d5f4c252e6d` | call_site | `third_party/libuv/src/unix/signal.c:76` | `uv__signal_global_reinit();` |
| `ev_6dacff143424` | call_site | `third_party/libuv/src/unix/tcp.c:310` | `r = connect(uv__stream_fd(handle), addr, addrlen);` |
| `ev_6dad2c55bfa8` | call_site | `third_party/libuv/src/unix/darwin.c:129` | `return uv_get_free_memory();` |
| `ev_6de247fe4648` | call_site | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_6e281d6e7a2f` | call_site | `third_party/libuv/src/unix/fsevents.c:746` | `item = uv__queue_head(&split_head);` |
| `ev_6e32e3735838` | call_site | `third_party/libuv/src/unix/loop.c:178` | `uv__close(loop->backend_fd);` |
| `ev_6e4e52a19053` | call_site | `third_party/libuv/src/unix/fsevents.c:720` | `pCFRunLoopRemoveSource(state->loop,` |
| `ev_6e565ce2957d` | call_site | `third_party/libuv/src/unix/core.c:1381` | `gr_mem = uv__malloc(name_size + mem_size);` |
| `ev_6e56ba1133e6` | call_site | `third_party/libuv/src/unix/stream.c:97` | `uv__queue_init(&stream->write_queue);` |
| `ev_6ed754a81fde` | call_site | `third_party/libuv/src/unix/async.c:109` | `uv__async_send(handle->loop);` |
| `ev_6ed962de3c19` | call_site | `third_party/libuv/src/unix/core.c:1161` | `uv__close(newfd);` |
| `ev_6f061adcc953` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:143` | `pLSSetApplicationLaunchServicesServerConnectionStatus(0, NULL);` |
| `ev_6f444a8f22bb` | call_site | `third_party/libuv/src/uv-common.c:109` | `uv__free(ptr);` |
| `ev_6f851eda2d79` | call_site | `third_party/libuv/src/uv-common.c:360` | `rc = uv__udp_init_ex(loop, handle, flags, domain);` |
| `ev_7032b2ad9f95` | call_site | `third_party/libuv/src/unix/tty.c:365` | `uv__stream_close((uv_stream_t*) handle);` |
| `ev_7063af7e594d` | call_site | `third_party/libuv/src/unix/core.c:363` | `handle->close_cb(handle);` |
| `ev_7069296110df` | call_site | `third_party/libuv/src/unix/signal.c:106` | `if (uv__signal_unlock())` |
| `ev_70ad00ca0156` | call_site | `third_party/libuv/src/unix/tcp.c:652` | `if ((err = uv__cloexec(temp[0], 1)))` |
| `ev_70b5fd2258d6` | call_site | `third_party/libuv/src/unix/stream.c:1263` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_70bdf8cb6036` | call_site | `third_party/libuv/src/unix/fs.c:2129` | `PATH;` |
| `ev_70f5dc732dff` | call_site | `third_party/libuv/src/unix/kqueue.c:615` | `uv__free(handle->path);` |
| `ev_7159861680a0` | call_site | `third_party/libuv/src/uv-common.c:203` | `copy = uv__strdup(buf);` |
| `ev_7170440dd9cb` | call_site | `third_party/libuv/src/unix/udp.c:61` | `uv__close(handle->io_watcher.fd);` |
| `ev_717c1e341227` | call_site | `third_party/libuv/src/unix/stream.c:888` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_71b1d11ab510` | call_site | `third_party/libuv/src/unix/core.c:1456` | `uv__free(buf);` |
| `ev_720266ec755c` | call_site | `third_party/libuv/src/unix/thread.c:113` | `return uv__default_stack_size();` |
| `ev_7249cdfb8c22` | call_site | `third_party/libuv/src/threadpool.c:211` | `threads = uv__malloc(nthreads * sizeof(threads[0]));` |
| `ev_727d04330d42` | call_site | `third_party/libuv/src/unix/core.c:807` | `if (uv__cloexec(fd, 1) && fd > 15)` |
| `ev_729679b71839` | call_site | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_72b324ab06dd` | call_site | `third_party/libuv/src/unix/proctitle.c:42` | `uv_mutex_init(&process_title_mutex);` |
| `ev_72d25a3e450c` | call_site | `third_party/libuv/src/fs-poll.c:221` | `uv_fs_req_cleanup(req);` |
| `ev_734814f05104` | call_site | `third_party/libuv/src/unix/process.c:301` | `uv__write_errno(error_fd);` |
| `ev_7355587f6539` | call_site | `third_party/libuv/src/unix/loop.c:84` | `uv__signal_global_once_init();` |
| `ev_736c6a1ee36d` | call_site | `third_party/libuv/src/unix/pipe.c:469` | `if (uv__stat(name_buffer, &pipe_stat) == -1)` |
| `ev_7389c7f3eade` | call_site | `third_party/libuv/src/fs-poll.c:171` | `uv__make_close_pending((uv_handle_t*)handle);` |
| `ev_739e63d8b500` | call_site | `third_party/libuv/src/unix/signal.c:94` | `uv__close(uv__signal_lock_pipefd[1]);` |
| `ev_73b38530cdae` | call_site | `third_party/libuv/src/unix/process.c:352` | `uv__write_int(error_fd, n);` |
| `ev_73b55b9d0886` | call_site | `third_party/libuv/src/unix/stream.c:1231` | `uv__write(stream);` |
| `ev_73b5d163aa4a` | call_site | `third_party/libuv/src/unix/pipe.c:215` | `err = uv__stream_try_select((uv_stream_t*) handle, &fd);` |
| `ev_73bbc97ad5bc` | call_site | `third_party/libuv/src/unix/fsevents.c:439` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_73ca266fd72c` | call_site | `third_party/libuv/src/threadpool.c:324` | `while (!uv__queue_empty(&wq)) {` |
| `ev_73d6a0e24c74` | call_site | `third_party/libuv/src/unix/stream.c:1435` | `return uv__try_write(stream, bufs, nbufs, send_handle);` |
| `ev_7400d8d34315` | call_site | `third_party/libuv/src/unix/fs.c:1420` | `err = uv__close_nocheckstdio(srcfd);` |
| `ev_74049b001659` | call_site | `third_party/libuv/src/unix/core.c:175` | `uv__tcp_close((uv_tcp_t*)handle);` |
| `ev_7405ce9f82b6` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:146` | `pLSApplicationCheckIn(-2,` |
| `ev_740962944152` | call_site | `third_party/libuv/src/uv-common.c:371` | `return uv_udp_init_ex(loop, handle, AF_UNSPEC);` |
| `ev_74419188bc2f` | call_site | `third_party/libuv/src/unix/fsevents.c:371` | `pFSEventStreamScheduleWithRunLoop(ref, state->loop, *pkCFRunLoopDefaultMode);` |
| `ev_74543600cfb2` | call_site | `third_party/libuv/src/uv-common.c:449` | `if (uv_udp_getpeername(handle, (struct sockaddr*) &addr, &addrlen) != 0)` |
| `ev_748ab347c266` | call_site | `third_party/libuv/src/threadpool.c:300` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_74a98bfe55ce` | call_site | `third_party/libuv/src/unix/thread.c:313` | `return uv__thread_getname(tid, name, size);` |
| `ev_74b634b3e8ff` | call_site | `third_party/libuv/src/threadpool.c:75` | `slow_io_work_running >= slow_work_thread_threshold())) {` |
| `ev_7522765d1036` | call_site | `third_party/libuv/src/unix/udp.c:872` | `uv__queue_init(&handle->write_queue);` |
| `ev_75392261f203` | call_site | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_75406c8b6161` | call_site | `third_party/libuv/src/unix/process.c:1071` | `uv__close_nocheckstdio(pipes[i][1]);` |
| `ev_75734426f05a` | call_site | `third_party/libuv/src/unix/fs.c:503` | `return uv__preadv_or_pwritev(fd, bufs, nbufs, off, &cache, /*is_pread*/1);` |
| `ev_757f45674b98` | call_site | `third_party/libuv/src/uv-common.c:77` | `return uv__allocator.local_malloc(size);` |
| `ev_75848779bc85` | call_site | `third_party/libuv/src/threadpool.c:102` | `if (uv__queue_empty(&slow_io_pending_wq))` |
| `ev_75cfe8001256` | call_site | `third_party/libuv/src/uv-common.c:249` | `return uv__unknown_err_code(err);` |
| `ev_7637f38d007a` | call_site | `third_party/libuv/src/unix/kqueue.c:407` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_765cb02c86a1` | call_site | `third_party/libuv/src/unix/udp.c:241` | `handle->alloc_cb((uv_handle_t*) handle, UV__UDP_DGRAM_MAXSIZE, &buf);` |
| `ev_766c7a4d2c9a` | call_site | `third_party/libuv/src/unix/core.c:478` | `uv__run_timers(loop);` |
| `ev_768cf1885315` | call_site | `third_party/libuv/src/unix/thread.c:306` | `return uv__thread_setname(name);` |
| `ev_76b88df8c6b7` | call_site | `third_party/libuv/src/unix/process.c:270` | `uv__write_int(error_fd, UV__ERR(errno));` |
| `ev_77282b3916c2` | call_site | `third_party/libuv/src/fs-poll.c:88` | `ctx->start_time = uv_now(loop);` |
| `ev_773cac45e64e` | assignment | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_773f11a10c5b` | call_site | `third_party/libuv/src/inet.c:152` | `return (inet_pton4(src, dst));` |
| `ev_787be673cf24` | call_site | `third_party/libuv/src/unix/async.c:193` | `while (!uv__queue_empty(&queue)) {` |
| `ev_791f66959b2c` | assignment | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_797ce2ad40cd` | call_site | `third_party/libuv/src/unix/kqueue.c:106` | `if (uv__fstat(fd, &sb))` |
| `ev_7987974b213e` | call_site | `third_party/libuv/src/unix/stream.c:254` | `uv__stream_io(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_79a966fecc53` | call_site | `third_party/libuv/src/unix/dl.c:42` | `uv__free(lib->errmsg);` |
| `ev_79cad2fd59d2` | call_site | `third_party/libuv/src/unix/loop.c:186` | `uv_mutex_destroy(&loop->wq_mutex);` |
| `ev_7a1766d69d6f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_7ad5392ecc96` | call_site | `third_party/libuv/src/unix/process.c:360` | `uv__write_errno(error_fd);` |
| `ev_7adfb00d6fc3` | assignment | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_7af545e4ff66` | call_site | `third_party/libuv/src/unix/core.c:852` | `uv__queue_init(q);` |
| `ev_7b055d7f58c9` | call_site | `third_party/libuv/src/unix/stream.c:911` | `while (!uv__queue_empty(&pq)) {` |
| `ev_7b2ab2ee5ea1` | call_site | `third_party/libuv/src/unix/core.c:978` | `uv__queue_remove(&w->pending_queue);` |
| `ev_7b49cdbdb717` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_7b875945d255` | call_site | `third_party/libuv/src/unix/tcp.c:375` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_7ba421a35714` | call_site | `third_party/libuv/src/unix/proctitle.c:121` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_7c1946c115dc` | call_site | `third_party/libuv/src/unix/proctitle.c:119` | `uv__set_process_title(pt->str);` |
| `ev_7c30a737a963` | call_site | `third_party/libuv/src/unix/udp.c:150` | `uv__udp_run_completed(handle);` |
| `ev_7c38728fe6ad` | call_site | `third_party/libuv/src/unix/core.c:416` | `return uv__backend_timeout(loop);` |
| `ev_7c453864dec2` | call_site | `third_party/libuv/src/unix/fs.c:1823` | `PATH;` |
| `ev_7c66fd136764` | call_site | `third_party/libuv/src/unix/core.c:396` | `!uv__queue_empty(&loop->pending_queue) \|\|` |
| `ev_7c677d651647` | call_site | `third_party/libuv/src/unix/udp.c:813` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET6, UV_UDP_REUSEADDR);` |
| `ev_7c8564c28616` | call_site | `third_party/libuv/src/unix/signal.c:353` | `uv__signal_stop(handle);` |
| `ev_7ca0a06a6b5b` | assignment | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_7cbe7f5d4fb7` | call_site | `third_party/libuv/src/unix/fsevents.c:484` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_7cc58377c31a` | call_site | `third_party/libuv/src/threadpool.c:148` | `if (!uv__queue_empty(&run_slow_work_message)) {` |
| `ev_7d269f408585` | call_site | `third_party/libuv/src/unix/signal.c:191` | `if (uv__signal_lock()) {` |
| `ev_7d27be801e6f` | call_site | `third_party/libuv/src/unix/stream.c:1566` | `return uv__nonblock(uv__stream_fd(handle), !blocking);` |
| `ev_7d4f0413754a` | call_site | `third_party/libuv/src/unix/async.c:197` | `uv__queue_remove(q);` |
| `ev_7d90fbb75433` | call_site | `third_party/libuv/src/unix/pipe.c:518` | `if ((err = uv__cloexec(temp[1], 1)))` |
| `ev_7df1be6a60da` | call_site | `third_party/libuv/src/unix/udp.c:1213` | `uv__io_start(handle->loop, &handle->io_watcher, POLLIN);` |
| `ev_7e0dc6f23a1f` | call_site | `third_party/libuv/src/unix/fsevents.c:425` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_7e2a9a65b588` | call_site | `third_party/libuv/src/unix/stream.c:1285` | `if (uv__stream_fd(stream) == -1)` |
| `ev_7e2f7ce88e7d` | call_site | `third_party/libuv/src/unix/core.c:819` | `fd_out = uv__stream_fd((uv_stream_t*) handle);` |
| `ev_7e4cb252a290` | call_site | `third_party/libuv/src/unix/random-devurandom.c:49` | `uv__close(fd);` |
| `ev_7e4d1b53780f` | call_site | `third_party/libuv/src/unix/fsevents.c:697` | `uv_mutex_destroy(&state->fsevent_mutex);` |
| `ev_7e50f4886f5d` | call_site | `third_party/libuv/src/unix/proctitle.c:107` | `uv_once(&process_title_mutex_once, init_process_title_mutex_once);` |
| `ev_7e6a3fa339ef` | call_site | `third_party/libuv/src/unix/stream.c:858` | `q = uv__queue_head(&stream->write_queue);` |
| `ev_7e7f6f944a88` | call_site | `third_party/libuv/src/fs-poll.c:119` | `if (!uv_is_active((uv_handle_t*)handle))` |
| `ev_7eac5862569a` | call_site | `third_party/libuv/src/unix/stream.c:466` | `uv__write_callbacks(stream);` |
| `ev_7f02ea6496ff` | assignment | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_7f05828baffe` | assignment | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_7f2edeedc5b0` | call_site | `third_party/libuv/src/unix/kqueue.c:369` | `w->cb(loop, w, w->events);` |
| `ev_7f35d7b5a699` | call_site | `third_party/libuv/src/unix/udp.c:926` | `return uv__udp_set_membership4(handle, &addr4, interface_addr, membership);` |
| `ev_7f3f110e9dfb` | call_site | `third_party/libuv/src/unix/signal.c:532` | `uv__signal_stop(handle);` |
| `ev_7f6793cbc485` | assignment | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_7f97a20176a3` | call_site | `third_party/libuv/src/unix/fsevents.c:684` | `uv_mutex_destroy(&loop->cf_mutex);` |
| `ev_7f9991823f2e` | call_site | `third_party/libuv/src/unix/signal.c:219` | `uv__signal_unlock();` |
| `ev_7fc004c222d4` | call_site | `third_party/libuv/src/unix/core.c:1808` | `r = uv_fileno(handle, &fd);` |
| `ev_7fca44d60f49` | call_site | `third_party/libuv/src/timer.c:89` | `heap_insert(timer_heap(handle->loop),` |
| `ev_7fda347c51a3` | call_site | `third_party/libuv/src/unix/stream.c:1521` | `uv_thread_join(&s->thread);` |
| `ev_7ffe0a334d62` | call_site | `third_party/libuv/src/unix/core.c:580` | `err = uv__nonblock(peerfd, 1);` |
| `ev_803d9fc2e66f` | call_site | `third_party/libuv/src/unix/stream.c:380` | `uv_sem_destroy(&s->async_sem);` |
| `ev_8053cf589106` | call_site | `third_party/libuv/src/unix/fsevents.c:659` | `uv_sem_destroy(&loop->cf_sem);` |
| `ev_807929ffb79d` | call_site | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_80caf9cfa23a` | call_site | `third_party/libuv/src/unix/stream.c:1290` | `uv__write_callbacks(stream);` |
| `ev_80ce08357450` | call_site | `third_party/libuv/src/uv-common.c:313` | `return uv_inet_ntop(AF_INET, &((struct sockaddr_in *)src)->sin_addr,` |
| `ev_814facd894f9` | call_site | `third_party/libuv/src/unix/tcp.c:136` | `uv__close(tcp->io_watcher.fd);` |
| `ev_81822f939bc1` | call_site | `third_party/libuv/src/threadpool.c:89` | `uv__queue_init(q);  /* Signal uv_cancel() that the work req is executing. */` |
| `ev_81c808a3bc76` | call_site | `third_party/libuv/src/unix/fs.c:2276` | `uv__fs_scandir_cleanup(req);` |
| `ev_81db7a9d7a79` | call_site | `third_party/libuv/src/unix/fs.c:2188` | `PATH2;` |
| `ev_81ddac4db117` | call_site | `third_party/libuv/src/unix/stream.c:1522` | `uv_sem_destroy(&s->close_sem);` |
| `ev_81f97056b8fd` | call_site | `third_party/libuv/src/timer.c:187` | `queue_node = uv__queue_head(&ready_queue);` |
| `ev_820f11433640` | call_site | `third_party/libuv/src/unix/poll.c:84` | `err = uv__nonblock_fcntl(fd, 1);` |
| `ev_826173396cba` | call_site | `third_party/libuv/src/uv-common.c:301` | `return uv_inet_ntop(AF_INET, &src->sin_addr, dst, size);` |
| `ev_827825785ab4` | call_site | `third_party/libuv/src/thread-common.c:110` | `uv_cond_wait((uv_cond_t*) &b->cond, &b->mutex);` |
| `ev_82c7f16d1e5e` | assignment | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_830154a4c8db` | call_site | `third_party/libuv/src/unix/core.c:195` | `uv__async_close((uv_async_t*)handle);` |
| `ev_834b0d3a1de5` | call_site | `third_party/libuv/src/unix/stream.c:383` | `uv_sem_destroy(&s->close_sem);` |
| `ev_834e9d8b5921` | call_site | `third_party/libuv/src/unix/stream.c:1204` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_8351687ab60b` | call_site | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_8398ce4bdc2f` | call_site | `third_party/libuv/src/threadpool.c:81` | `q = uv__queue_head(&wq);` |
| `ev_83bb25b6b9b4` | call_site | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_840307191aa9` | call_site | `third_party/libuv/src/unix/random-devurandom.c:82` | `status = uv__random_readpath("/dev/random", &c, 1);` |
| `ev_8421ff19b86f` | call_site | `third_party/libuv/src/unix/udp.c:125` | `req->send_cb(req, req->status);` |
| `ev_842791aeeedd` | call_site | `third_party/libuv/src/unix/udp.c:716` | `if (uv_ip6_addr(interface_addr, 0, &addr6))` |
| `ev_8443df6fae21` | call_site | `third_party/libuv/src/unix/stream.c:595` | `uv__io_start(server->loop, &server->io_watcher, POLLIN);` |
| `ev_8451186eb1f3` | call_site | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_845f29d716c9` | call_site | `third_party/libuv/src/unix/process.c:914` | `uv_rwlock_wrlock(&loop->cloexec_lock);` |
| `ev_848e03795dba` | call_site | `third_party/libuv/src/queue.h:66` | `uv__queue_split(h, h->next, n);` |
| `ev_8499d75c493c` | call_site | `third_party/libuv/src/random.c:116` | `uv__work_submit(loop,` |
| `ev_853fd77ee1a5` | call_site | `third_party/libuv/src/unix/stream.c:1525` | `uv__close(s->int_fd);` |
| `ev_8552f15a2590` | call_site | `third_party/libuv/src/idna.c:178` | `c = uv__utf8_decode1(&s, se);` |
| `ev_8556ed0432de` | call_site | `third_party/libuv/src/threadpool.c:302` | `uv_async_send(&loop->wq_async);` |
| `ev_85717ca19a40` | call_site | `third_party/libuv/src/unix/core.c:988` | `uv__queue_insert_tail(&loop->pending_queue, &w->pending_queue);` |
| `ev_85a3a740507a` | call_site | `third_party/libuv/src/unix/fsevents.c:240` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_85a89b637451` | call_site | `third_party/libuv/src/unix/fs.c:2214` | `PATH;` |
| `ev_85dd0d3a7986` | assignment | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_85ec735aee3a` | call_site | `third_party/libuv/src/unix/stream.c:1342` | `err = uv__check_before_write(stream, nbufs, send_handle);` |
| `ev_860dd1a2cd6b` | call_site | `third_party/libuv/src/unix/pipe.c:536` | `uv__close(temp[1]);` |
| `ev_86133c1a823d` | call_site | `third_party/libuv/src/unix/core.c:547` | `fd = uv__open_cloexec(path, O_RDONLY);` |
| `ev_861532f4f5e8` | call_site | `third_party/libuv/src/unix/fsevents.c:480` | `pCFRelease(cf_paths);` |
| `ev_863cb0ea432f` | call_site | `third_party/libuv/src/unix/stream.c:1523` | `uv_sem_destroy(&s->async_sem);` |
| `ev_866a9cce71ad` | call_site | `third_party/libuv/src/unix/core.c:849` | `while (!uv__queue_empty(&pq)) {` |
| `ev_867293ea574a` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:206` | `uv__work_submit(loop,` |
| `ev_8673ccdb7fa3` | call_site | `third_party/libuv/src/unix/loop.c:55` | `uv__queue_init(&loop->async_handles);` |
| `ev_8700275783f6` | call_site | `third_party/libuv/src/idna.c:356` | `rc = uv__idna_toascii_label(s, se, &d, de);` |
| `ev_8729f0989741` | call_site | `third_party/libuv/src/unix/getnameinfo.c:73` | `req->getnameinfo_cb(req, req->retcode, host, service);` |
| `ev_8759c9907e95` | call_site | `third_party/libuv/src/unix/fs.c:1278` | `dstfd = uv_fs_open(NULL,` |
| `ev_87780bd3e380` | call_site | `third_party/libuv/src/unix/async.c:373` | `uv__queue_remove(q);` |
| `ev_8784472b39e8` | call_site | `third_party/libuv/src/unix/poll.c:159` | `uv__poll_stop(handle);` |
| `ev_879b038cf0b3` | call_site | `third_party/libuv/src/threadpool.c:147` | `uv__queue_insert_tail(&slow_io_pending_wq, q);` |
| `ev_87ae09c864b6` | call_site | `third_party/libuv/src/unix/loop.c:168` | `uv__signal_loop_cleanup(loop);` |
| `ev_87e0b4b4f8e6` | call_site | `third_party/libuv/src/unix/fsevents.c:421` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_87ec923c051a` | call_site | `third_party/libuv/src/unix/pipe.c:338` | `uv__queue_init(&req->queue);` |
| `ev_8822dd8ed2e8` | call_site | `third_party/libuv/src/unix/stream.c:107` | `err = uv__open_cloexec("/", O_RDONLY);` |
| `ev_882b5680dbef` | call_site | `third_party/libuv/src/unix/darwin.c:42` | `if (uv__kqueue_init(loop))` |
| `ev_888f9cc8daa6` | call_site | `third_party/libuv/src/unix/udp.c:606` | `handle->send_queue_size += uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_888fccbe3315` | call_site | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_88d5bb7eae60` | call_site | `third_party/libuv/src/threadpool.c:134` | `uv_mutex_lock(&mutex);` |
| `ev_88f44777a60b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:103` | `S("_LSGetCurrentApplicationASN"));` |
| `ev_8908b0232434` | call_site | `third_party/libuv/src/unix/stream.c:1540` | `uv__close(handle->io_watcher.fd);` |
| `ev_892ce661d115` | call_site | `third_party/libuv/src/unix/fsevents.c:769` | `item = uv__malloc(sizeof(*item));` |
| `ev_8951169c97a8` | call_site | `third_party/libuv/src/timer.c:182` | `uv_timer_stop(handle);` |
| `ev_89832f95168f` | call_site | `third_party/libuv/src/unix/stream.c:173` | `if (uv__io_active(&stream->io_watcher, POLLIN))` |
| `ev_89944018e590` | call_site | `third_party/libuv/src/threadpool.c:326` | `uv__queue_remove(q);` |
| `ev_89a5c35c4a43` | call_site | `third_party/libuv/src/unix/udp.c:1022` | `return uv__setsockopt(handle, option4, option6, &arg, sizeof(arg));` |
| `ev_89b22020ea9e` | call_site | `third_party/libuv/src/unix/fsevents.c:890` | `uv_close((uv_handle_t*) handle->cf_cb, (uv_close_cb) uv__free);` |
| `ev_89ed7f7e890c` | call_site | `third_party/libuv/src/unix/stream.c:461` | `stream->connect_req->cb(stream->connect_req, UV_ECANCELED);` |
| `ev_8a079a656194` | call_site | `third_party/libuv/src/unix/tcp.c:94` | `return new_socket(handle, domain, flags);` |
| `ev_8a2d2e5b978b` | call_site | `third_party/libuv/src/uv-common.c:495` | `addrlen = uv__udp_check_before_send(handle, addr);` |
| `ev_8a3b2615659b` | call_site | `third_party/libuv/src/unix/core.c:851` | `uv__queue_remove(q);` |
| `ev_8a7645104cfb` | assignment | `third_party/libuv/src/unix/poll.c:91` | `uv__io_init(&handle->io_watcher, uv__poll_io, fd);` |
| `ev_8a8fef961a5b` | call_site | `third_party/libuv/src/unix/fs.c:353` | `if (r >= 0 && uv__cloexec(r, 1) != 0) {` |
| `ev_8aa5318c12f8` | call_site | `third_party/libuv/src/unix/stream.c:937` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_8ab5cf71b1e1` | call_site | `third_party/libuv/src/thread-common.c:107` | `uv_cond_broadcast((uv_cond_t*) &b->cond);` |
| `ev_8ad099db703f` | call_site | `third_party/libuv/src/unix/pipe.c:112` | `pipe_fname = uv__malloc(namelen + 1);` |
| `ev_8b09c69fb987` | call_site | `third_party/libuv/src/heap-inl.h:222` | `if (child->left != NULL && less_than(child->left, smallest))` |
| `ev_8b3fe28acd59` | call_site | `third_party/libuv/src/unix/core.c:1130` | `if (uv__close_nocheckstdio(fd))` |
| `ev_8bca323dfdca` | call_site | `third_party/libuv/src/unix/process.c:775` | `err = uv__spawn_set_posix_spawn_attrs(&attrs, posix_spawn_fncs, options);` |
| `ev_8bcba93cfab2` | call_site | `third_party/libuv/src/fs-poll.c:168` | `uv_fs_poll_stop(handle);` |
| `ev_8c1081a3c5b7` | call_site | `third_party/libuv/src/unix/fs.c:512` | `return uv__preadv_or_pwritev(fd, bufs, nbufs, off, &cache, /*is_pread*/0);` |
| `ev_8c212d16a019` | call_site | `third_party/libuv/src/unix/udp.c:128` | `if (uv__queue_empty(&handle->write_queue)) {` |
| `ev_8c3979abc4b1` | call_site | `third_party/libuv/src/unix/udp.c:1377` | `req->status = uv__count_bufs(req->bufs, req->nbufs);` |
| `ev_8c41ce7011b4` | assignment | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_8c5f4faca50f` | call_site | `third_party/libuv/src/unix/stream.c:1558` | `assert(!uv__io_active(&handle->io_watcher, POLLIN \| POLLOUT));` |
| `ev_8c69561c8948` | call_site | `third_party/libuv/src/uv-common.c:614` | `uv__print_handles(loop, 1, stream);` |
| `ev_8c6b6bb04461` | assignment | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_8c8fe0ae3395` | call_site | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_8ca419191127` | call_site | `third_party/libuv/src/fs-poll.c:80` | `ctx = uv__calloc(1, sizeof(*ctx) + len);` |
| `ev_8cbd97a1d7ff` | call_site | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_8d5bed6f359b` | call_site | `third_party/libuv/src/unix/udp.c:197` | `handle->recv_cb(handle, UV__ERR(errno), buf, NULL, 0);` |
| `ev_8d7e05f143e1` | call_site | `third_party/libuv/src/unix/stream.c:1385` | `uv__write(stream);` |
| `ev_8dc6560f30db` | call_site | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_8e0af9132b30` | call_site | `third_party/libuv/src/unix/random-devurandom.c:87` | `uv_once(&once, uv__random_devurandom_init);` |
| `ev_8e0f7f9df419` | call_site | `third_party/libuv/src/unix/process.c:703` | `path = uv__spawn_find_path_in_env(env);` |
| `ev_8e2afb8db7ba` | call_site | `third_party/libuv/src/unix/core.c:220` | `uv__poll_close((uv_poll_t*)handle);` |
| `ev_8e3d8b6539fb` | call_site | `third_party/libuv/src/unix/udp.c:1399` | `uv__queue_remove(&req->queue);` |
| `ev_8e52d127706f` | call_site | `third_party/libuv/src/unix/udp.c:1375` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_8e90f2f0061d` | call_site | `third_party/libuv/src/unix/fs.c:1203` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_8eb9f4be2d9f` | call_site | `third_party/libuv/src/uv-common.c:909` | `err = uv_loop_close(loop);` |
| `ev_8ecf7baf4b64` | call_site | `third_party/libuv/src/timer.c:189` | `uv__queue_init(queue_node);` |
| `ev_8ef1bbe13fbb` | call_site | `third_party/libuv/src/unix/dl.c:68` | `uv__free(lib->errmsg);` |
| `ev_8f018f9369dc` | assignment | `third_party/libuv/src/unix/getnameinfo.c:110` | `uv__work_submit(loop,` |
| `ev_8f26eb811f45` | call_site | `third_party/libuv/src/unix/stream.c:612` | `err = uv__pipe_listen((uv_pipe_t*)stream, backlog, cb);` |
| `ev_8f5ba541b11c` | call_site | `third_party/libuv/src/unix/async.c:345` | `uv__async_spin(h);` |
| `ev_8f83c2427ef5` | call_site | `third_party/libuv/src/unix/process.c:1047` | `err = uv__process_open_stream(options->stdio + i, pipes[i]);` |
| `ev_8fab43dca120` | call_site | `third_party/libuv/src/unix/process.c:246` | `return uv__stream_open(container->data.stream, pipefds[0], flags);` |
| `ev_8fba5d7ce7d4` | call_site | `third_party/libuv/src/unix/fsevents.c:898` | `uv_mutex_destroy(&handle->cf_mutex);` |
| `ev_8fc0e4559b5a` | call_site | `third_party/libuv/src/unix/core.c:452` | `uv__run_prepare(loop);` |
| `ev_903bee8fb2ff` | call_site | `third_party/libuv/src/unix/poll.c:114` | `uv__poll_stop(handle);` |
| `ev_90507fb3e4a5` | call_site | `third_party/libuv/src/uv-common.c:425` | `return uv__udp_disconnect(handle);` |
| `ev_906405d3e7d4` | call_site | `third_party/libuv/src/unix/signal.c:103` | `if (uv__make_pipe(uv__signal_lock_pipefd, 0))` |
| `ev_90ba0c8ebd79` | call_site | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_90f0cfd2d7f3` | call_site | `third_party/libuv/src/unix/udp.c:619` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_912142859eda` | call_site | `third_party/libuv/src/unix/pipe.c:99` | `if (uv__stream_fd(handle) >= 0)` |
| `ev_913d84408ff1` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:136` | `pCFBundleGetFunctionPointerForName(` |
| `ev_9145bd76d762` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_9153b09f77a1` | call_site | `third_party/libuv/src/unix/udp.c:1369` | `q = uv__queue_next(q);` |
| `ev_9187d4cf3774` | call_site | `third_party/libuv/src/unix/loop.c:169` | `uv__platform_loop_delete(loop);` |
| `ev_918f4160003e` | call_site | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_919d9de04858` | call_site | `third_party/libuv/src/unix/fsevents.c:419` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_91afe4964a4b` | call_site | `third_party/libuv/src/unix/udp.c:278` | `handle->recv_cb(handle, nread, &buf, (const struct sockaddr*) &peer, flags);` |
| `ev_91ecc97a6372` | call_site | `third_party/libuv/src/unix/fsevents.c:453` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_92021d222814` | call_site | `third_party/libuv/src/unix/pipe.c:167` | `if (listen(uv__stream_fd(handle), backlog))` |
| `ev_9211d111f581` | call_site | `third_party/libuv/src/unix/stream.c:1235` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_92655b3c6378` | call_site | `third_party/libuv/src/unix/udp.c:195` | `handle->recv_cb(handle, 0, buf, NULL, 0);` |
| `ev_92a32d90b1e1` | call_site | `third_party/libuv/src/unix/fsevents.c:691` | `uv__free(s);` |
| `ev_92cf37040163` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:116` | `S("_kLSDisplayNameKey"));` |
| `ev_92db1b96584c` | call_site | `third_party/libuv/src/unix/fsevents.c:741` | `uv_mutex_lock(&loop->cf_mutex);` |
| `ev_92e032141a9e` | call_site | `third_party/libuv/src/inet.c:57` | `uv__strscpy(dst, tmp, size);` |
| `ev_93301b7a3cbf` | call_site | `third_party/libuv/src/unix/loop.c:88` | `uv__queue_init(&loop->process_handles);` |
| `ev_933a7b9157fd` | assignment | `third_party/libuv/src/unix/fs.c:2251` | `POST;` |
| `ev_933abdc79656` | call_site | `third_party/libuv/src/unix/kqueue.c:368` | `uv__metrics_update_idle_time(loop);` |
| `ev_94193e1159f3` | call_site | `third_party/libuv/src/unix/fs.c:1284` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_944a82327899` | call_site | `third_party/libuv/src/unix/core.c:224` | `uv__fs_poll_close((uv_fs_poll_t*)handle);` |
| `ev_94be85a7e907` | call_site | `third_party/libuv/src/unix/core.c:924` | `maybe_resize(loop, w->fd + 1);` |
| `ev_94c476b48777` | call_site | `third_party/libuv/src/thread-common.c:61` | `rc = uv_mutex_init(&b->mutex);` |
| `ev_94e1933354c1` | call_site | `third_party/libuv/src/unix/core.c:977` | `uv__io_stop(loop, w, POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI);` |
| `ev_94f64ad7ca60` | call_site | `third_party/libuv/src/random.c:90` | `req->cb(req, status, req->buf, req->buflen);` |
| `ev_9521436d2375` | call_site | `third_party/libuv/src/queue.h:64` | `uv__queue_init(n);` |
| `ev_957e6f6b3269` | call_site | `third_party/libuv/src/unix/pipe.c:342` | `uv__io_feed(handle->loop, &handle->io_watcher);` |
| `ev_958b3e530e0d` | call_site | `third_party/libuv/src/unix/async.c:311` | `uv__io_init(&loop->async_io_watcher, uv__async_io, pipefd[0]);` |
| `ev_95b5c4d30645` | call_site | `third_party/libuv/src/unix/stream.c:1283` | `req->cb(req, error);` |
| `ev_95f5260e8fa3` | call_site | `third_party/libuv/src/unix/stream.c:788` | `fd_to_send = uv__handle_fd((uv_handle_t*) send_handle);` |
| `ev_960d6e13976f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_960ecf83810d` | call_site | `third_party/libuv/src/uv-common.c:1043` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_960f995b9028` | call_site | `third_party/libuv/src/unix/signal.c:410` | `err = uv__signal_register_handler(signum, oneshot);` |
| `ev_9622376feeb3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_96678e28119a` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_9685951f020b` | call_site | `third_party/libuv/src/unix/core.c:409` | `return uv__next_timeout(loop);` |
| `ev_96bc0c497273` | call_site | `third_party/libuv/src/unix/udp.c:1144` | `} else if (uv_ip6_addr(interface_addr, 0, addr6) == 0) {` |
| `ev_96fa53e797d9` | call_site | `third_party/libuv/src/unix/dl.c:73` | `lib->errmsg = uv__strdup(errmsg);` |
| `ev_9707b2acf0f3` | call_site | `third_party/libuv/src/random.c:77` | `req->status = uv__random(req->buf, req->buflen);` |
| `ev_9710e5865b80` | call_site | `third_party/libuv/src/unix/fsevents.c:615` | `uv__queue_init(&state->fsevent_handles);` |
| `ev_97493536527e` | call_site | `third_party/libuv/src/unix/core.c:1194` | `uv_os_free_passwd(&pwd);` |
| `ev_974d806447a4` | call_site | `third_party/libuv/src/unix/stream.c:1524` | `uv__close(s->fake_fd);` |
| `ev_97b855a06eb3` | call_site | `third_party/libuv/src/unix/udp.c:820` | `err = uv_ip6_addr(interface_addr, 0, &addr6);` |
| `ev_97c08b79bdee` | call_site | `third_party/libuv/src/unix/kqueue.c:625` | `uv__io_start(handle->loop, &handle->event_watcher, POLLIN);` |
| `ev_97f73163ce5b` | call_site | `third_party/libuv/src/unix/udp.c:871` | `uv__io_init(&handle->io_watcher, uv__udp_io, fd);` |
| `ev_981ed43605eb` | call_site | `third_party/libuv/src/uv-common.c:390` | `return uv__udp_bind(handle, addr, addrlen, flags);` |
| `ev_984d48ec7136` | call_site | `third_party/libuv/src/unix/fs.c:1162` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_9917b1319099` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9987d16484ee` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_9a0559702f1c` | call_site | `third_party/libuv/src/unix/udp.c:1379` | `uv__queue_insert_tail(&handle->write_completed_queue, &req->queue);` |
| `ev_9a23b1a90869` | call_site | `third_party/libuv/src/threadpool.c:72` | `while (uv__queue_empty(&wq) \|\|` |
| `ev_9a2a70fb12d5` | call_site | `third_party/libuv/src/thread-common.c:116` | `uv_cond_broadcast((uv_cond_t*) &b->cond);` |
| `ev_9a415b790894` | call_site | `third_party/libuv/src/unix/signal.c:325` | `uv__close(loop->signal_pipefd[0]);` |
| `ev_9a5679a6a157` | call_site | `third_party/libuv/src/unix/process.c:403` | `uv__write_errno(error_fd);` |
| `ev_9a5f048e1985` | call_site | `third_party/libuv/src/idna.c:251` | `c = uv__utf8_decode1(&s, se);` |
| `ev_9a8af568ba6d` | call_site | `third_party/libuv/src/unix/fsevents.c:392` | `pFSEventStreamInvalidate(state->fsevent_stream);` |
| `ev_9acfaae91c3f` | call_site | `third_party/libuv/src/unix/kqueue.c:653` | `uv__free(handle->path);` |
| `ev_9b5bab4789a4` | call_site | `third_party/libuv/src/unix/core.c:237` | `uv__make_close_pending(handle);` |
| `ev_9b5c1e099e5c` | call_site | `third_party/libuv/src/unix/udp.c:650` | `err = uv__udp_sendmsg1(handle->io_watcher.fd, bufs, nbufs, addr);` |
| `ev_9b8c8d69db30` | call_site | `third_party/libuv/src/unix/tcp.c:261` | `if (uv__is_ipv6_link_local(p->ifa_addr))` |
| `ev_9ba025374183` | call_site | `third_party/libuv/src/threadpool.c:109` | `uv__queue_remove(q);` |
| `ev_9bfffacd6a23` | call_site | `third_party/libuv/src/timer.c:105` | `uv__queue_remove(&handle->node.queue);` |
| `ev_9c5aa8a79c39` | call_site | `third_party/libuv/src/unix/stream.c:921` | `uv__free(req->bufs);` |
| `ev_9c783d6aa9ce` | call_site | `third_party/libuv/src/unix/fs.c:346` | `uv_rwlock_rdlock(&req->loop->cloexec_lock);` |
| `ev_9c78be2081b9` | call_site | `third_party/libuv/src/threadpool.c:352` | `req->work_cb(req);` |
| `ev_9ca11e61f466` | call_site | `third_party/libuv/src/unix/stream.c:1431` | `err = uv__check_before_write(stream, nbufs, NULL);` |
| `ev_9cbc9a4b05fa` | call_site | `third_party/libuv/src/unix/stream.c:813` | `n = uv__writev(uv__stream_fd(stream), iov, iovcnt);` |
| `ev_9d1464d2c4ee` | call_site | `third_party/libuv/src/unix/stream.c:1451` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_9d2740ba66c2` | call_site | `third_party/libuv/src/thread-common.c:141` | `uv_mutex_unlock(&b->mutex);` |
| `ev_9d34d39630ee` | call_site | `third_party/libuv/src/uv-common.c:955` | `uv__free(cpu_infos[i].model);` |
| `ev_9d579686632a` | call_site | `third_party/libuv/src/unix/tty.c:490` | `err = uv__tcsetattr(orig_termios_fd, TCSANOW, &orig_termios);` |
| `ev_9d59dc77cae7` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9d8621a083b6` | call_site | `third_party/libuv/src/unix/loop.c:182` | `uv_mutex_lock(&loop->wq_mutex);` |
| `ev_9d90a87fafb6` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9dbad9b909bd` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:149` | `asn = pLSGetCurrentApplicationASN();` |
| `ev_9dc0d3a7be75` | call_site | `third_party/libuv/src/unix/stream.c:896` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLOUT);` |
| `ev_9dd6f384b6a7` | call_site | `third_party/libuv/src/unix/stream.c:862` | `n = uv__try_write(stream,` |
| `ev_9e113808cf94` | call_site | `third_party/libuv/src/unix/async.c:338` | `while (!uv__queue_empty(&queue)) {` |
| `ev_9e3ce92db5ce` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_9e4fb987df49` | call_site | `third_party/libuv/src/unix/stream.c:1104` | `uv__io_stop(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_9e5eb687289c` | call_site | `third_party/libuv/src/unix/udp.c:902` | `err = uv__sock_reuseaddr(sock);` |
| `ev_9e97eff9a9db` | call_site | `third_party/libuv/src/unix/fsevents.c:757` | `uv__free(s);` |
| `ev_9eb0271d884f` | call_site | `third_party/libuv/src/unix/core.c:249` | `fd = uv__stream_fd((uv_stream_t*) handle);` |
| `ev_9edc75ea9c66` | assignment | `third_party/libuv/src/unix/fs.c:1987` | `POST;` |
| `ev_9ee824a37da7` | call_site | `third_party/libuv/src/unix/stream.c:560` | `uv__close(server->accepted_fd);` |
| `ev_9f206abdf92e` | call_site | `third_party/libuv/src/unix/udp.c:953` | `err = uv_ip4_addr(multicast_addr, 0, &mcast_addr.in);` |
| `ev_9f4405b082a5` | call_site | `third_party/libuv/src/unix/fsevents.c:372` | `if (!pFSEventStreamStart(ref)) {` |
| `ev_9f67531bd193` | call_site | `third_party/libuv/src/uv-common.c:306` | `return uv_inet_ntop(AF_INET6, &src->sin6_addr, dst, size);` |
| `ev_9fe9881bf08e` | call_site | `third_party/libuv/src/unix/fsevents.c:653` | `uv_mutex_destroy(&state->fsevent_mutex);` |
| `ev_9fe9cfc5a18c` | call_site | `third_party/libuv/src/unix/fsevents.c:320` | `if (!uv__queue_empty(&head))` |
| `ev_a01e467af70e` | call_site | `third_party/libuv/src/unix/stream.c:608` | `err = uv__tcp_listen((uv_tcp_t*)stream, backlog, cb);` |
| `ev_a05cb92ccdc8` | call_site | `third_party/libuv/src/unix/stream.c:445` | `uv__queue_remove(q);` |
| `ev_a086780577cf` | call_site | `third_party/libuv/src/unix/stream.c:518` | `fd = uv__stream_fd(stream);` |
| `ev_a08f4b3f95f8` | call_site | `third_party/libuv/src/unix/fsevents.c:835` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_a0bff9dd5a4c` | call_site | `third_party/libuv/src/unix/signal.c:321` | `uv__signal_stop((uv_signal_t*) handle);` |
| `ev_a14ec4757563` | call_site | `third_party/libuv/src/unix/loop.c:90` | `err = uv_rwlock_init(&loop->cloexec_lock);` |
| `ev_a15a8a935323` | call_site | `third_party/libuv/src/unix/udp.c:269` | `handle->recv_cb(handle, 0, &buf, NULL, 0);` |
| `ev_a177e7089af3` | call_site | `third_party/libuv/src/unix/fs.c:1686` | `uv__free(bufs);` |
| `ev_a19e7ff238c4` | call_site | `third_party/libuv/src/unix/tcp.c:171` | `err = uv__sock_reuseport(tcp->io_watcher.fd);` |
| `ev_a1aaa11c0827` | assignment | `third_party/libuv/src/unix/fs.c:2076` | `POST;` |
| `ev_a1fcf2e85ad5` | call_site | `third_party/libuv/src/unix/udp.c:1142` | `} else if (uv_ip4_addr(interface_addr, 0, addr4) == 0) {` |
| `ev_a243a907176c` | call_site | `third_party/libuv/src/unix/fsevents.c:303` | `event = uv__malloc(sizeof(*event) + len);` |
| `ev_a2a7b2ac5fa3` | call_site | `third_party/libuv/src/unix/fsevents.c:850` | `uv_mutex_destroy(&handle->cf_mutex);` |
| `ev_a2be3695e1c9` | call_site | `third_party/libuv/src/unix/process.c:860` | `uv_once(&posix_spawn_init_once, uv__spawn_init_posix_spawn);` |
| `ev_a2cd9b965dcc` | call_site | `third_party/libuv/src/unix/pipe.c:542` | `return uv_pipe(fds,` |
| `ev_a2e499120e77` | call_site | `third_party/libuv/src/unix/udp.c:971` | `return uv__udp_set_source_membership4(handle,` |
| `ev_a2e6417d69b2` | call_site | `third_party/libuv/src/unix/fsevents.c:829` | `err = uv_mutex_init(&handle->cf_mutex);` |
| `ev_a2ebd7c9e867` | call_site | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_a310bd633352` | call_site | `third_party/libuv/src/uv-common.c:717` | `nbufs = uv__get_nbufs(req);` |
| `ev_a31af428fee4` | call_site | `third_party/libuv/src/unix/process.c:387` | `uv__write_errno(error_fd);` |
| `ev_a33664095464` | call_site | `third_party/libuv/src/heap-inl.h:235` | `while (child->parent != NULL && less_than(child, child->parent))` |
| `ev_a3aa80ba6f7d` | call_site | `third_party/libuv/src/unix/core.c:909` | `uv__queue_init(&w->watcher_queue);` |
| `ev_a3c6b77761ea` | call_site | `third_party/libuv/src/unix/pipe.c:236` | `err = uv_pipe_connect2(req, handle, name, strlen(name), 0, cb);` |
| `ev_a3dcf6ec0abb` | call_site | `third_party/libuv/src/unix/core.c:460` | `uv__io_poll(loop, timeout);` |
| `ev_a4047c2b38aa` | call_site | `third_party/libuv/src/unix/core.c:908` | `uv__queue_init(&w->pending_queue);` |
| `ev_a42333feee1c` | assignment | `third_party/libuv/src/unix/fs.c:2130` | `POST;` |
| `ev_a4488dfde8d9` | assignment | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_a464e6686716` | call_site | `third_party/libuv/src/unix/fsevents.c:888` | `uv_sem_wait(&state->fsevent_sem);` |
| `ev_a48630075c98` | call_site | `third_party/libuv/src/threadpool.c:218` | `if (uv_cond_init(&cond))` |
| `ev_a49ff7469940` | call_site | `third_party/libuv/src/unix/stream.c:1520` | `uv__stream_osx_interrupt_select(handle);` |
| `ev_a536858e7057` | call_site | `third_party/libuv/src/unix/tcp.c:147` | `return uv_tcp_init_ex(loop, tcp, AF_UNSPEC);` |
| `ev_a55ab0a346df` | call_site | `third_party/libuv/src/unix/core.c:890` | `watchers = uv__reallocf(loop->watchers,` |
| `ev_a56d48f79faf` | call_site | `third_party/libuv/src/threadpool.c:301` | `uv__queue_insert_tail(&loop->wq, &w->wq);` |
| `ev_a588d2bfac42` | call_site | `third_party/libuv/src/threadpool.c:63` | `uv_sem_post((uv_sem_t*) arg);` |
| `ev_a59894688097` | call_site | `third_party/libuv/src/uv-common.c:940` | `uv__free(envitems[i].name);` |
| `ev_a59e80e88a08` | call_site | `third_party/libuv/src/unix/pipe.c:120` | `err = uv__socket(AF_UNIX, SOCK_STREAM, 0);` |
| `ev_a5b47c8f30ff` | call_site | `third_party/libuv/src/unix/udp.c:240` | `buf = uv_buf_init(NULL, 0);` |
| `ev_a5b9a2bcb11b` | call_site | `third_party/libuv/src/unix/udp.c:1384` | `if (uv__queue_empty(&handle->write_queue))` |
| `ev_a5dbecdabc93` | call_site | `third_party/libuv/src/unix/stream.c:346` | `err = uv_async_init(stream->loop, &s->async, uv__stream_osx_select_cb);` |
| `ev_a613248534b2` | assignment | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_a62cc61b73fc` | call_site | `third_party/libuv/src/uv-common.c:1022` | `uv_mutex_lock(&loop_metrics->lock);` |
| `ev_a65ffbef2eba` | call_site | `third_party/libuv/src/unix/stream.c:960` | `queued_fds = uv__realloc(queued_fds,` |
| `ev_a6b129d96fd3` | call_site | `third_party/libuv/src/timer.c:118` | `uv_timer_stop(handle);` |
| `ev_a6bc978a3d6f` | call_site | `third_party/libuv/src/unix/process.c:233` | `err = uv__close(pipefds[1]);` |
| `ev_a730bce52fc1` | call_site | `third_party/libuv/src/unix/signal.c:339` | `err = uv__signal_loop_once_init(loop);` |
| `ev_a73a6b33b2e3` | call_site | `third_party/libuv/src/unix/process.c:947` | `uv__close_nocheckstdio(signal_pipe[0]);` |
| `ev_a74f997bc693` | call_site | `third_party/libuv/src/uv-common.c:1009` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_a7813c766650` | call_site | `third_party/libuv/src/inet.c:141` | `uv__strscpy(dst, tmp, size);` |
| `ev_a7992ce27ded` | call_site | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_a7c0a39f1deb` | call_site | `third_party/libuv/src/unix/udp.c:1417` | `return uv__udp_sendmsgv(fd, count, bufs, nbufs, addrs);` |
| `ev_a7e15974aa1b` | call_site | `third_party/libuv/src/unix/udp.c:1066` | `return uv__setsockopt_maybe_char(handle,` |
| `ev_a84da80e0238` | call_site | `third_party/libuv/src/unix/core.c:1419` | `return uv__getpwuid_r(pwd, uid);` |
| `ev_a86d202f42f0` | call_site | `third_party/libuv/src/unix/fs.c:2203` | `POST;` |
| `ev_a86f60818c75` | call_site | `third_party/libuv/src/unix/core.c:406` | `uv__queue_empty(&loop->idle_handles) &&` |
| `ev_a89baec5eecf` | call_site | `third_party/libuv/src/unix/tcp.c:670` | `uv__close(temp[0]);` |
| `ev_a8a16ad1cbe6` | call_site | `third_party/libuv/src/unix/udp.c:598` | `req->bufs = uv__malloc(nbufs * sizeof(bufs[0]));` |
| `ev_a8a62afac3b6` | call_site | `third_party/libuv/src/unix/stream.c:809` | `n = sendmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_a8a7e4b4a4c1` | call_site | `third_party/libuv/src/unix/fs.c:827` | `uv__free(buf);` |
| `ev_a8b9edb851da` | call_site | `third_party/libuv/src/unix/core.c:961` | `uv__queue_remove(&w->watcher_queue);` |
| `ev_a8c59432791e` | call_site | `third_party/libuv/src/unix/fsevents.c:836` | `uv__queue_insert_tail(&state->fsevent_handles, &handle->cf_member);` |
| `ev_a8fc8ccf1dec` | call_site | `third_party/libuv/src/unix/tcp.c:583` | `if (uv__stream_fd(handle) != -1) {` |
| `ev_a90326fd425d` | call_site | `third_party/libuv/src/unix/loop.c:170` | `uv__async_stop(loop);` |
| `ev_a90c2e617c26` | call_site | `third_party/libuv/src/uv-common.c:213` | `UV_ERRNO_MAP(UV_ERR_NAME_GEN_R)` |
| `ev_a91e590cf299` | call_site | `third_party/libuv/src/unix/fs.c:1876` | `POST;` |
| `ev_a93694a5ef5d` | assignment | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_a94c6c91517a` | call_site | `third_party/libuv/src/unix/async.c:194` | `q = uv__queue_head(&queue);` |
| `ev_a957e6c7b4ac` | call_site | `third_party/libuv/src/threadpool.c:120` | `uv_mutex_unlock(&mutex);` |
| `ev_a96331e551e5` | call_site | `third_party/libuv/src/unix/fs.c:1945` | `PATH;` |
| `ev_a9825cfe39b1` | call_site | `third_party/libuv/src/unix/core.c:850` | `q = uv__queue_head(&pq);` |
| `ev_a9ae4d40bcff` | call_site | `third_party/libuv/src/unix/core.c:1899` | `token = uv__strtok(cloned_path, ":", &itr);` |
| `ev_a9bcf8435fed` | call_site | `third_party/libuv/src/unix/process.c:174` | `process->exit_cb(process, exit_status, term_signal);` |
| `ev_aa260097a8d3` | assignment | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_aa8c6bf6aa6b` | call_site | `third_party/libuv/src/unix/stream.c:846` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_aab818684f01` | call_site | `third_party/libuv/src/unix/signal.c:401` | `uv__signal_block_and_lock(&saved_sigmask);` |
| `ev_aacb2a06a7d9` | call_site | `third_party/libuv/src/unix/async.c:339` | `q = uv__queue_head(&queue);` |
| `ev_aad00c6d2c5b` | call_site | `third_party/libuv/src/unix/poll.c:64` | `handle->poll_cb(handle, 0, pevents);` |
| `ev_ab0980935fe6` | call_site | `third_party/libuv/src/unix/fs.c:681` | `uv__free(req->ptr);` |
| `ev_ab1965d3bb82` | call_site | `third_party/libuv/src/unix/async.c:369` | `while (!uv__queue_empty(&queue)) {` |
| `ev_ab19e5c82169` | call_site | `third_party/libuv/src/unix/core.c:179` | `uv__udp_close((uv_udp_t*)handle);` |
| `ev_ab2ba65eeb23` | call_site | `third_party/libuv/src/unix/stream.c:1172` | `assert(uv__stream_fd(stream) >= 0);` |
| `ev_ab3c40d25d92` | call_site | `third_party/libuv/src/unix/stream.c:547` | `err = uv__stream_open(client,` |
| `ev_ab60d56a63b9` | call_site | `third_party/libuv/src/unix/stream.c:584` | `uv__free(queued_fds);` |
| `ev_abf5b76d041d` | call_site | `third_party/libuv/src/unix/process.c:370` | `uv__write_errno(error_fd);` |
| `ev_abff54541877` | call_site | `third_party/libuv/src/unix/tty.c:224` | `uv__close(newfd);` |
| `ev_ac6554a105ef` | call_site | `third_party/libuv/src/unix/fsevents.c:373` | `pFSEventStreamInvalidate(ref);` |
| `ev_acb15c736951` | call_site | `third_party/libuv/src/unix/stream.c:1320` | `if (uv__handle_fd((uv_handle_t*) send_handle) < 0)` |
| `ev_acb247b17f6a` | call_site | `third_party/libuv/src/unix/loop.c:58` | `uv__queue_init(&loop->handle_queue);` |
| `ev_acc9cf94ce9a` | call_site | `third_party/libuv/src/idna.c:485` | `target = uv__malloc(target_len + 1);` |
| `ev_acce12c7d3c3` | call_site | `third_party/libuv/src/timer.c:192` | `uv_timer_again(handle);` |
| `ev_acd28a6f53ea` | call_site | `third_party/libuv/src/unix/udp.c:1268` | `if ((r = uv__udp_prep_pkt(&h, bufs, nbufs, addr)))` |
| `ev_acdc925eeeca` | call_site | `third_party/libuv/src/unix/core.c:747` | `uv__cloexec(*pfd, 1);` |
| `ev_acfde5ccbf3c` | call_site | `third_party/libuv/src/unix/fs.c:2314` | `POST;` |
| `ev_acfeed207e6c` | call_site | `third_party/libuv/src/unix/loop.c:183` | `assert(uv__queue_empty(&loop->wq) && "thread pool work queue not empty!");` |
| `ev_ad0e11307aea` | call_site | `third_party/libuv/src/uv-common.c:865` | `uv__free(loop);` |
| `ev_ad14661bf222` | call_site | `third_party/libuv/src/timer.c:174` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_ad23f3a12d24` | call_site | `third_party/libuv/src/unix/kqueue.c:523` | `path = uv__basename_r(pathbuf);` |
| `ev_ad31a1e71bc1` | call_site | `third_party/libuv/src/unix/poll.c:131` | `if (uv__fd_exists(handle->loop, w->fd))` |
| `ev_ad42ffea959f` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_ad9bd4bed3b4` | call_site | `third_party/libuv/src/unix/loop.c:155` | `if (w->pevents != 0 && uv__queue_empty(&w->watcher_queue)) {` |
| `ev_ade1d519f0a3` | call_site | `third_party/libuv/src/unix/stream.c:718` | `uv__queue_remove(&req->queue);` |
| `ev_ae21638ab04c` | call_site | `third_party/libuv/src/unix/proctitle.c:148` | `uv_mutex_unlock(&process_title_mutex);` |
| `ev_ae22a2e185ab` | call_site | `third_party/libuv/src/fs-poll.c:215` | `ctx->poll_cb(ctx->parent_handle, 0, &ctx->statbuf, statbuf);` |
| `ev_ae2ce7d79969` | assignment | `third_party/libuv/src/unix/fs.c:1906` | `POST;` |
| `ev_ae35213eb1a0` | call_site | `third_party/libuv/src/heap-inl.h:147` | `heap_node_swap(heap, newnode->parent, newnode);` |
| `ev_ae70e6957faf` | call_site | `third_party/libuv/src/unix/proctitle.c:135` | `uv_once(&process_title_mutex_once, init_process_title_mutex_once);` |
| `ev_aea39618776b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:110` | `S("_LSSetApplicationInformationItem"));` |
| `ev_aec41cea8269` | call_site | `third_party/libuv/src/fs-poll.c:257` | `uv__free(ctx);` |
| `ev_aecee77afd31` | call_site | `third_party/libuv/src/unix/signal.c:422` | `RB_INSERT(uv__signal_tree_s, &uv__signal_tree, handle);` |
| `ev_aee85be2bd11` | call_site | `third_party/libuv/src/unix/stream.c:1089` | `uv__io_start(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_aeefeb47cd7c` | call_site | `third_party/libuv/src/unix/udp.c:958` | `err = uv_ip6_addr(source_addr, 0, &src_addr.in6);` |
| `ev_af087f8af8cb` | call_site | `third_party/libuv/src/timer.c:174` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_af110f0f7675` | call_site | `third_party/libuv/src/unix/stream.c:387` | `uv__close(fds[1]);` |
| `ev_af3640fdb8e5` | call_site | `third_party/libuv/src/unix/async.c:398` | `return uv__async_start(loop);` |
| `ev_af912c87bd1e` | call_site | `third_party/libuv/src/unix/tty.c:217` | `uv__nonblock(fd, 1);` |
| `ev_afab56ac7dd9` | call_site | `third_party/libuv/src/unix/core.c:987` | `if (uv__queue_empty(&w->pending_queue))` |
| `ev_afc686a3a119` | call_site | `third_party/libuv/src/fs-poll.c:129` | `if (uv_is_active((uv_handle_t*)&ctx->timer_handle))` |
| `ev_b00a452f52a2` | call_site | `third_party/libuv/src/unix/pipe.c:210` | `err = uv__nonblock(fd, 1);` |
| `ev_b0536e333f74` | call_site | `third_party/libuv/src/unix/process.c:1052` | `uv__process_close_stream(options->stdio + i);` |
| `ev_b06b26a8fdc7` | call_site | `third_party/libuv/src/unix/core.c:583` | `uv__close(peerfd);` |
| `ev_b07eb122b0b1` | call_site | `third_party/libuv/src/timer.c:188` | `uv__queue_remove(queue_node);` |
| `ev_b09595ea95f9` | call_site | `third_party/libuv/src/uv-common.c:822` | `uv__free((char*) dirents[i].name);` |
| `ev_b0e08bae336a` | call_site | `third_party/libuv/src/unix/fsevents.c:477` | `uv__free(paths);` |
| `ev_b0e8907d4d85` | call_site | `third_party/libuv/src/unix/fsevents.c:593` | `state = uv__calloc(1, sizeof(*state));` |
| `ev_b1101e47316d` | call_site | `third_party/libuv/src/fs-poll.c:202` | `ctx->poll_cb(ctx->parent_handle,` |
| `ev_b13f8c34eaa7` | call_site | `third_party/libuv/src/unix/fsevents.c:687` | `while (!uv__queue_empty(&loop->cf_signals)) {` |
| `ev_b1d03e18b3f3` | call_site | `third_party/libuv/src/unix/core.c:936` | `uv__queue_insert_tail(&loop->watcher_queue, &w->watcher_queue);` |
| `ev_b1d9f14206de` | call_site | `third_party/libuv/src/unix/loop.c:54` | `uv__queue_init(&loop->idle_handles);` |
| `ev_b1e74516d7f4` | call_site | `third_party/libuv/src/unix/pipe.c:190` | `uv__stream_close((uv_stream_t*)handle);` |
| `ev_b295d1c02f2c` | call_site | `third_party/libuv/src/unix/kqueue.c:599` | `if (uv__fstat(fd, &statbuf))` |
| `ev_b296a8d4db33` | call_site | `third_party/libuv/src/unix/loop.c:126` | `uv__free(loop->watchers);` |
| `ev_b2a8a7ea72f0` | call_site | `third_party/libuv/src/uv-common.c:499` | `return uv__udp_send(req, handle, bufs, nbufs, addr, addrlen, send_cb);` |
| `ev_b2fe7f9b9e33` | call_site | `third_party/libuv/src/unix/kqueue.c:580` | `handle->path = uv__strdup(path);` |
| `ev_b3318f75c51b` | call_site | `third_party/libuv/src/unix/fs.c:608` | `dir = uv__malloc(sizeof(*dir));` |
| `ev_b34aecd9cd51` | call_site | `third_party/libuv/src/unix/loop.c:137` | `err = uv__io_fork(loop);` |
| `ev_b3590e089dda` | call_site | `third_party/libuv/src/threadpool.c:221` | `if (uv_mutex_init(&mutex))` |
| `ev_b366963f0cf1` | call_site | `third_party/libuv/src/unix/tty.c:225` | `uv__queue_remove(&tty->handle_queue);` |
| `ev_b39f960c4599` | call_site | `third_party/libuv/src/unix/fs.c:561` | `uv__free(req->bufs);` |
| `ev_b3da1033776b` | call_site | `third_party/libuv/src/uv-common.c:1024` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_b3edcccafe46` | call_site | `third_party/libuv/src/unix/tcp.c:584` | `err = uv__tcp_nodelay(uv__stream_fd(handle), on);` |
| `ev_b4105064da1e` | call_site | `third_party/libuv/src/unix/fs.c:1735` | `X(OPENDIR, uv__fs_opendir(req));` |
| `ev_b44af00b137a` | call_site | `third_party/libuv/src/threadpool.c:235` | `if (uv_thread_create_ex(threads + i, &config, worker, &sem))` |
| `ev_b45b5df7f9eb` | call_site | `third_party/libuv/src/unix/fs.c:1614` | `uv__to_stat(&pbuf, buf);` |
| `ev_b48f965e8c3f` | call_site | `third_party/libuv/src/unix/stream.c:388` | `uv_close((uv_handle_t*) &s->async, uv__stream_osx_cb_close);` |
| `ev_b4b4db014405` | call_site | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_b4b9b07cacda` | call_site | `third_party/libuv/src/unix/fs.c:1295` | `if (uv__fstat(dstfd, &dst_statsbuf)) {` |
| `ev_b4ead329de93` | call_site | `third_party/libuv/src/unix/fsevents.c:796` | `err = uv__fsevents_loop_init(handle->loop);` |
| `ev_b5096daadc0b` | call_site | `third_party/libuv/src/timer.c:149` | `heap_node = heap_min(timer_heap(loop));` |
| `ev_b521e4c95996` | call_site | `third_party/libuv/src/unix/fs.c:1267` | `if (uv__fstat(srcfd, &src_statsbuf)) {` |
| `ev_b59f0191959a` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_b5e2d9477d90` | call_site | `third_party/libuv/src/unix/tcp.c:72` | `err = uv__stream_open((uv_stream_t*) handle, sockfd, flags);` |
| `ev_b608025b3064` | call_site | `third_party/libuv/src/unix/async.c:355` | `uv__close(loop->async_io_watcher.fd);` |
| `ev_b60a1c9b57c3` | call_site | `third_party/libuv/src/unix/udp.c:1396` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_b66a27295773` | call_site | `third_party/libuv/src/unix/core.c:496` | `uv__update_time(loop);` |
| `ev_b66d9a2db378` | call_site | `third_party/libuv/src/unix/tcp.c:102` | `err = maybe_bind_socket(sockfd);` |
| `ev_b68dee444baa` | call_site | `third_party/libuv/src/unix/udp.c:861` | `fd = uv__socket(domain, SOCK_DGRAM, 0);` |
| `ev_b6d80ba09e1a` | call_site | `third_party/libuv/src/unix/core.c:1360` | `uv__free(buf);` |
| `ev_b6f7401f8869` | call_site | `third_party/libuv/src/threadpool.c:285` | `uv_once(&once, init_once);  /* Ensure \|mutex\| is initialized. */` |
| `ev_b732e1e6b2e9` | assignment | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_b745eb2c1aa3` | call_site | `third_party/libuv/src/unix/stream.c:651` | `else if (shutdown(uv__stream_fd(stream), SHUT_WR))` |
| `ev_b749c6ccdaab` | call_site | `third_party/libuv/src/unix/darwin.c:231` | `cpu_info->model = uv__strdup(model);` |
| `ev_b7605aff065c` | call_site | `third_party/libuv/src/unix/fsevents.c:489` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_b773d853e86c` | call_site | `third_party/libuv/src/unix/fsevents.c:605` | `uv__queue_init(&loop->cf_signals);` |
| `ev_b7898c619ca0` | call_site | `third_party/libuv/src/unix/async.c:337` | `uv__queue_move(&loop->async_handles, &queue);` |
| `ev_b79187295b36` | call_site | `third_party/libuv/src/threadpool.c:187` | `uv_cond_destroy(&cond);` |
| `ev_b7b65c3847dd` | call_site | `third_party/libuv/src/unix/kqueue.c:423` | `w->cb(loop, w, revents);` |
| `ev_b7c8e5094a23` | call_site | `third_party/libuv/src/unix/fs.c:329` | `r = uv__mkostemp(path, O_CLOEXEC);` |
| `ev_b7cc31f6f70b` | call_site | `third_party/libuv/src/unix/core.c:1350` | `buf = uv__malloc(bufsize);` |
| `ev_b7f1e8920312` | call_site | `third_party/libuv/src/unix/process.c:344` | `uv__write_errno(error_fd);` |
| `ev_b82262930047` | call_site | `third_party/libuv/src/unix/random-getentropy.c:53` | `if (uv__getentropy((char *) buf + pos, buflen - pos))` |
| `ev_b887dd34f8b4` | call_site | `third_party/libuv/src/threadpool.c:275` | `post(&w->wq, kind);` |
| `ev_b897d0abfe07` | call_site | `third_party/libuv/src/unix/stream.c:1554` | `uv__free(handle->queued_fds);` |
| `ev_b8af9b15bfd4` | call_site | `third_party/libuv/src/unix/tcp.c:671` | `uv__close(temp[1]);` |
| `ev_b93dfa208408` | call_site | `third_party/libuv/src/unix/fs.c:1737` | `X(CLOSEDIR, uv__fs_closedir(req));` |
| `ev_b973caa5bfd4` | call_site | `third_party/libuv/src/unix/stream.c:395` | `uv__close(fds[0]);` |
| `ev_b989201c298c` | call_site | `third_party/libuv/src/uv-common.c:943` | `uv__free(envitems);` |
| `ev_ba0705e7afdf` | call_site | `third_party/libuv/src/unix/fs.c:1400` | `uv_fs_sendfile(NULL, &fs_req, dstfd, srcfd, in_offset, bytes_chunk, NULL);` |
| `ev_ba31b5a1b27f` | call_site | `third_party/libuv/src/unix/fs.c:2238` | `req->bufs = uv__malloc(nbufs * sizeof(*bufs));` |
| `ev_ba652f5cbd24` | call_site | `third_party/libuv/src/unix/async.c:312` | `uv__io_start(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_bac54f612905` | call_site | `third_party/libuv/src/unix/random-devurandom.c:92` | `return uv__random_readpath("/dev/urandom", buf, buflen);` |
| `ev_bb20fd100806` | assignment | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_bb321b8aef5b` | call_site | `third_party/libuv/src/unix/signal.c:551` | `removed_handle = RB_REMOVE(uv__signal_tree_s, &uv__signal_tree, handle);` |
| `ev_bb5e75ad809e` | call_site | `third_party/libuv/src/unix/loop.c:141` | `err = uv__async_fork(loop);` |
| `ev_bb64305bd4c7` | assignment | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
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
| `ev_bc6c69b12c1d` | call_site | `third_party/libuv/src/unix/stream.c:1120` | `stream->read_cb(stream, err, &buf);` |
| `ev_bc92c818788f` | call_site | `third_party/libuv/src/unix/signal.c:330` | `uv__close(loop->signal_pipefd[1]);` |
| `ev_bca1a589e344` | call_site | `third_party/libuv/src/unix/core.c:475` | `uv__run_closing_handles(loop);` |
| `ev_bcaabc955863` | call_site | `third_party/libuv/src/threadpool.c:88` | `uv__queue_remove(q);` |
| `ev_bccc48b6f356` | call_site | `third_party/libuv/src/unix/tcp.c:162` | `err = maybe_new_socket(tcp, addr->sa_family, 0);` |
| `ev_bce0d87f8d38` | call_site | `third_party/libuv/src/unix/process.c:176` | `assert(uv__queue_empty(&pending));` |
| `ev_bce3a72b771e` | call_site | `third_party/libuv/src/unix/fsevents.c:713` | `pCFRunLoopAddSource(state->loop,` |
| `ev_bd406563202e` | call_site | `third_party/libuv/src/unix/loop.c:206` | `uv__free(lfields);` |
| `ev_bd5daafdd6f8` | call_site | `third_party/libuv/src/unix/stream.c:500` | `emfile_fd = uv__open_cloexec("/", O_RDONLY);` |
| `ev_bd662a3ae4eb` | call_site | `third_party/libuv/src/uv-common.c:913` | `uv__free(loop);` |
| `ev_bd9b2df6d84f` | call_site | `third_party/libuv/src/unix/stream.c:1364` | `req->bufs = uv__malloc(nbufs * sizeof(bufs[0]));` |
| `ev_bdd15c70a5c5` | call_site | `third_party/libuv/src/unix/udp.c:205` | `chunk_buf = uv_buf_init(iov[k].iov_base, iov[k].iov_len);` |
| `ev_be1e9a1af48d` | call_site | `third_party/libuv/src/unix/poll.c:91` | `uv__io_init(&handle->io_watcher, uv__poll_io, fd);` |
| `ev_be39dd23acb8` | call_site | `third_party/libuv/src/uv-common.c:542` | `return uv__udp_recv_start(handle, alloc_cb, recv_cb);` |
| `ev_be9938575c50` | call_site | `third_party/libuv/src/unix/core.c:448` | `uv__queue_empty(&loop->idle_handles);` |
| `ev_bece5b64ad2c` | call_site | `third_party/libuv/src/unix/core.c:633` | `rc = uv__close_nocancel(fd);` |
| `ev_bf05c39d5412` | call_site | `third_party/libuv/src/unix/getnameinfo.c:52` | `req->retcode = uv__getaddrinfo_translate_error(err);` |
| `ev_bf29d3d68222` | call_site | `third_party/libuv/src/thread-common.c:52` | `b = uv__malloc(sizeof(*b));` |
| `ev_bf2df9173317` | call_site | `third_party/libuv/src/unix/stream.c:465` | `uv__stream_flush_write_queue(stream, UV_ECANCELED);` |
| `ev_bf5a53f309f1` | call_site | `third_party/libuv/src/unix/fsevents.c:745` | `while (!uv__queue_empty(&split_head)) {` |
| `ev_bff28bab5e2d` | call_site | `third_party/libuv/src/uv-common.c:889` | `uv__loop_close(loop);` |
| `ev_c025fef04414` | call_site | `third_party/libuv/src/threadpool.c:239` | `uv_sem_wait(&sem);` |
| `ev_c02b572bcedf` | call_site | `third_party/libuv/src/uv-common.c:849` | `if (uv_loop_init(&default_loop_struct))` |
| `ev_c04da2825f29` | call_site | `third_party/libuv/src/unix/udp.c:575` | `err = uv__udp_maybe_deferred_bind(handle, addr->sa_family, 0);` |
| `ev_c0622aa8aa4c` | assignment | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_c07408c5e319` | call_site | `third_party/libuv/src/idna.c:555` | `*target_len_ptr = target_len + uv_utf16_length_as_wtf8(w_source_ptr, w_source_len);` |
| `ev_c07d8c90d04b` | call_site | `third_party/libuv/src/unix/udp.c:57` | `uv__io_close(handle->loop, &handle->io_watcher);` |
| `ev_c0943253e2da` | assignment | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_c0b8de5692e8` | call_site | `third_party/libuv/src/unix/tcp.c:134` | `uv__queue_remove(&tcp->handle_queue);` |
| `ev_c0bbe22885b3` | call_site | `third_party/libuv/src/unix/udp.c:922` | `if (uv_ip4_addr(multicast_addr, 0, &addr4) == 0) {` |
| `ev_c0bffae61bd8` | call_site | `third_party/libuv/src/threadpool.c:151` | `uv_mutex_unlock(&mutex);` |
| `ev_c0ebd547cc9c` | call_site | `third_party/libuv/src/unix/kqueue.c:193` | `q = uv__queue_head(&loop->watcher_queue);` |
| `ev_c1134f264544` | call_site | `third_party/libuv/src/unix/udp.c:928` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET6, UV_UDP_REUSEADDR);` |
| `ev_c149f02e1131` | call_site | `third_party/libuv/src/unix/fsevents.c:393` | `pFSEventStreamRelease(state->fsevent_stream);` |
| `ev_c14e3dacde4e` | call_site | `third_party/libuv/src/unix/udp.c:652` | `return uv__count_bufs(bufs, nbufs);` |
| `ev_c1aef9f437bf` | call_site | `third_party/libuv/src/unix/loop.c:114` | `uv__signal_loop_cleanup(loop);` |
| `ev_c1bbf875a0ee` | assignment | `third_party/libuv/src/unix/signal.c:272` | `uv__io_init(&loop->signal_io_watcher,` |
| `ev_c1e861b792c5` | call_site | `third_party/libuv/src/unix/thread.c:110` | `return uv__default_stack_size();` |
| `ev_c1f935620d26` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:109` | `pCFBundleGetFunctionPointerForName(launch_services_bundle,` |
| `ev_c21082c86542` | call_site | `third_party/libuv/src/unix/random-getentropy.c:43` | `uv_once(&once, uv__random_getentropy_init);` |
| `ev_c27367387ac4` | call_site | `third_party/libuv/src/unix/core.c:339` | `uv__make_close_pending(handle);  /* Back into the queue. */` |
| `ev_c2b6d2820953` | call_site | `third_party/libuv/src/unix/fsevents.c:782` | `pCFRunLoopWakeUp(state->loop);` |
| `ev_c308cadbf87a` | call_site | `third_party/libuv/src/unix/stream.c:1224` | `uv__stream_eof(stream, &buf);` |
| `ev_c34c08edf0bb` | call_site | `third_party/libuv/src/timer.c:193` | `handle->timer_cb(handle);` |
| `ev_c395b17befd0` | call_site | `third_party/libuv/src/unix/pipe.c:47` | `uv__stream_init(loop, (uv_stream_t*)handle, UV_NAMED_PIPE);` |
| `ev_c3c6513a28fe` | call_site | `third_party/libuv/src/unix/process.c:321` | `uv__write_errno(error_fd);` |
| `ev_c427326553fc` | call_site | `third_party/libuv/src/unix/fsevents.c:210` | `uv_async_send(handle->cf_cb);` |
| `ev_c4396c4709b0` | call_site | `third_party/libuv/src/unix/core.c:525` | `err = uv__cloexec(sockfd, 1);` |
| `ev_c4d1e0b5cd0c` | call_site | `third_party/libuv/src/uv-common.c:140` | `uv__free(pwd->username);` |
| `ev_c505b01b7556` | call_site | `third_party/libuv/src/unix/process.c:1084` | `return uv_kill(process->pid, signum);` |
| `ev_c516ecd16c03` | call_site | `third_party/libuv/src/unix/fsevents.c:682` | `uv_thread_join(&loop->cf_thread);` |
| `ev_c52c9e1d682b` | call_site | `third_party/libuv/src/unix/core.c:191` | `uv__idle_close((uv_idle_t*)handle);` |
| `ev_c52d264dcd1e` | call_site | `third_party/libuv/src/unix/loop.c:120` | `uv_mutex_destroy(&lfields->loop_metrics.lock);` |
| `ev_c53e0d09dab6` | call_site | `third_party/libuv/src/unix/fs.c:1732` | `X(OPEN, uv__fs_open(req));` |
| `ev_c54b4a9d40e6` | call_site | `third_party/libuv/src/threadpool.c:96` | `uv__queue_insert_tail(&wq, q);` |
| `ev_c55cf48c308d` | call_site | `third_party/libuv/src/unix/udp.c:1331` | `if ((r = uv__udp_sendmsg1(fd, bufs[i], nbufs[i], addrs[i])))` |
| `ev_c5b3e74bd33e` | call_site | `third_party/libuv/src/unix/fsevents.c:468` | `err = uv__fsevents_create_stream(state, loop, cf_paths);` |
| `ev_c5d6f7ed3be4` | call_site | `third_party/libuv/src/unix/fs.c:1778` | `req->cb(req);` |
| `ev_c5e7fc2d64fb` | call_site | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_c5f83192d6e8` | call_site | `third_party/libuv/src/unix/stream.c:519` | `err = uv__accept(fd);` |
| `ev_c60d0a32c382` | call_site | `third_party/libuv/src/unix/stream.c:467` | `uv__drain(stream);` |
| `ev_c6482a526097` | call_site | `third_party/libuv/src/unix/fs.c:1717` | `X(COPYFILE, uv__fs_copyfile(req));` |
| `ev_c69095c42f12` | call_site | `third_party/libuv/src/unix/fs.c:253` | `tv[1] = uv__fs_to_timeval(req->mtime);` |
| `ev_c6b1f09993c5` | call_site | `third_party/libuv/src/unix/poll.c:104` | `uv__io_stop(handle->loop,` |
| `ev_c6bc3a570d6e` | call_site | `third_party/libuv/src/unix/pipe.c:324` | `uv__stream_fd(handle),` |
| `ev_c6e91c01e8e1` | call_site | `third_party/libuv/src/thread-common.c:66` | `rc = uv_cond_init((uv_cond_t*) &b->cond);` |
| `ev_c6ed5938e44d` | call_site | `third_party/libuv/src/unix/fsevents.c:589` | `err = uv__fsevents_global_init();` |
| `ev_c709be5edd28` | assignment | `third_party/libuv/src/unix/fs.c:1896` | `POST;` |
| `ev_c71783f63439` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_c7551b537f72` | call_site | `third_party/libuv/src/unix/stream.c:633` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_c78a5316121d` | call_site | `third_party/libuv/src/unix/fs.c:818` | `len = uv__fs_pathmax_size(req->path);` |
| `ev_c8890363ff16` | call_site | `third_party/libuv/src/unix/fs.c:1596` | `ret = uv__stat(path, &pbuf);` |
| `ev_c8d34ac33e11` | assignment | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_c8d888c00b2a` | call_site | `third_party/libuv/src/threadpool.c:73` | `(uv__queue_head(&wq) == &run_slow_work_message &&` |
| `ev_c8f05efb9dda` | call_site | `third_party/libuv/src/unix/fsevents.c:843` | `err = uv__cf_loop_signal(handle->loop, handle, kUVCFLoopSignalRegular);` |
| `ev_c915d0137653` | call_site | `third_party/libuv/src/fs-poll.c:130` | `uv_close((uv_handle_t*)&ctx->timer_handle, timer_close_cb);` |
| `ev_c95e706f32f8` | call_site | `third_party/libuv/src/unix/fsevents.c:499` | `uv_sem_post(&state->fsevent_sem);` |
| `ev_c972bfdb3eda` | call_site | `third_party/libuv/src/unix/fs.c:2011` | `POST;` |
| `ev_c9b3a0ee6834` | call_site | `third_party/libuv/src/timer.c:183` | `uv__queue_insert_tail(&ready_queue, &handle->node.queue);` |
| `ev_c9d578b23872` | assignment | `third_party/libuv/src/unix/fs.c:1972` | `POST;` |
| `ev_ca209b632354` | call_site | `third_party/libuv/src/unix/loop.c:40` | `lfields = (uv__loop_internal_fields_t*) uv__calloc(1, sizeof(*lfields));` |
| `ev_ca49d7b8c64c` | call_site | `third_party/libuv/src/threadpool.c:320` | `uv_mutex_unlock(&loop->wq_mutex);` |
| `ev_ca4bc4ccb8a5` | call_site | `third_party/libuv/src/unix/core.c:1450` | `buf = uv__strdup(environ[j]);` |
| `ev_cad3b18749bb` | call_site | `third_party/libuv/src/unix/signal.c:558` | `first_handle = uv__signal_first_handle(handle->signum);` |
| `ev_cae38e8a39ab` | call_site | `third_party/libuv/src/unix/fsevents.c:743` | `uv_mutex_unlock(&loop->cf_mutex);` |
| `ev_cae4056ac64c` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_caeb2eecfeea` | assignment | `third_party/libuv/src/unix/fs.c:1784` | `uv__work_submit(loop,` |
| `ev_cb3e8930a9fc` | call_site | `third_party/libuv/src/unix/stream.c:532` | `uv__io_stop(loop, &stream->io_watcher, POLLIN);` |
| `ev_cb593684fcb7` | call_site | `third_party/libuv/src/unix/random-devurandom.c:43` | `if (uv__fstat(fd, &s)) {` |
| `ev_cba33e307b6f` | call_site | `third_party/libuv/src/unix/core.c:405` | `uv__queue_empty(&loop->pending_queue) &&` |
| `ev_cba6dcf89022` | call_site | `third_party/libuv/src/unix/async.c:390` | `uv__close(loop->async_wfd);` |
| `ev_cbc5db67d9b3` | call_site | `third_party/libuv/src/threadpool.c:77` | `uv_cond_wait(&cond, &mutex);` |
| `ev_cbe490a587ad` | call_site | `third_party/libuv/src/unix/stream.c:270` | `uv__free(s);` |
| `ev_cc272be5085b` | call_site | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_cc28c9c3a683` | call_site | `third_party/libuv/src/unix/stream.c:1236` | `uv__drain(stream);` |
| `ev_cc774e2e8c90` | call_site | `third_party/libuv/src/unix/pipe.c:329` | `uv__io_start(handle->loop, &handle->io_watcher, POLLOUT);` |
| `ev_cc7cc3445003` | call_site | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_cc99a9eccb0e` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:159` | `S(title),` |
| `ev_ccfb82ba279a` | call_site | `third_party/libuv/src/unix/fs.c:1132` | `return uv__fs_sendfile_emul(req);` |
| `ev_cd2024463a19` | call_site | `third_party/libuv/src/unix/process.c:1042` | `uv__queue_insert_tail(&loop->process_handles, &process->queue);` |
| `ev_cd7feb5c4c8f` | call_site | `third_party/libuv/src/uv-common.c:561` | `q = uv__queue_head(&queue);` |
| `ev_cde8f20c2347` | call_site | `third_party/libuv/src/unix/fsevents.c:894` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_ce1e1fb84570` | call_site | `third_party/libuv/src/idna.c:344` | `rc = uv__idna_toascii_label(s, st, &d, de);` |
| `ev_ce3ea056b547` | call_site | `third_party/libuv/src/unix/loop.c:192` | `uv_rwlock_destroy(&loop->cloexec_lock);` |
| `ev_ce40a7a8e04a` | call_site | `third_party/libuv/src/unix/udp.c:271` | `handle->recv_cb(handle, UV__ERR(errno), &buf, NULL, 0);` |
| `ev_ce9d66273be0` | call_site | `third_party/libuv/src/fs-poll.c:92` | `err = uv_timer_init(loop, &ctx->timer_handle);` |
| `ev_cecd940b830c` | call_site | `third_party/libuv/src/unix/fs.c:2167` | `POST;` |
| `ev_cee273c5b1f3` | call_site | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_cf5781b7a598` | call_site | `third_party/libuv/src/unix/poll.c:48` | `uv__io_stop(loop, w, POLLIN \| POLLOUT \| UV__POLLRDHUP \| UV__POLLPRI);` |
| `ev_cfb534324a96` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:132` | `if (uv__ifaddr_exclude(ent, UV__EXCLUDE_IFPHYS))` |
| `ev_d004a6ff2b9c` | call_site | `third_party/libuv/src/unix/fsevents.c:742` | `uv__queue_move(&loop->cf_signals, &split_head);` |
| `ev_d00bce033b87` | call_site | `third_party/libuv/src/unix/stream.c:175` | `if (uv__io_active(&stream->io_watcher, POLLOUT))` |
| `ev_d07ea6f4458d` | assignment | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_d0a1b705a388` | call_site | `third_party/libuv/src/unix/fsevents.c:683` | `uv_sem_destroy(&loop->cf_sem);` |
| `ev_d0aa403c8561` | call_site | `third_party/libuv/src/unix/core.c:465` | `uv__run_pending(loop);` |
| `ev_d0e63f23b3a5` | call_site | `third_party/libuv/src/unix/stream.c:1208` | `uv__read(stream);` |
| `ev_d118df7d8e6f` | call_site | `third_party/libuv/src/unix/stream.c:674` | `size = uv__count_bufs(req->bufs + req->write_index,` |
| `ev_d151a4d43dce` | call_site | `third_party/libuv/src/unix/signal.c:112` | `uv_once(&uv__signal_global_init_guard, uv__signal_global_init);` |
| `ev_d1735b689509` | call_site | `third_party/libuv/src/unix/process.c:339` | `uv__close_nocheckstdio(fd); /* Free up fd, if it happens to be open. */` |
| `ev_d1904d590835` | call_site | `third_party/libuv/src/uv-common.c:559` | `uv__queue_move(&loop->handle_queue, &queue);` |
| `ev_d1acf83af367` | call_site | `third_party/libuv/src/unix/kqueue.c:587` | `uv__free(handle->path);` |
| `ev_d22037b22151` | call_site | `third_party/libuv/src/unix/core.c:451` | `uv__run_idle(loop);` |
| `ev_d23022af4326` | call_site | `third_party/libuv/src/unix/core.c:474` | `uv__run_check(loop);` |
| `ev_d236797ac25a` | call_site | `third_party/libuv/src/unix/proctitle.c:108` | `uv_mutex_lock(&process_title_mutex);` |
| `ev_d23d39334710` | call_site | `third_party/libuv/src/threadpool.c:418` | `return uv__work_cancel(loop, req, wreq);` |
| `ev_d246b9d6fc6a` | call_site | `third_party/libuv/src/unix/stream.c:1566` | `return uv__nonblock(uv__stream_fd(handle), !blocking);` |
| `ev_d275eeb625e0` | call_site | `third_party/libuv/src/timer.c:63` | `uv__queue_init(&handle->node.queue);` |
| `ev_d2921f4ca6b9` | call_site | `third_party/libuv/src/idna.c:201` | `c = uv__utf8_decode1(&s, se);` |
| `ev_d2d800a82fff` | call_site | `third_party/libuv/src/unix/loop.c:205` | `uv_mutex_destroy(&lfields->loop_metrics.lock);` |
| `ev_d2dba493dabd` | call_site | `third_party/libuv/src/unix/async.c:350` | `uv__close(loop->async_wfd);` |
| `ev_d308d52ab182` | call_site | `third_party/libuv/src/unix/kqueue.c:194` | `uv__queue_remove(q);` |
| `ev_d3091cd2fb7f` | call_site | `third_party/libuv/src/unix/stream.c:1518` | `uv_sem_post(&s->close_sem);` |
| `ev_d33c72089950` | call_site | `third_party/libuv/src/unix/kqueue.c:611` | `r = uv__fsevents_init(handle);` |
| `ev_d4496da193ab` | call_site | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_d47015d076db` | call_site | `third_party/libuv/src/unix/async.c:155` | `uv__queue_remove(&handle->queue);` |
| `ev_d479a038ac24` | call_site | `third_party/libuv/src/unix/signal.c:59` | `RB_GENERATE_STATIC(uv__signal_tree_s,` |
| `ev_d47a1f5e850a` | assignment | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_d485c564824e` | call_site | `third_party/libuv/src/unix/poll.c:135` | `uv__poll_stop(handle);` |
| `ev_d49198b19d93` | call_site | `third_party/libuv/src/threadpool.c:228` | `if (uv_sem_init(&sem, 0))` |
| `ev_d49b8d363cb4` | call_site | `third_party/libuv/src/unix/signal.c:478` | `handle->signal_cb(handle, handle->signum);` |
| `ev_d4c708994794` | call_site | `third_party/libuv/src/unix/stream.c:386` | `uv__close(fds[0]);` |
| `ev_d534de3458da` | call_site | `third_party/libuv/src/fs-poll.c:197` | `if (!uv_is_active((uv_handle_t*)handle) \|\| uv__is_closing(handle))` |
| `ev_d53598a463b9` | call_site | `third_party/libuv/src/unix/udp.c:83` | `uv__udp_run_completed(handle);` |
| `ev_d539e9f39d97` | call_site | `third_party/libuv/src/unix/tty.c:182` | `if (uv__tty_is_slave(fd) && ttyname_r(fd, path, sizeof(path)) == 0)` |
| `ev_d55238e49819` | call_site | `third_party/libuv/src/unix/udp.c:1313` | `r = sendmsg_x(fd, m, n, MSG_DONTWAIT);` |
| `ev_d5868fb8b040` | call_site | `third_party/libuv/src/unix/signal.c:413` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_d5ae787393b9` | call_site | `third_party/libuv/src/unix/tty.c:196` | `r = uv__dup2_cloexec(newfd, fd);` |
| `ev_d5c23a2f7c40` | call_site | `third_party/libuv/src/unix/stream.c:87` | `uv__handle_init(loop, (uv_handle_t*)stream, type);` |
| `ev_d5fdcab2928b` | call_site | `third_party/libuv/src/unix/core.c:1159` | `err = uv__cloexec(newfd, 1);` |
| `ev_d612ed3a00de` | call_site | `third_party/libuv/src/timer.c:171` | `uv__queue_init(&ready_queue);` |
| `ev_d68b49cbe223` | call_site | `third_party/libuv/src/fs-poll.c:111` | `uv__free(ctx);` |
| `ev_d6954cdf136e` | call_site | `third_party/libuv/src/unix/fsevents.c:719` | `pCFRunLoopRun();` |
| `ev_d6fe3495ec3c` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:164` | `uv__thread_setname(title);  /* Don't care if it fails. */` |
| `ev_d715863dffdf` | call_site | `third_party/libuv/src/unix/stream.c:1017` | `uv__close(fd);` |
| `ev_d72f0beb12e3` | call_site | `third_party/libuv/src/unix/udp.c:955` | `err = uv_ip6_addr(multicast_addr, 0, &mcast_addr.in6);` |
| `ev_d78995402e2b` | call_site | `third_party/libuv/src/unix/fs.c:1996` | `req->path = uv__strdup(tpl);` |
| `ev_d7a51c466740` | call_site | `third_party/libuv/src/uv-common.c:560` | `while (!uv__queue_empty(&queue)) {` |
| `ev_d7b8bce3c1e1` | assignment | `third_party/libuv/src/threadpool.c:299` | `w->work = uv__cancelled;` |
| `ev_d7e1459ebd63` | call_site | `third_party/libuv/src/unix/core.c:962` | `uv__queue_init(&w->watcher_queue);` |
| `ev_d7ea4f1875c6` | assignment | `third_party/libuv/src/unix/fs.c:2085` | `POST;` |
| `ev_d80a543af3a2` | call_site | `third_party/libuv/src/unix/udp.c:1358` | `if (uv__queue_empty(&handle->write_queue))` |
| `ev_d8cc95480d02` | call_site | `third_party/libuv/src/unix/fs.c:1722` | `X(FSTAT, uv__fs_fstat(req->file, &req->statbuf));` |
| `ev_d92622f525a0` | call_site | `third_party/libuv/src/unix/fsevents.c:631` | `if (pthread_attr_setstacksize(&attr, uv__thread_stack_size()))` |
| `ev_d96996a4e23e` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:128` | `*(void **)(&pLSApplicationCheckIn) = pCFBundleGetFunctionPointerForName(` |
| `ev_d980178ead5f` | call_site | `third_party/libuv/src/uv-common.c:1046` | `uv_mutex_unlock(&loop_metrics->lock);` |
| `ev_d98c185e6143` | call_site | `third_party/libuv/src/unix/thread.c:165` | `min_stack_size = uv__min_stack_size();` |
| `ev_d991d8e355d5` | call_site | `third_party/libuv/src/unix/fsevents.c:883` | `err = uv__cf_loop_signal(handle->loop, handle, kUVCFLoopSignalClosing);` |
| `ev_d9b48b296894` | call_site | `third_party/libuv/src/unix/stream.c:262` | `uv_sem_post(&s->async_sem);` |
| `ev_d9b775c1b739` | call_site | `third_party/libuv/src/uv-common.c:564` | `uv__queue_remove(q);` |
| `ev_d9b8a14b214b` | call_site | `third_party/libuv/src/unix/random-devurandom.c:44` | `uv__close(fd);` |
| `ev_d9c72db34f59` | call_site | `third_party/libuv/src/unix/loop.c:173` | `uv__close(loop->emfile_fd);` |
| `ev_d9f9e99c55da` | call_site | `third_party/libuv/src/unix/core.c:971` | `else if (uv__queue_empty(&w->watcher_queue))` |
| `ev_da3813cceef7` | assignment | `third_party/libuv/src/unix/fs.c:2064` | `POST;` |
| `ev_da52e95b1bb8` | call_site | `third_party/libuv/src/unix/loop.c:145` | `err = uv__signal_loop_fork(loop);` |
| `ev_da53b740ac75` | call_site | `third_party/libuv/src/unix/signal.c:174` | `handle = RB_NFIND(uv__signal_tree_s, &uv__signal_tree, &lookup);` |
| `ev_da55ccdc0657` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:102` | `pCFBundleGetFunctionPointerForName(launch_services_bundle,` |
| `ev_da63896531df` | call_site | `third_party/libuv/src/unix/fsevents.c:428` | `uv__fsevents_destroy_stream(state);` |
| `ev_da951e41c57b` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_daaa2020b0fc` | call_site | `third_party/libuv/src/unix/kqueue.c:270` | `uv__metrics_set_provider_entry_time(loop);` |
| `ev_dab34f097b37` | call_site | `third_party/libuv/src/unix/udp.c:1206` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, 0);` |
| `ev_dabc52a0c57b` | call_site | `third_party/libuv/src/unix/tcp.c:132` | `err = new_socket(tcp, domain, 0);` |
| `ev_dabc8bf7594d` | call_site | `third_party/libuv/src/unix/loop.c:65` | `uv__queue_init(&loop->pending_queue);` |
| `ev_dabd12372cbc` | call_site | `third_party/libuv/src/fs-poll.c:232` | `if (uv_timer_start(&ctx->timer_handle, timer_cb, interval, 0))` |
| `ev_db04d5f16aeb` | call_site | `third_party/libuv/src/unix/process.c:350` | `n = uv__cloexec(use_fd, 0);` |
| `ev_db260f3c2fdf` | call_site | `third_party/libuv/src/unix/getnameinfo.c:117` | `uv__getnameinfo_work(&req->work_req);` |
| `ev_db51894a5d1d` | call_site | `third_party/libuv/src/unix/fs.c:1812` | `POST;` |
| `ev_db68e296a675` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:214` | `uv__getaddrinfo_done(&req->work_req, 0);` |
| `ev_db8b7d85c4a3` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_dbd96d75b158` | call_site | `third_party/libuv/src/unix/stream.c:1532` | `uv__io_close(handle->loop, &handle->io_watcher);` |
| `ev_dbfcab4bbeda` | call_site | `third_party/libuv/src/unix/fsevents.c:208` | `uv_mutex_unlock(&handle->cf_mutex);` |
| `ev_dc2253994514` | call_site | `third_party/libuv/src/unix/signal.c:61` | `uv__signal_compare)` |
| `ev_dc428e004347` | assignment | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_dc43525b117d` | call_site | `third_party/libuv/src/unix/stream.c:1264` | `getsockopt(uv__stream_fd(stream),` |
| `ev_dc4bcbd12d70` | call_site | `third_party/libuv/src/unix/stream.c:1090` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_dc75e83d673c` | call_site | `third_party/libuv/src/threadpool.c:380` | `uv__work_submit(loop,` |
| `ev_dc76621ba905` | call_site | `third_party/libuv/src/threadpool.c:116` | `uv_cond_signal(&cond);` |
| `ev_dc7cf7fd7b36` | call_site | `third_party/libuv/src/unix/fs.c:2144` | `POST;` |
| `ev_dc87f5ae3010` | assignment | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_dcbb581b1c53` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:138` | `S("_LSSetApplicationLaunchServicesServerConnectionStatus"));` |
| `ev_dcd84d97a726` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:95` | `*addresses = uv__calloc(*count, sizeof(**addresses));` |
| `ev_dd189c9138d2` | call_site | `third_party/libuv/src/fs-poll.c:145` | `if (!uv_is_active((uv_handle_t*)handle)) {` |
| `ev_dd5ae7911c0a` | call_site | `third_party/libuv/src/unix/fsevents.c:811` | `uv__queue_init(&handle->cf_events);` |
| `ev_dd626872b911` | call_site | `third_party/libuv/src/unix/udp.c:1378` | `uv__queue_remove(&req->queue);` |
| `ev_dd666cf67398` | call_site | `third_party/libuv/src/unix/tcp.c:300` | `if (uv__is_ipv6_link_local(addr)) {` |
| `ev_ddc5cbe49251` | call_site | `third_party/libuv/src/unix/udp.c:185` | `nread = recvmsg_x(handle->io_watcher.fd, msgs, chunks, MSG_DONTWAIT);` |
| `ev_de07f5091653` | call_site | `third_party/libuv/src/idna.c:375` | `code_point = uv__wtf8_decode1(&source_ptr);` |
| `ev_de4d7aa9f85a` | call_site | `third_party/libuv/src/unix/core.c:480` | `r = uv__loop_alive(loop);` |
| `ev_de76c6d228d4` | call_site | `third_party/libuv/src/unix/signal.c:358` | `return uv__signal_start(handle, signal_cb, signum, 0);` |
| `ev_decace04d316` | call_site | `third_party/libuv/src/unix/core.c:183` | `uv__prepare_close((uv_prepare_t*)handle);` |
| `ev_ded0ab7c4a90` | call_site | `third_party/libuv/src/unix/udp.c:669` | `err = uv_inet_pton(AF_INET, interface_addr, &mreq.imr_interface.s_addr);` |
| `ev_dee20cff60e7` | call_site | `third_party/libuv/src/threadpool.c:110` | `uv__queue_init(q);` |
| `ev_dee784303ee8` | call_site | `third_party/libuv/src/unix/udp.c:767` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, UV_UDP_REUSEADDR);` |
| `ev_dee788a63b0e` | call_site | `third_party/libuv/src/unix/tcp.c:416` | `uv_close((uv_handle_t*) handle, close_cb);` |
| `ev_df005a1d2457` | call_site | `third_party/libuv/src/unix/process.c:154` | `q = uv__queue_head(h);` |
| `ev_df2040900d3d` | call_site | `third_party/libuv/src/unix/fsevents.c:827` | `uv_unref((uv_handle_t*) handle->cf_cb);` |
| `ev_df9758321799` | call_site | `third_party/libuv/src/unix/fs.c:1836` | `POST;` |
| `ev_dfd30a980cde` | call_site | `third_party/libuv/src/unix/core.c:456` | `timeout = uv__backend_timeout(loop);` |
| `ev_dfdafa4552b5` | call_site | `third_party/libuv/src/unix/fsevents.c:698` | `pCFRelease(state->signal_source);` |
| `ev_dffce2460e6b` | call_site | `third_party/libuv/src/unix/stream.c:1472` | `uv__stream_osx_interrupt_select(stream);` |
| `ev_e05e77ba98fc` | call_site | `third_party/libuv/src/unix/core.c:1477` | `uv__free(*envitems);` |
| `ev_e06579cbe923` | call_site | `third_party/libuv/src/unix/core.c:441` | `uv__update_time(loop);` |
| `ev_e07a8584df14` | call_site | `third_party/libuv/src/uv-common.c:1049` | `idle_time += uv_hrtime() - entry_time;` |
| `ev_e0fee20d38e0` | call_site | `third_party/libuv/src/uv-common.c:98` | `return uv__allocator.local_realloc(ptr, size);` |
| `ev_e119d0a7b836` | call_site | `third_party/libuv/src/unix/stream.c:1118` | `err = uv__stream_recv_cmsg(stream, &msg);` |
| `ev_e12fdcba4223` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_e13f690b8a80` | call_site | `third_party/libuv/src/unix/fs.c:703` | `stat_fs = uv__malloc(sizeof(*stat_fs));` |
| `ev_e1a0d7948334` | call_site | `third_party/libuv/src/unix/pipe.c:146` | `uv__free(pipe_fname);` |
| `ev_e238f71022b7` | call_site | `third_party/libuv/src/unix/core.c:442` | `uv__run_timers(loop);` |
| `ev_e2416169733b` | call_site | `third_party/libuv/src/unix/async.c:198` | `uv__queue_insert_tail(&loop->async_handles, q);` |
| `ev_e2476d7128eb` | call_site | `third_party/libuv/src/unix/proctitle.c:155` | `uv__free(args_mem);  /* Keep valgrind happy. */` |
| `ev_e24881a2ea4c` | call_site | `third_party/libuv/src/unix/fs.c:2273` | `uv__fs_readdir_cleanup(req);` |
| `ev_e25a6ba620bf` | call_site | `third_party/libuv/src/unix/tty.c:290` | `fd = uv__stream_fd(tty);` |
| `ev_e261bff047ce` | call_site | `third_party/libuv/src/unix/fsevents.c:487` | `uv__fsevents_push_event(curr, NULL, err);` |
| `ev_e28abeefea5b` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:130` | `S("_LSApplicationCheckIn"));` |
| `ev_e34d2661654d` | call_site | `third_party/libuv/src/unix/stream.c:1553` | `uv__close(queued_fds->fds[i]);` |
| `ev_e3543af49f75` | call_site | `third_party/libuv/src/unix/signal.c:275` | `uv__io_start(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_e3559fad69eb` | call_site | `third_party/libuv/src/unix/fs.c:2313` | `PATH;` |
| `ev_e375559df85a` | call_site | `third_party/libuv/src/unix/poll.c:50` | `handle->poll_cb(handle, UV_EBADF, 0);` |
| `ev_e39b436dd838` | call_site | `third_party/libuv/src/unix/fsevents.c:317` | `uv__queue_insert_tail(&head, &event->member);` |
| `ev_e3ae11ec3a59` | call_site | `third_party/libuv/src/unix/darwin.c:61` | `uv_once(&once, uv__hrtime_init_once);` |
| `ev_e3bca43bbc2d` | call_site | `third_party/libuv/src/unix/fs.c:2283` | `uv__free(req->ptr);` |
| `ev_e42091574791` | call_site | `third_party/libuv/src/unix/tty.c:374` | `err = ioctl(uv__stream_fd(tty), TIOCGWINSZ, &ws);` |
| `ev_e4cafe2eebda` | call_site | `third_party/libuv/src/unix/stream.c:909` | `uv__queue_move(&stream->write_completed_queue, &pq);` |
| `ev_e536beb3b044` | call_site | `third_party/libuv/src/uv-common.c:88` | `uv__allocator.local_free(ptr);` |
| `ev_e539607ea3c4` | call_site | `third_party/libuv/src/threadpool.c:325` | `q = uv__queue_head(&wq);` |
| `ev_e56ad485e290` | call_site | `third_party/libuv/src/unix/udp.c:131` | `if (!uv__io_active(&handle->io_watcher, POLLIN))` |
| `ev_e572759def4a` | call_site | `third_party/libuv/src/unix/pipe.c:304` | `r = connect(uv__stream_fd(handle), (struct sockaddr*)&saddr, addrlen);` |
| `ev_e5736bdf88e3` | call_site | `third_party/libuv/src/uv-common.c:513` | `return uv__udp_try_send(handle, bufs, nbufs, addr, addrlen);` |
| `ev_e5d92615b65f` | call_site | `third_party/libuv/src/unix/fs.c:1261` | `uv_fs_req_cleanup(&fs_req);` |
| `ev_e60690493e4f` | call_site | `third_party/libuv/src/threadpool.c:130` | `uv_mutex_unlock(&w->loop->wq_mutex);` |
| `ev_e62a5d70cd10` | call_site | `third_party/libuv/src/unix/fsevents.c:458` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_e6472c7d418c` | assignment | `third_party/libuv/src/unix/tcp.c:447` | `tcp->io_watcher.cb = uv__server_io;` |
| `ev_e65471c64fc6` | assignment | `third_party/libuv/src/unix/fs.c:1948` | `POST;` |
| `ev_e699bd5397f4` | call_site | `third_party/libuv/src/unix/kqueue.c:59` | `uv__cloexec(loop->backend_fd, 1);` |
| `ev_e6d0259e7006` | call_site | `third_party/libuv/src/unix/fs.c:1958` | `POST;` |
| `ev_e6e427366243` | call_site | `third_party/libuv/src/unix/thread.c:160` | `stack_size = uv__thread_stack_size();` |
| `ev_e6e4340ec169` | call_site | `third_party/libuv/src/unix/fsevents.c:243` | `uv__queue_init(&head);` |
| `ev_e6f42e853812` | call_site | `third_party/libuv/src/unix/process.c:989` | `pipes = uv__malloc(stdio_count * sizeof(*pipes));` |
| `ev_e70c838ebb27` | call_site | `third_party/libuv/src/unix/tcp.c:601` | `if (uv__stream_fd(handle) != -1) {` |
| `ev_e717033a79f7` | call_site | `third_party/libuv/src/unix/process.c:552` | `err = posix_spawn_fncs->file_actions.addchdir_np(actions, options->cwd);` |
| `ev_e74876777124` | call_site | `third_party/libuv/src/unix/udp.c:923` | `err = uv__udp_maybe_deferred_bind(handle, AF_INET, UV_UDP_REUSEADDR);` |
| `ev_e768d308c774` | call_site | `third_party/libuv/src/unix/process.c:238` | `uv__nonblock(pipefds[0], 1);` |
| `ev_e77f14d51879` | call_site | `third_party/libuv/src/unix/stream.c:906` | `if (uv__queue_empty(&stream->write_completed_queue))` |
| `ev_e7ad50b09c69` | call_site | `third_party/libuv/src/idna.c:434` | `code_point = uv__get_surrogate_value(w_source_ptr, w_source_len);` |
| `ev_e7ade02159ec` | call_site | `third_party/libuv/src/unix/kqueue.c:649` | `uv__close(handle->event_watcher.fd);` |
| `ev_e7b285aadff2` | call_site | `third_party/libuv/src/unix/udp.c:774` | `err = uv_inet_pton(AF_INET, interface_addr, &mreq.imr_interface.s_addr);` |
| `ev_e7bca5df2fd0` | call_site | `third_party/libuv/src/uv-common.c:1020` | `now = uv_hrtime();` |
| `ev_e7c93fafb96c` | call_site | `third_party/libuv/src/threadpool.c:225` | `uv__queue_init(&slow_io_pending_wq);` |
| `ev_e7f42bdec3e0` | call_site | `third_party/libuv/src/unix/poll.c:81` | `err = uv__nonblock(fd, 1);` |
| `ev_e88d9afa7f1e` | call_site | `third_party/libuv/src/threadpool.c:144` | `uv_mutex_lock(&mutex);` |
| `ev_e8de2944e3c7` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:162` | `uv__free(addresses);` |
| `ev_e8f7befb4b22` | call_site | `third_party/libuv/src/unix/core.c:1475` | `uv__free(envitem->name);` |
| `ev_e8fb6ae744c8` | call_site | `third_party/libuv/src/unix/fs.c:2084` | `PATH;` |
| `ev_e985f0370341` | call_site | `third_party/libuv/src/unix/udp.c:968` | `err = uv_ip4_addr(source_addr, 0, &src_addr.in);` |
| `ev_e9f83b888ca3` | call_site | `third_party/libuv/src/unix/signal.c:89` | `uv__close(uv__signal_lock_pipefd[0]);` |
| `ev_ea1ce297616f` | assignment | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_ea1e7036fb81` | call_site | `third_party/libuv/src/unix/stream.c:1278` | `if (error < 0 \|\| uv__queue_empty(&stream->write_queue)) {` |
| `ev_ea3df173b246` | call_site | `third_party/libuv/src/unix/process.c:159` | `uv__queue_remove(&process->queue);` |
| `ev_ea55b7d1dd22` | call_site | `third_party/libuv/src/unix/fs.c:1800` | `POST;` |
| `ev_ea6049b9893c` | call_site | `third_party/libuv/src/unix/process.c:210` | `fd = uv__stream_fd(container->data.stream);` |
| `ev_ea716ea2ec06` | assignment | `third_party/libuv/src/unix/fs.c:2098` | `POST;` |
| `ev_ea82f8dc73cd` | call_site | `third_party/libuv/src/unix/fs.c:1826` | `POST;` |
| `ev_ead793d1052c` | call_site | `third_party/libuv/src/unix/stream.c:1101` | `stream->read_cb(stream, UV__ERR(errno), &buf);` |
| `ev_eb09084eed64` | assignment | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_eb16e34c0c31` | call_site | `third_party/libuv/src/unix/stream.c:251` | `uv__stream_io(stream->loop, &stream->io_watcher, POLLIN);` |
| `ev_eb17e2273625` | call_site | `third_party/libuv/src/threadpool.c:95` | `if (slow_io_work_running >= slow_work_thread_threshold()) {` |
| `ev_eb2068a865ca` | call_site | `third_party/libuv/src/unix/fs.c:1628` | `ret = uv__fstat(fd, &pbuf);` |
| `ev_eb46ba8a9e94` | call_site | `third_party/libuv/src/unix/core.c:847` | `uv__queue_move(&loop->pending_queue, &pq);` |
| `ev_ebf6dd43e814` | call_site | `third_party/libuv/src/unix/fsevents.c:717` | `uv_sem_post(&loop->cf_sem);` |
| `ev_ec6d52a9c2a8` | call_site | `third_party/libuv/src/unix/fs.c:1935` | `POST;` |
| `ev_ec9679f03cf1` | call_site | `third_party/libuv/src/unix/loop-watcher.c:66` | `UV_LOOP_WATCHER_DEFINE(prepare, PREPARE)` |
| `ev_ecc849e922a7` | call_site | `third_party/libuv/src/unix/fsevents.c:374` | `pFSEventStreamRelease(ref);` |
| `ev_ecc8fcb91523` | call_site | `third_party/libuv/src/threadpool.c:286` | `uv_mutex_lock(&mutex);` |
| `ev_ecde99fe2d17` | call_site | `third_party/libuv/src/unix/signal.c:424` | `uv__signal_unlock_and_unblock(&saved_sigmask);` |
| `ev_ece7d55feb91` | call_site | `third_party/libuv/src/unix/fsevents.c:656` | `uv_sem_destroy(&state->fsevent_sem);` |
| `ev_ed2ae77589b1` | call_site | `third_party/libuv/src/unix/loop-watcher.c:67` | `UV_LOOP_WATCHER_DEFINE(check, CHECK)` |
| `ev_ed2b2e4c111d` | call_site | `third_party/libuv/src/unix/bsd-ifaddrs.c:108` | `address->name = uv__strdup(ent->ifa_name);` |
| `ev_ed37ad6ff868` | call_site | `third_party/libuv/src/unix/udp.c:1308` | `if ((r = uv__udp_prep_pkt(&m[n].msg_hdr, bufs[i], nbufs[i], addrs[i])))` |
| `ev_ed4ec597b507` | call_site | `third_party/libuv/src/unix/fs.c:1954` | `PATH;` |
| `ev_ed577decb294` | call_site | `third_party/libuv/src/unix/core.c:1122` | `fd = uv__open_cloexec(filename, O_RDONLY);` |
| `ev_ed60072d3f15` | call_site | `third_party/libuv/src/unix/stream.c:1079` | `nread = uv__recvmsg(uv__stream_fd(stream), &msg, 0);` |
| `ev_ed97b73719aa` | call_site | `third_party/libuv/src/unix/fs.c:1862` | `POST;` |
| `ev_edfae655fde1` | call_site | `third_party/libuv/src/unix/udp.c:612` | `uv__udp_sendmsg(handle);` |
| `ev_ee643cd7f570` | call_site | `third_party/libuv/src/unix/stream.c:895` | `uv__write_req_finish(req);` |
| `ev_ee6977999ce1` | call_site | `third_party/libuv/src/unix/udp.c:75` | `q = uv__queue_head(&handle->write_queue);` |
| `ev_eee9634e0e53` | call_site | `third_party/libuv/src/unix/tcp.c:404` | `fd = uv__stream_fd(handle);` |
| `ev_ef175a01b7ed` | call_site | `third_party/libuv/src/unix/stream.c:415` | `if ((stream->flags & UV_HANDLE_TCP_NODELAY) && uv__tcp_nodelay(fd, 1))` |
| `ev_ef1e7852ba07` | call_site | `third_party/libuv/src/unix/poll.c:108` | `uv__platform_invalidate_fd(handle->loop, handle->io_watcher.fd);` |
| `ev_ef8b4633bd50` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:147` | `pCFBundleGetInfoDictionary(pCFBundleGetMainBundle()));` |
| `ev_f060d986633d` | call_site | `third_party/libuv/src/unix/fs.c:1630` | `uv__to_stat(&pbuf, buf);` |
| `ev_f0ac2565abe9` | call_site | `third_party/libuv/src/unix/darwin-proctitle.c:156` | `if (pLSSetApplicationInformationItem(-2,  /* Magic value. */` |
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
| `ev_f22623d5590c` | call_site | `third_party/libuv/src/unix/signal.c:288` | `uv__close(loop->signal_pipefd[1]);` |
| `ev_f27ea6337e6f` | call_site | `third_party/libuv/src/uv-common.c:410` | `return uv__tcp_connect(req, handle, addr, addrlen, cb);` |
| `ev_f32eac08d2bc` | call_site | `third_party/libuv/src/unix/process.c:1075` | `uv__free(pipes);` |
| `ev_f3480debb9b7` | call_site | `third_party/libuv/src/unix/udp.c:1188` | `return uv__getsockpeername((const uv_handle_t*) handle,` |
| `ev_f355b4f31eac` | call_site | `third_party/libuv/src/unix/process.c:875` | `err = uv__spawn_and_init_child_posix_spawn(options,` |
| `ev_f37958c3a5a4` | call_site | `third_party/libuv/src/unix/core.c:423` | `return uv__loop_alive(loop);` |
| `ev_f3832ed1291f` | call_site | `third_party/libuv/src/unix/fs.c:1999` | `POST;` |
| `ev_f3aa3a485991` | call_site | `third_party/libuv/src/threadpool.c:241` | `uv_sem_destroy(&sem);` |
| `ev_f3b589da3099` | call_site | `third_party/libuv/src/unix/dl.c:37` | `return lib->handle ? 0 : uv__dlerror(lib);` |
| `ev_f3deb2934d98` | call_site | `third_party/libuv/src/unix/core.c:155` | `return uv__hrtime(UV_CLOCK_PRECISE);` |
| `ev_f3faef45b6cb` | call_site | `third_party/libuv/src/unix/pipe.c:274` | `if (includes_nul(name, namelen))` |
| `ev_f451aaf7215d` | call_site | `third_party/libuv/src/unix/fsevents.c:839` | `uv_mutex_unlock(&state->fsevent_mutex);` |
| `ev_f501081cc60b` | call_site | `third_party/libuv/src/unix/stream.c:1182` | `if (uv__queue_empty(&stream->write_queue))` |
| `ev_f5634bb23ca0` | call_site | `third_party/libuv/src/unix/getaddrinfo.c:213` | `uv__getaddrinfo_work(&req->work_req);` |
| `ev_f563ea107417` | call_site | `third_party/libuv/src/unix/fsevents.c:607` | `err = uv_sem_init(&state->fsevent_sem, 0);` |
| `ev_f58a5cd461d9` | call_site | `third_party/libuv/src/threadpool.c:319` | `uv__queue_move(&loop->wq, &wq);` |
| `ev_f5af8d523511` | assignment | `third_party/libuv/src/unix/fs.c:2028` | `POST;` |
| `ev_f5da7c8542e9` | call_site | `third_party/libuv/src/unix/stream.c:1210` | `if (uv__stream_fd(stream) == -1)` |
| `ev_f5f546380dc5` | call_site | `third_party/libuv/src/unix/tty.c:325` | `uv__tty_make_raw(&tmp);` |
| `ev_f61ceabe42fc` | call_site | `third_party/libuv/src/unix/thread.c:118` | `if (lim.rlim_cur >= (rlim_t) uv__min_stack_size())` |
| `ev_f6395d2a38b4` | call_site | `third_party/libuv/src/unix/tcp.c:355` | `if (uv__fd_exists(handle->loop, sock))` |
| `ev_f692596f7f95` | call_site | `third_party/libuv/src/unix/process.c:1010` | `exec_errorno = uv__spawn_and_init_child(loop, options, stdio_count, pipes, &pid);` |
| `ev_f697f0d480ca` | call_site | `third_party/libuv/src/unix/fsevents.c:875` | `uv_mutex_lock(&state->fsevent_mutex);` |
| `ev_f7156c120f5a` | call_site | `third_party/libuv/src/unix/fs.c:2177` | `POST;` |
| `ev_f79e414930c4` | call_site | `third_party/libuv/src/unix/pipe.c:523` | `if ((err = uv__nonblock(temp[0], 1)))` |
| `ev_f7b579a18d9c` | call_site | `third_party/libuv/src/unix/core.c:1047` | `return uv__getrusage(RUSAGE_SELF, rusage);` |
| `ev_f7b6e217c75e` | call_site | `third_party/libuv/src/unix/loop-watcher.c:68` | `UV_LOOP_WATCHER_DEFINE(idle, IDLE)` |
| `ev_f7e698584085` | call_site | `third_party/libuv/src/unix/stream.c:353` | `err = uv_sem_init(&s->close_sem, 0);` |
| `ev_f7fd900cabe3` | call_site | `third_party/libuv/src/unix/core.c:528` | `uv__close(sockfd);` |
| `ev_f80093ab98fd` | call_site | `third_party/libuv/src/threadpool.c:74` | `uv__queue_next(&run_slow_work_message) == &wq &&` |
| `ev_f8059c4eb9dc` | call_site | `third_party/libuv/src/unix/fs.c:1592` | `ret = uv__fs_statx(-1, path, /* is_fstat */ 0, /* is_lstat */ 0, buf);` |
| `ev_f8253cf22497` | call_site | `third_party/libuv/src/unix/stream.c:949` | `queued_fds = uv__malloc((queue_size - 1) * sizeof(*queued_fds->fds) +` |
| `ev_f85910885849` | assignment | `third_party/libuv/src/unix/fs.c:2111` | `POST;` |
| `ev_f87e32bcc811` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_f8a5f2b68799` | call_site | `third_party/libuv/src/thread-common.c:118` | `uv_mutex_unlock(&b->mutex);` |
| `ev_f8ddfd55deff` | assignment | `third_party/libuv/src/unix/async.c:311` | `uv__io_init(&loop->async_io_watcher, uv__async_io, pipefd[0]);` |
| `ev_f92cba05b32c` | call_site | `third_party/libuv/src/queue.h:63` | `if (uv__queue_empty(h))` |
| `ev_f93d256542e1` | call_site | `third_party/libuv/src/unix/udp.c:113` | `uv__free(req->bufs);` |
| `ev_f97f0d23a079` | call_site | `third_party/libuv/src/unix/stream.c:1533` | `uv_read_stop(handle);` |
| `ev_f9b645bbed9f` | call_site | `third_party/libuv/src/unix/core.c:889` | `nwatchers = next_power_of_two(len + 2) - 2;` |
| `ev_f9f790410cf0` | call_site | `third_party/libuv/src/unix/fs.c:2267` | `uv__free((void*) req->path);  /* Memory is shared with req->new_path. */` |
| `ev_f9fd744d1594` | call_site | `third_party/libuv/src/unix/stream.c:913` | `q = uv__queue_head(&pq);` |
| `ev_fa334f184c7d` | call_site | `third_party/libuv/src/unix/tty.c:210` | `uv__stream_init(loop, (uv_stream_t*) tty, UV_TTY);` |
| `ev_facf1520fd2a` | call_site | `third_party/libuv/src/unix/fs.c:2193` | `POST;` |
| `ev_fb04137a2540` | call_site | `third_party/libuv/src/unix/process.c:618` | `uv__nonblock_fcntl(use_fd, 0);` |
| `ev_fb547ffabf46` | call_site | `third_party/libuv/src/unix/core.c:578` | `err = uv__cloexec(peerfd, 1);` |
| `ev_fbb40e372bcd` | call_site | `third_party/libuv/src/unix/fs.c:2120` | `POST;` |
| `ev_fbdab1c688e3` | assignment | `third_party/libuv/src/unix/fs.c:2151` | `POST;` |
| `ev_fc5635c5b5d0` | call_site | `third_party/libuv/src/unix/stream.c:1052` | `stream->alloc_cb((uv_handle_t*)stream, 64 * 1024, &buf);` |
| `ev_fc6251443018` | call_site | `third_party/libuv/src/unix/fs.c:1202` | `tv[0] = uv__fs_to_timeval(req->atime);` |
| `ev_fc75b96e58bf` | call_site | `third_party/libuv/src/unix/fs.c:1982` | `PATH;` |
| `ev_fc9c201f311f` | call_site | `third_party/libuv/src/unix/poll.c:74` | `err = uv__io_check_fd(loop, fd);` |
| `ev_fcd5f4f38ae4` | call_site | `third_party/libuv/src/unix/fs.c:2302` | `PATH2;` |
| `ev_fd0fe73b6c39` | call_site | `third_party/libuv/src/threadpool.c:291` | `uv__queue_remove(&w->wq);` |
| `ev_fd40b04980f7` | assignment | `third_party/libuv/src/unix/fs.c:1886` | `POST;` |
| `ev_fd4278805330` | call_site | `third_party/libuv/src/unix/fsevents.c:188` | `UV__FSEVENTS_PROCESS(handle, {` |
| `ev_fd83b0b24448` | call_site | `third_party/libuv/src/unix/signal.c:286` | `uv__io_stop(loop, &loop->signal_io_watcher, POLLIN);` |
| `ev_fd8677621322` | call_site | `third_party/libuv/src/unix/core.c:351` | `uv__udp_finish_close((uv_udp_t*)handle);` |
| `ev_fd9ce8da62a2` | call_site | `third_party/libuv/src/unix/fs.c:1727` | `X(LSTAT, uv__fs_lstat(req->path, &req->statbuf));` |
| `ev_fe1cee440e9e` | call_site | `third_party/libuv/src/unix/async.c:394` | `uv__io_stop(loop, &loop->async_io_watcher, POLLIN);` |
| `ev_fe26acb7066c` | call_site | `third_party/libuv/src/idna.c:232` | `c = uv__utf8_decode1(&s, se);` |
| `ev_fe6137adc778` | call_site | `third_party/libuv/src/unix/core.c:1777` | `r = uv__strscpy(buffer->version, buf.version, sizeof(buffer->version));` |
| `ev_fe6b3fbeb2f8` | call_site | `third_party/libuv/src/unix/kqueue.c:360` | `uv__kqueue_delete(loop->backend_fd, ev);` |
| `ev_fec163fa5680` | call_site | `third_party/libuv/src/unix/kqueue.c:72` | `err = uv__kqueue_init(loop);` |
| `ev_fee781bf7238` | assignment | `third_party/libuv/src/unix/fs.c:1848` | `POST;` |
| `ev_ff728f86ed86` | call_site | `third_party/libuv/src/unix/core.c:377` | `uv__finish_close(p);` |
| `ev_ff7e59f3db4f` | call_site | `third_party/libuv/src/unix/fs.c:2217` | `POST;` |
| `ev_ffa07e66dc9b` | call_site | `third_party/libuv/src/unix/random-devurandom.c:38` | `fd = uv__open_cloexec(path, O_RDONLY);` |
| `ev_ffe2a3be3446` | call_site | `third_party/libuv/src/unix/fs.c:1731` | `X(MKSTEMP, uv__fs_mkstemp(req));` |
