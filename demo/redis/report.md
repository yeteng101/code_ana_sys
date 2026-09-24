# 代码逆向分析 Demo

- Run: `redis-7.2.4-validation`
- Build profile: `redis-linux-clang`
- Analyzer: `clang++ -Xclang -ast-dump=json`
- Nodes: 682 / Edges: 1864
- Verification: 88%

## 模块架构

- **core**: 核心逻辑
  - Files: ``
  - Symbols: `defragalloc、defragkey、defragval、fn、getMonotonicUs`
- **src**: 事件循环驱动、事件等待、停止循环、初始化、核心逻辑
  - Files: `third_party/redis/src/adlist.c`, `third_party/redis/src/adlist.h`, `third_party/redis/src/ae.c`, `third_party/redis/src/ae.h`, `third_party/redis/src/ae_epoll.c`, `third_party/redis/src/anet.h`, `third_party/redis/src/bio.c`, `third_party/redis/src/cluster.h`, `third_party/redis/src/connection.h`, `third_party/redis/src/db.c`, `third_party/redis/src/dict.c`, `third_party/redis/src/dict.h`, `third_party/redis/src/endianconv.h`, `third_party/redis/src/functions.h`, `third_party/redis/src/latency.h`, `third_party/redis/src/lazyfree.c`, `third_party/redis/src/listpack.h`, `third_party/redis/src/monotonic.h`, `third_party/redis/src/mt19937-64.h`, `third_party/redis/src/networking.c`, `third_party/redis/src/rax.h`, `third_party/redis/src/rdb.h`, `third_party/redis/src/redisassert.h`, `third_party/redis/src/rio.h`, `third_party/redis/src/script.h`, `third_party/redis/src/sds.h`, `third_party/redis/src/server.h`, `third_party/redis/src/stream.h`, `third_party/redis/src/t_string.c`, `third_party/redis/src/util.h`, `third_party/redis/src/zmalloc.h`
  - Symbols: `ConnectionType::accept、ConnectionType::addr、ConnectionType::blocking_connect、ConnectionType::close、ConnectionType::configure、ConnectionType::conn_create、ConnectionType::conn_create_accepted、ConnectionType::connect、ConnectionType::get_last_error、ConnectionType::get_peer_cert、ConnectionType::get_type、ConnectionType::is_local、ConnectionType::listen、ConnectionType::read、ConnectionType::set_read_handler、ConnectionType::set_write_handler、ConnectionType::shutdown、ConnectionType::sync_read、ConnectionType::sync_readline、ConnectionType::sync_write、ConnectionType::write、ConnectionType::writev、_rio::flush、_rio::read、_rio::tell、_rio::update_cksum、_rio::write、aeEventLoop::aftersleep、aeEventLoop::beforesleep、aeFileEvent::rfileProc、aeFileEvent::wfileProc、aeTimeEvent::finalizerProc、aeTimeEvent::timeProc、bio_job::struct (unnamed at /home/runner/work/code_ana_sys/code_ana_sys/third_party/redis/src/bio.c:105:5)::free_fn、dictType::afterReplaceEntry、dictType::dictEntryMetadataBytes、dictType::dictMetadataBytes、dictType::expandAllowed、dictType::hashFunction、dictType::keyCompare、dictType::keyDestructor、dictType::keyDup、dictType::valDestructor、dictType::valDup、list::dup、list::free、list::match、redisCommand::getkeys_proc、ACLAuthenticateUser、ACLGetUserByName、AddReplyFromClient、IOThreadMain、LFUDecrAndReturn、LFUGetTimeInMinutes、LFULogIncr、LRU_CLOCK、_addReplyProtoToList、_addReplyToBuffer、_addReplyToBufferOrList、_dictClear、_dictExpand、_dictExpandIfNeeded、_dictGetStatsHt、_dictInit、_dictNextExp、_dictRehashStep、_dictReset、_serverAssert、_serverAssertWithInfo、_serverLog、_serverPanic、_writeToClient、_writevToClient、abortShutdown、acceptCommonHandler、addAuthErrReply、addReply、addReplyAggregateLen、addReplyArrayLen、addReplyAttributeLen、addReplyBigNum、addReplyBool、addReplyBulk、addReplyBulkCBuffer、addReplyBulkCString、addReplyBulkLen、addReplyBulkLongLong、addReplyBulkSds、addReplyDeferredLen、addReplyDouble、addReplyError、addReplyErrorArity、addReplyErrorExpireTime、addReplyErrorFormat、addReplyErrorFormatEx、addReplyErrorFormatInternal、addReplyErrorLength、addReplyErrorObject、addReplyErrorSds、addReplyErrorSdsEx、addReplyErrorSdsSafe、addReplyHelp、addReplyHumanLongDouble、addReplyLoadedModules、addReplyLongLong、addReplyLongLongWithPrefix、addReplyMapLen、addReplyNull、addReplyNullArray、addReplyOrErrorObject、addReplyProto、addReplyPushLen、addReplySds、addReplySetLen、addReplyStatus、addReplyStatusFormat、addReplyStatusLength、addReplySubcommandSyntaxError、addReplyVerbatim、aeApiAddEvent、aeApiCreate、aeApiDelEvent、aeApiFree、aeApiName、aeApiPoll、aeApiResize、aeCreateEventLoop、aeCreateFileEvent、aeCreateTimeEvent、aeDeleteEventLoop、aeDeleteFileEvent、aeGetApiName、aeMain、aeProcessEvents、aeResizeSetSize、afterErrorReply、alsoPropagate、anetCloexec、anyOtherSlaveWaitRdb、appendCommand、authRequired、beforeNextClient、bioCreateCloseAofJob、bioCreateCloseJob、bioCreateFsyncJob、bioCreateLazyFreeJob、bioInit、bioKillThreads、bioProcessBackgroundJobs、bioSubmitJob、bitfieldGetKeys、blmpopGetKeys、blockClientShutdown、bzmpopGetKeys、catClientInfoString、checkAlreadyExpired、checkClientOutputBufferLimits、checkPrefixCollisionsOrReply、checkStringLength、checkType、clearClientConnectionState、clientAcceptHandler、clientCommand、clientHasPendingReplies、clientSetDefaultAuth、clientSetName、clientSetNameOrReply、clientSetinfoCommand、closeClientOnOutputBufferLimitReached、cmdHasPushAsReply、commandProcessed、commandTimeSnapshot、connAccept、connAddr、connAddrPeerName、connAddrSockName、connBlockingConnect、connClose、connConnect、connCreate、connCreateAccepted、connEnableTcpNoDelay、connFormatAddr、connGetInfo、connGetLastError、connGetPeerCert、connGetPrivateData、connGetState、connGetType、connHasReadHandler、connHasWriteHandler、connIsLocal、connIsTLS、connKeepAlive、connListen、connRead、connSetPrivateData、connSetReadHandler、connSetWriteHandler、connSetWriteHandlerWithBarrier、connShutdown、connSyncRead、connSyncReadLine、connSyncWrite、connTypeConfigure、connWrite、connWritev、connectionTypeTls、copyCommand、copyReplicaOutputBuffer、createClient、createEntryNoValue、createObject、createRawStringObject、createStringObject、createStringObjectFromLongDouble、createStringObjectFromLongLong、createStringObjectFromLongLongForValue、d2string、dbAdd、dbAddInternal、dbAddRDBLoad、dbAsyncDelete、dbDelete、dbGenericDelete、dbRandomKey、dbReplaceValue、dbSetValue、dbSwapDatabases、dbSyncDelete、dbUnshareStringValue、dbsizeCommand、decodeEntryNoValue、decodeMaskedPtr、decrCommand、decrRefCount、decrbyCommand、deferredAfterErrorReply、delCommand、delGenericCommand、deleteExpiredKeyAndPropagate、dictAdd、dictAddOrFind、dictAddRaw、dictCreate、dictDefragBucket、dictDelete、dictEmpty、dictEntryMetadata、dictExpand、dictFetchValue、dictFind、dictFindEntryByPtrAndHash、dictFindPositionForInsert、dictFingerprint、dictFreeUnlinkedEntry、dictGenCaseHashFunction、dictGenHashFunction、dictGenericDelete、dictGetDoubleVal、dictGetDoubleValPtr、dictGetFairRandomKey、dictGetHash、dictGetIterator、dictGetKey、dictGetNext、dictGetNextRef、dictGetRandomKey、dictGetSafeIterator、dictGetSignedIntegerVal、dictGetSomeKeys、dictGetStats、dictGetUnsignedIntegerVal、dictGetVal、dictIncrDoubleVal、dictIncrSignedIntegerVal、dictIncrUnsignedIntegerVal、dictInitIterator、dictInitSafeIterator、dictInsertAtPosition、dictMetadata、dictNext、dictRehash、dictRehashMilliseconds、dictRelease、dictReleaseIterator、dictReplace、dictResetIterator、dictResize、dictScan、dictScanDefrag、dictSetDoubleVal、dictSetKey、dictSetNext、dictSetSignedIntegerVal、dictSetUnsignedIntegerVal、dictSetVal、dictTryExpand、dictTwoPhaseUnlinkFind、dictTwoPhaseUnlinkFree、dictTypeExpandAllowed、dictUnlink、digits10、disableTracking、discardTempDb、discardTransaction、disconnectSlaves、doesCommandHaveKeys、dupClientReplyValue、dupStringObject、elapsedMs、elapsedStart、elapsedUs、emptyData、emptyDbAsync、emptyDbStructure、enableTracking、encodeMaskedPtr、entryHasValue、entryIsKey、entryIsNoValue、entryIsNormal、evalGetKeys、evictClients、existsCommand、expireIfNeeded、flushAllDataAndResetRDB、flushSlaveKeysWithExpireList、flushSlavesOutputBuffers、flushallCommand、flushdbCommand、forceCommandPropagation、formatAddr、freeClient、freeClientArgv、freeClientAsync、freeClientMultiState、freeClientOriginalArgv、freeClientReplyValue、freeClientsInAsyncFreeQueue、freeFunctionsAsync、freeLuaScriptsAsync、freeObjAsync、freeReplicaReferencedReplBuffer、freeReplicationBacklogRefMemAsync、freeTrackingRadixTree、freeTrackingRadixTreeAsync、functionGetKeys、functionsLibCtxClearCurrent、functionsLibCtxFree、functionsLibCtxfunctionsLen、genClientAddrString、genericGetKeys、genrand64_int64、georadiusGetKeys、getAllClientsInfoString、getAllKeySpecsFlags、getChannelsFromCommand、getClientEvictionLimit、getClientMemoryUsage、getClientOutputBufferMemoryUsage、getClientPeerId、getClientSockname、getClientType、getClientTypeByName、getClusterConnectionsCount、getCommand、getDecodedObject、getExpire、getExpireMillisecondsOrReply、getFlushCommandFlags、getGenericCommand、getIOPendingCount、getIntFromObjectOrReply、getKeysFreeResult、getKeysFromCommand、getKeysFromCommandWithSpecs、getKeysPrepareResult、getKeysUsingKeySpecs、getKeysUsingLegacyRangeSpec、getLongDoubleFromObjectOrReply、getLongFromObjectOrReply、getLongLongFromObjectOrReply、getObjectTypeByName、getObjectTypeName、getRangeLongFromObjectOrReply、getStringObjectLen、getStringObjectSdsUsedMemory、getTimeoutFromObjectOrReply、getdelCommand、getexCommand、getrangeCommand、getsetCommand、handleClientsWithPendingReadsUsingThreads、handleClientsWithPendingWrites、handleClientsWithPendingWritesUsingThreads、hasActiveChildProcess、hashTypeDup、helloCommand、incrCommand、incrDecrCommand、incrRefCount、incrbyCommand、incrbyfloatCommand、incrementErrorCount、incrementalTrimReplicationBacklog、initClientBlockingState、initClientMultiState、initObjectLRUOrLFU、initTempDb、initThreadedIO、installClientWriteHandler、intrev64、isInsideYieldingLongCommand、isPausedActionsWithUpdate、keyIsExpired、keysCommand、killIOThreads、killRDBChild、lastsaveCommand、latencyAddSample、lazyFreeFunctionsCtx、lazyFreeLuaScripts、lazyFreeReplicationBacklogRefMem、lazyFreeTrackingTable、lazyfreeFreeDatabase、lazyfreeFreeObject、lazyfreeGetFreeEffort、lcsCommand、ld2string、linkClient、listAddNodeHead、listAddNodeTail、listCreate、listDelNode、listDup、listEmpty、listGetIterator、listInitNode、listInsertNode、listJoin、listLinkNodeHead、listLinkNodeTail、listNext、listRelease、listReleaseIterator、listRewind、listSearchKey、listTypeDup、listUnlinkNode、ll2string、lmpopGetKeys、logInvalidUseAndFreeClientAsync、lookupClientByID、lookupCommandOrOriginal、lookupKey、lookupKeyRead、lookupKeyReadOrReply、lookupKeyReadWithFlags、lookupKeyWrite、lookupKeyWriteOrReply、lookupKeyWriteWithFlags、lpFirst、lpGet、lpNext、makeThreadKillable、mgetCommand、migrateGetKeys、moduleBlockedClientMayTimeout、moduleFireServerEvent、moduleGetCommandChannelsViaAPI、moduleGetCommandKeysViaAPI、moduleGetFreeEffort、moduleNotifyKeyUnlink、moduleNotifyUserChanged、moduleTypeDupOrReply、moduleTypeLookupModuleByNameIgnoreCase、monotonicInit、moveCommand、msetCommand、msetGenericCommand、msetnxCommand、mstime、multiStateMemOverhead、mustObeyClient、notifyKeyspaceEvent、objectTypeCompare、parseExtendedStringArgumentsOrReply、parseScanCursorOrReply、pauseActions、pauseClientsByClient、postponeClientRead、prepareClientToWrite、prepareForShutdown、processCommand、processCommandAndResetClient、processEventsWhileBlocked、processInlineBuffer、processInputBuffer、processMultibulkBuffer、processPendingCommandAndInputBuffer、processTimeEvents、propagateDeletion、protectClient、psetexCommand、pubsubMemOverhead、pubsubUnsubscribeAllChannels、pubsubUnsubscribeAllPatterns、pubsubUnsubscribeShardAllChannels、putClientInPendingWriteQueue、quitCommand、randomkeyCommand、raxFind、raxFree、raxInsert、raxNext、raxRemove、raxSeek、raxSize、raxStart、raxStop、rdbPipeWriteHandlerConnRemoved、rdbPopulateSaveInfo、rdbSave、readQueryFromClient、reclaimFilePageCache、redactClientCommandArgument、redisSetCpuAffinity、refreshGoodSlavesCount、rememberSlaveKeyWithExpire、removeClientFromMemUsageBucket、removeExpire、renameCommand、renameGenericCommand、renamenxCommand、replaceClientCommandVector、replicationCacheMaster、replicationFeedStreamFromMasterStream、replicationGetSlaveName、replicationHandleMasterDisconnection、reqresAppendResponse、reqresSaveClientReplyOffset、resetClient、resetCommand、retainOriginalCommandVector、rev、rewriteClientCommandArgument、rewriteClientCommandVector、rioFlush、rioRead、rioTell、rioWrite、scanCallback、scanCommand、scanDatabaseForDeletedKeys、scanDatabaseForReadyKeys、scanGenericCommand、scriptIsEval、sdsAllocPtr、sdsIncrLen、sdsMakeRoomFor、sdsMakeRoomForNonGreedy、sdsZmallocSize、sdsalloc、sdsavail、sdscatfmt、sdscatlen、sdscatprintf、sdscatrepr、sdscatvprintf、sdsclear、sdscmp、sdsdup、sdsempty、sdsfree、sdsfreesplitres、sdsgrowzero、sdslen、sdsmapchars、sdsnew、sdsnewlen、sdsrange、sdssplitargs、sdstoupper、sdstrim、securityWarningCommand、selectCommand、selectDb、sendReplyToClient、setCommand、setDeferredAggregateLen、setDeferredArrayLen、setDeferredAttributeLen、setDeferredMapLen、setDeferredPushLen、setDeferredReply、setDeferredReplyBulkSds、setDeferredSetLen、setExpire、setGenericCommand、setGetKeys、setIOPendingCount、setKey、setProtocolError、setTypeDup、setTypeInitIterator、setTypeNext、setTypeReleaseIterator、setexCommand、setnxCommand、setrangeCommand、showLatestBacklog、shutdownCommand、signalDeletedKeyAsReady、signalFlushedDb、signalKeyAsReady、signalModifiedKey、sintercardGetKeys、siphash、siphash_nocase、slotToKeyAddEntry、slotToKeyDelEntry、slotToKeyDestroy、slotToKeyFlush、slotToKeyInit、sortGetKeys、sortROGetKeys、startThreadedIO、stopThreadedIO、stopThreadedIOIfNeeded、streamDup、string2ll、stringObjectLen、stringmatchlen、strlenCommand、swapMainDbWithTempDb、swapdbCommand、timeInMilliseconds、touchAllWatchedKeysInDb、touchWatchedKey、trackingInvalidateKey、trackingInvalidateKeysOnFlush、trimReplyUnusedTailSpace、tryObjectEncoding、typeCommand、unblockClient、unblockClientOnError、unblockClientOnTimeout、unblockPostponedClients、unlinkClient、unlinkCommand、unpauseActions、unprotectClient、unwatchAllKeys、updateCachedTime、updateClientMemUsageAndBucket、updateLFU、updatePausedActions、usUntilEarliestTimer、validateClientAttr、validateClientName、whileBlockedCron、writeToClient、xreadGetKeys、zcalloc、zfree、zmalloc、zmalloc_usable、zmalloc_used_memory、zmpopGetKeys、zrealloc、zrealloc_usable、zsetDup、ztrycalloc、ztrymalloc、zunionInterDiffGetKeys、zunionInterDiffStoreGetKeys`

Dependencies: `src -> core`

## 调用关系图

```mermaid
flowchart TD
  subgraph sg_core["core"]
    N1["defragalloc"]
    N2["defragkey"]
    N3["defragval"]
    N4["fn"]
    N5["getMonotonicUs"]
  end
  subgraph sg_src["src"]
    N6["ConnectionType::accept"]
    N7["ConnectionType::addr"]
    N8["ConnectionType::blocking_connect"]
    N9["ConnectionType::close"]
    N10["ConnectionType::configure"]
    N11["ConnectionType::conn_create"]
    N12["ConnectionType::conn_create_accepted"]
    N13["ConnectionType::connect"]
    N14["ConnectionType::get_last_error"]
    N15["ConnectionType::get_peer_cert"]
    N16["ConnectionType::get_type"]
    N17["ConnectionType::is_local"]
    N18["ConnectionType::listen"]
    N19["ConnectionType::read"]
    N20["ConnectionType::set_read_handler"]
    N21["ConnectionType::set_write_handler"]
    N22["ConnectionType::shutdown"]
    N23["ConnectionType::sync_read"]
    N24["ConnectionType::sync_readline"]
    N25["ConnectionType::sync_write"]
    N26["ConnectionType::write"]
    N27["ConnectionType::writev"]
    N28["_rio::flush"]
    N29["_rio::read"]
    N30["_rio::tell"]
    N31["_rio::update_cksum"]
    N32["_rio::write"]
    N33["aeEventLoop::aftersleep"]
    N34["aeEventLoop::beforesleep"]
    N35["aeFileEvent::rfileProc"]
    N36["aeFileEvent::wfileProc"]
    N37["aeTimeEvent::finalizerProc"]
    N38["aeTimeEvent::timeProc"]
    N39["bio_job::struct (unnamed at /home/runner/work/code_ana_sys/code_ana_sys/third_party/redis/src/bio.c:105:5)::free_fn"]
    N40["dictType::afterReplaceEntry"]
    N41["dictType::dictEntryMetadataBytes"]
    N42["dictType::dictMetadataBytes"]
    N43["dictType::expandAllowed"]
    N44["dictType::hashFunction"]
    N45["dictType::keyCompare"]
    N46["dictType::keyDestructor"]
    N47["dictType::keyDup"]
    N48["dictType::valDestructor"]
    N49["dictType::valDup"]
    N50["list::dup"]
    N51["list::free"]
    N52["list::match"]
    N53["redisCommand::getkeys_proc"]
    N54["ACLAuthenticateUser"]
    N55["ACLGetUserByName"]
    N56["AddReplyFromClient"]
    N57["IOThreadMain"]
    N58["LFUDecrAndReturn"]
    N59["LFUGetTimeInMinutes"]
    N60["LFULogIncr"]
    N61["LRU_CLOCK"]
    N62["_addReplyProtoToList"]
    N63["_addReplyToBuffer"]
    N64["_addReplyToBufferOrList"]
    N65["_dictClear"]
    N66["_dictExpand"]
    N67["_dictExpandIfNeeded"]
    N68["_dictGetStatsHt"]
    N69["_dictInit"]
    N70["_dictNextExp"]
    N71["_dictRehashStep"]
    N72["_dictReset"]
    N73["_serverAssert"]
    N74["_serverAssertWithInfo"]
    N75["_serverLog"]
    N76["_serverPanic"]
    N77["_writeToClient"]
    N78["_writevToClient"]
    N79["abortShutdown"]
    N80["acceptCommonHandler"]
    N81["addAuthErrReply"]
    N82["addReply"]
    N83["addReplyAggregateLen"]
    N84["addReplyArrayLen"]
    N85["addReplyAttributeLen"]
    N86["addReplyBigNum"]
    N87["addReplyBool"]
    N88["addReplyBulk"]
    N89["addReplyBulkCBuffer"]
    N90["addReplyBulkCString"]
    N91["addReplyBulkLen"]
    N92["addReplyBulkLongLong"]
    N93["addReplyBulkSds"]
    N94["addReplyDeferredLen"]
    N95["addReplyDouble"]
    N96["addReplyError"]
    N97["addReplyErrorArity"]
    N98["addReplyErrorExpireTime"]
    N99["addReplyErrorFormat"]
    N100["addReplyErrorFormatEx"]
    N101["addReplyErrorFormatInternal"]
    N102["addReplyErrorLength"]
    N103["addReplyErrorObject"]
    N104["addReplyErrorSds"]
    N105["addReplyErrorSdsEx"]
    N106["addReplyErrorSdsSafe"]
    N107["addReplyHelp"]
    N108["addReplyHumanLongDouble"]
    N109["addReplyLoadedModules"]
    N110["addReplyLongLong"]
    N111["addReplyLongLongWithPrefix"]
    N112["addReplyMapLen"]
    N113["addReplyNull"]
    N114["addReplyNullArray"]
    N115["addReplyOrErrorObject"]
    N116["addReplyProto"]
    N117["addReplyPushLen"]
    N118["addReplySds"]
    N119["addReplySetLen"]
    N120["addReplyStatus"]
    N121["addReplyStatusFormat"]
    N122["addReplyStatusLength"]
    N123["addReplySubcommandSyntaxError"]
    N124["addReplyVerbatim"]
    N125["aeApiAddEvent"]
    N126["aeApiCreate"]
    N127["aeApiDelEvent"]
    N128["aeApiFree"]
    N129["aeApiName"]
    N130["aeApiPoll"]
    N131["aeApiResize"]
    N132["aeCreateEventLoop"]
    N133["aeCreateFileEvent"]
    N134["aeCreateTimeEvent"]
    N135["aeDeleteEventLoop"]
    N136["aeDeleteFileEvent"]
    N137["aeGetApiName"]
    N138["aeMain"]
    N139["aeProcessEvents"]
    N140["aeResizeSetSize"]
    N141["afterErrorReply"]
    N142["alsoPropagate"]
    N143["anetCloexec"]
    N144["anyOtherSlaveWaitRdb"]
    N145["appendCommand"]
    N146["authRequired"]
    N147["beforeNextClient"]
    N148["bioCreateCloseAofJob"]
    N149["bioCreateCloseJob"]
    N150["bioCreateFsyncJob"]
    N151["bioCreateLazyFreeJob"]
    N152["bioInit"]
    N153["bioKillThreads"]
    N154["bioProcessBackgroundJobs"]
    N155["bioSubmitJob"]
    N156["bitfieldGetKeys"]
    N157["blmpopGetKeys"]
    N158["blockClientShutdown"]
    N159["bzmpopGetKeys"]
    N160["catClientInfoString"]
    N161["checkAlreadyExpired"]
    N162["checkClientOutputBufferLimits"]
    N163["checkPrefixCollisionsOrReply"]
    N164["checkStringLength"]
    N165["checkType"]
    N166["clearClientConnectionState"]
    N167["clientAcceptHandler"]
    N168["clientCommand"]
    N169["clientHasPendingReplies"]
    N170["clientSetDefaultAuth"]
    N171["clientSetName"]
    N172["clientSetNameOrReply"]
    N173["clientSetinfoCommand"]
    N174["closeClientOnOutputBufferLimitReached"]
    N175["cmdHasPushAsReply"]
    N176["commandProcessed"]
    N177["commandTimeSnapshot"]
    N178["connAccept"]
    N179["connAddr"]
    N180["connAddrPeerName"]
    N181["connAddrSockName"]
    N182["connBlockingConnect"]
    N183["connClose"]
    N184["connConnect"]
    N185["connCreate"]
    N186["connCreateAccepted"]
    N187["connEnableTcpNoDelay"]
    N188["connFormatAddr"]
    N189["connGetInfo"]
    N190["connGetLastError"]
    N191["connGetPeerCert"]
    N192["connGetPrivateData"]
    N193["connGetState"]
    N194["connGetType"]
    N195["connHasReadHandler"]
    N196["connHasWriteHandler"]
    N197["connIsLocal"]
    N198["connIsTLS"]
    N199["connKeepAlive"]
    N200["connListen"]
    N201["connRead"]
    N202["connSetPrivateData"]
    N203["connSetReadHandler"]
    N204["connSetWriteHandler"]
    N205["connSetWriteHandlerWithBarrier"]
    N206["connShutdown"]
    N207["connSyncRead"]
    N208["connSyncReadLine"]
    N209["connSyncWrite"]
    N210["connTypeConfigure"]
    N211["connWrite"]
    N212["connWritev"]
    N213["connectionTypeTls"]
    N214["copyCommand"]
    N215["copyReplicaOutputBuffer"]
    N216["createClient"]
    N217["createEntryNoValue"]
    N218["createObject"]
    N219["createRawStringObject"]
    N220["createStringObject"]
    N221["createStringObjectFromLongDouble"]
    N222["createStringObjectFromLongLong"]
    N223["createStringObjectFromLongLongForValue"]
    N224["d2string"]
    N225["dbAdd"]
    N226["dbAddInternal"]
    N227["dbAddRDBLoad"]
    N228["dbAsyncDelete"]
    N229["dbDelete"]
    N230["dbGenericDelete"]
    N231["dbRandomKey"]
    N232["dbReplaceValue"]
    N233["dbSetValue"]
    N234["dbSwapDatabases"]
    N235["dbSyncDelete"]
    N236["dbUnshareStringValue"]
    N237["dbsizeCommand"]
    N238["decodeEntryNoValue"]
    N239["decodeMaskedPtr"]
    N240["decrCommand"]
    N241["decrRefCount"]
    N242["decrbyCommand"]
    N243["deferredAfterErrorReply"]
    N244["delCommand"]
    N245["delGenericCommand"]
    N246["deleteExpiredKeyAndPropagate"]
    N247["dictAdd"]
    N248["dictAddOrFind"]
    N249["dictAddRaw"]
    N250["dictCreate"]
    N251["dictDefragBucket"]
    N252["dictDelete"]
    N253["dictEmpty"]
    N254["dictEntryMetadata"]
    N255["dictExpand"]
    N256["dictFetchValue"]
    N257["dictFind"]
    N258["dictFindEntryByPtrAndHash"]
    N259["dictFindPositionForInsert"]
    N260["dictFingerprint"]
    N261["dictFreeUnlinkedEntry"]
    N262["dictGenCaseHashFunction"]
    N263["dictGenHashFunction"]
    N264["dictGenericDelete"]
    N265["dictGetDoubleVal"]
    N266["dictGetDoubleValPtr"]
    N267["dictGetFairRandomKey"]
    N268["dictGetHash"]
    N269["dictGetIterator"]
    N270["dictGetKey"]
    N271["dictGetNext"]
    N272["dictGetNextRef"]
    N273["dictGetRandomKey"]
    N274["dictGetSafeIterator"]
    N275["dictGetSignedIntegerVal"]
    N276["dictGetSomeKeys"]
    N277["dictGetStats"]
    N278["dictGetUnsignedIntegerVal"]
    N279["dictGetVal"]
    N280["dictIncrDoubleVal"]
    N281["dictIncrSignedIntegerVal"]
    N282["dictIncrUnsignedIntegerVal"]
    N283["dictInitIterator"]
    N284["dictInitSafeIterator"]
    N285["dictInsertAtPosition"]
    N286["dictMetadata"]
    N287["dictNext"]
    N288["dictRehash"]
    N289["dictRehashMilliseconds"]
    N290["dictRelease"]
    N291["dictReleaseIterator"]
    N292["dictReplace"]
    N293["dictResetIterator"]
    N294["dictResize"]
    N295["dictScan"]
    N296["dictScanDefrag"]
    N297["dictSetDoubleVal"]
    N298["dictSetKey"]
    N299["dictSetNext"]
    N300["dictSetSignedIntegerVal"]
    N301["dictSetUnsignedIntegerVal"]
    N302["dictSetVal"]
    N303["dictTryExpand"]
    N304["dictTwoPhaseUnlinkFind"]
    N305["dictTwoPhaseUnlinkFree"]
    N306["dictTypeExpandAllowed"]
    N307["dictUnlink"]
    N308["digits10"]
    N309["disableTracking"]
    N310["discardTempDb"]
    N311["discardTransaction"]
    N312["disconnectSlaves"]
    N313["doesCommandHaveKeys"]
    N314["dupClientReplyValue"]
    N315["dupStringObject"]
    N316["elapsedMs"]
    N317["elapsedStart"]
    N318["elapsedUs"]
    N319["emptyData"]
    N320["emptyDbAsync"]
    N321["emptyDbStructure"]
    N322["enableTracking"]
    N323["encodeMaskedPtr"]
    N324["entryHasValue"]
    N325["entryIsKey"]
    N326["entryIsNoValue"]
    N327["entryIsNormal"]
    N328["evalGetKeys"]
    N329["evictClients"]
    N330["existsCommand"]
    N331["expireIfNeeded"]
    N332["flushAllDataAndResetRDB"]
    N333["flushSlaveKeysWithExpireList"]
    N334["flushSlavesOutputBuffers"]
    N335["flushallCommand"]
    N336["flushdbCommand"]
    N337["forceCommandPropagation"]
    N338["formatAddr"]
    N339["freeClient"]
    N340["freeClientArgv"]
    N341["freeClientAsync"]
    N342["freeClientMultiState"]
    N343["freeClientOriginalArgv"]
    N344["freeClientReplyValue"]
    N345["freeClientsInAsyncFreeQueue"]
    N346["freeFunctionsAsync"]
    N347["freeLuaScriptsAsync"]
    N348["freeObjAsync"]
    N349["freeReplicaReferencedReplBuffer"]
    N350["freeReplicationBacklogRefMemAsync"]
    N351["freeTrackingRadixTree"]
    N352["freeTrackingRadixTreeAsync"]
    N353["functionGetKeys"]
    N354["functionsLibCtxClearCurrent"]
    N355["functionsLibCtxFree"]
    N356["functionsLibCtxfunctionsLen"]
    N357["genClientAddrString"]
    N358["genericGetKeys"]
    N359["genrand64_int64"]
    N360["georadiusGetKeys"]
    N361["getAllClientsInfoString"]
    N362["getAllKeySpecsFlags"]
    N363["getChannelsFromCommand"]
    N364["getClientEvictionLimit"]
    N365["getClientMemoryUsage"]
    N366["getClientOutputBufferMemoryUsage"]
    N367["getClientPeerId"]
    N368["getClientSockname"]
    N369["getClientType"]
    N370["getClientTypeByName"]
    N371["getClusterConnectionsCount"]
    N372["getCommand"]
    N373["getDecodedObject"]
    N374["getExpire"]
    N375["getExpireMillisecondsOrReply"]
    N376["getFlushCommandFlags"]
    N377["getGenericCommand"]
    N378["getIOPendingCount"]
    N379["getIntFromObjectOrReply"]
    N380["getKeysFreeResult"]
    N381["getKeysFromCommand"]
    N382["getKeysFromCommandWithSpecs"]
    N383["getKeysPrepareResult"]
    N384["getKeysUsingKeySpecs"]
    N385["getKeysUsingLegacyRangeSpec"]
    N386["getLongDoubleFromObjectOrReply"]
    N387["getLongFromObjectOrReply"]
    N388["getLongLongFromObjectOrReply"]
    N389["getObjectTypeByName"]
    N390["getObjectTypeName"]
    N391["getRangeLongFromObjectOrReply"]
    N392["getStringObjectLen"]
    N393["getStringObjectSdsUsedMemory"]
    N394["getTimeoutFromObjectOrReply"]
    N395["getdelCommand"]
    N396["getexCommand"]
    N397["getrangeCommand"]
    N398["getsetCommand"]
    N399["handleClientsWithPendingReadsUsingThreads"]
    N400["handleClientsWithPendingWrites"]
    N401["handleClientsWithPendingWritesUsingThreads"]
    N402["hasActiveChildProcess"]
    N403["hashTypeDup"]
    N404["helloCommand"]
    N405["incrCommand"]
    N406["incrDecrCommand"]
    N407["incrRefCount"]
    N408["incrbyCommand"]
    N409["incrbyfloatCommand"]
    N410["incrementErrorCount"]
    N411["incrementalTrimReplicationBacklog"]
    N412["initClientBlockingState"]
    N413["initClientMultiState"]
    N414["initObjectLRUOrLFU"]
    N415["initTempDb"]
    N416["initThreadedIO"]
    N417["installClientWriteHandler"]
    N418["intrev64"]
    N419["isInsideYieldingLongCommand"]
    N420["isPausedActionsWithUpdate"]
    N421["keyIsExpired"]
    N422["keysCommand"]
    N423["killIOThreads"]
    N424["killRDBChild"]
    N425["lastsaveCommand"]
    N426["latencyAddSample"]
    N427["lazyFreeFunctionsCtx"]
    N428["lazyFreeLuaScripts"]
    N429["lazyFreeReplicationBacklogRefMem"]
    N430["lazyFreeTrackingTable"]
    N431["lazyfreeFreeDatabase"]
    N432["lazyfreeFreeObject"]
    N433["lazyfreeGetFreeEffort"]
    N434["lcsCommand"]
    N435["ld2string"]
    N436["linkClient"]
    N437["listAddNodeHead"]
    N438["listAddNodeTail"]
    N439["listCreate"]
    N440["listDelNode"]
    N441["listDup"]
    N442["listEmpty"]
    N443["listGetIterator"]
    N444["listInitNode"]
    N445["listInsertNode"]
    N446["listJoin"]
    N447["listLinkNodeHead"]
    N448["listLinkNodeTail"]
    N449["listNext"]
    N450["listRelease"]
    N451["listReleaseIterator"]
    N452["listRewind"]
    N453["listSearchKey"]
    N454["listTypeDup"]
    N455["listUnlinkNode"]
    N456["ll2string"]
    N457["lmpopGetKeys"]
    N458["logInvalidUseAndFreeClientAsync"]
    N459["lookupClientByID"]
    N460["lookupCommandOrOriginal"]
    N461["lookupKey"]
    N462["lookupKeyRead"]
    N463["lookupKeyReadOrReply"]
    N464["lookupKeyReadWithFlags"]
    N465["lookupKeyWrite"]
    N466["lookupKeyWriteOrReply"]
    N467["lookupKeyWriteWithFlags"]
    N468["lpFirst"]
    N469["lpGet"]
    N470["lpNext"]
    N471["makeThreadKillable"]
    N472["mgetCommand"]
    N473["migrateGetKeys"]
    N474["moduleBlockedClientMayTimeout"]
    N475["moduleFireServerEvent"]
    N476["moduleGetCommandChannelsViaAPI"]
    N477["moduleGetCommandKeysViaAPI"]
    N478["moduleGetFreeEffort"]
    N479["moduleNotifyKeyUnlink"]
    N480["moduleNotifyUserChanged"]
    N481["moduleTypeDupOrReply"]
    N482["moduleTypeLookupModuleByNameIgnoreCase"]
    N483["monotonicInit"]
    N484["moveCommand"]
    N485["msetCommand"]
    N486["msetGenericCommand"]
    N487["msetnxCommand"]
    N488["mstime"]
    N489["multiStateMemOverhead"]
    N490["mustObeyClient"]
    N491["notifyKeyspaceEvent"]
    N492["objectTypeCompare"]
    N493["parseExtendedStringArgumentsOrReply"]
    N494["parseScanCursorOrReply"]
    N495["pauseActions"]
    N496["pauseClientsByClient"]
    N497["postponeClientRead"]
    N498["prepareClientToWrite"]
    N499["prepareForShutdown"]
    N500["processCommand"]
    N501["processCommandAndResetClient"]
    N502["processEventsWhileBlocked"]
    N503["processInlineBuffer"]
    N504["processInputBuffer"]
    N505["processMultibulkBuffer"]
    N506["processPendingCommandAndInputBuffer"]
    N507["processTimeEvents"]
    N508["propagateDeletion"]
    N509["protectClient"]
    N510["psetexCommand"]
    N511["pubsubMemOverhead"]
    N512["pubsubUnsubscribeAllChannels"]
    N513["pubsubUnsubscribeAllPatterns"]
    N514["pubsubUnsubscribeShardAllChannels"]
    N515["putClientInPendingWriteQueue"]
    N516["quitCommand"]
    N517["randomkeyCommand"]
    N518["raxFind"]
    N519["raxFree"]
    N520["raxInsert"]
    N521["raxNext"]
    N522["raxRemove"]
    N523["raxSeek"]
    N524["raxSize"]
    N525["raxStart"]
    N526["raxStop"]
    N527["rdbPipeWriteHandlerConnRemoved"]
    N528["rdbPopulateSaveInfo"]
    N529["rdbSave"]
    N530["readQueryFromClient"]
    N531["reclaimFilePageCache"]
    N532["redactClientCommandArgument"]
    N533["redisSetCpuAffinity"]
    N534["refreshGoodSlavesCount"]
    N535["rememberSlaveKeyWithExpire"]
    N536["removeClientFromMemUsageBucket"]
    N537["removeExpire"]
    N538["renameCommand"]
    N539["renameGenericCommand"]
    N540["renamenxCommand"]
    N541["replaceClientCommandVector"]
    N542["replicationCacheMaster"]
    N543["replicationFeedStreamFromMasterStream"]
    N544["replicationGetSlaveName"]
    N545["replicationHandleMasterDisconnection"]
    N546["reqresAppendResponse"]
    N547["reqresSaveClientReplyOffset"]
    N548["resetClient"]
    N549["resetCommand"]
    N550["retainOriginalCommandVector"]
    N551["rev"]
    N552["rewriteClientCommandArgument"]
    N553["rewriteClientCommandVector"]
    N554["rioFlush"]
    N555["rioRead"]
    N556["rioTell"]
    N557["rioWrite"]
    N558["scanCallback"]
    N559["scanCommand"]
    N560["scanDatabaseForDeletedKeys"]
    N561["scanDatabaseForReadyKeys"]
    N562["scanGenericCommand"]
    N563["scriptIsEval"]
    N564["sdsAllocPtr"]
    N565["sdsIncrLen"]
    N566["sdsMakeRoomFor"]
    N567["sdsMakeRoomForNonGreedy"]
    N568["sdsZmallocSize"]
    N569["sdsalloc"]
    N570["sdsavail"]
    N571["sdscatfmt"]
    N572["sdscatlen"]
    N573["sdscatprintf"]
    N574["sdscatrepr"]
    N575["sdscatvprintf"]
    N576["sdsclear"]
    N577["sdscmp"]
    N578["sdsdup"]
    N579["sdsempty"]
    N580["sdsfree"]
    N581["sdsfreesplitres"]
    N582["sdsgrowzero"]
    N583["sdslen"]
    N584["sdsmapchars"]
    N585["sdsnew"]
    N586["sdsnewlen"]
    N587["sdsrange"]
    N588["sdssplitargs"]
    N589["sdstoupper"]
    N590["sdstrim"]
    N591["securityWarningCommand"]
    N592["selectCommand"]
    N593["selectDb"]
    N594["sendReplyToClient"]
    N595["setCommand"]
    N596["setDeferredAggregateLen"]
    N597["setDeferredArrayLen"]
    N598["setDeferredAttributeLen"]
    N599["setDeferredMapLen"]
    N600["setDeferredPushLen"]
    N601["setDeferredReply"]
    N602["setDeferredReplyBulkSds"]
    N603["setDeferredSetLen"]
    N604["setExpire"]
    N605["setGenericCommand"]
    N606["setGetKeys"]
    N607["setIOPendingCount"]
    N608["setKey"]
    N609["setProtocolError"]
    N610["setTypeDup"]
    N611["setTypeInitIterator"]
    N612["setTypeNext"]
    N613["setTypeReleaseIterator"]
    N614["setexCommand"]
    N615["setnxCommand"]
    N616["setrangeCommand"]
    N617["showLatestBacklog"]
    N618["shutdownCommand"]
    N619["signalDeletedKeyAsReady"]
    N620["signalFlushedDb"]
    N621["signalKeyAsReady"]
    N622["signalModifiedKey"]
    N623["sintercardGetKeys"]
    N624["siphash"]
    N625["siphash_nocase"]
    N626["slotToKeyAddEntry"]
    N627["slotToKeyDelEntry"]
    N628["slotToKeyDestroy"]
    N629["slotToKeyFlush"]
    N630["slotToKeyInit"]
    N631["sortGetKeys"]
    N632["sortROGetKeys"]
    N633["startThreadedIO"]
    N634["stopThreadedIO"]
    N635["stopThreadedIOIfNeeded"]
    N636["streamDup"]
    N637["string2ll"]
    N638["stringObjectLen"]
    N639["stringmatchlen"]
    N640["strlenCommand"]
    N641["swapMainDbWithTempDb"]
    N642["swapdbCommand"]
    N643["timeInMilliseconds"]
    N644["touchAllWatchedKeysInDb"]
    N645["touchWatchedKey"]
    N646["trackingInvalidateKey"]
    N647["trackingInvalidateKeysOnFlush"]
    N648["trimReplyUnusedTailSpace"]
    N649["tryObjectEncoding"]
    N650["typeCommand"]
    N651["unblockClient"]
    N652["unblockClientOnError"]
    N653["unblockClientOnTimeout"]
    N654["unblockPostponedClients"]
    N655["unlinkClient"]
    N656["unlinkCommand"]
    N657["unpauseActions"]
    N658["unprotectClient"]
    N659["unwatchAllKeys"]
    N660["updateCachedTime"]
    N661["updateClientMemUsageAndBucket"]
    N662["updateLFU"]
    N663["updatePausedActions"]
    N664["usUntilEarliestTimer"]
    N665["validateClientAttr"]
    N666["validateClientName"]
    N667["whileBlockedCron"]
    N668["writeToClient"]
    N669["xreadGetKeys"]
    N670["zcalloc"]
    N671["zfree"]
    N672["zmalloc"]
    N673["zmalloc_usable"]
    N674["zmalloc_used_memory"]
    N675["zmpopGetKeys"]
    N676["zrealloc"]
    N677["zrealloc_usable"]
    N678["zsetDup"]
    N679["ztrycalloc"]
    N680["ztrymalloc"]
    N681["zunionInterDiffGetKeys"]
    N682["zunionInterDiffStoreGetKeys"]
  end
  N330 --> N464
  N668 --> N341
  N145 --> N165
  N168 --> N583
  N174 --> N341
  N339 --> N369
  N530 --> N504
  N331 --> N421
  N329 --> N75
  N310 --> N628
  N505 --> N609
  N434 --> N586
  N168 --> N160
  N561 --> N279
  N662 --> N60
  N141 --> N439
  N332 --> N528
  N111 --> N116
  N441 --> N450
  N530 --> N579
  N382 --> N477
  N139 -. fd_ready .-> N36
  N266 --> N73
  N562 --> N387
  N65 --> N671
  N401 --> N455
  N616 --> N218
  N404 --> N99
  N288 --> N217
  N274 --> N269
  N136 --> N127
  N434 --> N110
  N141 --> N75
  N397 --> N388
  N406 --> N223
  N171 --> N241
  N251 --> N323
  N105 --> N141
  N486 --> N608
  N436 --> N438
  N383 --> N672
  N642 --> N82
  N485 --> N486
  N361 --> N572
  N167 --> N367
  N668 --> N341
  N154 --> N75
  N436 --> N418
  N94 --> N498
  N505 --> N583
  N216 --> N673
  N206 -. fd_ready .-> N22
  N562 --> N639
  N562 --> N639
  N227 --> N414
  N214 --> N403
  N305 --> N325
  N443 --> N672
  N433 --> N524
  N101 --> N575
  N166 --> N170
  N329 --> N452
  N560 --> N279
  N609 --> N583
  N530 --> N583
  N618 --> N419
  N64 --> N369
  N505 --> N609
  N396 --> N622
  N365 --> N511
  N429 --> N519
  N251 --> N325
  N404 --> N110
  N505 --> N583
  N596 --> N601
  N293 --> N73
  N631 --> N383
  N422 --> N583
  N618 --> N96
  N404 --> N90
  N250 --> N69
  N503 --> N583
  N399 --> N449
  N484 --> N491
  N609 --> N75
  N137 --> N129
  N124 --> N116
  N440 --> N455
  N384 --> N73
  N464 --> N73
  N80 --> N75
  N57 --> N607
  N103 --> N141
  N215 --> N73
  N242 --> N388
  N86 --> N116
  N154 --> N440
  N78 --> N452
  N561 --> N274
  N331 --> N220
  N288 --> N325
  N361 --> N586
  N259 --> N271
  N101 --> N590
  N209 -. fd_ready .-> N25
  N168 --> N525
  N395 --> N235
  N484 --> N593
  N168 --> N449
  N339 --> N75
  N57 --> N449
  N121 --> N579
  N530 --> N201
  N616 --> N164
  N56 --> N580
  N227 --> N626
  N484 --> N593
  N168 --> N671
  N457 --> N358
  N605 --> N491
  N434 --> N96
  N553 --> N541
  N233 --> N257
  N503 --> N218
  N275 --> N324
  N365 --> N489
  N508 --> N241
  N539 --> N622
  N324 --> N327
  N404 --> N96
  N141 --> N617
  N169 --> N73
  N268 -. fd_ready .-> N44
  N484 --> N374
  N434 --> N96
  N339 --> N369
  N242 --> N406
  N168 --> N112
  N245 --> N622
  N505 --> N609
  N616 --> N96
  N640 --> N110
  N472 --> N113
  N540 --> N539
  N602 --> N583
  N141 --> N369
  N530 --> N569
  N458 --> N75
  N171 --> N666
  N80 --> N75
  N562 --> N438
  N562 --> N439
  N214 --> N604
  N331 --> N246
  N246 --> N426
  N168 --> N90
  N168 --> N110
  N641 --> N560
  N450 --> N442
  N377 --> N463
  N145 --> N491
  N415 --> N250
  N609 --> N579
  N655 --> N418
  N384 --> N583
  N415 --> N670
  N401 --> N417
  N591 --> N180
  N173 --> N241
  N464 --> N461
  N503 --> N671
  N156 --> N383
  N423 --> N75
  N67 --> N306
  N655 --> N440
  N64 --> N62
  N285 --> N73
  N601 --> N73
  N404 --> N112
  N530 --> N147
  N292 -. fd_ready .-> N48
  N509 --> N203
  N438 --> N448
  N594 --> N192
  N117 --> N74
  N246 --> N491
  N258 --> N271
  N433 --> N523
  N141 --> N438
  N422 --> N287
  N91 --> N638
  N261 --> N671
  N562 --> N586
  N434 --> N110
  N616 --> N491
  N339 --> N453
  N440 --> N671
  N614 --> N649
  N537 --> N252
  N264 --> N271
  N396 --> N222
  N432 --> N241
  N530 --> N341
  N484 --> N82
  N404 --> N96
  N508 --> N142
  N288 --> N671
  N118 --> N583
  N171 --> N407
  N62 --> N673
  N331 --> N420
  N56 --> N579
  N503 --> N609
  N463 --> N462
  N377 --> N165
  N618 --> N103
  N608 --> N465
  N154 --> N533
  N562 --> N456
  N233 -. fd_ready .-> N48
  N404 --> N90
  N95 --> N224
  N347 --> N290
  N434 --> N597
  N236 --> N241
  N216 --> N250
  N239 --> N73
  N93 --> N583
  N305 -. fd_ready .-> N48
  N88 --> N91
  N352 --> N151
  N168 --> N388
  N505 --> N609
  N310 --> N290
  N396 --> N553
  N486 --> N465
  N658 --> N515
  N434 --> N583
  N214 --> N96
  N339 --> N475
  N668 --> N204
  N641 --> N561
  N264 --> N271
  N273 --> N359
  N339 --> N580
  N234 --> N561
  N345 --> N452
  N80 --> N188
  N406 --> N225
  N453 --> N449
  N78 --> N212
  N562 --> N583
  N616 --> N583
  N107 --> N121
  N406 --> N165
  N214 --> N636
  N640 --> N463
  N433 --> N478
  N254 --> N73
  N558 --> N586
  N186 -. fd_ready .-> N12
  N122 --> N116
  N126 --> N672
  N335 --> N337
  N160 --> N367
  N135 --> N671
  N168 --> N583
  N404 --> N90
  N669 --> N383
  N313 --> N362
  N398 --> N649
  N451 --> N671
  N168 --> N96
  N339 --> N534
  N168 --> N523
  N642 --> N96
  N561 --> N287
  N57 --> N73
  N168 --> N452
  N401 --> N635
  N602 --> N580
  N296 --> N271
  N345 --> N449
  N350 --> N450
  N168 --> N113
  N230 --> N619
  N532 --> N241
  N339 --> N343
  N404 --> N90
  N154 --> N75
  N398 --> N377
  N276 --> N359
  N90 --> N113
  N110 --> N111
  N216 --> N672
  N80 --> N75
  N214 --> N96
  N231 --> N270
  N230 --> N279
  N505 --> N576
  N168 --> N671
  N253 --> N65
  N80 --> N178
  N389 --> N482
  N339 --> N450
  N605 --> N608
  N375 --> N98
  N642 --> N234
  N530 --> N574
  N216 --> N187
  N539 --> N577
  N207 -. fd_ready .-> N23
  N132 --> N483
  N168 --> N521
  N102 --> N116
  N561 --> N270
  N230 --> N479
  N560 --> N619
  N380 --> N671
  N214 --> N96
  N251 --> N272
  N306 --> N70
  N404 --> N388
  N256 --> N257
  N473 --> N583
  N168 --> N96
  N332 --> N319
  N434 --> N96
  N530 --> N341
  N504 --> N661
  N132 --> N671
  N505 --> N587
  N250 --> N672
  N296 -. fd_ready .-> N4
  N555 -. fd_ready .-> N31
  N662 --> N59
  N65 --> N239
  N539 --> N229
  N107 --> N120
  N399 --> N169
  N234 --> N560
  N108 --> N241
  N516 --> N82
  N140 --> N676
  N305 --> N239
  N510 --> N649
  N141 --> N76
  N461 --> N257
  N289 --> N643
  N439 --> N672
  N503 --> N609
  N608 --> N233
  N214 --> N103
  N381 --> N385
  N118 --> N580
  N562 --> N583
  N505 --> N220
  N168 --> N580
  N296 --> N271
  N642 --> N475
  N616 --> N622
  N367 --> N357
  N111 --> N116
  N397 --> N165
  N243 --> N583
  N682 --> N358
  N301 --> N324
  N331 --> N241
  N179 -. fd_ready .-> N7
  N167 --> N341
  N168 --> N572
  N400 --> N452
  N57 --> N668
  N347 --> N151
  N434 --> N462
  N434 --> N462
  N384 --> N76
  N397 --> N82
  N176 --> N546
  N288 --> N73
  N458 --> N341
  N92 --> N456
  N539 --> N374
  N392 --> N583
  N562 --> N331
  N562 --> N389
  N600 --> N596
  N406 --> N622
  N259 -. fd_ready .-> N44
  N124 --> N116
  N225 --> N226
  N312 --> N449
  N558 --> N279
  N108 --> N116
  N504 --> N548
  N160 --> N196
  N409 --> N225
  N655 --> N440
  N655 --> N73
  N434 --> N94
  N97 --> N99
  N397 --> N463
  N264 -. fd_ready .-> N44
  N277 --> N68
  N401 --> N661
  N111 --> N116
  N168 --> N82
  N214 --> N103
  N211 -. fd_ready .-> N26
  N115 --> N583
  N396 --> N375
  N348 --> N241
  N458 --> N579
  N484 --> N379
  N508 --> N407
  N556 -. fd_ready .-> N30
  N261 -. fd_ready .-> N48
  N422 --> N639
  N642 --> N379
  N350 --> N524
  N168 --> N96
  N339 --> N580
  N282 --> N324
  N316 --> N318
  N185 -. fd_ready .-> N11
  N558 --> N76
  N503 --> N671
  N396 --> N161
  N484 --> N491
  N78 --> N449
  N56 --> N75
  N114 --> N116
  N339 --> N342
  N82 --> N64
  N216 --> N444
  N562 --> N103
  N160 --> N189
  N345 --> N339
  N505 --> N74
  N246 --> N488
  N168 --> N103
  N363 --> N476
  N505 --> N96
  N396 --> N463
  N434 --> N84
  N154 -. fd_ready .-> N39
  N288 --> N326
  N226 --> N233
  N285 --> N254
  N472 --> N462
  N296 --> N551
  N107 --> N597
  N132 --> N672
  N174 --> N579
  N453 -. fd_ready .-> N52
  N409 --> N386
  N415 --> N250
  N423 --> N75
  N562 --> N583
  N339 --> N655
  N265 --> N73
  N204 -. fd_ready .-> N21
  N335 --> N332
  N339 --> N512
  N484 --> N622
  N635 --> N634
  N530 --> N192
  N78 --> N452
  N396 --> N73
  N634 --> N399
  N261 --> N270
  N339 --> N475
  N320 --> N151
  N615 --> N605
  N562 --> N84
  N83 --> N111
  N618 --> N158
  N401 --> N369
  N168 --> N99
  N251 -. fd_ready .-> N1
  N168 --> N388
  N401 --> N449
  N91 --> N111
  N230 --> N302
  N251 --> N73
  N135 --> N671
  N144 --> N449
  N57 --> N452
  N80 --> N190
  N281 --> N73
  N365 --> N366
  N486 --> N97
  N126 --> N672
  N288 -. fd_ready .-> N44
  N262 --> N625
  N508 --> N407
  N422 --> N291
  N319 --> N475
  N278 --> N324
  N655 --> N522
  N329 --> N449
  N304 --> N270
  N105 --> N102
  N505 --> N637
  N560 --> N274
  N245 --> N235
  N167 --> N211
  N622 --> N646
  N174 --> N75
  N126 --> N143
  N168 --> N82
  N357 --> N188
  N160 --> N195
  N618 --> N79
  N89 --> N116
  N668 --> N190
  N503 --> N75
  N422 --> N583
  N562 --> N103
  N154 --> N73
  N602 --> N601
  N272 --> N238
  N398 --> N491
  N235 --> N230
  N346 --> N151
  N339 --> N450
  N604 --> N248
  N341 --> N438
  N77 --> N73
  N80 --> N188
  N396 --> N491
  N399 --> N378
  N503 --> N580
  N404 --> N90
  N168 --> N82
  N69 --> N72
  N124 --> N89
  N404 --> N90
  N66 --> N679
  N111 --> N116
  N366 --> N369
  N604 --> N74
  N554 -. fd_ready .-> N28
  N98 --> N99
  N530 --> N497
  N623 --> N358
  N250 -. fd_ready .-> N42
  N168 --> N82
  N409 --> N465
  N557 -. fd_ready .-> N31
  N618 --> N499
  N405 --> N406
  N562 --> N492
  N510 --> N605
  N201 -. fd_ready .-> N19
  N396 --> N537
  N251 -. fd_ready .-> N2
  N552 --> N460
  N153 --> N75
  N86 --> N116
  N145 --> N583
  N319 --> N629
  N162 --> N369
  N287 --> N271
  N655 --> N309
  N216 --> N202
  N171 --> N583
  N267 --> N273
  N668 --> N169
  N396 --> N230
  N434 --> N110
  N396 --> N491
  N132 --> N671
  N148 --> N155
  N420 --> N663
  N505 --> N583
  N288 --> N239
  N517 --> N231
  N462 --> N464
  N434 --> N103
  N139 -. fd_ready .-> N33
  N296 --> N251
  N121 --> N122
  N484 --> N103
  N558 --> N435
  N608 --> N407
  N339 --> N544
  N396 --> N241
  N181 --> N179
  N65 --> N271
  N600 --> N73
  N453 --> N452
  N562 --> N76
  N253 --> N65
  N641 --> N333
  N550 --> N407
  N65 --> N325
  N319 --> N620
  N65 --> N270
  N94 --> N438
  N250 --> N286
  N216 --> N412
  N168 --> N671
  N65 --> N279
  N434 --> N93
  N616 --> N164
  N552 --> N74
  N505 --> N586
  N173 --> N665
  N336 --> N376
  N427 --> N356
  N361 --> N576
  N339 --> N450
  N530 --> N193
  N101 --> N141
  N396 --> N493
  N339 --> N290
  N214 --> N82
  N236 --> N219
  N321 --> N320
  N650 --> N120
  N608 --> N225
  N505 --> N672
  N103 --> N82
  N214 --> N678
  N350 --> N151
  N297 --> N73
  N147 --> N339
  N341 --> N438
  N119 --> N83
  N616 --> N583
  N406 --> N232
  N214 --> N379
  N400 --> N668
  N168 --> N367
  N270 --> N326
  N381 -. fd_ready .-> N53
  N95 --> N224
  N65 -. fd_ready .-> N46
  N168 --> N496
  N290 --> N65
  N86 --> N116
  N295 --> N296
  N296 --> N271
  N503 --> N672
  N271 --> N238
  N484 --> N407
  N173 --> N583
  N151 --> N672
  N503 --> N369
  N226 --> N249
  N539 --> N82
  N168 --> N84
  N234 --> N644
  N168 --> N88
  N506 --> N583
  N530 --> N583
  N168 --> N671
  N539 --> N604
  N642 --> N96
  N292 --> N279
  N96 --> N102
  N292 --> N302
  N318 -. fd_ready .-> N5
  N168 --> N82
  N276 --> N359
  N618 --> N96
  N553 --> N407
  N558 --> N438
  N505 --> N583
  N562 --> N438
  N335 --> N376
  N287 --> N260
  N285 --> N73
  N507 -. fd_ready .-> N37
  N67 --> N255
  N160 --> N368
  N173 --> N407
  N280 --> N73
  N539 --> N466
  N592 --> N96
  N105 --> N583
  N532 --> N550
  N404 --> N90
  N64 --> N458
  N340 --> N241
  N559 --> N494
  N459 --> N518
  N505 --> N567
  N557 -. fd_ready .-> N32
  N409 --> N552
  N562 --> N73
  N404 --> N90
  N80 --> N216
  N154 --> N671
  N634 --> N73
  N65 --> N72
  N530 --> N583
  N404 --> N532
  N64 --> N547
  N310 --> N671
  N399 --> N661
  N616 --> N638
  N384 --> N73
  N80 --> N183
  N166 --> N513
  N77 --> N211
  N339 --> N513
  N422 --> N583
  N214 --> N374
  N336 --> N82
  N107 --> N589
  N498 --> N169
  N562 --> N440
  N445 --> N672
  N484 --> N622
  N541 --> N392
  N120 --> N122
  N486 --> N491
  N93 --> N111
  N257 --> N271
  N301 --> N73
  N168 --> N536
  N80 --> N193
  N655 --> N183
  N459 --> N418
  N290 --> N65
  N232 --> N233
  N174 --> N339
  N399 --> N515
  N94 --> N458
  N65 -. fd_ready .-> N48
  N381 --> N477
  N299 --> N238
  N168 --> N123
  N434 --> N373
  N168 --> N369
  N396 --> N553
  N486 --> N82
  N86 --> N89
  N288 --> N299
  N312 --> N339
  N246 --> N622
  N236 --> N583
  N257 -. fd_ready .-> N45
  N473 --> N383
  N434 --> N110
  N246 --> N230
  N139 -. fd_ready .-> N35
  N668 --> N661
  N562 --> N469
  N145 --> N638
  N118 --> N498
  N655 --> N440
  N190 -. fd_ready .-> N14
  N404 --> N241
  N466 --> N115
  N601 --> N440
  N562 --> N470
  N80 --> N193
  N132 --> N126
  N113 --> N116
  N668 --> N193
  N87 --> N116
  N361 --> N160
  N339 --> N671
  N397 --> N388
  N152 --> N439
  N57 --> N442
  N392 --> N74
  N530 --> N567
  N552 --> N392
  N539 --> N407
  N291 --> N293
  N107 --> N585
  N275 --> N73
  N339 --> N580
  N168 --> N90
  N605 --> N82
  N441 --> N439
  N111 --> N456
  N168 --> N676
  N251 --> N327
  N168 --> N94
  N560 --> N291
  N461 --> N61
  N560 --> N257
  N230 --> N407
  N329 --> N339
  N382 --> N384
  N562 --> N586
  N339 --> N290
  N339 --> N73
  N269 --> N672
  N84 --> N83
  N339 --> N440
  N334 --> N196
  N484 --> N229
  N226 --> N414
  N393 --> N74
  N154 --> N531
  N66 --> N70
  N328 --> N358
  N249 --> N259
  N214 --> N491
  N166 --> N593
  N343 --> N241
  N505 --> N146
  N505 --> N676
  N484 --> N225
  N57 --> N76
  N168 --> N82
  N233 --> N407
  N251 --> N73
  N441 --> N450
  N101 --> N584
  N329 --> N579
  N430 --> N351
  N57 --> N533
  N434 --> N583
  N169 --> N369
  N299 --> N73
  N399 --> N442
  N233 --> N619
  N106 --> N105
  N422 --> N274
  N168 --> N82
  N191 -. fd_ready .-> N15
  N434 --> N373
  N168 --> N110
  N507 --> N671
  N620 --> N560
  N118 --> N580
  N245 --> N331
  N609 --> N160
  N168 --> N96
  N562 --> N469
  N504 --> N505
  N401 --> N378
  N601 --> N174
  N229 --> N230
  N259 --> N270
  N113 --> N116
  N329 --> N580
  N310 --> N321
  N504 --> N503
  N602 --> N580
  N288 --> N299
  N290 --> N671
  N85 --> N83
  N64 --> N175
  N463 --> N115
  N168 --> N82
  N436 --> N520
  N505 --> N609
  N134 -. fd_ready .-> N5
  N216 --> N579
  N441 --> N452
  N505 --> N583
  N288 --> N671
  N384 --> N383
  N484 --> N82
  N216 --> N439
  N562 --> N470
  N530 --> N580
  N168 --> N474
  N616 --> N582
  N461 --> N279
  N230 --> N348
  N472 --> N84
  N264 -. fd_ready .-> N45
  N397 --> N456
  N299 --> N326
  N159 --> N358
  N168 --> N103
  N346 --> N356
  N592 --> N96
  N168 --> N370
  N168 --> N391
  N80 --> N190
  N271 --> N326
  N168 --> N172
  N168 --> N661
  N339 --> N241
  N562 --> N89
  N65 --> N671
  N339 --> N73
  N168 --> N322
  N399 --> N449
  N145 --> N583
  N350 --> N519
  N135 --> N128
  N334 --> N452
  N416 --> N439
  N562 --> N611
  N334 --> N668
  N306 -. fd_ready .-> N43
  N226 --> N578
  N618 --> N103
  N108 --> N88
  N145 --> N236
  N502 --> N667
  N200 -. fd_ready .-> N18
  N562 --> N470
  N361 --> N369
  N595 --> N605
  N605 --> N541
  N160 --> N365
  N385 --> N383
  N226 --> N298
  N304 --> N272
  N505 --> N583
  N339 --> N580
  N494 --> N96
  N504 --> N587
  N56 --> N116
  N655 --> N73
  N393 --> N568
  N461 --> N491
  N504 --> N501
  N95 --> N116
  N434 --> N671
  N145 --> N638
  N168 --> N96
  N632 --> N383
  N339 --> N424
  N168 --> N368
  N139 --> N664
  N176 --> N583
  N257 -. fd_ready .-> N44
  N434 --> N680
  N168 --> N82
  N154 --> N76
  N236 --> N73
  N404 --> N666
  N269 --> N283
  N257 --> N71
  N384 --> N73
  N504 --> N419
  N145 --> N407
  N681 --> N358
  N83 --> N73
  N214 --> N462
  N214 --> N229
  N168 --> N459
  N105 --> N580
  N401 --> N438
  N166 --> N309
  N145 --> N110
  N558 --> N578
  N552 --> N392
  N422 --> N94
  N272 --> N326
  N77 --> N211
  N168 --> N526
  N133 --> N125
  N168 --> N90
  N168 --> N107
  N401 --> N452
  N180 --> N179
  N434 --> N110
  N166 --> N453
  N82 --> N76
  N399 --> N452
  N168 --> N90
  N401 --> N455
  N228 --> N230
  N641 --> N644
  N530 --> N341
  N320 --> N250
  N230 --> N627
  N118 --> N64
  N555 -. fd_ready .-> N29
  N151 --> N155
  N399 --> N607
  N541 --> N460
  N332 --> N529
  N339 --> N290
  N234 --> N561
  N264 --> N271
  N503 --> N583
  N57 --> N378
  N233 --> N241
  N648 --> N677
  N392 --> N583
  N245 --> N110
  N505 --> N146
  N398 --> N552
  N437 --> N672
  N501 --> N500
  N80 --> N367
  N558 --> N279
  N99 --> N101
  N80 --> N190
  N615 --> N649
  N264 --> N261
  N367 --> N585
  N108 --> N221
  N467 --> N461
  N168 --> N55
  N383 --> N73
  N166 --> N512
  N122 --> N116
  N504 --> N73
  N530 --> N579
  N598 --> N73
  N429 --> N450
  N550 --> N672
  N303 --> N66
  N376 --> N103
  N348 --> N151
  N148 --> N672
  N154 --> N75
  N530 --> N75
  N160 --> N583
  N214 --> N454
  N549 --> N96
  N168 --> N124
  N422 --> N270
  N168 --> N96
  N618 --> N82
  N300 --> N73
  N168 --> N103
  N404 --> N532
  N505 --> N583
  N507 -. fd_ready .-> N5
  N168 --> N124
  N395 --> N377
  N541 --> N550
  N484 --> N96
  N434 --> N110
  N251 --> N270
  N654 --> N651
  N505 --> N671
  N168 --> N82
  N663 --> N654
  N343 --> N671
  N251 --> N238
  N296 --> N551
  N273 --> N359
  N226 --> N626
  N675 --> N358
  N285 --> N217
  N123 --> N99
  N168 --> N583
  N396 --> N604
  N530 --> N160
  N552 --> N550
  N305 -. fd_ready .-> N46
  N655 --> N527
  N409 --> N232
  N131 --> N676
  N548 --> N450
  N299 --> N325
  N278 --> N73
  N382 --> N362
  N401 --> N169
  N409 --> N96
  N374 --> N257
  N618 --> N99
  N530 --> N570
  N507 -. fd_ready .-> N5
  N668 --> N369
  N261 -. fd_ready .-> N46
  N214 --> N610
  N530 --> N580
  N656 --> N245
  N168 --> N671
  N168 --> N657
  N399 --> N73
  N216 --> N439
  N377 --> N88
  N541 --> N74
  N300 --> N324
  N288 --> N325
  N304 --> N71
  N77 --> N78
  N141 --> N586
  N541 --> N340
  N517 --> N241
  N134 --> N672
  N657 --> N663
  N530 --> N580
  N561 --> N291
  N339 --> N659
  N434 --> N90
  N304 -. fd_ready .-> N45
  N358 --> N383
  N331 --> N583
  N437 --> N447
  N305 --> N671
  N168 --> N90
  N592 --> N379
  N121 --> N583
  N461 --> N402
  N332 --> N424
  N145 --> N649
  N616 --> N583
  N168 --> N579
  N128 --> N671
  N505 --> N74
  N592 --> N82
  N154 --> N75
  N108 --> N435
  N292 --> N249
  N503 --> N96
  N92 --> N89
  N251 -. fd_ready .-> N3
  N77 --> N369
  N281 --> N324
  N168 --> N361
  N396 --> N491
  N658 --> N203
  N604 --> N535
  N168 --> N96
  N616 --> N583
  N230 --> N241
  N502 --> N139
  N616 --> N236
  N368 --> N357
  N132 --> N671
  N604 --> N270
  N56 --> N498
  N168 --> N103
  N382 --> N362
  N339 --> N545
  N261 --> N279
  N168 --> N103
  N64 --> N62
  N616 --> N110
  N530 --> N75
  N174 --> N75
  N562 --> N440
  N285 --> N672
  N382 -. fd_ready .-> N53
  N270 --> N325
  N396 --> N622
  N372 --> N377
  N503 --> N96
  N395 --> N553
  N139 -. fd_ready .-> N34
  N80 --> N371
  N605 --> N465
  N591 --> N341
  N226 --> N302
  N266 --> N324
  N421 --> N374
  N666 --> N583
  N427 --> N355
  N505 --> N99
  N276 --> N359
  N517 --> N88
  N107 --> N120
  N166 --> N311
  N539 --> N465
  N173 --> N82
  N168 --> N671
  N162 --> N366
  N248 --> N249
  N168 --> N82
  N502 --> N73
  N434 --> N96
  N214 --> N593
  N183 -. fd_ready .-> N9
  N168 --> N603
  N640 --> N165
  N168 --> N671
  N539 --> N82
  N216 --> N593
  N279 --> N324
  N145 --> N465
  N484 --> N465
  N319 --> N73
  N562 --> N450
  N259 -. fd_ready .-> N45
  N618 --> N103
  N339 --> N290
  N458 --> N160
  N433 --> N524
  N602 --> N579
  N288 --> N73
  N504 --> N76
  N168 --> N96
  N233 --> N279
  N111 --> N116
  N501 --> N661
  N433 --> N73
  N668 --> N73
  N95 --> N308
  N214 --> N481
  N422 --> N421
  N184 -. fd_ready .-> N13
  N329 --> N364
  N296 --> N251
  N614 --> N605
  N78 --> N440
  N95 --> N73
  N561 --> N621
  N197 -. fd_ready .-> N17
  N188 --> N179
  N409 --> N88
  N231 --> N267
  N662 --> N58
  N404 --> N171
  N400 --> N449
  N429 --> N524
  N89 --> N111
  N434 --> N241
  N340 --> N671
  N245 --> N491
  N258 --> N270
  N267 --> N276
  N273 --> N271
  N433 --> N525
  N141 --> N410
  N77 --> N73
  N57 --> N378
  N606 --> N383
  N145 --> N225
  N503 --> N581
  N174 --> N73
  N210 -. fd_ready .-> N10
  N616 --> N110
  N396 --> N622
  N434 --> N241
  N168 --> N580
  N168 --> N524
  N319 --> N354
  N602 --> N573
  N568 --> N564
  N182 -. fd_ready .-> N8
  N530 --> N566
  N505 --> N583
  N226 --> N491
  N668 --> N169
  N591 --> N75
  N339 --> N440
  N594 --> N668
  N406 --> N388
  N385 --> N76
  N157 --> N358
  N562 --> N92
  N302 --> N324
  N123 --> N580
  N80 --> N192
  N273 --> N271
  N56 --> N174
  N365 --> N568
  N361 --> N452
  N560 --> N287
  N319 --> N321
  N428 --> N290
  N168 --> N96
  N289 --> N643
  N167 --> N192
  N339 --> N349
  N497 --> N437
  N168 --> N459
  N406 --> N491
  N336 --> N337
  N214 --> N465
  N251 -. fd_ready .-> N40
  N509 --> N204
  N320 --> N250
  N666 --> N665
  N395 --> N622
  N168 --> N370
  N89 --> N116
  N168 --> N671
  N78 --> N449
  N214 --> N225
  N329 --> N75
  N167 --> N341
  N296 --> N551
  N305 --> N270
  N279 --> N73
  N505 --> N565
  N166 --> N73
  N194 -. fd_ready .-> N16
  N296 -. fd_ready .-> N4
  N506 --> N501
  N276 --> N271
  N154 --> N471
  N243 --> N141
  N233 --> N279
  N166 --> N73
  N216 --> N199
  N404 --> N90
  N254 --> N324
  N167 --> N475
  N231 --> N241
  N640 --> N638
  N173 --> N99
  N168 --> N394
  N346 --> N355
  N539 --> N82
  N404 --> N90
  N397 --> N583
  N434 --> N90
  N305 --> N279
  N160 --> N570
  N441 -. fd_ready .-> N51
  N102 --> N116
  N339 --> N671
  N404 --> N90
  N87 --> N82
  N96 --> N141
  N558 --> N639
  N101 --> N580
  N138 --> N139
  N256 --> N279
  N442 --> N671
  N539 --> N229
  N261 --> N325
  N505 --> N74
  N368 --> N585
  N599 --> N596
  N123 --> N585
  N616 --> N82
  N288 --> N270
  N493 --> N103
  N69 --> N72
  N339 --> N75
  N434 --> N583
  N167 --> N197
  N334 --> N449
  N168 --> N572
  N530 --> N583
  N406 --> N465
  N504 --> N583
  N121 --> N580
  N56 --> N450
  N80 --> N183
  N539 --> N241
  N409 --> N491
  N396 --> N165
  N246 --> N488
  N348 --> N433
  N375 --> N98
  N562 --> N583
  N291 --> N671
  N552 --> N676
  N174 --> N580
  N298 -. fd_ready .-> N47
  N112 --> N83
  N230 --> N252
  N128 --> N671
  N654 --> N449
  N396 --> N553
  N93 --> N116
  N616 --> N165
  N264 --> N299
  N601 --> N440
  N101 --> N579
  N605 --> N407
  N655 --> N453
  N168 --> N163
  N107 --> N580
  N168 --> N90
  N106 --> N584
  N433 --> N521
  N121 --> N575
  N236 --> N232
  N264 --> N71
  N171 --> N241
  N80 --> N339
  N642 --> N379
  N330 --> N110
  N212 -. fd_ready .-> N27
  N616 --> N583
  N251 --> N325
  N174 --> N160
  N552 --> N407
  N130 --> N76
  N399 --> N530
  N487 --> N486
  N231 --> N257
  N397 --> N89
  N117 --> N73
  N408 --> N406
  N336 --> N319
  N198 --> N213
  N434 --> N112
  N145 --> N583
  N168 --> N82
  N434 --> N220
  N57 --> N471
  N93 --> N118
  N57 --> N378
  N562 --> N586
  N409 --> N165
  N80 --> N188
  N168 --> N110
  N168 --> N339
  N80 --> N183
  N82 --> N456
  N249 --> N285
  N434 --> N580
  N409 --> N552
  N168 --> N671
  N633 --> N73
  N234 --> N560
  N94 --> N648
  N168 --> N671
  N507 -. fd_ready .-> N5
  N173 --> N99
  N361 --> N449
  N417 --> N341
  N605 --> N222
  N434 --> N96
  N259 --> N71
  N104 --> N105
  N174 --> N369
  N484 --> N604
  N216 --> N170
  N431 --> N290
  N592 --> N593
  N515 --> N447
  N168 --> N459
  N605 --> N553
  N302 --> N73
  N68 --> N271
  N505 --> N637
  N399 --> N440
  N339 --> N340
  N88 --> N116
  N314 --> N672
  N399 --> N506
  N501 --> N176
  N375 --> N388
  N233 --> N348
  N244 --> N245
  N288 --> N271
  N548 --> N73
  N562 --> N464
  N168 --> N90
  N160 --> N571
  N344 --> N671
  N252 --> N264
  N234 --> N644
  N319 --> N333
  N335 --> N82
  N503 --> N586
  N167 --> N190
  N409 --> N221
  N346 --> N356
  N339 --> N480
  N616 --> N583
  N154 --> N531
  N288 --> N73
  N233 --> N74
  N401 --> N400
  N216 --> N250
  N271 --> N325
  N168 --> N96
  N67 --> N255
  N505 --> N609
  N498 --> N515
  N505 --> N218
  N595 --> N649
  N472 --> N88
  N101 --> N583
  N352 --> N351
  N168 --> N580
  N605 --> N672
  N270 --> N238
  N82 --> N583
  N539 --> N225
  N140 --> N131
  N77 --> N411
  N145 --> N572
  N135 --> N671
  N506 --> N504
  N105 --> N583
  N231 --> N331
  N440 -. fd_ready .-> N51
  N595 --> N493
  N166 --> N480
  N107 --> N94
  N239 --> N325
  N226 --> N74
  N100 --> N101
  N502 --> N660
  N62 --> N174
  N77 --> N73
  N334 --> N169
  N230 --> N304
  N496 --> N495
  N251 --> N326
  N396 --> N88
  N434 --> N220
  N227 --> N249
  N167 --> N193
  N408 --> N388
  N484 --> N465
  N217 --> N672
  N122 --> N116
  N530 --> N565
  N601 --> N673
  N57 --> N530
  N240 --> N406
  N562 --> N449
  N302 -. fd_ready .-> N49
  N507 -. fd_ready .-> N38
  N168 --> N90
  N486 --> N649
  N406 --> N96
  N56 --> N446
  N168 --> N652
  N243 --> N452
  N80 --> N211
  N168 --> N110
  N139 --> N507
  N425 --> N110
  N176 --> N548
  N558 --> N73
  N609 --> N580
  N285 --> N73
  N339 --> N514
  N71 --> N288
  N214 --> N82
  N64 --> N63
  N562 --> N452
  N152 --> N75
  N310 --> N290
  N231 --> N583
  N400 --> N169
  N608 --> N537
  N230 --> N305
  N115 --> N73
  N397 --> N82
  N517 --> N113
  N141 --> N410
  N168 --> N653
  N539 --> N491
  N562 --> N612
  N461 --> N331
  N620 --> N644
  N168 --> N110
  N438 --> N672
  N618 --> N103
  N560 --> N270
  N296 -. fd_ready .-> N4
  N103 --> N583
  N305 --> N271
  N56 --> N243
  N167 --> N368
  N85 --> N73
  N608 --> N622
  N616 --> N583
  N458 --> N580
  N321 --> N253
  N604 --> N300
  N208 -. fd_ready .-> N24
  N495 --> N663
  N596 --> N73
  N166 --> N514
  N168 --> N96
  N434 --> N84
  N155 --> N438
  N596 --> N601
  N237 --> N110
  N434 --> N84
  N233 --> N302
  N398 --> N608
  N233 --> N479
  N404 --> N81
  N168 --> N103
  N549 --> N166
  N416 --> N75
  N238 --> N239
  N288 --> N72
  N339 --> N671
  N139 --> N130
  N339 --> N241
  N390 --> N73
  N110 --> N82
  N561 --> N257
  N88 --> N82
  N292 --> N302
  N312 --> N452
  N123 --> N589
  N257 --> N270
  N168 --> N89
  N668 --> N75
  N508 --> N241
  N562 --> N440
  N82 --> N498
  N484 --> N82
  N374 --> N275
  N404 --> N110
  N214 --> N82
  N339 --> N440
  N422 --> N597
  N124 --> N116
  N401 --> N449
  N329 --> N160
  N280 --> N324
  N604 --> N257
  N168 --> N671
  N102 --> N116
  N417 --> N205
  N108 --> N116
  N605 --> N375
  N658 --> N169
  N107 --> N120
  N416 --> N607
  N339 --> N241
  N126 --> N671
  N505 --> N609
  N115 --> N103
  N618 --> N103
  N66 --> N670
  N174 --> N162
  N616 --> N586
  N353 --> N358
  N56 --> N341
  N345 --> N440
  N605 --> N377
  N139 -. fd_ready .-> N35
  N321 --> N253
  N230 --> N279
  N255 --> N66
  N284 --> N283
  N596 --> N601
  N399 --> N452
  N605 --> N241
  N415 --> N630
  N188 --> N338
  N285 --> N325
  N132 --> N672
  N168 --> N309
  N172 --> N96
  N409 --> N552
  N216 --> N203
  N401 --> N668
  N168 --> N103
  N401 --> N633
  N339 --> N542
  N259 --> N67
  N458 --> N575
  N409 --> N386
  N297 --> N324
  N164 --> N490
  N168 --> N110
  N236 --> N373
  N168 --> N84
  N668 --> N674
  N317 -. fd_ready .-> N5
  N441 --> N449
  N168 --> N103
  N135 --> N671
  N399 --> N438
  N62 --> N438
  N421 --> N177
  N505 --> N96
  N591 --> N75
  N655 --> N455
  N450 --> N671
  N458 --> N580
  N503 --> N609
  N562 --> N295
  N145 --> N164
  N530 --> N190
  N609 --> N583
  N400 --> N417
  N539 --> N622
  N78 --> N440
  N530 --> N75
  N246 --> N508
  N126 --> N671
  N616 --> N225
  N149 --> N672
  N441 -. fd_ready .-> N50
  N249 -. fd_ready .-> N47
  N294 --> N255
  N149 --> N155
  N383 --> N676
  N80 --> N368
  N559 --> N562
  N616 --> N583
  N176 --> N543
  N622 --> N645
  N484 --> N96
  N298 --> N73
  N558 --> N270
  N401 --> N452
  N178 -. fd_ready .-> N6
  N433 --> N526
  N404 --> N90
  N154 --> N75
  N251 -. fd_ready .-> N1
  N203 -. fd_ready .-> N20
  N431 --> N290
  N401 --> N452
  N168 --> N388
  N94 --> N369
  N538 --> N539
  N145 --> N622
  N539 --> N491
  N404 --> N109
  N56 --> N160
  N530 --> N160
  N422 --> N89
  N505 --> N96
  N350 --> N524
  N668 --> N77
  N168 --> N103
  N605 --> N82
  N603 --> N596
  N216 --> N250
  N401 --> N438
  N461 --> N662
  N126 --> N671
  N505 --> N96
  N101 --> N583
  N620 --> N647
  N466 --> N465
  N265 --> N324
  N214 --> N315
  N616 --> N465
  N140 --> N676
  N277 --> N68
  N654 --> N452
  N164 --> N96
  N596 --> N601
  N166 --> N440
  N329 --> N452
  N558 --> N438
  N339 --> N453
  N558 --> N583
  N323 --> N73
  N285 -. fd_ready .-> N41
  N168 --> N99
  N605 --> N604
  N650 --> N390
  N168 --> N671
  N116 --> N64
  N434 --> N110
  N288 --> N325
  N263 --> N624
  N650 --> N464
  N285 --> N73
  N289 --> N288
  N273 --> N71
  N400 --> N455
  N472 --> N113
  N141 --> N410
  N434 --> N388
  N296 --> N551
  N458 --> N579
  N293 --> N260
  N251 --> N279
  N655 --> N206
  N264 --> N270
  N214 --> N593
  N549 --> N120
  N90 --> N89
  N548 --> N340
  N144 --> N452
  N409 --> N622
  N216 --> N436
  N245 --> N228
  N339 --> N144
  N562 --> N84
  N247 --> N249
  N168 --> N90
  N166 --> N241
  N597 --> N596
  N562 --> N613
  N416 --> N75
  N168 --> N90
  N261 --> N239
  N285 --> N327
  N94 --> N547
  N276 --> N71
  N95 --> N116
  N442 -. fd_ready .-> N51
  N307 --> N264
  N504 --> N587
  N296 --> N251
  N168 --> N103
  N231 --> N220
  N319 --> N475
  N401 --> N607
  N486 --> N82
  N216 --> N413
  N552 --> N241
  N505 --> N96
  N226 --> N621
  N560 --> N257
  N116 --> N498
  N282 --> N73
  N168 --> N160
  N132 --> N672
  N243 --> N449
  N664 -. fd_ready .-> N5
  N168 --> N579
  N108 --> N116
  N441 --> N438
  N114 --> N116
  N101 --> N102
  N401 --> N449
  N227 --> N302
  N602 --> N583
  N641 --> N647
  N214 --> N622
  N404 --> N96
  N167 --> N75
  N363 --> N383
  N339 --> N341
  N562 --> N438
  N168 --> N96
  N168 --> N82
  N505 --> N96
  N304 -. fd_ready .-> N44
  N205 -. fd_ready .-> N21
  N172 --> N171
  N608 --> N226
  N115 --> N82
  N168 --> N99
  N339 --> N651
  N605 --> N491
  N339 --> N580
  N618 --> N563
  N150 --> N155
  N401 --> N442
  N598 --> N596
  N150 --> N672
  N616 --> N583
  N117 --> N83
  N242 --> N96
  N655 --> N73
  N168 --> N96
  N404 --> N90
  N503 --> N588
  N375 --> N177
  N82 --> N64
  N360 --> N383
  N153 --> N75
  N168 --> N90
  N406 --> N110
  N110 --> N82
  N272 --> N325
  N395 --> N491
  N80 --> N188
  N399 --> N147
  N465 --> N467
  N616 --> N387
  N404 --> N54
  N560 --> N279
  N562 --> N468
  N553 --> N672
  N247 --> N302
  N384 --> N637
  N214 --> N577
  N39 -. fd_ready .-> N427
  N39 -. fd_ready .-> N428
  N39 -. fd_ready .-> N429
  N39 -. fd_ready .-> N430
  N39 -. fd_ready .-> N431
  N39 -. fd_ready .-> N432
  N51 -. fd_ready .-> N344
  N50 -. fd_ready .-> N314
```

## 关键调用链

- `aeProcessEvents -> aeFileEvent::wfileProc` (leaf)
- `aeProcessEvents -> aeEventLoop::aftersleep` (leaf)
- `aeProcessEvents -> aeFileEvent::rfileProc` (leaf)
- `aeProcessEvents -> usUntilEarliestTimer -> getMonotonicUs` (leaf)
- `aeProcessEvents -> aeEventLoop::beforesleep` (leaf)
- `aeProcessEvents -> processTimeEvents -> aeTimeEvent::finalizerProc` (leaf)
- `aeProcessEvents -> processTimeEvents -> zfree` (leaf)
- `aeProcessEvents -> processTimeEvents -> getMonotonicUs` (leaf)
- `aeProcessEvents -> processTimeEvents -> getMonotonicUs` (leaf)
- `aeProcessEvents -> processTimeEvents -> getMonotonicUs` (leaf)

## 自然语言分析

# 自然语言分析

## 模块架构
仓库由 core、src 组成。入口负责初始化运行时、注册回调并驱动主循环；事件循环组件负责等待就绪事件、遍历句柄并分发回调。

## 关键调用链
入口 `aeProcessEvents` 的关键路径是：`aeProcessEvents -> aeFileEvent::wfileProc`。

## 异步回调链
fd_ready 事件在 third_party/redis/src/connection.h:243 触发回调，但候选为空，需要进一步分析。

## 函数指针
静态分析发现回调字段存在多个候选：`dupClientReplyValue、freeClientReplyValue、lazyFreeFunctionsCtx、lazyFreeLuaScripts、lazyFreeReplicationBacklogRefMem、lazyFreeTrackingTable、lazyfreeFreeDatabase、lazyfreeFreeObject`，无法唯一确定目标，置信度为 0.30。

## 复杂宏
本次分析覆盖：ACL_DENIED_AUTH (third_party/redis/src/server.h:2891)、ACL_DENIED_CHANNEL (third_party/redis/src/server.h:2892)、ACL_DENIED_CMD (third_party/redis/src/server.h:2889)、ACL_DENIED_KEY (third_party/redis/src/server.h:2890)、ACL_LOG_CTX_LUA (third_party/redis/src/server.h:2896)。宏展开记录已挂到对应调用边的 `macro_stack` 证据上。

## 结论
验证覆盖率为 88%，报告状态为 not ready；所有结论均引用源码文件、行号和原始代码片段。

## 异步回调链

- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:444` -> `third_party/redis/src/ae.c:444` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:247` -> `third_party/redis/src/connection.h:247` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:262` -> `third_party/redis/src/connection.h:262` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1485` -> `third_party/redis/src/dict.c:1485` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:536` -> `third_party/redis/src/dict.c:536` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/db.c:272` -> `third_party/redis/src/db.c:272` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:743` -> `third_party/redis/src/dict.c:743` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:411` -> `third_party/redis/src/connection.h:411` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:266` -> `third_party/redis/src/connection.h:266` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1326` -> `third_party/redis/src/dict.c:1326` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:133` -> `third_party/redis/src/rio.h:133` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:286` -> `third_party/redis/src/connection.h:286` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1445` -> `third_party/redis/src/dict.c:1445` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:565` -> `third_party/redis/src/dict.c:565` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:195` -> `third_party/redis/src/connection.h:195` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:142` -> `third_party/redis/src/rio.h:142` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:629` -> `third_party/redis/src/dict.c:629` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:405` -> `third_party/redis/src/connection.h:405` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/lazyfree.c:167` -> `third_party/redis/src/bio.c:287` -> callbacks: lazyFreeFunctionsCtx, lazyFreeLuaScripts, lazyFreeReplicationBacklogRefMem, lazyFreeTrackingTable, lazyfreeFreeDatabase, lazyfreeFreeObject
  - Confidence: 0.60, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/adlist.c:329` -> `third_party/redis/src/adlist.c:329` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:227` -> `third_party/redis/src/connection.h:227` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1143` -> `third_party/redis/src/dict.c:1143` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:326` -> `third_party/redis/src/dict.c:326` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:146` -> `third_party/redis/src/rio.h:146` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:187` -> `third_party/redis/src/dict.c:187` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:113` -> `third_party/redis/src/rio.h:113` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:219` -> `third_party/redis/src/connection.h:219` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1136` -> `third_party/redis/src/dict.c:1136` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:408` -> `third_party/redis/src/ae.c:408` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/db.c:2178` -> `third_party/redis/src/db.c:2178` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:646` -> `third_party/redis/src/dict.c:646` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/monotonic.h:54` -> `third_party/redis/src/monotonic.h:54` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:308` -> `third_party/redis/src/ae.c:308` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:114` -> `third_party/redis/src/rio.h:114` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:647` -> `third_party/redis/src/dict.c:647` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:681` -> `third_party/redis/src/dict.c:681` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:436` -> `third_party/redis/src/ae.c:436` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:258` -> `third_party/redis/src/connection.h:258` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:376` -> `third_party/redis/src/connection.h:376` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:229` -> `third_party/redis/src/ae.c:229` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:573` -> `third_party/redis/src/dict.c:573` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1399` -> `third_party/redis/src/dict.c:1399` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:432` -> `third_party/redis/src/connection.h:432` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:675` -> `third_party/redis/src/dict.c:675` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/rio.h:129` -> `third_party/redis/src/rio.h:129` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:309` -> `third_party/redis/src/ae.c:309` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:742` -> `third_party/redis/src/dict.c:742` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:287` -> `third_party/redis/src/ae.c:287` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:628` -> `third_party/redis/src/dict.c:628` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:725` -> `third_party/redis/src/dict.c:725` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1137` -> `third_party/redis/src/dict.c:1137` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/db.c:2022` -> `third_party/redis/src/db.c:2022` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:379` -> `third_party/redis/src/ae.c:379` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:251` -> `third_party/redis/src/connection.h:251` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1458` -> `third_party/redis/src/dict.c:1458` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:174` -> `third_party/redis/src/connection.h:174` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:324` -> `third_party/redis/src/connection.h:324` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:418` -> `third_party/redis/src/connection.h:418` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:184` -> `third_party/redis/src/connection.h:184` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1158` -> `third_party/redis/src/dict.c:1158` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:275` -> `third_party/redis/src/connection.h:275` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1359` -> `third_party/redis/src/dict.c:1359` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/networking.c:190` -> `third_party/redis/src/adlist.c:303` -> callbacks: freeClientReplyValue
  - Confidence: 0.95, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:751` -> `third_party/redis/src/dict.c:751` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:207` -> `third_party/redis/src/connection.h:207` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:334` -> `third_party/redis/src/ae.c:334` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/networking.c:190` -> `third_party/redis/src/adlist.c:185` -> callbacks: freeClientReplyValue
  - Confidence: 0.95, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:758` -> `third_party/redis/src/dict.c:758` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:331` -> `third_party/redis/src/ae.c:331` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1373` -> `third_party/redis/src/dict.c:1373` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:270` -> `third_party/redis/src/connection.h:270` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:456` -> `third_party/redis/src/ae.c:456` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/monotonic.h:50` -> `third_party/redis/src/monotonic.h:50` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/networking.c:191` -> `third_party/redis/src/adlist.c:292` -> callbacks: dupClientReplyValue
  - Confidence: 0.95, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:458` -> `third_party/redis/src/dict.c:458` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:160` -> `third_party/redis/src/connection.h:160` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:1150` -> `third_party/redis/src/dict.c:1150` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:234` -> `third_party/redis/src/connection.h:234` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:475` -> `third_party/redis/src/dict.c:475` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/networking.c:190` -> `third_party/redis/src/adlist.c:66` -> callbacks: freeClientReplyValue
  - Confidence: 0.95, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/ae.c:275` -> `third_party/redis/src/ae.c:275` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/dict.c:718` -> `third_party/redis/src/dict.c:718` -> callbacks:
  - Confidence: 0.30, loop back: True
- `third_party/redis/src/ae_epoll.c:109` `fd_ready` -> `third_party/redis/src/connection.h:243` -> `third_party/redis/src/connection.h:243` -> callbacks:
  - Confidence: 0.30, loop back: True

## 函数指针候选

- `aeFileEvent::wfileProc` @ `third_party/redis/src/ae.c:444`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::shutdown` @ `third_party/redis/src/connection.h:247`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::sync_write` @ `third_party/redis/src/connection.h:262`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:1485`
  - Candidates:
  - Confidence: 0.30
- `dictType::valDestructor` @ `third_party/redis/src/dict.c:536`
  - Candidates:
  - Confidence: 0.30
- `dictType::valDestructor` @ `third_party/redis/src/db.c:272`
  - Candidates:
  - Confidence: 0.30
- `dictType::valDestructor` @ `third_party/redis/src/dict.c:743`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::conn_create_accepted` @ `third_party/redis/src/connection.h:411`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::sync_read` @ `third_party/redis/src/connection.h:266`
  - Candidates:
  - Confidence: 0.30
- `fn` @ `third_party/redis/src/dict.c:1326`
  - Candidates:
  - Confidence: 0.30
- `_rio::update_cksum` @ `third_party/redis/src/rio.h:133`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::addr` @ `third_party/redis/src/connection.h:286`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:1445`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:565`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::write` @ `third_party/redis/src/connection.h:195`
  - Candidates:
  - Confidence: 0.30
- `_rio::tell` @ `third_party/redis/src/rio.h:142`
  - Candidates:
  - Confidence: 0.30
- `dictType::valDestructor` @ `third_party/redis/src/dict.c:629`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::conn_create` @ `third_party/redis/src/connection.h:405`
  - Candidates:
  - Confidence: 0.30
- `bio_job::struct (unnamed at /home/runner/work/code_ana_sys/code_ana_sys/third_party/redis/src/bio.c:105:5)::free_fn` @ `third_party/redis/src/bio.c:287`
  - Candidates: `lazyFreeFunctionsCtx` (third_party/redis/src/lazyfree.c:51), `lazyFreeLuaScripts` (third_party/redis/src/lazyfree.c:42), `lazyFreeReplicationBacklogRefMem` (third_party/redis/src/lazyfree.c:60), `lazyFreeTrackingTable` (third_party/redis/src/lazyfree.c:33), `lazyfreeFreeDatabase` (third_party/redis/src/lazyfree.c:21), `lazyfreeFreeObject` (third_party/redis/src/lazyfree.c:11)
  - Confidence: 0.60
- `list::match` @ `third_party/redis/src/adlist.c:329`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::set_write_handler` @ `third_party/redis/src/connection.h:227`
  - Candidates:
  - Confidence: 0.30
- `defragalloc` @ `third_party/redis/src/dict.c:1143`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:326`
  - Candidates:
  - Confidence: 0.30
- `_rio::flush` @ `third_party/redis/src/rio.h:146`
  - Candidates:
  - Confidence: 0.30
- `dictType::dictMetadataBytes` @ `third_party/redis/src/dict.c:187`
  - Candidates:
  - Confidence: 0.30
- `_rio::update_cksum` @ `third_party/redis/src/rio.h:113`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::read` @ `third_party/redis/src/connection.h:219`
  - Candidates:
  - Confidence: 0.30
- `defragkey` @ `third_party/redis/src/dict.c:1136`
  - Candidates:
  - Confidence: 0.30
- `aeEventLoop::aftersleep` @ `third_party/redis/src/ae.c:408`
  - Candidates:
  - Confidence: 0.30
- `redisCommand::getkeys_proc` @ `third_party/redis/src/db.c:2178`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyDestructor` @ `third_party/redis/src/dict.c:646`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/monotonic.h:54`
  - Candidates:
  - Confidence: 0.30
- `aeTimeEvent::finalizerProc` @ `third_party/redis/src/ae.c:308`
  - Candidates:
  - Confidence: 0.30
- `_rio::write` @ `third_party/redis/src/rio.h:114`
  - Candidates:
  - Confidence: 0.30
- `dictType::valDestructor` @ `third_party/redis/src/dict.c:647`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyCompare` @ `third_party/redis/src/dict.c:681`
  - Candidates:
  - Confidence: 0.30
- `aeFileEvent::rfileProc` @ `third_party/redis/src/ae.c:436`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::get_last_error` @ `third_party/redis/src/connection.h:258`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::get_peer_cert` @ `third_party/redis/src/connection.h:376`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/ae.c:229`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyCompare` @ `third_party/redis/src/dict.c:573`
  - Candidates:
  - Confidence: 0.30
- `dictType::expandAllowed` @ `third_party/redis/src/dict.c:1399`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::listen` @ `third_party/redis/src/connection.h:432`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:675`
  - Candidates:
  - Confidence: 0.30
- `_rio::read` @ `third_party/redis/src/rio.h:129`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/ae.c:309`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyDestructor` @ `third_party/redis/src/dict.c:742`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/ae.c:287`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyDestructor` @ `third_party/redis/src/dict.c:628`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyCompare` @ `third_party/redis/src/dict.c:725`
  - Candidates:
  - Confidence: 0.30
- `defragval` @ `third_party/redis/src/dict.c:1137`
  - Candidates:
  - Confidence: 0.30
- `redisCommand::getkeys_proc` @ `third_party/redis/src/db.c:2022`
  - Candidates:
  - Confidence: 0.30
- `aeEventLoop::beforesleep` @ `third_party/redis/src/ae.c:379`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::close` @ `third_party/redis/src/connection.h:251`
  - Candidates:
  - Confidence: 0.30
- `dictType::keyCompare` @ `third_party/redis/src/dict.c:1458`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::connect` @ `third_party/redis/src/connection.h:174`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::is_local` @ `third_party/redis/src/connection.h:324`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::configure` @ `third_party/redis/src/connection.h:418`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::blocking_connect` @ `third_party/redis/src/connection.h:184`
  - Candidates:
  - Confidence: 0.30
- `dictType::afterReplaceEntry` @ `third_party/redis/src/dict.c:1158`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::get_type` @ `third_party/redis/src/connection.h:275`
  - Candidates:
  - Confidence: 0.30
- `fn` @ `third_party/redis/src/dict.c:1359`
  - Candidates:
  - Confidence: 0.30
- `list::free` @ `third_party/redis/src/adlist.c:303`
  - Candidates: `freeClientReplyValue` (third_party/redis/src/networking.c:84)
  - Confidence: 0.95
- `dictType::keyDup` @ `third_party/redis/src/dict.c:751`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::writev` @ `third_party/redis/src/connection.h:207`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/ae.c:334`
  - Candidates:
  - Confidence: 0.30
- `list::free` @ `third_party/redis/src/adlist.c:185`
  - Candidates: `freeClientReplyValue` (third_party/redis/src/networking.c:84)
  - Confidence: 0.95
- `dictType::valDup` @ `third_party/redis/src/dict.c:758`
  - Candidates:
  - Confidence: 0.30
- `aeTimeEvent::timeProc` @ `third_party/redis/src/ae.c:331`
  - Candidates:
  - Confidence: 0.30
- `fn` @ `third_party/redis/src/dict.c:1373`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::sync_readline` @ `third_party/redis/src/connection.h:270`
  - Candidates:
  - Confidence: 0.30
- `aeFileEvent::rfileProc` @ `third_party/redis/src/ae.c:456`
  - Candidates:
  - Confidence: 0.30
- `getMonotonicUs` @ `third_party/redis/src/monotonic.h:50`
  - Candidates:
  - Confidence: 0.30
- `list::dup` @ `third_party/redis/src/adlist.c:292`
  - Candidates: `dupClientReplyValue` (third_party/redis/src/networking.c:77)
  - Confidence: 0.95
- `dictType::keyDup` @ `third_party/redis/src/dict.c:458`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::accept` @ `third_party/redis/src/connection.h:160`
  - Candidates:
  - Confidence: 0.30
- `defragalloc` @ `third_party/redis/src/dict.c:1150`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::set_read_handler` @ `third_party/redis/src/connection.h:234`
  - Candidates:
  - Confidence: 0.30
- `dictType::dictEntryMetadataBytes` @ `third_party/redis/src/dict.c:475`
  - Candidates:
  - Confidence: 0.30
- `list::free` @ `third_party/redis/src/adlist.c:66`
  - Candidates: `freeClientReplyValue` (third_party/redis/src/networking.c:84)
  - Confidence: 0.95
- `getMonotonicUs` @ `third_party/redis/src/ae.c:275`
  - Candidates:
  - Confidence: 0.30
- `dictType::hashFunction` @ `third_party/redis/src/dict.c:718`
  - Candidates:
  - Confidence: 0.30
- `ConnectionType::set_write_handler` @ `third_party/redis/src/connection.h:243`
  - Candidates:
  - Confidence: 0.30

## 宏分析

| macro | file:line | definition | call sites |
| --- | --- | --- | --- |

## Evidence

| id | kind | file:line | snippet |
| --- | --- | --- | --- |
| `ev_00a342612e8b` | call_site | `third_party/redis/src/db.c:1621` | `if (getIntFromObjectOrReply(c, c->argv[1], &id1,` |
| `ev_00e66b38b047` | call_site | `third_party/redis/src/t_string.c:513` | `checkType(c,o,OBJ_STRING)) return;` |
| `ev_0135fdc0b874` | call_site | `third_party/redis/src/networking.c:3090` | `addReplyVerbatim(c,o,sdslen(o),"txt");` |
| `ev_01375211e81e` | call_site | `third_party/redis/src/t_string.c:694` | `rewriteClientCommandArgument(c,3,shared.keepttl);` |
| `ev_017717512902` | call_site | `third_party/redis/src/networking.c:2568` | `serverAssert(io_threads_op == IO_THREADS_OP_READ);` |
| `ev_0187d787735c` | call_site | `third_party/redis/src/t_string.c:125` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"expire",key,c->db->id);` |
| `ev_01af0f9e7f95` | call_site | `third_party/redis/src/dict.c:188` | `dict *d = zmalloc(sizeof(*d) + metasize);` |
| `ev_01cb3f1711f6` | call_site | `third_party/redis/src/t_string.c:758` | `objb = objb ? getDecodedObject(objb) : createStringObject("",0);` |
| `ev_01cd129c9a0a` | call_site | `third_party/redis/src/t_string.c:136` | `robj **argv = zmalloc((c->argc-1)*sizeof(robj*));` |
| `ev_01ee59300af3` | call_site | `third_party/redis/src/t_string.c:435` | `notifyKeyspaceEvent(NOTIFY_STRING,"set",c->argv[1],c->db->id);` |
| `ev_01f853f858a0` | call_site | `third_party/redis/src/networking.c:3178` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_01f9ce1df0c1` | call_site | `third_party/redis/src/networking.c:2396` | `sdsclear(c->querybuf);` |
| `ev_0221e65f652e` | call_site | `third_party/redis/src/networking.c:3111` | `addReply(c,shared.ok);` |
| `ev_0247fad2b4d6` | call_site | `third_party/redis/src/t_string.c:525` | `addReply(c,shared.emptybulk);` |
| `ev_027778d8e0c7` | call_site | `third_party/redis/src/db.c:159` | `return lookupKeyReadWithFlags(db,key,LOOKUP_NONE);` |
| `ev_027c3dc869fd` | call_site | `third_party/redis/src/networking.c:1738` | `sdsfree(client);` |
| `ev_02ade963432f` | call_site | `third_party/redis/src/adlist.c:186` | `zfree(node);` |
| `ev_02e49081b191` | call_site | `third_party/redis/src/networking.c:2701` | `sds ci = catClientInfoString(sdsempty(),c), bytes = sdsempty();` |
| `ev_02f149c10b64` | call_site | `third_party/redis/src/networking.c:3578` | `if (err) decrRefCount(err);` |
| `ev_0308856a985c` | call_site | `third_party/redis/src/dict.c:1143` | `if ((newentry = defragalloc(entry))) {` |
| `ev_032a08fa97b5` | call_site | `third_party/redis/src/db.c:56` | `unsigned long counter = LFUDecrAndReturn(val);` |
| `ev_0340ace8f0d7` | call_site | `third_party/redis/src/db.c:1178` | `o = lookupKeyReadWithFlags(c->db,c->argv[1],LOOKUP_NOTOUCH);` |
| `ev_0383ba80d97d` | call_site | `third_party/redis/src/networking.c:2802` | `if (connHasReadHandler(client->conn)) *p++ = 'r';` |
| `ev_03b51f706396` | call_site | `third_party/redis/src/t_string.c:123` | `decrRefCount(milliseconds_obj);` |
| `ev_03c771d6d0d7` | call_site | `third_party/redis/src/networking.c:232` | `if (connSetWriteHandlerWithBarrier(c->conn, sendReplyToClient, ae_barrier) == C_ERR) {` |
| `ev_03d8dbc8d480` | call_site | `third_party/redis/src/connection.h:243` | `return conn->type->set_write_handler(conn, func, barrier);` |
| `ev_03dfdfe495d7` | call_site | `third_party/redis/src/dict.c:343` | `assert(entryIsKey(key));` |
| `ev_0421da70b7a9` | call_site | `third_party/redis/src/networking.c:2297` | `if (c->argv) zfree(c->argv);` |
| `ev_043a4c1ad6b5` | call_site | `third_party/redis/src/networking.c:2336` | `} else if (ll > 16384 && authRequired(c)) {` |
| `ev_047941abd9e0` | call_site | `third_party/redis/src/networking.c:1694` | `if (c->lib_name) decrRefCount(c->lib_name);` |
| `ev_047a9f3a2bbf` | call_site | `third_party/redis/src/networking.c:1731` | `sds info = sdscatvprintf(sdsempty(), fmt, ap);` |
| `ev_048a5be55832` | call_site | `third_party/redis/src/networking.c:1417` | `listRewind(server.slaves, &li);` |
| `ev_048e90bc4296` | call_site | `third_party/redis/src/dict.c:1379` | `v = rev(v);` |
| `ev_0499ba62407d` | call_site | `third_party/redis/src/dict.c:1424` | `return dictExpand(d, d->ht_used[0] + 1);` |
| `ev_04c784caaf8e` | call_site | `third_party/redis/src/networking.c:2680` | `sds info = catClientInfoString(sdsempty(), c);` |
| `ev_04eaebe49102` | call_site | `third_party/redis/src/t_string.c:792` | `addReplyError(c, "String too long for LCS");` |
| `ev_051a549369ac` | call_site | `third_party/redis/src/dict.c:804` | `assert(entryHasValue(de));` |
| `ev_053252f68eed` | call_site | `third_party/redis/src/db.c:1928` | `if (!string2ll(keynum_str,sdslen(keynum_str),&numkeys) \|\| numkeys < 0) {` |
| `ev_0548462e714f` | call_site | `third_party/redis/src/networking.c:3315` | `zfree(prefix);` |
| `ev_0563abb45507` | call_site | `third_party/redis/src/db.c:1917` | `serverAssert(spec->fk.range.lastkey == -1);` |
| `ev_058049852d07` | call_site | `third_party/redis/src/db.c:1106` | `if (use_pattern && !stringmatchlen(pat, sdslen(pat), (char *)str, len, 0)) {` |
| `ev_05827933cdb3` | call_site | `third_party/redis/src/networking.c:2319` | `if (newline-(c->querybuf+c->qb_pos) > (ssize_t)(sdslen(c->querybuf)-c->qb_pos-2))` |
| `ev_05a454deee4a` | call_site | `third_party/redis/src/networking.c:1148` | `sdstoupper(cmd);` |
| `ev_05d03043ebb2` | call_site | `third_party/redis/src/networking.c:2671` | `if (connGetState(conn) == CONN_STATE_CONNECTED) {` |
| `ev_05d21b29febc` | call_site | `third_party/redis/src/bio.c:166` | `bio_job *job = zmalloc(sizeof(*job) + sizeof(void *) * (arg_count));` |
| `ev_05f363e5fabb` | call_site | `third_party/redis/src/dict.c:346` | `} else if (entryIsKey(de)) {` |
| `ev_05fcb1548eb5` | call_site | `third_party/redis/src/dict.c:693` | `he = dictFind(d,key);` |
| `ev_062e1d33ff52` | call_site | `third_party/redis/src/db.c:1286` | `renameGenericCommand(c,0);` |
| `ev_063e855a7978` | call_site | `third_party/redis/src/db.c:173` | `return lookupKeyWriteWithFlags(db, key, LOOKUP_NONE);` |
| `ev_066335d0336b` | call_site | `third_party/redis/src/t_string.c:114` | `notifyKeyspaceEvent(NOTIFY_STRING,"set",key,c->db->id);` |
| `ev_067047633188` | call_site | `third_party/redis/src/networking.c:2960` | `addReply(c,shared.ok);` |
| `ev_0673334534be` | call_site | `third_party/redis/src/networking.c:186` | `c->reply = listCreate();` |
| `ev_067c054b6317` | call_site | `third_party/redis/src/bio.c:336` | `serverLog(LL_WARNING,` |
| `ev_068bd88ed6bf` | call_site | `third_party/redis/src/dict.c:646` | `dictFreeKey(d, he);` |
| `ev_06a05731e10d` | call_site | `third_party/redis/src/dict.c:348` | `de = createEntryNoValue(key, d->ht_table[1][h]);` |
| `ev_06bf24483e77` | call_site | `third_party/redis/src/dict.c:576` | `dictSetNext(prevHe, dictGetNext(he));` |
| `ev_06d396455356` | call_site | `third_party/redis/src/networking.c:2203` | `c->argv_len_sum += sdslen(argv[j]);` |
| `ev_06e2f1fcb982` | call_site | `third_party/redis/src/networking.c:418` | `server.executing_client && !cmdHasPushAsReply(server.executing_client->cmd))` |
| `ev_070307f033b3` | call_site | `third_party/redis/src/db.c:1155` | `listDelNode(keys, node);` |
| `ev_07121e6d0425` | call_site | `third_party/redis/src/networking.c:2470` | `updateClientMemUsageAndBucket(c);` |
| `ev_0717ad38d8fc` | call_site | `third_party/redis/src/networking.c:1491` | `serverAssert(ln != NULL);` |
| `ev_073ca1c22b39` | call_site | `third_party/redis/src/connection.h:251` | `conn->type->close(conn);` |
| `ev_076cb60ceacf` | call_site | `third_party/redis/src/ae_epoll.c:40` | `aeApiState *state = zmalloc(sizeof(aeApiState));` |
| `ev_076e10de2c10` | call_site | `third_party/redis/src/networking.c:613` | `addReplyErrorLength(c,err,strlen(err));` |
| `ev_078601d2382f` | call_site | `third_party/redis/src/networking.c:3110` | `removeClientFromMemUsageBucket(c, 0);` |
| `ev_07a8f2f9720f` | call_site | `third_party/redis/src/dict.c:731` | `ref = dictGetNextRef(*ref);` |
| `ev_07c9755b1eb1` | call_site | `third_party/redis/src/networking.c:1466` | `if (server.child_type) connShutdown(c->conn);` |
| `ev_07cb6510cb4f` | call_site | `third_party/redis/src/connection.h:305` | `if (connAddr(conn, ip, sizeof(ip), &port, remote) < 0) {` |
| `ev_07dda408c4ef` | call_site | `third_party/redis/src/networking.c:1734` | `sds client = catClientInfoString(sdsempty(), c);` |
| `ev_07e3132a2a76` | call_site | `third_party/redis/src/t_string.c:493` | `memcpy((char*)o->ptr+offset,value,sdslen(value));` |
| `ev_07e4927fc483` | call_site | `third_party/redis/src/connection.h:207` | `return conn->type->writev(conn, iov, iovcnt);` |
| `ev_07e79b107435` | call_site | `third_party/redis/src/networking.c:4052` | `updatePausedActions();` |
| `ev_07ffdde3f94e` | call_site | `third_party/redis/src/networking.c:1492` | `listDelNode(server.unblocked_clients,ln);` |
| `ev_080a2db8dc5a` | call_site | `third_party/redis/src/dict.c:1381` | `v = rev(v);` |
| `ev_084709873014` | call_site | `third_party/redis/src/dict.c:1321` | `dictDefragBucket(d, &d->ht_table[htidx0][v & m0], defragfns);` |
| `ev_0849802b8315` | call_site | `third_party/redis/src/networking.c:684` | `addReplyProto(c,s,len);` |
| `ev_086b8be29efa` | call_site | `third_party/redis/src/db.c:860` | `if (!stringmatchlen(data->pattern, sdslen(data->pattern), keysds, sdslen(keysds), 0)) {` |
| `ev_087a6f806095` | call_site | `third_party/redis/src/db.c:376` | `dictSetVal(db->dict, de, NULL);` |
| `ev_087e64e64315` | call_site | `third_party/redis/src/ae.c:95` | `zfree(eventLoop->fired);` |
| `ev_0883641955e8` | call_site | `third_party/redis/src/db.c:789` | `int plen = sdslen(pattern), allkeys;` |
| `ev_08ce7a4a66d5` | call_site | `third_party/redis/src/networking.c:3763` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_08df4f0e79b9` | call_site | `third_party/redis/src/db.c:1450` | `signalModifiedKey(c,dst,c->argv[2]);` |
| `ev_093a4aa5581d` | call_site | `third_party/redis/src/networking.c:2684` | `freeClientAsync(c);` |
| `ev_094df4857942` | call_site | `third_party/redis/src/networking.c:3090` | `addReplyVerbatim(c,o,sdslen(o),"txt");` |
| `ev_097aea478de1` | call_site | `third_party/redis/src/db.c:1734` | `mstime_t when = getExpire(db,key);` |
| `ev_09864d7168b6` | call_site | `third_party/redis/src/db.c:2505` | `keys = getKeysPrepareResult(result, 1);` |
| `ev_0986fd778e60` | call_site | `third_party/redis/src/networking.c:2803` | `if (connHasWriteHandler(client->conn)) *p++ = 'w';` |
| `ev_098d7aae8074` | call_site | `third_party/redis/src/networking.c:3072` | `if (getLongLongFromObjectOrReply(c, c->argv[j], &cid,` |
| `ev_09e63bd708c5` | call_site | `third_party/redis/src/db.c:802` | `addReplyBulkCBuffer(c, key, sdslen(key));` |
| `ev_09fca1747af5` | call_site | `third_party/redis/src/dict.c:772` | `assert(entryHasValue(de));` |
| `ev_0a1d6fb8b382` | call_site | `third_party/redis/src/dict.c:1504` | `he = dictGetNext(he);` |
| `ev_0a4cfdb2648d` | call_site | `third_party/redis/src/networking.c:3574` | `int auth_result = ACLAuthenticateUser(c, username, password, &err);` |
| `ev_0a605674c84e` | call_site | `third_party/redis/src/networking.c:3704` | `retainOriginalCommandVector(c);` |
| `ev_0a89dd1af9d0` | call_site | `third_party/redis/src/networking.c:3525` | `addReplySubcommandSyntaxError(c);` |
| `ev_0af43845dd25` | call_site | `third_party/redis/src/t_string.c:933` | `addReplyLongLong(c,LCS(alen,blen));` |
| `ev_0b4be458ae60` | call_site | `third_party/redis/src/networking.c:1596` | `replicationGetSlaveName(c));` |
| `ev_0b68d6c07a02` | call_site | `third_party/redis/src/db.c:1446` | `dbAdd(dst,newkey,newobj);` |
| `ev_0ba8152f5fa0` | call_site | `third_party/redis/src/dict.c:998` | `h = d->rehashidx + (randomULong() % (dictSlots(d) - d->rehashidx));` |
| `ev_0bac130f845d` | call_site | `third_party/redis/src/networking.c:4191` | `if (getIOPendingCount(id) == 0) {` |
| `ev_0bad91052b51` | call_site | `third_party/redis/src/networking.c:3115` | `addReply(c,shared.ok);` |
| `ev_0bb1e3acbc92` | call_site | `third_party/redis/src/networking.c:4389` | `listRewind(server.clients_pending_write,&li);` |
| `ev_0bf390cb2e6d` | call_site | `third_party/redis/src/connection.h:309` | `return formatAddr(buf, buf_len, ip, port);` |
| `ev_0c14861b358f` | call_site | `third_party/redis/src/db.c:1035` | `list *keys = listCreate();` |
| `ev_0c1ce48ab400` | call_site | `third_party/redis/src/networking.c:447` | `serverPanic("Wrong obj->encoding in addReply()");` |
| `ev_0cb82b93191d` | call_site | `third_party/redis/src/db.c:1274` | `dbDelete(c->db,c->argv[1]);` |
| `ev_0ccc6ee82afd` | call_site | `third_party/redis/src/db.c:183` | `robj *o = lookupKeyWrite(c->db, key);` |
| `ev_0cedd883b692` | call_site | `third_party/redis/src/dict.c:524` | `dictSetVal(d, entry, val);` |
| `ev_0cf572676e4b` | call_site | `third_party/redis/src/adlist.c:66` | `if (list->free) list->free(current->value);` |
| `ev_0d03366977d2` | call_site | `third_party/redis/src/dict.c:819` | `assert(entryHasValue(de));` |
| `ev_0d18e1cfff2c` | call_site | `third_party/redis/src/networking.c:1914` | `serverAssert(c->reply_bytes == 0);` |
| `ev_0d3c2aabd1fe` | call_site | `third_party/redis/src/networking.c:1594` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_0d91e0352c8c` | call_site | `third_party/redis/src/ae_epoll.c:51` | `zfree(state);` |
| `ev_0d9262eb9d4f` | call_site | `third_party/redis/src/networking.c:2122` | `connSetReadHandler(c->conn,readQueryFromClient);` |
| `ev_0da0ee96808e` | call_site | `third_party/redis/src/dict.c:846` | `assert(!entryIsKey(de));` |
| `ev_0dcb920898b2` | call_site | `third_party/redis/src/networking.c:1310` | `connGetLastError(conn), addr, laddr);` |
| `ev_0dd8d64cbbc7` | call_site | `third_party/redis/src/networking.c:3117` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_0e010796a6b0` | call_site | `third_party/redis/src/networking.c:3705` | `freeClientArgv(c);` |
| `ev_0e12093c2589` | call_site | `third_party/redis/src/dict.c:498` | `assert(entryIsNormal(entry)); /* Check alignment of allocation */` |
| `ev_0e226a347264` | call_site | `third_party/redis/src/networking.c:403` | `logInvalidUseAndFreeClientAsync(c, "Replica generated a reply to command '%s'",` |
| `ev_0e53148c9852` | call_site | `third_party/redis/src/db.c:1164` | `if (parseScanCursorOrReply(c,c->argv[1],&cursor) == C_ERR) return;` |
| `ev_0e9d8f792a87` | call_site | `third_party/redis/src/db.c:1496` | `robj *value = dictGetVal(kde);` |
| `ev_0ea5bf269f8e` | call_site | `third_party/redis/src/t_string.c:947` | `if (obja) decrRefCount(obja);` |
| `ev_0ea7b348f80e` | call_site | `third_party/redis/src/networking.c:3751` | `c->cmd = lookupCommandOrOriginal(c->argv,c->argc);` |
| `ev_0ecbea3b1918` | call_site | `third_party/redis/src/dict.c:979` | `dictResetIterator(iter);` |
| `ev_0ece081c87a8` | call_site | `third_party/redis/src/networking.c:2899` | `if (validateClientName(name, err) == C_ERR) {` |
| `ev_0f037516b422` | call_site | `third_party/redis/src/adlist.c:292` | `value = copy->dup(node->value);` |
| `ev_0f3e46ef81f6` | call_site | `third_party/redis/src/db.c:1300` | `addReplyError(c,"MOVE is not allowed in cluster mode");` |
| `ev_0f63aced9722` | call_site | `third_party/redis/src/t_string.c:329` | `if (checkType(c,o,OBJ_STRING)) {` |
| `ev_0f99163256c5` | call_site | `third_party/redis/src/networking.c:1617` | `dictRelease(c->pubsub_channels);` |
| `ev_0fcc15308902` | call_site | `third_party/redis/src/t_string.c:432` | `if (getGenericCommand(c) == C_ERR) return;` |
| `ev_0fdb3226d0f0` | call_site | `third_party/redis/src/dict.c:646` | `dictFreeKey(d, he);` |
| `ev_10134173367e` | call_site | `third_party/redis/src/dict.c:1325` | `next = dictGetNext(de);` |
| `ev_10380d6f75a9` | call_site | `third_party/redis/src/networking.c:1856` | `listRewind(c->reply, &iter);` |
| `ev_103eccd36cba` | call_site | `third_party/redis/src/networking.c:3477` | `addReplyBulkCString(c,"caching-no");` |
| `ev_105468c6932d` | call_site | `third_party/redis/src/lazyfree.c:178` | `db->dict = dictCreate(&dbDictType);` |
| `ev_10a009e3ec83` | call_site | `third_party/redis/src/dict.c:663` | `_dictClear(d,0,NULL);` |
| `ev_10c89dc5af18` | call_site | `third_party/redis/src/networking.c:490` | `addReplyProto(c,"\r\n",2);` |
| `ev_10ca1b26cdfe` | call_site | `third_party/redis/src/networking.c:3486` | `addReplyBulkCString(c,"broken_redirect");` |
| `ev_10ec90e33acc` | call_site | `third_party/redis/src/networking.c:2703` | `bytes = sdscatrepr(bytes,c->querybuf,64);` |
| `ev_1106588c24a5` | call_site | `third_party/redis/src/lazyfree.c:138` | `raxStop(&ri);` |
| `ev_1141eb39b06d` | call_site | `third_party/redis/src/networking.c:3624` | `addReplyBulkCString(c,"modules");` |
| `ev_11523b0b285b` | call_site | `third_party/redis/src/dict.c:572` | `void *he_key = dictGetKey(he);` |
| `ev_115b97a76d63` | call_site | `third_party/redis/src/networking.c:1976` | `"Error writing to client: %s", connGetLastError(c->conn));` |
| `ev_1169be83a392` | call_site | `third_party/redis/src/networking.c:2338` | `setProtocolError("unauth bulk length", c);` |
| `ev_11767930b113` | call_site | `third_party/redis/src/networking.c:1263` | `if (connIsLocal(conn) != 1) {` |
| `ev_118001ae76ca` | call_site | `third_party/redis/src/networking.c:4566` | `freeClient(c);` |
| `ev_11812f13c87f` | call_site | `third_party/redis/src/networking.c:2467` | `commandProcessed(c);` |
| `ev_11db66578196` | call_site | `third_party/redis/src/t_string.c:305` | `setGenericCommand(c,flags,c->argv[1],c->argv[2],expire,unit,NULL,NULL);` |
| `ev_11f46dd93be3` | call_site | `third_party/redis/src/networking.c:1192` | `listRelease(src->deferred_reply_errors);` |
| `ev_11faf50f4405` | call_site | `third_party/redis/src/networking.c:3260` | `addReply(c,shared.ok);` |
| `ev_11fe614f6838` | call_site | `third_party/redis/src/t_string.c:424` | `rewriteClientCommandVector(c,2,shared.del,c->argv[1]);` |
| `ev_120dcef1bd80` | call_site | `third_party/redis/src/lazyfree.c:169` | `decrRefCount(obj);` |
| `ev_123452ff8596` | call_site | `third_party/redis/src/db.c:2235` | `return genericGetKeys(0, 1, 2, 1, argv, argc, result);` |
| `ev_129712a7f316` | call_site | `third_party/redis/src/networking.c:3651` | `freeClientAsync(c);` |
| `ev_12a6a46e847f` | call_site | `third_party/redis/src/networking.c:505` | `listAddNodeTail(c->deferred_reply_errors, sdsnewlen(s, len));` |
| `ev_12ca6e3ece1f` | call_site | `third_party/redis/src/t_string.c:122` | `rewriteClientCommandVector(c, 5, shared.set, key, val, shared.pxat, milliseconds_obj);` |
| `ev_12dbfb51107f` | call_site | `third_party/redis/src/connection.h:405` | `return ct->conn_create();` |
| `ev_12e261114f8c` | call_site | `third_party/redis/src/t_string.c:464` | `if (checkStringLength(c,offset,sdslen(value)) != C_OK)` |
| `ev_12e73a55db2e` | call_site | `third_party/redis/src/networking.c:3744` | `if (newval) c->argv_len_sum += getStringObjectLen(newval);` |
| `ev_130da3cd0bf7` | call_site | `third_party/redis/src/ae.c:73` | `if ((eventLoop = zmalloc(sizeof(*eventLoop))) == NULL) goto err;` |
| `ev_1371e7891daf` | call_site | `third_party/redis/src/networking.c:1977` | `freeClientAsync(c);` |
| `ev_13900a788a02` | call_site | `third_party/redis/src/t_string.c:117` | `setExpire(c,c->db,key,milliseconds);` |
| `ev_13a30fce9ce3` | call_site | `third_party/redis/src/dict.c:841` | `if (entryIsNoValue(de)) return &decodeEntryNoValue(de)->next;` |
| `ev_13cc26416def` | call_site | `third_party/redis/src/t_string.c:710` | `if (checkType(c,o,OBJ_STRING))` |
| `ev_13d0558828d5` | call_site | `third_party/redis/src/db.c:2187` | `zfree(result->keys);` |
| `ev_13e0f9f07a51` | call_site | `third_party/redis/src/networking.c:2832` | `(unsigned long long) sdslen(client->querybuf),` |
| `ev_13f83eaf9321` | call_site | `third_party/redis/src/lazyfree.c:64` | `len += raxSize(index);` |
| `ev_145975289560` | call_site | `third_party/redis/src/networking.c:2337` | `addReplyError(c, "Protocol error: unauthenticated bulk length");` |
| `ev_14aacdbe167a` | call_site | `third_party/redis/src/ae.c:155` | `zfree(eventLoop);` |
| `ev_14f1111205a9` | call_site | `third_party/redis/src/networking.c:3251` | `unblockClientOnTimeout(target);` |
| `ev_14f389d56561` | call_site | `third_party/redis/src/t_string.c:624` | `new = createStringObjectFromLongLongForValue(value);` |
| `ev_1512a4725efa` | call_site | `third_party/redis/src/t_string.c:488` | `o = dbUnshareStringValue(c->db,c->argv[1],o);` |
| `ev_152d0bd2f70e` | call_site | `third_party/redis/src/networking.c:4245` | `setIOPendingCount(i, 0);` |
| `ev_15390282b3b3` | call_site | `third_party/redis/src/db.c:791` | `void *replylen = addReplyDeferredLen(c);` |
| `ev_15999ad499ed` | call_site | `third_party/redis/src/networking.c:3743` | `if (oldval) c->argv_len_sum -= getStringObjectLen(oldval);` |
| `ev_15aa6fbee8c9` | call_site | `third_party/redis/src/networking.c:753` | `trimReplyUnusedTailSpace(c);` |
| `ev_15ef0da561b0` | call_site | `third_party/redis/src/networking.c:3375` | `zfree(prefix);` |
| `ev_15f2df1860d1` | call_site | `third_party/redis/src/networking.c:1600` | `sdsfree(c->querybuf);` |
| `ev_15febc20a194` | call_site | `third_party/redis/src/networking.c:4575` | `listRewind(server.client_mem_usage_buckets[curr_bucket].clients, &bucket_iter);` |
| `ev_161116177aa9` | call_site | `third_party/redis/src/networking.c:3213` | `addReply(c,shared.ok);` |
| `ev_161aa58e4109` | call_site | `third_party/redis/src/ae.c:275` | `monotime now = getMonotonicUs();` |
| `ev_161ffd314492` | call_site | `third_party/redis/src/networking.c:4351` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_1641b8fd6d67` | call_site | `third_party/redis/src/networking.c:2706` | `sdsfree(bytes);` |
| `ev_16425502d5bf` | call_site | `third_party/redis/src/db.c:1529` | `scanDatabaseForDeletedKeys(db1, db2);` |
| `ev_16b0c3c8f5d1` | call_site | `third_party/redis/src/db.c:1431` | `case OBJ_HASH: newobj = hashTypeDup(o); break;` |
| `ev_16f64fc4cea7` | call_site | `third_party/redis/src/networking.c:1988` | `if (!clientHasPendingReplies(c)) {` |
| `ev_1703c3e2410a` | call_site | `third_party/redis/src/networking.c:2046` | `if (clientHasPendingReplies(c)) {` |
| `ev_173f0de6f8ac` | call_site | `third_party/redis/src/bio.c:174` | `bioSubmitJob(BIO_LAZY_FREE, job);` |
| `ev_1741b8a5ffd2` | call_site | `third_party/redis/src/lazyfree.c:208` | `if (functionsLibCtxfunctionsLen(functions_lib_ctx) > LAZYFREE_THRESHOLD) {` |
| `ev_1774e7a6a212` | call_site | `third_party/redis/src/t_string.c:715` | `if (checkStringLength(c,stringObjectLen(o),sdslen(append->ptr)) != C_OK)` |
| `ev_17a4b24b566f` | call_site | `third_party/redis/src/t_string.c:705` | `dbAdd(c->db,c->argv[1],c->argv[2]);` |
| `ev_17c23c1e0d98` | call_site | `third_party/redis/src/networking.c:2738` | `connFormatAddr(client->conn,addr,addr_len,remote);` |
| `ev_17c3d6815f1f` | call_site | `third_party/redis/src/db.c:1430` | `case OBJ_ZSET: newobj = zsetDup(o); break;` |
| `ev_17d963522392` | call_site | `third_party/redis/src/dict.c:1114` | `he = dictGetNext(he);` |
| `ev_17e2bcb39db9` | call_site | `third_party/redis/src/networking.c:377` | `listAddNodeTail(reply_list, tail);` |
| `ev_17ed52eeb2a9` | call_site | `third_party/redis/src/dict.c:1445` | `uint64_t hash = dictHashKey(d, key);` |
| `ev_1806e7521fa0` | call_site | `third_party/redis/src/db.c:1128` | `listRewind(keys, &li);` |
| `ev_1818e42bc7b3` | call_site | `third_party/redis/src/networking.c:805` | `clientReplyBlock *buf = zmalloc_usable(length + sizeof(clientReplyBlock), &usable_size);` |
| `ev_182063ee2343` | call_site | `third_party/redis/src/db.c:1635` | `moduleFireServerEvent(REDISMODULE_EVENT_SWAPDB,0,&si);` |
| `ev_182d29c486bd` | call_site | `third_party/redis/src/db.c:1488` | `robj *value = dictGetVal(kde);` |
| `ev_1836e2ef9c87` | call_site | `third_party/redis/src/networking.c:3453` | `addReplyMapLen(c,3);` |
| `ev_1849d97e7c28` | call_site | `third_party/redis/src/db.c:124` | `val->lru = LRU_CLOCK();` |
| `ev_18683ed4e439` | call_site | `third_party/redis/src/networking.c:444` | `size_t len = ll2string(buf,sizeof(buf),(long)obj->ptr);` |
| `ev_186f502998a2` | call_site | `third_party/redis/src/networking.c:3289` | `pauseClientsByClient(end, isPauseClientAll);` |
| `ev_187115929651` | call_site | `third_party/redis/src/networking.c:695` | `sds s = sdscatvprintf(sdsempty(),fmt,ap);` |
| `ev_187876c34110` | call_site | `third_party/redis/src/networking.c:678` | `addReplyErrorFormat(c, "invalid expire time in '%s' command",` |
| `ev_187cdf814df9` | call_site | `third_party/redis/src/networking.c:3435` | `addReplyError(c,"CLIENT CACHING NO is only valid when tracking is enabled in OPTOUT mode.");` |
| `ev_189ae4e8980d` | call_site | `third_party/redis/src/dict.c:1400` | `DICTHT_SIZE(_dictNextExp(d->ht_used[0] + 1)) * sizeof(dictEntry*),` |
| `ev_18c68f7bbc74` | call_site | `third_party/redis/src/adlist.c:79` | `listEmpty(list);` |
| `ev_190c367be16a` | call_site | `third_party/redis/src/networking.c:1046` | `addReply(c,obj);` |
| `ev_192deb5ad58f` | call_site | `third_party/redis/src/networking.c:4366` | `setIOPendingCount(j, count);` |
| `ev_194aec0265d3` | call_site | `third_party/redis/src/networking.c:878` | `const int dlen = d2string(dbuf+1,sizeof(dbuf)-1,d);` |
| `ev_1951db0555ec` | call_site | `third_party/redis/src/db.c:1686` | `notifyKeyspaceEvent(NOTIFY_EXPIRED,"expired",keyobj,db->id);` |
| `ev_19a7c2fe580f` | call_site | `third_party/redis/src/networking.c:1061` | `addReplyProto(c,"\r\n",2);` |
| `ev_19e23d5a1b7d` | call_site | `third_party/redis/src/networking.c:1881` | `serverAssert(c->bufpos == 0 && listLength(c->reply) == 0);` |
| `ev_19f6afdaca1a` | call_site | `third_party/redis/src/networking.c:3162` | `sdslen(c->argv[i+1]->ptr));` |
| `ev_1a6128ee2dde` | call_site | `third_party/redis/src/t_string.c:473` | `if (checkType(c,o,OBJ_STRING))` |
| `ev_1abc1493bfea` | call_site | `third_party/redis/src/t_string.c:103` | `addReply(c, abort_reply ? abort_reply : shared.null[c->resp]);` |
| `ev_1ac7922d1b1c` | call_site | `third_party/redis/src/dict.c:629` | `dictFreeVal(d, he);` |
| `ev_1ad8f3ee6888` | call_site | `third_party/redis/src/networking.c:195` | `c->pubsub_channels = dictCreate(&objectKeyPointerValueDictType);` |
| `ev_1ae4d641f6ab` | call_site | `third_party/redis/src/db.c:1427` | `case OBJ_STRING: newobj = dupStringObject(o); break;` |
| `ev_1aee01a458ea` | call_site | `third_party/redis/src/networking.c:2862` | `if (type != -1 && getClientType(client) != type) continue;` |
| `ev_1b027d82cd19` | call_site | `third_party/redis/src/networking.c:1595` | `serverLog(LL_NOTICE,"Connection with replica %s lost.",` |
| `ev_1b111c65efbb` | call_site | `third_party/redis/src/t_string.c:433` | `c->argv[2] = tryObjectEncoding(c->argv[2]);` |
| `ev_1b1b154135e0` | call_site | `third_party/redis/src/networking.c:4472` | `readQueryFromClient(c->conn);` |
| `ev_1b55c77a631f` | call_site | `third_party/redis/src/t_string.c:915` | `addReplyLongLong(c,arange_start);` |
| `ev_1b888e465870` | call_site | `third_party/redis/src/networking.c:3193` | `if (laddr && strcmp(getClientSockname(client),laddr) != 0) continue;` |
| `ev_1bbb9f489849` | call_site | `third_party/redis/src/db.c:206` | `notifyKeyspaceEvent(NOTIFY_NEW,"new",key,db->id);` |
| `ev_1bbdc6928867` | call_site | `third_party/redis/src/networking.c:636` | `addReplyErrorSdsEx(c, err, 0);` |
| `ev_1bbdee788973` | call_site | `third_party/redis/src/networking.c:4495` | `if (beforeNextClient(c) == C_ERR) {` |
| `ev_1c2a80a389c1` | call_site | `third_party/redis/src/networking.c:1066` | `sds reply = sdscatprintf(sdsempty(), "$%d\r\n%s\r\n", (unsigned)sdslen(s), s);` |
| `ev_1c2f13cf49dd` | call_site | `third_party/redis/src/db.c:1464` | `while((de = dictNext(di)) != NULL) {` |
| `ev_1c30ad88c98e` | call_site | `third_party/redis/src/rio.h:129` | `if (r->read(r,buf,bytes_to_read) == 0) {` |
| `ev_1c3a69bcf6a5` | call_site | `third_party/redis/src/t_string.c:683` | `dbAdd(c->db,c->argv[1],new);` |
| `ev_1c4110390a00` | call_site | `third_party/redis/src/networking.c:3246` | `if (target && target->flags & CLIENT_BLOCKED && moduleBlockedClientMayTimeout(target)) {` |
| `ev_1c4783757c2e` | call_site | `third_party/redis/src/networking.c:765` | `serverAssert(!listNodeValue(ln));` |
| `ev_1cb0396dd8b1` | call_site | `third_party/redis/src/networking.c:3365` | `zfree(prefix);` |
| `ev_1cb2881827ea` | call_site | `third_party/redis/src/networking.c:4456` | `listAddNodeTail(io_threads_list[target_id],c);` |
| `ev_1cd6fdd2c954` | call_site | `third_party/redis/src/networking.c:4370` | `listRewind(io_threads_list[0],&li);` |
| `ev_1d4e9fbc83e0` | call_site | `third_party/redis/src/networking.c:1337` | `connClose(conn);` |
| `ev_1d55fb0fc3bb` | call_site | `third_party/redis/src/db.c:1739` | `now = commandTimeSnapshot();` |
| `ev_1d744eeb95b7` | call_site | `third_party/redis/src/db.c:314` | `if (!(flags & SETKEY_NO_SIGNAL)) signalModifiedKey(c,db,key);` |
| `ev_1d7802918f0d` | call_site | `third_party/redis/src/db.c:1238` | `if (prepareForShutdown(flags) == C_OK) exit(0);` |
| `ev_1d843f750392` | call_site | `third_party/redis/src/networking.c:1967` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_1d98b662a6ff` | call_site | `third_party/redis/src/db.c:1682` | `latencyStartMonitor(expire_latency);` |
| `ev_1dbd0417711d` | call_site | `third_party/redis/src/networking.c:420` | `_addReplyProtoToList(c,server.pending_push_messages,s,len);` |
| `ev_1dbdc9bdd924` | call_site | `third_party/redis/src/dict.c:628` | `dictFreeKey(d, he);` |
| `ev_1de298318f37` | call_site | `third_party/redis/src/t_string.c:404` | `robj *milliseconds_obj = createStringObjectFromLongLong(milliseconds);` |
| `ev_1df20a62a1dc` | call_site | `third_party/redis/src/networking.c:2557` | `serverPanic("Unknown request type");` |
| `ev_1df682961309` | call_site | `third_party/redis/src/networking.c:2863` | `o = catClientInfoString(o,client);` |
| `ev_1e2a0bb429ea` | call_site | `third_party/redis/src/networking.c:1623` | `zfree(c->buf);` |
| `ev_1e368bb89b57` | call_site | `third_party/redis/src/networking.c:2858` | `sdsclear(o);` |
| `ev_1e3da0b91388` | call_site | `third_party/redis/src/networking.c:1974` | `if (connGetState(c->conn) != CONN_STATE_CONNECTED) {` |
| `ev_1e4a74d7c9d4` | call_site | `third_party/redis/src/dict.c:352` | `assert(entryIsNoValue(de));` |
| `ev_1e6bd0b40af2` | call_site | `third_party/redis/src/dict.c:1326` | `fn(privdata, de);` |
| `ev_1e8bd5e174de` | call_site | `third_party/redis/src/networking.c:4214` | `listEmpty(io_threads_list[id]);` |
| `ev_1ec65bb1a6a6` | call_site | `third_party/redis/src/networking.c:870` | `setDeferredAggregateLen(c,node,length,'>');` |
| `ev_1ef0ea0bc2c8` | call_site | `third_party/redis/src/db.c:1179` | `addReplyStatus(c, getObjectTypeName(o));` |
| `ev_1f0ff84f4c77` | call_site | `third_party/redis/src/bio.c:178` | `bio_job *job = zmalloc(sizeof(*job));` |
| `ev_1f49663258eb` | call_site | `third_party/redis/src/dict.c:159` | `assert(!entryIsKey(de));` |
| `ev_1f4bfd89be18` | call_site | `third_party/redis/src/networking.c:3080` | `o = sdscatlen(o, "\n", 1);` |
| `ev_1f52e4978060` | call_site | `third_party/redis/src/dict.c:1070` | `unsigned long i = randomULong() & maxsizemask;` |
| `ev_1f54c1c7ee0a` | call_site | `third_party/redis/src/db.c:306` | `dbAdd(db,key,val);` |
| `ev_1f6c8988251d` | call_site | `third_party/redis/src/db.c:1205` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_1f7da879f908` | call_site | `third_party/redis/src/networking.c:845` | `setDeferredReply(c, node, lenstr, lenstr_len);` |
| `ev_1f84b97750d4` | call_site | `third_party/redis/src/t_string.c:146` | `incrRefCount(c->argv[j]);` |
| `ev_1fa9faaa79f2` | call_site | `third_party/redis/src/dict.c:743` | `dictFreeVal(d, he);` |
| `ev_2005ade1ebdb` | call_site | `third_party/redis/src/networking.c:3052` | `sds o = catClientInfoString(sdsempty(), c);` |
| `ev_200f8404fac8` | call_site | `third_party/redis/src/networking.c:3184` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_2032abe779ea` | call_site | `third_party/redis/src/networking.c:3063` | `addReplyErrorFormat(c,"Unknown client type '%s'",` |
| `ev_203952121f71` | call_site | `third_party/redis/src/networking.c:614` | `afterErrorReply(c,err,strlen(err),0);` |
| `ev_206e61044923` | call_site | `third_party/redis/src/networking.c:983` | `addReplyAggregateLen(c,length,'*');` |
| `ev_2074ac620ef2` | call_site | `third_party/redis/src/t_string.c:655` | `if (getLongLongFromObjectOrReply(c, c->argv[2], &incr, NULL) != C_OK) return;` |
| `ev_2090e32d1ce5` | call_site | `third_party/redis/src/db.c:1810` | `key = createStringObject(key->ptr, sdslen(key->ptr));` |
| `ev_20bc6aa41a49` | call_site | `third_party/redis/src/t_string.c:668` | `o = lookupKeyWrite(c->db,c->argv[1]);` |
| `ev_20e3f5934caa` | call_site | `third_party/redis/src/networking.c:3077` | `client *cl = lookupClientByID(cid);` |
| `ev_20e7593d9fc3` | call_site | `third_party/redis/src/networking.c:2195` | `c->argv = zmalloc(sizeof(robj*)*c->argv_len);` |
| `ev_20f846f8d182` | call_site | `third_party/redis/src/networking.c:3660` | `c->original_argv = zmalloc(sizeof(robj*)*(c->argc));` |
| `ev_21520edd5c66` | call_site | `third_party/redis/src/dict.c:578` | `d->ht_table[table][idx] = dictGetNext(he);` |
| `ev_216dcdf6dc46` | call_site | `third_party/redis/src/db.c:858` | `sds keysds = dictGetKey(de);` |
| `ev_216eb174395a` | call_site | `third_party/redis/src/connection.h:234` | `return conn->type->set_read_handler(conn, func);` |
| `ev_2183cf74f684` | call_site | `third_party/redis/src/networking.c:1018` | `addReply(c, b ? shared.cone : shared.czero);` |
| `ev_21d9cae43ae8` | assignment | `third_party/redis/src/lazyfree.c:210` | `bioCreateLazyFreeJob(lazyFreeFunctionsCtx,1,functions_lib_ctx);` |
| `ev_21de0da8e077` | call_site | `third_party/redis/src/networking.c:1380` | `decrRefCount(c->original_argv[j]);` |
| `ev_21f1f49bffb9` | call_site | `third_party/redis/src/dict.c:1150` | `newde = defragalloc(de);` |
| `ev_21ff31ca7a27` | call_site | `third_party/redis/src/networking.c:1823` | `listRewind(c->reply, &iter);` |
| `ev_220b5c25383c` | call_site | `third_party/redis/src/db.c:313` | `if (!(flags & SETKEY_KEEPTTL)) removeExpire(db,key);` |
| `ev_221e1f7a9ee7` | call_site | `third_party/redis/src/networking.c:2123` | `if (clientHasPendingReplies(c)) putClientInPendingWriteQueue(c);` |
| `ev_227bf1703673` | call_site | `third_party/redis/src/networking.c:3096` | `addReply(c,shared.ok);` |
| `ev_22c17036f50c` | call_site | `third_party/redis/src/networking.c:697` | `addReplyStatusLength(c,s,sdslen(s));` |
| `ev_23115e9e73a0` | call_site | `third_party/redis/src/dict.c:804` | `assert(entryHasValue(de));` |
| `ev_2314cb65f2a0` | call_site | `third_party/redis/src/networking.c:1622` | `listRelease(c->reply);` |
| `ev_231adcfb98a1` | call_site | `third_party/redis/src/bio.c:183` | `bioSubmitJob(BIO_CLOSE_FILE, job);` |
| `ev_23356cbef213` | call_site | `third_party/redis/src/networking.c:1575` | `serverAssert(ln != NULL);` |
| `ev_233b33182db4` | call_site | `third_party/redis/src/db.c:312` | `incrRefCount(val);` |
| `ev_237f0e6b2698` | call_site | `third_party/redis/src/dict.c:522` | `entry = dictAddRaw(d,key,&existing);` |
| `ev_239f0dd2cdb0` | call_site | `third_party/redis/src/networking.c:1152` | `sdsfree(cmd);` |
| `ev_23b936998ad0` | call_site | `third_party/redis/src/networking.c:3617` | `else addReplyBulkCString(c,"standalone");` |
| `ev_23bbabb83e1c` | call_site | `third_party/redis/src/networking.c:71` | `case OBJ_ENCODING_EMBSTR: return sdslen(o->ptr);` |
| `ev_246b4a07c4cf` | call_site | `third_party/redis/src/t_string.c:864` | `addReplyBulkCString(c,"matches");` |
| `ev_247aa35d392a` | call_site | `third_party/redis/src/lazyfree.c:212` | `functionsLibCtxFree(functions_lib_ctx);` |
| `ev_2480a9297fc3` | call_site | `third_party/redis/src/db.c:1141` | `if (expireIfNeeded(c->db, &kobj, 0)) {` |
| `ev_24b8129f6b32` | call_site | `third_party/redis/src/dict.c:645` | `nextHe = dictGetNext(he);` |
| `ev_24b9a36b0837` | call_site | `third_party/redis/src/networking.c:3647` | `serverLog(LL_WARNING,"Possible SECURITY ATTACK detected. It looks like somebody is sending POST or Host: commands to Redis. This is likely due to an attacker attempting to use Cross Protocol Scripting to compromise your Redis instance. Connection from %s:%d aborted.", ip, port);` |
| `ev_24c05be4e466` | call_site | `third_party/redis/src/adlist.c:152` | `if ((node = zmalloc(sizeof(*node))) == NULL)` |
| `ev_253bfecfd0dc` | call_site | `third_party/redis/src/db.c:1685` | `latencyAddSampleIfNeeded("expire-del",expire_latency);` |
| `ev_2546660fe901` | call_site | `third_party/redis/src/rio.h:142` | `return r->tell(r);` |
| `ev_256c98236b54` | call_site | `third_party/redis/src/ae_epoll.c:62` | `state->events = zrealloc(state->events, sizeof(struct epoll_event)*setsize);` |
| `ev_25716c9ae69f` | call_site | `third_party/redis/src/db.c:660` | `if (server.child_type == CHILD_TYPE_RDB) killRDBChild();` |
| `ev_258128a04d42` | call_site | `third_party/redis/src/bio.c:340` | `serverLog(LL_WARNING,` |
| `ev_259c87167f60` | call_site | `third_party/redis/src/networking.c:2902` | `int len = (name != NULL) ? sdslen(name->ptr) : 0;` |
| `ev_25b382386a42` | call_site | `third_party/redis/src/db.c:542` | `redisDb *tempDb = zcalloc(sizeof(redisDb)*server.dbnum);` |
| `ev_25f4b0eccde3` | call_site | `third_party/redis/src/ae_epoll.c:54` | `anetCloexec(state->epfd);` |
| `ev_26219cbe26be` | call_site | `third_party/redis/src/t_string.c:582` | `c->argv[j+1] = tryObjectEncoding(c->argv[j+1]);` |
| `ev_2679865c40a3` | call_site | `third_party/redis/src/networking.c:154` | `c->querybuf = sdsempty();` |
| `ev_267a1d311ace` | call_site | `third_party/redis/src/dict.c:799` | `if (entryIsNoValue(de)) return decodeEntryNoValue(de)->key;` |
| `ev_267a9ef0f936` | call_site | `third_party/redis/src/t_string.c:405` | `rewriteClientCommandVector(c,3,shared.pexpireat,c->argv[1],milliseconds_obj);` |
| `ev_26bfd80647e5` | call_site | `third_party/redis/src/db.c:1148` | `addReplyArrayLen(c, 2);` |
| `ev_270b8be55327` | call_site | `third_party/redis/src/networking.c:472` | `if (prepareClientToWrite(c) != C_OK) return;` |
| `ev_273514351de7` | call_site | `third_party/redis/src/networking.c:1858` | `next = listNext(&iter);` |
| `ev_275432c13f9a` | call_site | `third_party/redis/src/db.c:334` | `keyobj = createStringObject(key,sdslen(key));` |
| `ev_275a418d0dd1` | call_site | `third_party/redis/src/networking.c:3496` | `addReplyLongLong(c,-1);` |
| `ev_2770dd4718a4` | call_site | `third_party/redis/src/networking.c:3625` | `addReplyLoadedModules(c);` |
| `ev_278304c82d6b` | call_site | `third_party/redis/src/networking.c:3855` | `class = getClientType(c);` |
| `ev_278d46ad425d` | call_site | `third_party/redis/src/adlist.c:305` | `listRelease(copy);` |
| `ev_281906162eb8` | call_site | `third_party/redis/src/networking.c:4118` | `long long ae_events = aeProcessEvents(server.el,` |
| `ev_28479b4876df` | call_site | `third_party/redis/src/networking.c:2822` | `connGetInfo(client->conn, conninfo, sizeof(conninfo)),` |
| `ev_284effa0d550` | call_site | `third_party/redis/src/t_string.c:548` | `robj *o = lookupKeyRead(c->db,c->argv[j]);` |
| `ev_285f268ad4d1` | call_site | `third_party/redis/src/db.c:1218` | `addReplyError(c, "SHUTDOWN without NOW or ABORT isn't allowed for DENY BLOCKING client");` |
| `ev_28997892e330` | call_site | `third_party/redis/src/db.c:1554` | `scanDatabaseForReadyKeys(db1);` |
| `ev_28bf269f1b3f` | call_site | `third_party/redis/src/networking.c:4423` | `listAddNodeHead(server.clients_pending_read,c);` |
| `ev_28ffee73c0c0` | call_site | `third_party/redis/src/networking.c:4516` | `putClientInPendingWriteQueue(c);` |
| `ev_291030f6318d` | call_site | `third_party/redis/src/networking.c:4375` | `listEmpty(io_threads_list[0]);` |
| `ev_292892248e4d` | call_site | `third_party/redis/src/lazyfree.c:181` | `bioCreateLazyFreeJob(lazyfreeFreeDatabase,2,oldht1,oldht2);` |
| `ev_2952cd5d71c5` | call_site | `third_party/redis/src/networking.c:593` | `afterErrorReply(c, err->ptr, sdslen(err->ptr)-2, 0); /* Ignore trailing \r\n */` |
| `ev_2959f351f925` | call_site | `third_party/redis/src/db.c:1845` | `result->keys = zmalloc(numkeys * sizeof(keyReference));` |
| `ev_2965b53ed87b` | call_site | `third_party/redis/src/dict.c:1141` | `} else if (entryIsNoValue(de)) {` |
| `ev_29880edfed82` | call_site | `third_party/redis/src/db.c:1222` | `if (!(flags & SHUTDOWN_NOSAVE) && isInsideYieldingLongCommand()) {` |
| `ev_29a9775548dc` | call_site | `third_party/redis/src/networking.c:892` | `serverAssert(start >= 0);` |
| `ev_29b2a954bf1b` | call_site | `third_party/redis/src/networking.c:2357` | `if (sdslen(c->querybuf)-c->qb_pos <= (size_t)ll+2) {` |
| `ev_29c2a84ec3f7` | call_site | `third_party/redis/src/networking.c:1734` | `sds client = catClientInfoString(sdsempty(), c);` |
| `ev_29db0979806c` | call_site | `third_party/redis/src/networking.c:1394` | `zfree(c->argv);` |
| `ev_29ea78d648b7` | call_site | `third_party/redis/src/db.c:2397` | `keys = getKeysPrepareResult(result, num);` |
| `ev_29f5086e9e6f` | call_site | `third_party/redis/src/db.c:438` | `o = createRawStringObject(decoded->ptr, sdslen(decoded->ptr));` |
| `ev_29f9142384fb` | call_site | `third_party/redis/src/networking.c:3211` | `addReplyError(c,"No such client");` |
| `ev_2a2baab784ab` | call_site | `third_party/redis/src/lazyfree.c:54` | `functionsLibCtxFree(functions_lib_ctx);` |
| `ev_2a377ac13b78` | call_site | `third_party/redis/src/networking.c:1197` | `closeClientOnOutputBufferLimitReached(dst, 1);` |
| `ev_2a6ddadfffb5` | call_site | `third_party/redis/src/t_string.c:720` | `o->ptr = sdscatlen(o->ptr,append->ptr,sdslen(append->ptr));` |
| `ev_2a9982d08059` | call_site | `third_party/redis/src/networking.c:2950` | `addReplyErrorFormat(c,` |
| `ev_2a9fb4c1b9fe` | call_site | `third_party/redis/src/dict.c:1016` | `he = dictGetNext(he);` |
| `ev_2b3d47b33d51` | call_site | `third_party/redis/src/t_string.c:319` | `c->argv[3] = tryObjectEncoding(c->argv[3]);` |
| `ev_2b67d41589b8` | call_site | `third_party/redis/src/networking.c:2303` | `serverAssertWithInfo(c,NULL,c->multibulklen > 0);` |
| `ev_2b821c83999f` | call_site | `third_party/redis/src/ae.c:334` | `now = getMonotonicUs();` |
| `ev_2b98ff2aa197` | call_site | `third_party/redis/src/lazyfree.c:45` | `dictRelease(lua_scripts);` |
| `ev_2ba892402d61` | call_site | `third_party/redis/src/dict.c:312` | `assert(DICTHT_SIZE(d->ht_size_exp[0]) > (unsigned long)d->rehashidx);` |
| `ev_2bb79fcd583d` | call_site | `third_party/redis/src/dict.c:809` | `assert(entryHasValue(de));` |
| `ev_2bc2d4e908ed` | call_site | `third_party/redis/src/dict.c:848` | `dictEntryNoValue *entry = decodeEntryNoValue(de);` |
| `ev_2bf223ddb2ef` | call_site | `third_party/redis/src/db.c:777` | `addReplyNull(c);` |
| `ev_2bfcd13c0eaa` | call_site | `third_party/redis/src/networking.c:948` | `addReplyProto(c,shared.mbulkhdr[ll]->ptr,hdr_len);` |
| `ev_2c3be0f5aaa3` | call_site | `third_party/redis/src/db.c:1480` | `dictIterator *di = dictGetSafeIterator(emptied->blocking_keys);` |
| `ev_2ca8b4c506af` | call_site | `third_party/redis/src/dict.c:586` | `he = dictGetNext(he);` |
| `ev_2cb7b57b4324` | call_site | `third_party/redis/src/networking.c:4028` | `pauseActions(PAUSE_BY_CLIENT_COMMAND, endTime, actions);` |
| `ev_2cdfc411f03b` | call_site | `third_party/redis/src/dict.c:629` | `dictFreeVal(d, he);` |
| `ev_2ce1807f7d29` | call_site | `third_party/redis/src/db.c:1230` | `addReplyErrorObject(c, shared.slowevalerr);` |
| `ev_2d41fca1bf38` | call_site | `third_party/redis/src/connection.h:451` | `return conn && conn->type == connectionTypeTls();` |
| `ev_2d77dd5af6a8` | call_site | `third_party/redis/src/db.c:470` | `dictEmpty(dbarray[j].expires,callback);` |
| `ev_2d877b161b70` | call_site | `third_party/redis/src/networking.c:2015` | `client *c = connGetPrivateData(conn);` |
| `ev_2d8d976215b5` | call_site | `third_party/redis/src/networking.c:2817` | `sds ret = sdscatfmt(s,` |
| `ev_2d8e3c56ec12` | call_site | `third_party/redis/src/networking.c:2028` | `listRewind(server.clients_pending_write,&li);` |
| `ev_2daec50101f7` | call_site | `third_party/redis/src/t_string.c:626` | `dbReplaceValue(c->db,c->argv[1],new);` |
| `ev_2e0688bf4c40` | call_site | `third_party/redis/src/networking.c:1113` | `addReplyProto(c,buf,preflen);` |
| `ev_2e283e410808` | call_site | `third_party/redis/src/dict.c:744` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_2e41fe68817e` | call_site | `third_party/redis/src/db.c:2250` | `return genericGetKeys(0, 2, 3, 1, argv, argc, result);` |
| `ev_2e6343bbaf75` | call_site | `third_party/redis/src/networking.c:79` | `clientReplyBlock *buf = zmalloc(sizeof(clientReplyBlock) + old->size);` |
| `ev_2e6afc2a9232` | call_site | `third_party/redis/src/t_string.c:684` | `signalModifiedKey(c,c->db,c->argv[1]);` |
| `ev_2e72f08b1606` | call_site | `third_party/redis/src/connection.h:219` | `int ret = conn->type->read(conn, buf, buf_len);` |
| `ev_2e875b672264` | call_site | `third_party/redis/src/networking.c:4261` | `serverLog(LL_WARNING,` |
| `ev_2ec23b21effe` | call_site | `third_party/redis/src/t_string.c:495` | `notifyKeyspaceEvent(NOTIFY_STRING,` |
| `ev_2ecf256d8052` | call_site | `third_party/redis/src/networking.c:905` | `addReplyProto(c,dbuf+start,dlen+9-start);` |
| `ev_2ee497a71b49` | call_site | `third_party/redis/src/networking.c:473` | `_addReplyToBufferOrList(c,s,len);` |
| `ev_2f16ad189be0` | call_site | `third_party/redis/src/db.c:1438` | `addReplyError(c, "unknown type object");` |
| `ev_2f3e4e042ff8` | call_site | `third_party/redis/src/db.c:1716` | `incrRefCount(argv[1]);` |
| `ev_2f99afc8c12e` | call_site | `third_party/redis/src/networking.c:1191` | `deferredAfterErrorReply(dst, src->deferred_reply_errors);` |
| `ev_2f9ed659cb05` | call_site | `third_party/redis/src/t_string.c:286` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_2f9f067210ee` | call_site | `third_party/redis/src/db.c:1469` | `signalKeyAsReady(db, key, value->type);` |
| `ev_2faa9721a7b0` | call_site | `third_party/redis/src/dict.c:159` | `assert(!entryIsKey(de));` |
| `ev_2fb1e2548842` | call_site | `third_party/redis/src/networking.c:1418` | `while((ln = listNext(&li))) {` |
| `ev_2fdb359279ec` | call_site | `third_party/redis/src/networking.c:2286` | `setProtocolError("unauth mbulk count", c);` |
| `ev_2ff293493535` | call_site | `third_party/redis/src/db.c:203` | `dictSetVal(db->dict, de, val);` |
| `ev_2fff6074ccf1` | call_site | `third_party/redis/src/networking.c:1652` | `anyOtherSlaveWaitRdb(c) == 0)` |
| `ev_3010d8b29691` | call_site | `third_party/redis/src/t_string.c:745` | `objb = lookupKeyRead(c->db,c->argv[2]);` |
| `ev_3024083c31b2` | call_site | `third_party/redis/src/networking.c:3114` | `updateClientMemUsageAndBucket(c);` |
| `ev_3037170d5e76` | call_site | `third_party/redis/src/networking.c:1625` | `freeClientArgv(c);` |
| `ev_30c449552507` | call_site | `third_party/redis/src/networking.c:3697` | `replaceClientCommandVector(c, argc, argv);` |
| `ev_30c98d6cc41b` | call_site | `third_party/redis/src/networking.c:3971` | `writeToClient(slave,0);` |
| `ev_3157466c055d` | call_site | `third_party/redis/src/networking.c:644` | `sds s = sdscatvprintf(sdsempty(),fmt,cpy);` |
| `ev_315cefbe2de2` | call_site | `third_party/redis/src/t_string.c:917` | `addReplyArrayLen(c,2);` |
| `ev_318c49a7f014` | call_site | `third_party/redis/src/t_string.c:372` | `if ((o = lookupKeyReadOrReply(c,c->argv[1],shared.null[c->resp])) == NULL)` |
| `ev_31c3e6aa63dc` | call_site | `third_party/redis/src/networking.c:2399` | `createStringObject(c->querybuf+c->qb_pos,c->bulklen);` |
| `ev_322157e8b941` | call_site | `third_party/redis/src/networking.c:3535` | `if (getLongLongFromObjectOrReply(c, c->argv[next_arg++], &ver,` |
| `ev_3234ff12d0c4` | call_site | `third_party/redis/src/networking.c:2833` | `(unsigned long long) sdsavail(client->querybuf),` |
| `ev_32461e6d30d6` | call_site | `third_party/redis/src/db.c:246` | `if (!de) de = dictFind(db->dict,key->ptr);` |
| `ev_32702ce24fdb` | call_site | `third_party/redis/src/networking.c:1900` | `incrementalTrimReplicationBacklog(REPL_BACKLOG_TRIM_BLOCKS_PER_CALL);` |
| `ev_32cb8fd0136d` | call_site | `third_party/redis/src/db.c:1472` | `dictReleaseIterator(di);` |
| `ev_32ec6c470cff` | call_site | `third_party/redis/src/dict.c:777` | `assert(entryHasValue(de));` |
| `ev_330a91cb91e5` | call_site | `third_party/redis/src/networking.c:194` | `c->watched_keys = listCreate();` |
| `ev_3338f8ed310a` | call_site | `third_party/redis/src/networking.c:3255` | `addReply(c,shared.czero);` |
| `ev_3367ce75d471` | call_site | `third_party/redis/src/networking.c:4197` | `serverAssert(getIOPendingCount(id) != 0);` |
| `ev_3385eb5e40c8` | call_site | `third_party/redis/src/db.c:991` | `patlen = sdslen(pat);` |
| `ev_3386a1623b0a` | call_site | `third_party/redis/src/networking.c:4561` | `listNode *ln = listNext(&bucket_iter);` |
| `ev_3389a619146d` | call_site | `third_party/redis/src/ae.c:309` | `now = getMonotonicUs();` |
| `ev_33d169939e81` | call_site | `third_party/redis/src/connection.h:184` | `return conn->type->blocking_connect(conn, addr, port, timeout);` |
| `ev_33d9c0a64742` | call_site | `third_party/redis/src/db.c:1352` | `addReply(c,shared.cone);` |
| `ev_34241078c347` | call_site | `third_party/redis/src/networking.c:4555` | `listRewind(server.client_mem_usage_buckets[curr_bucket].clients, &bucket_iter);` |
| `ev_3459482ea127` | call_site | `third_party/redis/src/networking.c:3054` | `addReplyVerbatim(c,o,sdslen(o),"txt");` |
| `ev_3467da5e30da` | call_site | `third_party/redis/src/t_string.c:406` | `decrRefCount(milliseconds_obj);` |
| `ev_347f29521a69` | call_site | `third_party/redis/src/dict.c:787` | `assert(entryHasValue(de));` |
| `ev_34bb2d04cb5e` | call_site | `third_party/redis/src/networking.c:2047` | `installClientWriteHandler(c);` |
| `ev_34c60338b2c6` | call_site | `third_party/redis/src/networking.c:1731` | `sds info = sdscatvprintf(sdsempty(), fmt, ap);` |
| `ev_34d6e6461649` | call_site | `third_party/redis/src/networking.c:3174` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_35452a8eb97e` | call_site | `third_party/redis/src/db.c:1419` | `addReply(c,shared.czero);` |
| `ev_357a302561d3` | call_site | `third_party/redis/src/networking.c:742` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_3585ac172874` | call_site | `third_party/redis/src/t_string.c:397` | `signalModifiedKey(c, c->db, c->argv[1]);` |
| `ev_35973eb15e7d` | call_site | `third_party/redis/src/networking.c:1369` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_35a2b6169fc4` | call_site | `third_party/redis/src/db.c:809` | `dictReleaseIterator(di);` |
| `ev_35c407ef9db2` | call_site | `third_party/redis/src/db.c:204` | `signalKeyAsReady(db, key, val->type);` |
| `ev_35c6863ae979` | call_site | `third_party/redis/src/ae_epoll.c:50` | `zfree(state->events);` |
| `ev_35c876ec8c6b` | call_site | `third_party/redis/src/networking.c:2651` | `qblen = sdslen(c->querybuf);` |
| `ev_35e004263e5e` | call_site | `third_party/redis/src/dict.c:674` | `if (dictIsRehashing(d)) _dictRehashStep(d);` |
| `ev_3605ab4bcfb7` | call_site | `third_party/redis/src/networking.c:3711` | `c->argv_len_sum += getStringObjectLen(c->argv[j]);` |
| `ev_36694a7aed37` | call_site | `third_party/redis/src/ae.c:226` | `te = zmalloc(sizeof(*te));` |
| `ev_36cef1eef5ec` | call_site | `third_party/redis/src/networking.c:4474` | `listEmpty(io_threads_list[0]);` |
| `ev_36d37f9ab4c5` | call_site | `third_party/redis/src/t_string.c:676` | `addReplyError(c,"increment would produce NaN or Infinity");` |
| `ev_371721d83a24` | call_site | `third_party/redis/src/networking.c:1164` | `sds client = catClientInfoString(sdsempty(),dst);` |
| `ev_3743c9d042fc` | call_site | `third_party/redis/src/bio.c:202` | `bioSubmitJob(BIO_AOF_FSYNC, job);` |
| `ev_37606094da5a` | call_site | `third_party/redis/src/networking.c:622` | `afterErrorReply(c,err,sdslen(err),flags);` |
| `ev_3762b6d05bd2` | call_site | `third_party/redis/src/networking.c:3747` | `if (oldval) decrRefCount(oldval);` |
| `ev_376e54d54294` | call_site | `third_party/redis/src/networking.c:3596` | `if (clientname) clientSetName(c, clientname, NULL);` |
| `ev_377c06f66551` | call_site | `third_party/redis/src/networking.c:3399` | `if (!checkPrefixCollisionsOrReply(c,prefix,numprefix)) {` |
| `ev_377f3fe02ab1` | call_site | `third_party/redis/src/dict.c:758` | `de->v.val = d->type->valDup ? d->type->valDup(d, val) : val;` |
| `ev_379f175ba36f` | call_site | `third_party/redis/src/networking.c:1654` | `killRDBChild();` |
| `ev_37d31a9ace6b` | call_site | `third_party/redis/src/networking.c:3605` | `addReplyBulkCString(c,"version");` |
| `ev_38196dbfba2e` | call_site | `third_party/redis/src/networking.c:1284` | `if (connWrite(c->conn,err,strlen(err)) == -1) {` |
| `ev_3857c3a3f459` | call_site | `third_party/redis/src/t_string.c:943` | `sdsfree(result);` |
| `ev_387bf0b10066` | call_site | `third_party/redis/src/t_string.c:815` | `lcs = ztrymalloc(lcsalloc);` |
| `ev_3944f9ebc30c` | call_site | `third_party/redis/src/db.c:688` | `forceCommandPropagation(c, PROPAGATE_REPL \| PROPAGATE_AOF);` |
| `ev_39dbda6c819a` | call_site | `third_party/redis/src/t_string.c:919` | `addReplyLongLong(c,brange_end);` |
| `ev_39e178c042b6` | call_site | `third_party/redis/src/dict.c:793` | `assert(entryHasValue(de));` |
| `ev_3a4985300a39` | call_site | `third_party/redis/src/dict.c:767` | `assert(entryHasValue(de));` |
| `ev_3ac9ad11a4ce` | call_site | `third_party/redis/src/networking.c:1527` | `discardTransaction(c);` |
| `ev_3acc2ab3682d` | call_site | `third_party/redis/src/bio.c:255` | `serverLog(LL_NOTICE,"Unable to reclaim page cache: %s", strerror(errno));` |
| `ev_3adc816a3d02` | call_site | `third_party/redis/src/dict.c:460` | `return dictInsertAtPosition(d, key, position);` |
| `ev_3b04a6cca75f` | call_site | `third_party/redis/src/networking.c:4572` | `serverLog(LL_WARNING, "Over client maxmemory after evicting all evictable clients");` |
| `ev_3b0d2705ca00` | call_site | `third_party/redis/src/t_string.c:537` | `addReply(c,shared.emptybulk);` |
| `ev_3b1394c63350` | call_site | `third_party/redis/src/networking.c:1663` | `listDelNode(l,ln);` |
| `ev_3b1f1d68b5ce` | call_site | `third_party/redis/src/networking.c:1518` | `selectDb(c,0);` |
| `ev_3b4f2f3f16b3` | call_site | `third_party/redis/src/adlist.c:287` | `listRewind(orig, &iter);` |
| `ev_3bc2a19feccc` | call_site | `third_party/redis/src/t_string.c:733` | `addReplyLongLong(c,stringObjectLen(o));` |
| `ev_3bd0161dd962` | call_site | `third_party/redis/src/adlist.c:288` | `while((node = listNext(&iter)) != NULL) {` |
| `ev_3bd0b35db2cf` | call_site | `third_party/redis/src/db.c:1331` | `expire = getExpire(c->db,c->argv[1]);` |
| `ev_3c19d97f3a2f` | call_site | `third_party/redis/src/db.c:2002` | `int has_keyspec = (getAllKeySpecsFlags(cmd, 1) & CMD_KEY_NOT_KEY);` |
| `ev_3c47071e3236` | call_site | `third_party/redis/src/db.c:562` | `emptyDbStructure(tempDb, -1, async, callback);` |
| `ev_3c527ffb584c` | call_site | `third_party/redis/src/networking.c:2510` | `return processInputBuffer(c);` |
| `ev_3c5a4dc7befb` | call_site | `third_party/redis/src/db.c:1443` | `dbDelete(dst,newkey);` |
| `ev_3c8e1dc8ced7` | call_site | `third_party/redis/src/networking.c:1722` | `listAddNodeTail(server.clients_to_close,c);` |
| `ev_3c9e2c6e3957` | call_site | `third_party/redis/src/t_string.c:715` | `if (checkStringLength(c,stringObjectLen(o),sdslen(append->ptr)) != C_OK)` |
| `ev_3cc9f4116ce1` | call_site | `third_party/redis/src/networking.c:3509` | `raxStop(&ri);` |
| `ev_3ced0bb8ae14` | call_site | `third_party/redis/src/lazyfree.c:222` | `bioCreateLazyFreeJob(lazyFreeReplicationBacklogRefMem,2,blocks,index);` |
| `ev_3d2d8765bb85` | call_site | `third_party/redis/src/db.c:2176` | `return moduleGetCommandKeysViaAPI(cmd,argv,argc,result);` |
| `ev_3d41ba4c61b6` | call_site | `third_party/redis/src/networking.c:4283` | `serverAssert(server.io_threads_active == 1);` |
| `ev_3d83f371b34e` | call_site | `third_party/redis/src/networking.c:1128` | `sdstoupper(cmd);` |
| `ev_3decf359e121` | call_site | `third_party/redis/src/dict.c:846` | `assert(!entryIsKey(de));` |
| `ev_3df4dd812355` | call_site | `third_party/redis/src/networking.c:1346` | `connFormatAddr(conn, laddr, sizeof(addr), 0);` |
| `ev_3df7225d06a7` | call_site | `third_party/redis/src/dict.c:1095` | `i = randomULong() & maxsizemask;` |
| `ev_3ecb0ca6846a` | call_site | `third_party/redis/src/networking.c:3324` | `zfree(prefix);` |
| `ev_3f0533de84e9` | call_site | `third_party/redis/src/networking.c:788` | `listDelNode(c->reply, ln);` |
| `ev_3f3569aa9135` | call_site | `third_party/redis/src/dict.c:675` | `h = dictHashKey(d, key);` |
| `ev_3f854fbd158d` | call_site | `third_party/redis/src/networking.c:2704` | `serverLog(LL_WARNING,"Closing client that reached max query buffer length: %s (qbuf initial bytes: %s)", ci, bytes);` |
| `ev_3fa008ac9c85` | call_site | `third_party/redis/src/networking.c:1658` | `if (c->replpreamble) sdsfree(c->replpreamble);` |
| `ev_3fb00cd6e0cf` | call_site | `third_party/redis/src/networking.c:2669` | `nread = connRead(c->conn, c->querybuf+qblen, readlen);` |
| `ev_3fc1a7558317` | call_site | `third_party/redis/src/db.c:776` | `if ((key = dbRandomKey(c->db)) == NULL) {` |
| `ev_3fe0976d7e11` | call_site | `third_party/redis/src/dict.c:1110` | `unsigned long r = randomULong() % (stored + 1);` |
| `ev_4002dc98b3c1` | call_site | `third_party/redis/src/networking.c:1735` | `serverLog(LL_WARNING, "%s, disconnecting it: %s", info, client);` |
| `ev_400680a38872` | call_site | `third_party/redis/src/networking.c:4352` | `listAddNodeTail(io_threads_list[0],c);` |
| `ev_4051d61d3eb7` | call_site | `third_party/redis/src/t_string.c:338` | `getGenericCommand(c);` |
| `ev_40771174112b` | call_site | `third_party/redis/src/db.c:92` | `val = dictGetVal(de);` |
| `ev_4093576150e5` | call_site | `third_party/redis/src/dict.c:725` | `if (key == de_key \|\| dictCompareKeys(d, key, de_key)) {` |
| `ev_40babd746729` | call_site | `third_party/redis/src/db.c:967` | `serverAssert(o == NULL \|\| o->type == OBJ_SET \|\| o->type == OBJ_HASH \|\|` |
| `ev_40c532010b91` | call_site | `third_party/redis/src/networking.c:3383` | `zfree(prefix);` |
| `ev_40de8cdaca28` | call_site | `third_party/redis/src/lazyfree.c:192` | `freeTrackingRadixTree(tracking);` |
| `ev_40f32c82cdf0` | call_site | `third_party/redis/src/networking.c:2016` | `writeToClient(c,1);` |
| `ev_4128683d2f2e` | call_site | `third_party/redis/src/adlist.c:216` | `if ((iter = zmalloc(sizeof(*iter))) == NULL) return NULL;` |
| `ev_412a65bbad36` | call_site | `third_party/redis/src/db.c:107` | `if (expireIfNeeded(db, key, expire_flags)) {` |
| `ev_41500545aa4f` | call_site | `third_party/redis/src/db.c:1684` | `latencyEndMonitor(expire_latency);` |
| `ev_41790acc4d07` | call_site | `third_party/redis/src/networking.c:96` | `uint64_t id = htonu64(c->id);` |
| `ev_418434766e6a` | call_site | `third_party/redis/src/db.c:1813` | `deleteExpiredKeyAndPropagate(db,key);` |
| `ev_419320cdb344` | call_site | `third_party/redis/src/networking.c:2057` | `freeClientArgv(c);` |
| `ev_421688db5524` | call_site | `third_party/redis/src/networking.c:2222` | `snprintf(buf,sizeof(buf),"Query buffer during protocol error: '%.*s' (... more %zu bytes ...) '%.*s'", PROTO_DUMP_LEN/2, c->querybuf+c->qb_pos, sdslen(c->querybuf)-c->qb_pos-PROTO_DUMP_LEN, PROTO_DUMP_LEN/2, c->querybuf+sdslen(c->querybuf)-PROTO_DUMP_LEN/2);` |
| `ev_421c2ff5df2e` | call_site | `third_party/redis/src/t_string.c:393` | `int deleted = dbGenericDelete(c->db, c->argv[1], server.lazyfree_lazy_expire, DB_FLAG_KEY_EXPIRED);` |
| `ev_4224796e3d2e` | call_site | `third_party/redis/src/db.c:565` | `dictRelease(tempDb[i].expires);` |
| `ev_42c444f7a6a7` | call_site | `third_party/redis/src/networking.c:855` | `setDeferredAggregateLen(c,node,length,prefix);` |
| `ev_42cc45376cf9` | call_site | `third_party/redis/src/t_string.c:300` | `if (parseExtendedStringArgumentsOrReply(c,&flags,&unit,&expire,COMMAND_SET) != C_OK) {` |
| `ev_42e71bd0cce4` | call_site | `third_party/redis/src/networking.c:2562` | `resetClient(c);` |
| `ev_43025406f785` | call_site | `third_party/redis/src/dict.c:841` | `if (entryIsNoValue(de)) return &decodeEntryNoValue(de)->next;` |
| `ev_4306fd555cb7` | call_site | `third_party/redis/src/networking.c:2973` | `addReplyError(c,"can only reset normal client connections");` |
| `ev_432b31961e35` | call_site | `third_party/redis/src/t_string.c:932` | `addReplyBulkCString(c,"len");` |
| `ev_436c7d355bc9` | call_site | `third_party/redis/src/db.c:1114` | `str = lpGet(p, &len, intbuf);` |
| `ev_43743221325c` | call_site | `third_party/redis/src/db.c:1959` | `serverPanic("Redis built-in command declared keys positions not matching the arity requirements.");` |
| `ev_4378a18b4103` | call_site | `third_party/redis/src/db.c:1335` | `addReply(c,shared.czero);` |
| `ev_437998e83b0b` | call_site | `third_party/redis/src/db.c:1344` | `signalModifiedKey(c,src,c->argv[1]);` |
| `ev_449b9e6e580f` | call_site | `third_party/redis/src/t_string.c:314` | `c->argv[3] = tryObjectEncoding(c->argv[3]);` |
| `ev_44e1ba3e4af2` | call_site | `third_party/redis/src/networking.c:3602` | `addReplyBulkCString(c,"server");` |
| `ev_44ef6d7a0e9d` | call_site | `third_party/redis/src/db.c:622` | `trackingInvalidateKeysOnFlush(async);` |
| `ev_4529c484de05` | call_site | `third_party/redis/src/networking.c:3353` | `zfree(prefix);` |
| `ev_4542aa7cd92e` | call_site | `third_party/redis/src/networking.c:2860` | `while ((ln = listNext(&li)) != NULL) {` |
| `ev_4568ff91d507` | call_site | `third_party/redis/src/dict.c:1158` | `d->type->afterReplaceEntry(d, newde);` |
| `ev_456eb73ac782` | call_site | `third_party/redis/src/db.c:878` | `serverPanic("Type not handled in SCAN callback.");` |
| `ev_456ed813cc6c` | call_site | `third_party/redis/src/networking.c:835` | `setDeferredReply(c, node, shared.maphdr[length]->ptr, hdr_len);` |
| `ev_458aa74306e3` | call_site | `third_party/redis/src/db.c:2022` | `return cmd->getkeys_proc(cmd,argv,argc,result);` |
| `ev_45959cb75565` | call_site | `third_party/redis/src/networking.c:2312` | `setProtocolError("too big bulk count string",c);` |
| `ev_45a9ff8412d1` | call_site | `third_party/redis/src/networking.c:1135` | `addReplyStatus(c,"HELP");` |
| `ev_45c8a6e52ff2` | call_site | `third_party/redis/src/dict.c:825` | `assert(entryHasValue(de));` |
| `ev_45f7937e701c` | call_site | `third_party/redis/src/db.c:201` | `dictSetKey(db->dict, de, sdsdup(key->ptr));` |
| `ev_45fbbe74badb` | call_site | `third_party/redis/src/networking.c:965` | `addReplyProto(c,buf,len+3);` |
| `ev_464068c129d5` | call_site | `third_party/redis/src/networking.c:3409` | `zfree(prefix);` |
| `ev_46622f689d6a` | call_site | `third_party/redis/src/networking.c:1784` | `freeClient(c);` |
| `ev_469664985032` | call_site | `third_party/redis/src/db.c:1112` | `listAddNodeTail(keys, sdsnewlen(str, len));` |
| `ev_469d4de924f7` | call_site | `third_party/redis/src/networking.c:2436` | `c->reploff = c->read_reploff - sdslen(c->querybuf) + c->qb_pos;` |
| `ev_469fe7353784` | call_site | `third_party/redis/src/dict.c:248` | `new_ht_table = ztrycalloc(newsize*sizeof(dictEntry*));` |
| `ev_46b4710f0afe` | call_site | `third_party/redis/src/dict.c:1450` | `if (_dictExpandIfNeeded(d) == DICT_ERR)` |
| `ev_471af0725da1` | call_site | `third_party/redis/src/db.c:533` | `moduleFireServerEvent(REDISMODULE_EVENT_FLUSHDB,` |
| `ev_472da8af94d3` | call_site | `third_party/redis/src/networking.c:2358` | `sdsrange(c->querybuf,c->qb_pos,-1);` |
| `ev_472ffd89589d` | call_site | `third_party/redis/src/ae.c:130` | `if (aeApiResize(eventLoop,setsize) == -1) return AE_ERR;` |
| `ev_475d2d7af6b0` | call_site | `third_party/redis/src/networking.c:736` | `if (prepareClientToWrite(c) != C_OK) return NULL;` |
| `ev_475e90a6f85c` | call_site | `third_party/redis/src/networking.c:1490` | `ln = listSearchKey(server.unblocked_clients,c);` |
| `ev_4788396f44dd` | call_site | `third_party/redis/src/networking.c:1796` | `client *c = raxFind(server.clients_index,(unsigned char*)&id,sizeof(id));` |
| `ev_47a585ec4887` | call_site | `third_party/redis/src/networking.c:4399` | `installClientWriteHandler(c);` |
| `ev_4820a8dc4714` | call_site | `third_party/redis/src/networking.c:653` | `sdsfree(s);` |
| `ev_4833b3d37165` | call_site | `third_party/redis/src/networking.c:4324` | `if (server.io_threads_num == 1 \|\| stopThreadedIOIfNeeded()) {` |
| `ev_486c2d6b9b61` | call_site | `third_party/redis/src/monotonic.h:54` | `return getMonotonicUs() - start_time;` |
| `ev_487ca34a1dad` | call_site | `third_party/redis/src/db.c:303` | `keyfound = (lookupKeyWrite(db,key) != NULL);` |
| `ev_4898cd6515d7` | call_site | `third_party/redis/src/db.c:793` | `di = dictGetSafeIterator(c->db->dict);` |
| `ev_48ba0a0ce5d6` | call_site | `third_party/redis/src/t_string.c:799` | `uint32_t blen = sdslen(b);` |
| `ev_48edb1d2303d` | call_site | `third_party/redis/src/ae.c:75` | `eventLoop->fired = zmalloc(sizeof(aeFiredEvent)*setsize);` |
| `ev_48f68ab92cd7` | call_site | `third_party/redis/src/db.c:392` | `return dbGenericDelete(db, key, 0, DB_FLAG_KEY_DELETED);` |
| `ev_4906d207cb48` | call_site | `third_party/redis/src/bio.c:156` | `listAddNodeTail(bio_jobs[worker],job);` |
| `ev_490bd08e0f65` | call_site | `third_party/redis/src/networking.c:697` | `addReplyStatusLength(c,s,sdslen(s));` |
| `ev_492675d18aab` | call_site | `third_party/redis/src/db.c:1116` | `p = lpNext(o->ptr, p);` |
| `ev_494f7b973d06` | call_site | `third_party/redis/src/t_string.c:632` | `notifyKeyspaceEvent(NOTIFY_STRING,"incrby",c->argv[1],c->db->id);` |
| `ev_49ae44e66756` | call_site | `third_party/redis/src/db.c:1151` | `addReplyArrayLen(c, listLength(keys));` |
| `ev_49cae8a4df00` | call_site | `third_party/redis/src/dict.c:742` | `dictFreeKey(d, he);` |
| `ev_4a117a0b4d04` | call_site | `third_party/redis/src/dict.c:1358` | `next = dictGetNext(de);` |
| `ev_4a4478b72e09` | call_site | `third_party/redis/src/networking.c:2159` | `aux = sdsnewlen(c->querybuf+c->qb_pos,querylen);` |
| `ev_4a72e5c008aa` | call_site | `third_party/redis/src/networking.c:1908` | `int ret = _writevToClient(c, nwritten);` |
| `ev_4a92269f584b` | call_site | `third_party/redis/src/t_string.c:726` | `addReplyLongLong(c,totlen);` |
| `ev_4acd6ced4753` | call_site | `third_party/redis/src/networking.c:3712` | `c->cmd = lookupCommandOrOriginal(c->argv,c->argc);` |
| `ev_4acdebedb496` | call_site | `third_party/redis/src/networking.c:1125` | `void *blenp = addReplyDeferredLen(c);` |
| `ev_4ad10e22fdf5` | call_site | `third_party/redis/src/db.c:2030` | `(getAllKeySpecsFlags(cmd, 1) & CMD_KEY_NOT_KEY);        /* has at least one key-spec not marked as NOT_KEY */` |
| `ev_4af951df6f18` | call_site | `third_party/redis/src/t_string.c:706` | `incrRefCount(c->argv[2]);` |
| `ev_4b167f194513` | call_site | `third_party/redis/src/networking.c:930` | `addReplyProto(c,",",1);` |
| `ev_4b3d12242169` | call_site | `third_party/redis/src/dict.c:1485` | `return dictHashKey(d, key);` |
| `ev_4b8e94afffb0` | call_site | `third_party/redis/src/networking.c:4371` | `while((ln = listNext(&li))) {` |
| `ev_4ba3f0c1d730` | call_site | `third_party/redis/src/networking.c:3918` | `sds client = catClientInfoString(sdsempty(),c);` |
| `ev_4bb6253daaeb` | call_site | `third_party/redis/src/db.c:1279` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"rename_to",` |
| `ev_4c0a7a86431a` | call_site | `third_party/redis/src/networking.c:2820` | `getClientPeerId(client),` |
| `ev_4c4456d42bf8` | call_site | `third_party/redis/src/db.c:310` | `dbSetValue(db,key,val,1,NULL);` |
| `ev_4c514fcf1287` | call_site | `third_party/redis/src/db.c:1115` | `listAddNodeTail(keys, sdsnewlen(str, len));` |
| `ev_4c635c89a630` | call_site | `third_party/redis/src/db.c:714` | `addReply(c,shared.ok);` |
| `ev_4c74df29306b` | call_site | `third_party/redis/src/ae.c:308` | `te->finalizerProc(eventLoop, te->clientData);` |
| `ev_4c7f1ea0501e` | call_site | `third_party/redis/src/networking.c:172` | `clientSetDefaultAuth(c);` |
| `ev_4cf60be7b1bb` | call_site | `third_party/redis/src/networking.c:3322` | `addReplyError(c,"The client ID you want redirect to "` |
| `ev_4d1d82c65646` | call_site | `third_party/redis/src/networking.c:2215` | `sds client = catClientInfoString(sdsempty(),c);` |
| `ev_4d202abe516f` | call_site | `third_party/redis/src/connection.h:262` | `return conn->type->sync_write(conn, ptr, size, timeout);` |
| `ev_4d6d481acbf1` | call_site | `third_party/redis/src/t_string.c:607` | `if (getLongLongFromObjectOrReply(c,o,&value,NULL) != C_OK) return;` |
| `ev_4d869d2ccfa8` | call_site | `third_party/redis/src/db.c:372` | `decrRefCount(val);` |
| `ev_4d9f45372127` | call_site | `third_party/redis/src/networking.c:4505` | `if (processPendingCommandAndInputBuffer(c) == C_ERR) {` |
| `ev_4daf2e5d7968` | call_site | `third_party/redis/src/networking.c:1226` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_4df3a3012a3a` | call_site | `third_party/redis/src/db.c:1415` | `if (lookupKeyWrite(dst,newkey) != NULL) {` |
| `ev_4e210cc07369` | call_site | `third_party/redis/src/networking.c:607` | `addReply(c, reply);` |
| `ev_4e2ecef975b6` | call_site | `third_party/redis/src/t_string.c:394` | `serverAssert(deleted);` |
| `ev_4e50e0a0c101` | call_site | `third_party/redis/src/networking.c:4209` | `readQueryFromClient(c->conn);` |
| `ev_4e5f6e89aa33` | call_site | `third_party/redis/src/db.c:1158` | `listRelease(keys);` |
| `ev_4edc2cdae9be` | assignment | `third_party/redis/src/lazyfree.c:222` | `bioCreateLazyFreeJob(lazyFreeReplicationBacklogRefMem,2,blocks,index);` |
| `ev_4efb2851357e` | call_site | `third_party/redis/src/networking.c:1303` | `if (connGetState(conn) != CONN_STATE_ACCEPTING) {` |
| `ev_4f008b058ae8` | call_site | `third_party/redis/src/networking.c:2664` | `c->querybuf = sdsMakeRoomFor(c->querybuf, readlen);` |
| `ev_4f1106e5d264` | call_site | `third_party/redis/src/networking.c:2123` | `if (clientHasPendingReplies(c)) putClientInPendingWriteQueue(c);` |
| `ev_4f15832749f7` | call_site | `third_party/redis/src/bio.c:254` | `if (reclaimFilePageCache(job->fd_args.fd, 0, 0) == -1) {` |
| `ev_4f25769c76ad` | call_site | `third_party/redis/src/networking.c:754` | `listAddNodeTail(c->reply,NULL); /* NULL is our placeholder. */` |
| `ev_4f4397f167e2` | call_site | `third_party/redis/src/networking.c:3414` | `addReply(c,shared.ok);` |
| `ev_4f54d1262656` | call_site | `third_party/redis/src/db.c:1273` | `if (expire != -1) setExpire(c,c->db,c->argv[2],expire);` |
| `ev_4f6092851d68` | call_site | `third_party/redis/src/networking.c:593` | `afterErrorReply(c, err->ptr, sdslen(err->ptr)-2, 0); /* Ignore trailing \r\n */` |
| `ev_4f6bfb6fdf91` | call_site | `third_party/redis/src/networking.c:4305` | `if (server.io_threads_active) stopThreadedIO();` |
| `ev_4faabaa1a7ac` | call_site | `third_party/redis/src/networking.c:2603` | `sdsrange(c->querybuf,c->qb_pos,-1);` |
| `ev_4fd12e9326fa` | call_site | `third_party/redis/src/networking.c:2193` | `if (c->argv) zfree(c->argv);` |
| `ev_5061b6d76a2a` | call_site | `third_party/redis/src/networking.c:3927` | `serverLog(LL_WARNING,` |
| `ev_50806b676715` | call_site | `third_party/redis/src/db.c:1842` | `result->keys = zrealloc(result->keys, numkeys * sizeof(keyReference));` |
| `ev_5087f1209efb` | call_site | `third_party/redis/src/networking.c:2808` | `size_t obufmem, total_mem = getClientMemoryUsage(client, &obufmem);` |
| `ev_50964b781121` | call_site | `third_party/redis/src/dict.c:1502` | `if (oldptr == dictGetKey(he))` |
| `ev_50b22764482f` | call_site | `third_party/redis/src/t_string.c:628` | `dbAdd(c->db,c->argv[1],new);` |
| `ev_50b3ed55bb3e` | call_site | `third_party/redis/src/monotonic.h:58` | `return elapsedUs(start_time) / 1000;` |
| `ev_50fdff3aa087` | call_site | `third_party/redis/src/networking.c:3052` | `sds o = catClientInfoString(sdsempty(), c);` |
| `ev_5115b6634f1f` | call_site | `third_party/redis/src/networking.c:2066` | `serverAssert(c->duration == 0);` |
| `ev_513f29a4eeab` | call_site | `third_party/redis/src/lazyfree.c:224` | `listRelease(blocks);` |
| `ev_51aff9b4ed60` | call_site | `third_party/redis/src/networking.c:1205` | `listRewind(errors,&li);` |
| `ev_51c873c12926` | call_site | `third_party/redis/src/networking.c:925` | `addReplyBulk(c,o);` |
| `ev_51c8aab96a97` | call_site | `third_party/redis/src/networking.c:3084` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_51cb136a7032` | call_site | `third_party/redis/src/db.c:1400` | `if (src == dst && (sdscmp(key->ptr, newkey->ptr) == 0)) {` |
| `ev_51d1ebf315ff` | call_site | `third_party/redis/src/ae.c:390` | `usUntilTimer = usUntilEarliestTimer(eventLoop);` |
| `ev_51e6bf57eb44` | call_site | `third_party/redis/src/t_string.c:520` | `strlen = sdslen(str);` |
| `ev_51f6dcb5be20` | call_site | `third_party/redis/src/db.c:782` | `decrRefCount(key);` |
| `ev_521f7d52326c` | call_site | `third_party/redis/src/db.c:1378` | `addReplyError(c,"DB index is out of range");` |
| `ev_52304984f5f5` | call_site | `third_party/redis/src/dict.c:648` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_5236bc833d23` | call_site | `third_party/redis/src/t_string.c:590` | `addReply(c, nx ? shared.cone : shared.ok);` |
| `ev_523ff994fd11` | call_site | `third_party/redis/src/db.c:2436` | `keys = getKeysPrepareResult(result, num);` |
| `ev_5256b6b16c58` | call_site | `third_party/redis/src/networking.c:1004` | `serverAssertWithInfo(c, NULL, c->flags & CLIENT_PUSHING);` |
| `ev_525fd5647de7` | call_site | `third_party/redis/src/networking.c:683` | `addReplyProto(c,"+",1);` |
| `ev_527fe98da05c` | call_site | `third_party/redis/src/db.c:1428` | `case OBJ_LIST: newobj = listTypeDup(o); break;` |
| `ev_5283bcde6093` | call_site | `third_party/redis/src/networking.c:1306` | `connFormatAddr(conn, addr, sizeof(addr), 1);` |
| `ev_5294505632ce` | call_site | `third_party/redis/src/db.c:248` | `robj *old = dictGetVal(de);` |
| `ev_52c044933a76` | call_site | `third_party/redis/src/dict.c:253` | `new_ht_table = zcalloc(newsize*sizeof(dictEntry*));` |
| `ev_52d145de3197` | call_site | `third_party/redis/src/networking.c:3103` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_52d2a233066f` | call_site | `third_party/redis/src/networking.c:1311` | `connClose(conn);` |
| `ev_5323e516b1df` | call_site | `third_party/redis/src/networking.c:1172` | `addReplyProto(dst,src->buf, src->bufpos);` |
| `ev_532c80dc63c0` | call_site | `third_party/redis/src/connection.h:313` | `return connAddr(conn, ip, ip_len, port, 1);` |
| `ev_533bb1146127` | call_site | `third_party/redis/src/bio.c:271` | `serverLog(LL_WARNING,` |
| `ev_533bb264f922` | call_site | `third_party/redis/src/networking.c:1610` | `unwatchAllKeys(c);` |
| `ev_5379a313aeea` | call_site | `third_party/redis/src/db.c:651` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_53845e44ddea` | call_site | `third_party/redis/src/networking.c:629` | `addReplyErrorSdsEx(c, err, 0);` |
| `ev_53bf4ff77444` | call_site | `third_party/redis/src/db.c:1657` | `kde = dictFind(db->dict,key->ptr);` |
| `ev_53cb3371f580` | call_site | `third_party/redis/src/db.c:1401` | `addReplyErrorObject(c,shared.sameobjecterr);` |
| `ev_53dcf910866a` | call_site | `third_party/redis/src/db.c:1646` | `return dictDelete(db->expires,key->ptr) == DICT_OK;` |
| `ev_53dd7cb0e39d` | call_site | `third_party/redis/src/networking.c:1381` | `zfree(c->original_argv);` |
| `ev_5415b4cf43b0` | call_site | `third_party/redis/src/networking.c:2680` | `sds info = catClientInfoString(sdsempty(), c);` |
| `ev_543cdc1721bf` | call_site | `third_party/redis/src/connection.h:195` | `return conn->type->write(conn, data, data_len);` |
| `ev_545dbe83d83a` | call_site | `third_party/redis/src/networking.c:4187` | `if (getIOPendingCount(id) != 0) break;` |
| `ev_546fc04284d7` | call_site | `third_party/redis/src/networking.c:673` | `addReplyErrorFormat(c, "wrong number of arguments for '%s' command",` |
| `ev_54bc7faf3035` | call_site | `third_party/redis/src/networking.c:1696` | `freeClientMultiState(c);` |
| `ev_54c42376e2b8` | call_site | `third_party/redis/src/networking.c:3695` | `incrRefCount(a);` |
| `ev_54fdea2970d3` | call_site | `third_party/redis/src/networking.c:972` | `addReply(c,shared.cone);` |
| `ev_5501e651702d` | call_site | `third_party/redis/src/networking.c:1459` | `rdbPipeWriteHandlerConnRemoved(c->conn);` |
| `ev_55247ef0523c` | call_site | `third_party/redis/src/networking.c:602` | `serverAssert(sdsEncodedObject(reply));` |
| `ev_5532685d4fd4` | call_site | `third_party/redis/src/networking.c:932` | `addReplyProto(c,"\r\n",2);` |
| `ev_557184ba5724` | call_site | `third_party/redis/src/networking.c:1887` | `*nwritten = connWrite(c->conn, o->buf+c->ref_block_pos,` |
| `ev_5574be939c72` | call_site | `third_party/redis/src/networking.c:4248` | `serverLog(LL_WARNING,"Fatal: Can't initialize IO thread.");` |
| `ev_559f3b02cbc9` | call_site | `third_party/redis/src/db.c:1664` | `rememberSlaveKeyWithExpire(db,key);` |
| `ev_55e75baf694f` | call_site | `third_party/redis/src/networking.c:3502` | `addReplyArrayLen(c,raxSize(c->client_tracking_prefixes));` |
| `ev_561a1cd73eac` | call_site | `third_party/redis/src/networking.c:951` | `addReplyProto(c,shared.bulkhdr[ll]->ptr,hdr_len);` |
| `ev_561ebab9a453` | call_site | `third_party/redis/src/monotonic.h:50` | `*start_time = getMonotonicUs();` |
| `ev_562377a959fe` | call_site | `third_party/redis/src/db.c:767` | `addReplyError(c,"DB index is out of range");` |
| `ev_5624fa996fd4` | call_site | `third_party/redis/src/networking.c:1389` | `decrRefCount(c->argv[j]);` |
| `ev_5630a7137910` | call_site | `third_party/redis/src/dict.c:147` | `dictEntryNoValue *entry = zmalloc(sizeof(*entry));` |
| `ev_564926cc3963` | call_site | `third_party/redis/src/networking.c:1248` | `if (connGetState(conn) != CONN_STATE_CONNECTED) {` |
| `ev_5657449ab9a6` | call_site | `third_party/redis/src/networking.c:1661` | `ln = listSearchKey(l,c);` |
| `ev_566e4906f83a` | call_site | `third_party/redis/src/networking.c:3054` | `addReplyVerbatim(c,o,sdslen(o),"txt");` |
| `ev_56a0cb9874fe` | call_site | `third_party/redis/src/dict.c:952` | `iter->fingerprint = dictFingerprint(iter->d);` |
| `ev_56c4348c2873` | call_site | `third_party/redis/src/networking.c:1946` | `int ret = _writeToClient(c, &nwritten);` |
| `ev_56d8c3af0ede` | call_site | `third_party/redis/src/networking.c:130` | `connSetReadHandler(conn, readQueryFromClient);` |
| `ev_571974c5c143` | call_site | `third_party/redis/src/networking.c:1607` | `dictRelease(c->bstate.keys);` |
| `ev_571e82fc9166` | call_site | `third_party/redis/src/db.c:1941` | `keys = getKeysPrepareResult(result, result->numkeys + count);` |
| `ev_57201f52da6f` | call_site | `third_party/redis/src/dict.c:648` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_574d179d10cc` | call_site | `third_party/redis/src/networking.c:2266` | `addReplyError(c,"Protocol error: too big mbulk count string");` |
| `ev_5765d66c0e30` | call_site | `third_party/redis/src/lazyfree.c:128` | `if (s->cgroups && raxSize(s->cgroups)) {` |
| `ev_5771e868f1c3` | call_site | `third_party/redis/src/networking.c:622` | `afterErrorReply(c,err,sdslen(err),flags);` |
| `ev_57a613cb8aa2` | call_site | `third_party/redis/src/networking.c:4357` | `listAddNodeTail(io_threads_list[target_id],c);` |
| `ev_57c1a59b54eb` | call_site | `third_party/redis/src/bio.c:211` | `serverAssert(worker < BIO_WORKER_NUM);` |
| `ev_57c924c99d62` | call_site | `third_party/redis/src/db.c:1343` | `dbDelete(src,c->argv[1]);` |
| `ev_57e6cdb0237d` | call_site | `third_party/redis/src/networking.c:2509` | `if (c->querybuf && sdslen(c->querybuf) > 0) {` |
| `ev_5800a63f6259` | call_site | `third_party/redis/src/t_string.c:693` | `rewriteClientCommandArgument(c,2,new);` |
| `ev_58022c18f62e` | call_site | `third_party/redis/src/dict.c:536` | `d->type->valDestructor(d, oldval);` |
| `ev_5808972800d2` | call_site | `third_party/redis/src/t_string.c:721` | `totlen = sdslen(o->ptr);` |
| `ev_587e3e46069c` | call_site | `third_party/redis/src/dict.c:1556` | `he = dictGetNext(he);` |
| `ev_5895759863f1` | call_site | `third_party/redis/src/db.c:438` | `o = createRawStringObject(decoded->ptr, sdslen(decoded->ptr));` |
| `ev_58be111ce384` | call_site | `third_party/redis/src/networking.c:2638` | `ssize_t remaining = (size_t)(c->bulklen+2)-(sdslen(c->querybuf)-c->qb_pos);` |
| `ev_59167e94886d` | call_site | `third_party/redis/src/networking.c:744` | `logInvalidUseAndFreeClientAsync(c, "Replica generated a reply to command '%s'",` |
| `ev_5950494ba62f` | call_site | `third_party/redis/src/networking.c:954` | `addReplyProto(c,shared.maphdr[ll]->ptr,hdr_len);` |
| `ev_5964c9c64f5f` | call_site | `third_party/redis/src/lazyfree.c:209` | `atomicIncr(lazyfree_objects,functionsLibCtxfunctionsLen(functions_lib_ctx));` |
| `ev_599d01ceccae` | call_site | `third_party/redis/src/db.c:439` | `decrRefCount(decoded);` |
| `ev_59e04ec76b7b` | call_site | `third_party/redis/src/db.c:1001` | `type = getObjectTypeByName(typename);` |
| `ev_59ec3afd3b19` | call_site | `third_party/redis/src/networking.c:1149` | `addReplyErrorFormat(c,` |
| `ev_5a5d5c24eee3` | call_site | `third_party/redis/src/db.c:1197` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_5a6c9adf0c83` | call_site | `third_party/redis/src/networking.c:929` | `int len = ld2string(buf,sizeof(buf),d,LD_STR_HUMAN);` |
| `ev_5a8d7b98b6fc` | call_site | `third_party/redis/src/db.c:2217` | `keys = getKeysPrepareResult(result, numkeys);` |
| `ev_5ac6a6889f5c` | call_site | `third_party/redis/src/networking.c:1446` | `listDelNode(server.clients,c->client_list_node);` |
| `ev_5acc9bc01a8a` | call_site | `third_party/redis/src/networking.c:3645` | `serverLog(LL_WARNING,"Possible SECURITY ATTACK detected. It looks like somebody is sending POST or Host: commands to Redis. This is likely due to an attacker attempting to use Cross Protocol Scripting to compromise your Redis instance. Connection aborted.");` |
| `ev_5af0b14d55b4` | call_site | `third_party/redis/src/lazyfree.c:26` | `dictRelease(ht1);` |
| `ev_5b1775dcd0d7` | call_site | `third_party/redis/src/networking.c:3270` | `addReply(c,shared.ok);` |
| `ev_5b2b709bf449` | call_site | `third_party/redis/src/networking.c:2653` | `(big_arg \|\| sdsalloc(c->querybuf) < PROTO_IOBUF_LEN)) {` |
| `ev_5b330052c1b9` | call_site | `third_party/redis/src/db.c:1637` | `addReply(c,shared.ok);` |
| `ev_5b80a305bae5` | call_site | `third_party/redis/src/networking.c:1115` | `addReplyProto(c,"\r\n",2);` |
| `ev_5bbbfce0beea` | call_site | `third_party/redis/src/networking.c:4453` | `while((ln = listNext(&li))) {` |
| `ev_5bf14f7402cd` | call_site | `third_party/redis/src/adlist.c:327` | `while((node = listNext(&iter)) != NULL) {` |
| `ev_5c193115ca66` | call_site | `third_party/redis/src/dict.c:980` | `zfree(iter);` |
| `ev_5c59c488a798` | call_site | `third_party/redis/src/dict.c:628` | `dictFreeKey(d, he);` |
| `ev_5c5e1992e371` | call_site | `third_party/redis/src/connection.h:266` | `return conn->type->sync_read(conn, ptr, size, timeout);` |
| `ev_5c61e6e646d6` | call_site | `third_party/redis/src/networking.c:3474` | `addReplyBulkCString(c,"optout");` |
| `ev_5cc1d2d208b0` | call_site | `third_party/redis/src/networking.c:1131` | `sdsfree(cmd);` |
| `ev_5cdebf78d3f1` | call_site | `third_party/redis/src/ae.c:503` | `return aeApiName();` |
| `ev_5d451c3b9226` | call_site | `third_party/redis/src/ae.c:408` | `eventLoop->aftersleep(eventLoop);` |
| `ev_5d520f12ee9d` | call_site | `third_party/redis/src/db.c:708` | `flushAllDataAndResetRDB(flags \| EMPTYDB_NOFUNCTIONS);` |
| `ev_5d5ae29cec18` | call_site | `third_party/redis/src/db.c:1311` | `if (selectDb(c,dbid) == C_ERR) {` |
| `ev_5d70f2143979` | call_site | `third_party/redis/src/networking.c:1628` | `listRelease(c->deferred_reply_errors);` |
| `ev_5d7b2be6f718` | call_site | `third_party/redis/src/networking.c:1251` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_5dae40c25d91` | call_site | `third_party/redis/src/db.c:2316` | `keys = getKeysPrepareResult(result, 2); /* Alloc 2 places for the worst case. */` |
| `ev_5e38d3a052a8` | call_site | `third_party/redis/src/networking.c:1052` | `addReplyLongLongWithPrefix(c,len,'$');` |
| `ev_5e42480bb04a` | call_site | `third_party/redis/src/networking.c:3520` | `addReply(c,shared.ok);` |
| `ev_5e65c0c50474` | call_site | `third_party/redis/src/dict.c:1359` | `fn(privdata, de);` |
| `ev_5e8494cb4b10` | call_site | `third_party/redis/src/db.c:727` | `notifyKeyspaceEvent(NOTIFY_GENERIC,` |
| `ev_5e919e0a692e` | call_site | `third_party/redis/src/dict.c:1354` | `dictDefragBucket(d, &d->ht_table[htidx0][v & m0], defragfns);` |
| `ev_5ea728e2dcc7` | call_site | `third_party/redis/src/networking.c:3459` | `addReplyBulkCString(c,c->flags & CLIENT_TRACKING ? "on" : "off");` |
| `ev_5ebe8e5c6876` | call_site | `third_party/redis/src/dict.c:1447` | `if (dictIsRehashing(d)) _dictRehashStep(d);` |
| `ev_5ec0b8f838c6` | call_site | `third_party/redis/src/networking.c:4556` | `size_t client_eviction_limit = getClientEvictionLimit();` |
| `ev_5eda95e2d810` | call_site | `third_party/redis/src/networking.c:2284` | `} else if (ll > 10 && authRequired(c)) {` |
| `ev_5f7cd89f9511` | call_site | `third_party/redis/src/db.c:570` | `slotToKeyDestroy(tempDb);` |
| `ev_5f7d5b9b50a3` | call_site | `third_party/redis/src/adlist.c:96` | `listLinkNodeHead(list, node);` |
| `ev_5fa0f819b1b8` | call_site | `third_party/redis/src/networking.c:1068` | `sdsfree(reply);` |
| `ev_5fd139e3a65b` | call_site | `third_party/redis/src/db.c:1277` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"rename_from",` |
| `ev_60035ca85e65` | call_site | `third_party/redis/src/db.c:1232` | `addReplyErrorObject(c, shared.slowscripterr);` |
| `ev_602f8d51a765` | call_site | `third_party/redis/src/db.c:269` | `freeObjAsync(key,old,db->id);` |
| `ev_60463bdf4754` | call_site | `third_party/redis/src/dict.c:1335` | `v = rev(v);` |
| `ev_606799bff691` | call_site | `third_party/redis/src/t_string.c:863` | `addReplyMapLen(c,2);` |
| `ev_606f0db6666d` | call_site | `third_party/redis/src/networking.c:454` | `if (prepareClientToWrite(c) != C_OK) {` |
| `ev_60a4d4ae1859` | call_site | `third_party/redis/src/networking.c:1530` | `pubsubUnsubscribeShardAllChannels(c, 0);` |
| `ev_60dfe1b4d525` | call_site | `third_party/redis/src/t_string.c:865` | `arraylenptr = addReplyDeferredLen(c);` |
| `ev_610c16fcbf27` | call_site | `third_party/redis/src/db.c:796` | `while((de = dictNext(di)) != NULL) {` |
| `ev_614432abb1ed` | call_site | `third_party/redis/src/networking.c:410` | `reqresSaveClientReplyOffset(c);` |
| `ev_6165ec638ef2` | call_site | `third_party/redis/src/dict.c:565` | `h = dictHashKey(d, key);` |
| `ev_617bce6b0ee9` | call_site | `third_party/redis/src/dict.c:201` | `_dictReset(d, 1);` |
| `ev_61a396e2e068` | call_site | `third_party/redis/src/db.c:1607` | `flushSlaveKeysWithExpireList();` |
| `ev_61b6edfc1ab1` | call_site | `third_party/redis/src/networking.c:4182` | `makeThreadKillable();` |
| `ev_61cf28dbd82b` | call_site | `third_party/redis/src/dict.c:352` | `assert(entryIsNoValue(de));` |
| `ev_620b7dc3159b` | call_site | `third_party/redis/src/db.c:1465` | `robj *key = dictGetKey(de);` |
| `ev_620d7e5da3bb` | call_site | `third_party/redis/src/networking.c:2147` | `addReplyError(c,"Protocol error: too big inline request");` |
| `ev_621eff5e3d3b` | call_site | `third_party/redis/src/networking.c:2574` | `if (processCommandAndResetClient(c) == C_ERR) {` |
| `ev_6220ea9dae7d` | call_site | `third_party/redis/src/networking.c:1140` | `setDeferredArrayLen(c,blenp,blen);` |
| `ev_625b93386f6c` | call_site | `third_party/redis/src/t_string.c:478` | `if (sdslen(value) == 0) {` |
| `ev_6284ec9f1e46` | call_site | `third_party/redis/src/dict.c:276` | `return _dictExpand(d, size, NULL);` |
| `ev_62d315737871` | call_site | `third_party/redis/src/db.c:1429` | `case OBJ_SET: newobj = setTypeDup(o); break;` |
| `ev_6333b79e8bd1` | call_site | `third_party/redis/src/networking.c:4211` | `serverPanic("io_threads_op value is unknown");` |
| `ev_634a2c5497c0` | call_site | `third_party/redis/src/db.c:1688` | `propagateDeletion(db,keyobj,server.lazyfree_lazy_expire);` |
| `ev_6353dc5175aa` | call_site | `third_party/redis/src/t_string.c:798` | `uint32_t alen = sdslen(a);` |
| `ev_6360959914e0` | call_site | `third_party/redis/src/dict.c:1600` | `_dictGetStatsHt(buf,bufsize,d,1,full);` |
| `ev_636f308cdcc6` | call_site | `third_party/redis/src/db.c:367` | `moduleNotifyKeyUnlink(key,val,db->id,flags);` |
| `ev_63e4ff042110` | call_site | `third_party/redis/src/networking.c:3428` | `addReplyError(c,"CLIENT CACHING YES is only valid when tracking is enabled in OPTIN mode.");` |
| `ev_640e66de7f5d` | call_site | `third_party/redis/src/networking.c:3161` | `user = ACLGetUserByName(c->argv[i+1]->ptr,` |
| `ev_64226cc441b5` | call_site | `third_party/redis/src/t_string.c:648` | `if (getLongLongFromObjectOrReply(c, c->argv[2], &incr, NULL) != C_OK) return;` |
| `ev_6439315d7748` | call_site | `third_party/redis/src/bio.c:217` | `makeThreadKillable();` |
| `ev_6440fdfbb385` | call_site | `third_party/redis/src/networking.c:3091` | `sdsfree(o);` |
| `ev_647949565d86` | call_site | `third_party/redis/src/networking.c:1215` | `serverAssert(src->bufpos == 0 && listLength(src->reply) == 0);` |
| `ev_648193372401` | call_site | `third_party/redis/src/networking.c:4381` | `pending += getIOPendingCount(j);` |
| `ev_64a3bd8dc50f` | call_site | `third_party/redis/src/networking.c:1785` | `listDelNode(server.clients_to_close,ln);` |
| `ev_64a5650af3e4` | call_site | `third_party/redis/src/networking.c:3381` | `addReplyError(c,` |
| `ev_64c7aa78d467` | call_site | `third_party/redis/src/networking.c:2906` | `if (c->name) decrRefCount(c->name);` |
| `ev_64e1befde985` | call_site | `third_party/redis/src/networking.c:659` | `addReplyErrorFormatInternal(c, flags, fmt, ap);` |
| `ev_6531455c5141` | call_site | `third_party/redis/src/networking.c:438` | `_addReplyToBufferOrList(c,obj->ptr,sdslen(obj->ptr));` |
| `ev_654f5feddfe0` | call_site | `third_party/redis/src/dict.c:782` | `assert(entryHasValue(de));` |
| `ev_6555f823adff` | call_site | `third_party/redis/src/networking.c:3511` | `addReplyArrayLen(c,0);` |
| `ev_65583515c1ed` | call_site | `third_party/redis/src/networking.c:1778` | `while ((ln = listNext(&li)) != NULL) {` |
| `ev_65cb868fd450` | call_site | `third_party/redis/src/networking.c:4006` | `while ((ln = listNext(&li)) != NULL) {` |
| `ev_65f4417f6694` | call_site | `third_party/redis/src/networking.c:652` | `afterErrorReply(c,s,sdslen(s),flags);` |
| `ev_66355456e5d5` | call_site | `third_party/redis/src/t_string.c:467` | `o = createObject(OBJ_STRING,sdsnewlen(NULL, offset+sdslen(value)));` |
| `ev_663a5283f94f` | call_site | `third_party/redis/src/t_string.c:413` | `rewriteClientCommandVector(c, 2, shared.persist, c->argv[1]);` |
| `ev_665ededf681e` | call_site | `third_party/redis/src/db.c:1270` | `dbDelete(c->db,c->argv[2]);` |
| `ev_669336e620c4` | call_site | `third_party/redis/src/t_string.c:121` | `robj *milliseconds_obj = createStringObjectFromLongLong(milliseconds);` |
| `ev_66b3ad0c7878` | call_site | `third_party/redis/src/networking.c:1067` | `setDeferredReply(c, node, reply, sdslen(reply));` |
| `ev_66cf27bf9ade` | call_site | `third_party/redis/src/dict.c:1149` | `assert(entryIsNormal(de));` |
| `ev_66e43dcdbf12` | call_site | `third_party/redis/src/dict.c:992` | `if (dictIsRehashing(d)) _dictRehashStep(d);` |
| `ev_66ebf7965a2a` | call_site | `third_party/redis/src/t_string.c:333` | `addReplyBulk(c,o);` |
| `ev_67002eabb8fe` | call_site | `third_party/redis/src/db.c:1115` | `listAddNodeTail(keys, sdsnewlen(str, len));` |
| `ev_6703c971e4dd` | call_site | `third_party/redis/src/t_string.c:679` | `new = createStringObjectFromLongDouble(value,1);` |
| `ev_67272d04594c` | call_site | `third_party/redis/src/networking.c:1229` | `serverAssert(c->bufpos == 0 && listLength(c->reply) == 0);` |
| `ev_67314de5290b` | call_site | `third_party/redis/src/networking.c:1697` | `sdsfree(c->peerid);` |
| `ev_673bf4ee702e` | call_site | `third_party/redis/src/db.c:605` | `trackingInvalidateKey(c,key,1);` |
| `ev_676e561d77f0` | call_site | `third_party/redis/src/networking.c:974` | `addReplyLongLongWithPrefix(c,ll,':');` |
| `ev_6790f837dc73` | call_site | `third_party/redis/src/networking.c:1482` | `listDelNode(server.clients_pending_read,c->pending_read_list_node);` |
| `ev_67938ccb55dc` | call_site | `third_party/redis/src/t_string.c:517` | `strlen = ll2string(llbuf,sizeof(llbuf),(long)o->ptr);` |
| `ev_67d2433b3251` | call_site | `third_party/redis/src/networking.c:4490` | `listDelNode(server.clients_pending_read,ln);` |
| `ev_6805fd49d3b1` | call_site | `third_party/redis/src/dict.c:415` | `if (d->pauserehash == 0) dictRehash(d,1);` |
| `ev_681cdbd0bbbf` | call_site | `third_party/redis/src/networking.c:3603` | `addReplyBulkCString(c,"redis");` |
| `ev_68278520f8c5` | call_site | `third_party/redis/src/dict.c:218` | `return dictExpand(d, minimal);` |
| `ev_6846c54331da` | call_site | `third_party/redis/src/networking.c:425` | `if (len > reply_len) _addReplyProtoToList(c,c->reply,s+reply_len,len-reply_len);` |
| `ev_6856b43800ac` | call_site | `third_party/redis/src/dict.c:680` | `void *he_key = dictGetKey(he);` |
| `ev_68a9bf5b49cc` | call_site | `third_party/redis/src/db.c:1486` | `dictEntry *kde = dictFind(emptied->dict, key->ptr);` |
| `ev_68c0f2955a72` | call_site | `third_party/redis/src/networking.c:2161` | `sdsfree(aux);` |
| `ev_68d286292bce` | call_site | `third_party/redis/src/lazyfree.c:202` | `dictRelease(lua_scripts);` |
| `ev_69029c47f902` | call_site | `third_party/redis/src/networking.c:1349` | `connGetLastError(conn), addr, laddr);` |
| `ev_695966500109` | call_site | `third_party/redis/src/networking.c:4398` | `if (clientHasPendingReplies(c)) {` |
| `ev_6977e23a12aa` | call_site | `third_party/redis/src/networking.c:3505` | `raxSeek(&ri,"^",NULL,0);` |
| `ev_699cf7ef25fd` | call_site | `third_party/redis/src/db.c:1090` | `listAddNodeTail(keys, sdsnewlen(key, len));` |
| `ev_6a052a9c6bdb` | call_site | `third_party/redis/src/networking.c:635` | `err = sdsmapchars(err, "\r\n", "  ",  2);` |
| `ev_6a2b7fc194aa` | call_site | `third_party/redis/src/dict.c:630` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_6a2eb1c3e0bc` | call_site | `third_party/redis/src/t_string.c:918` | `addReplyLongLong(c,brange_start);` |
| `ev_6a35609048e2` | call_site | `third_party/redis/src/db.c:1834` | `serverAssert(!result->numkeys);` |
| `ev_6a4344bb9f55` | call_site | `third_party/redis/src/networking.c:1611` | `listRelease(c->watched_keys);` |
| `ev_6a6944595a03` | call_site | `third_party/redis/src/dict.c:665` | `zfree(d);` |
| `ev_6a9a304423dd` | call_site | `third_party/redis/src/db.c:507` | `moduleFireServerEvent(REDISMODULE_EVENT_FLUSHDB,` |
| `ev_6af33a60ab36` | call_site | `third_party/redis/src/t_string.c:704` | `c->argv[2] = tryObjectEncoding(c->argv[2]);` |
| `ev_6af9965fcd69` | call_site | `third_party/redis/src/dict.c:282` | `_dictExpand(d, size, &malloc_failed);` |
| `ev_6afc9fdf27d6` | call_site | `third_party/redis/src/db.c:1250` | `if (sdscmp(c->argv[1]->ptr,c->argv[2]->ptr) == 0) samekey = 1;` |
| `ev_6ba2c165e45f` | call_site | `third_party/redis/src/db.c:690` | `addReply(c,shared.ok);` |
| `ev_6ba386dc9188` | call_site | `third_party/redis/src/networking.c:3469` | `addReplyBulkCString(c,"caching-yes");` |
| `ev_6bc3ca824519` | call_site | `third_party/redis/src/db.c:383` | `dictTwoPhaseUnlinkFree(db->dict,de,plink,table);` |
| `ev_6bfb365498cc` | call_site | `third_party/redis/src/db.c:1406` | `o = lookupKeyRead(c->db, key);` |
| `ev_6c0d00957b50` | call_site | `third_party/redis/src/db.c:330` | `de = dictGetFairRandomKey(db->dict);` |
| `ev_6c59cf1cc75a` | call_site | `third_party/redis/src/lazyfree.c:219` | `raxSize(index) > LAZYFREE_THRESHOLD)` |
| `ev_6c9d2b46a8d9` | call_site | `third_party/redis/src/connection.h:258` | `return conn->type->get_last_error(conn);` |
| `ev_6cbe83697d75` | call_site | `third_party/redis/src/db.c:1226` | `addReplyErrorFormat(c, "-BUSY %s", server.busy_module_yield_reply);` |
| `ev_6d0034d7b779` | call_site | `third_party/redis/src/t_string.c:401` | `setExpire(c,c->db,c->argv[1],milliseconds);` |
| `ev_6d1ee1e72b6e` | call_site | `third_party/redis/src/db.c:1616` | `addReplyError(c,"SWAPDB is not allowed in cluster mode");` |
| `ev_6d42ce039141` | call_site | `third_party/redis/src/networking.c:1995` | `serverAssert(io_threads_op == IO_THREADS_OP_IDLE);` |
| `ev_6d8d28e38626` | call_site | `third_party/redis/src/lazyfree.c:13` | `decrRefCount(o);` |
| `ev_6db877304dcc` | call_site | `third_party/redis/src/networking.c:1996` | `connSetWriteHandler(c->conn, NULL);` |
| `ev_6dbf4df7dd72` | call_site | `third_party/redis/src/dict.c:743` | `dictFreeVal(d, he);` |
| `ev_6de48b75991a` | call_site | `third_party/redis/src/bio.c:291` | `zfree(job);` |
| `ev_6dfd1cd42175` | call_site | `third_party/redis/src/networking.c:134` | `selectDb(c,0);` |
| `ev_6e0add7338ab` | call_site | `third_party/redis/src/dict.c:369` | `zfree(d->ht_table[0]);` |
| `ev_6e360b53a131` | call_site | `third_party/redis/src/dict.c:840` | `if (entryIsKey(de)) return NULL;` |
| `ev_6e5f567a9e2b` | call_site | `third_party/redis/src/networking.c:1185` | `listJoin(dst->reply,src->reply);` |
| `ev_6e677013f00b` | call_site | `third_party/redis/src/connection.h:275` | `return conn->type->get_type(conn);` |
| `ev_6ea50d2631cb` | call_site | `third_party/redis/src/dict.c:717` | `if (dictIsRehashing(d)) _dictRehashStep(d);` |
| `ev_6f481e2e7772` | call_site | `third_party/redis/src/db.c:524` | `if (dbnum == -1) flushSlaveKeysWithExpireList();` |
| `ev_6f67eb460bc8` | call_site | `third_party/redis/src/db.c:875` | `key = sdsdup(keysds);` |
| `ev_6f7842e7d8a2` | call_site | `third_party/redis/src/networking.c:1167` | `sdsfree(client);` |
| `ev_6f8f4beb1d18` | call_site | `third_party/redis/src/networking.c:3917` | `if (checkClientOutputBufferLimits(c)) {` |
| `ev_6f8fc2fde467` | call_site | `third_party/redis/src/db.c:706` | `if (getFlushCommandFlags(c,&flags) == C_ERR) return;` |
| `ev_6f9f7ba0a696` | call_site | `third_party/redis/src/networking.c:1945` | `while(clientHasPendingReplies(c)) {` |
| `ev_6fb598ecccd4` | call_site | `third_party/redis/src/networking.c:2390` | `c->argv[c->argc++] = createObject(OBJ_STRING,c->querybuf);` |
| `ev_6fe2c3d67e03` | call_site | `third_party/redis/src/db.c:1603` | `scanDatabaseForReadyKeys(activedb);` |
| `ev_705efc50a7d4` | call_site | `third_party/redis/src/db.c:712` | `forceCommandPropagation(c, PROPAGATE_REPL \| PROPAGATE_AOF);` |
| `ev_709453262c4c` | call_site | `third_party/redis/src/networking.c:2112` | `connSetReadHandler(c->conn,NULL);` |
| `ev_70d39c7c09a1` | call_site | `third_party/redis/src/networking.c:3450` | `addReplyLongLong(c,-1);` |
| `ev_70df37111781` | call_site | `third_party/redis/src/networking.c:582` | `serverPanic("This %s panicked sending an error to its %s"` |
| `ev_711815a012be` | call_site | `third_party/redis/src/db.c:195` | `dictEntry *de = dictAddRaw(db->dict, key->ptr, &existing);` |
| `ev_716418aa1f38` | call_site | `third_party/redis/src/networking.c:3567` | `addReplyErrorFormat(c,"Syntax error in HELLO option '%s'",opt);` |
| `ev_716767291dfa` | call_site | `third_party/redis/src/db.c:544` | `tempDb[i].dict = dictCreate(&dbDictType);` |
| `ev_7193ae6ae25b` | call_site | `third_party/redis/src/networking.c:3400` | `zfree(prefix);` |
| `ev_719a532d1229` | call_site | `third_party/redis/src/networking.c:962` | `len = ll2string(buf+1,sizeof(buf)-1,ll);` |
| `ev_71cb29641864` | call_site | `third_party/redis/src/networking.c:3203` | `freeClient(client);` |
| `ev_723ca15c3365` | call_site | `third_party/redis/src/networking.c:1717` | `listAddNodeTail(server.clients_to_close,c);` |
| `ev_724068ad84f9` | call_site | `third_party/redis/src/db.c:1129` | `while ((ln = listNext(&li))) {` |
| `ev_7265327f13e2` | call_site | `third_party/redis/src/t_string.c:315` | `setGenericCommand(c,OBJ_EX,c->argv[1],c->argv[3],c->argv[2],UNIT_SECONDS,NULL,NULL);` |
| `ev_727f1eb92a64` | call_site | `third_party/redis/src/networking.c:2372` | `if (sdslen(c->querybuf)-c->qb_pos < (size_t)(c->bulklen+2)) {` |
| `ev_729943a86022` | call_site | `third_party/redis/src/networking.c:1667` | `if (getClientType(c) == CLIENT_TYPE_SLAVE && listLength(server.slaves) == 0)` |
| `ev_733fef3ebc22` | call_site | `third_party/redis/src/dict.c:621` | `return dictGenericDelete(d,key,1);` |
| `ev_73cb7d9c21a9` | call_site | `third_party/redis/src/networking.c:1060` | `addReplySds(c,s);` |
| `ev_73ec74f36ed9` | call_site | `third_party/redis/src/t_string.c:375` | `if (checkType(c,o,OBJ_STRING)) {` |
| `ev_741ea455d3f0` | call_site | `third_party/redis/src/networking.c:1672` | `moduleFireServerEvent(REDISMODULE_EVENT_REPLICA_CHANGE,` |
| `ev_742d0bed3002` | call_site | `third_party/redis/src/networking.c:3502` | `addReplyArrayLen(c,raxSize(c->client_tracking_prefixes));` |
| `ev_745cc9150f15` | call_site | `third_party/redis/src/networking.c:3606` | `addReplyBulkCString(c,REDIS_VERSION);` |
| `ev_745d066f5414` | call_site | `third_party/redis/src/t_string.c:499` | `addReplyLongLong(c,sdslen(o->ptr));` |
| `ev_747c133a3f91` | assignment | `third_party/redis/src/networking.c:190` | `listSetFreeMethod(c->reply,freeClientReplyValue);` |
| `ev_74acd8504c06` | call_site | `third_party/redis/src/t_string.c:938` | `addReplyBulkSds(c,result);` |
| `ev_74c55ccf03c2` | call_site | `third_party/redis/src/networking.c:4451` | `listRewind(server.clients_pending_read,&li);` |
| `ev_74eaf9ef55cf` | call_site | `third_party/redis/src/db.c:663` | `rsiptr = rdbPopulateSaveInfo(&rsi);` |
| `ev_7543b267834a` | call_site | `third_party/redis/src/dict.c:656` | `_dictReset(d, htidx);` |
| `ev_754fed2b6806` | call_site | `third_party/redis/src/networking.c:1020` | `addReplyProto(c, b ? "#t\r\n" : "#f\r\n",4);` |
| `ev_755579096603` | call_site | `third_party/redis/src/bio.c:251` | `serverLog(LL_WARNING, "Fail to fsync the AOF file: %s",strerror(errno));` |
| `ev_75740557c2a3` | call_site | `third_party/redis/src/networking.c:4515` | `if (!(c->flags & CLIENT_PENDING_WRITE) && clientHasPendingReplies(c))` |
| `ev_75a46f909359` | call_site | `third_party/redis/src/networking.c:1406` | `freeClient((client*)ln->value);` |
| `ev_75b0492d6e8d` | call_site | `third_party/redis/src/db.c:1282` | `addReply(c,nx ? shared.cone : shared.ok);` |
| `ev_75ba9d436f3b` | call_site | `third_party/redis/src/networking.c:2713` | `if (processInputBuffer(c) == C_ERR)` |
| `ev_75c2cf3d8979` | call_site | `third_party/redis/src/networking.c:3269` | `unpauseActions(PAUSE_BY_CLIENT_COMMAND);` |
| `ev_75e975fe2a8e` | call_site | `third_party/redis/src/networking.c:2466` | `if (processCommand(c) == C_OK) {` |
| `ev_762846e0db58` | call_site | `third_party/redis/src/networking.c:2707` | `freeClientAsync(c);` |
| `ev_764a2f1500cd` | call_site | `third_party/redis/src/networking.c:1473` | `serverAssert(&c->clients_pending_write_node.next != NULL \|\|` |
| `ev_76668e05ca5d` | call_site | `third_party/redis/src/connection.h:174` | `return conn->type->connect(conn, addr, port, src_addr, connect_handler);` |
| `ev_76a34986acc8` | call_site | `third_party/redis/src/networking.c:1101` | `addReplyBulkCBuffer(c,s,len);` |
| `ev_76aa751f0ad7` | call_site | `third_party/redis/src/t_string.c:723` | `signalModifiedKey(c,c->db,c->argv[1]);` |
| `ev_76bc3aad4836` | call_site | `third_party/redis/src/dict.c:1137` | `void *newval = defragval ? defragval(dictGetVal(de)) : NULL;` |
| `ev_76bc54cc1732` | call_site | `third_party/redis/src/dict.c:454` | `void *position = dictFindPositionForInsert(d, key, existing);` |
| `ev_76d5e19c700a` | call_site | `third_party/redis/src/networking.c:3522` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_76d807f998c2` | call_site | `third_party/redis/src/networking.c:4394` | `updateClientMemUsageAndBucket(c);` |
| `ev_7719bf95470e` | call_site | `third_party/redis/src/networking.c:3562` | `addReplyError(c, err);` |
| `ev_771e68bdcc77` | call_site | `third_party/redis/src/networking.c:3466` | `addReplyBulkCString(c,"optin");` |
| `ev_77219ebd70de` | call_site | `third_party/redis/src/db.c:1252` | `if ((o = lookupKeyWriteOrReply(c,c->argv[1],shared.nokeyerr)) == NULL)` |
| `ev_7722dd1e0308` | call_site | `third_party/redis/src/networking.c:3600` | `addReplyMapLen(c,6 + !server.sentinel_mode);` |
| `ev_773f75698649` | call_site | `third_party/redis/src/networking.c:2821` | `getClientSockname(client),` |
| `ev_775c95065785` | call_site | `third_party/redis/src/dict.c:926` | `assert(iter->fingerprint == dictFingerprint(iter->d));` |
| `ev_77b6b2de8fd9` | call_site | `third_party/redis/src/t_string.c:920` | `if (withmatchlen) addReplyLongLong(c,match_len);` |
| `ev_77f30daf03ae` | call_site | `third_party/redis/src/networking.c:435` | `if (prepareClientToWrite(c) != C_OK) return;` |
| `ev_77fa6831f696` | call_site | `third_party/redis/src/db.c:1092` | `setTypeReleaseIterator(si);` |
| `ev_7803ab1e4eb0` | call_site | `third_party/redis/src/dict.c:916` | `dictInitIterator(iter, d);` |
| `ev_7811637b6d59` | call_site | `third_party/redis/src/networking.c:1534` | `decrRefCount(c->name);` |
| `ev_7840786f559d` | call_site | `third_party/redis/src/dict.c:832` | `if (entryIsKey(de)) return NULL; /* there's no next */` |
| `ev_7846fba0ec93` | call_site | `third_party/redis/src/dict.c:1137` | `void *newval = defragval ? defragval(dictGetVal(de)) : NULL;` |
| `ev_786917aafc2c` | call_site | `third_party/redis/src/t_string.c:546` | `addReplyArrayLen(c,c->argc-1);` |
| `ev_787bf5c8c878` | call_site | `third_party/redis/src/networking.c:1828` | `listDelNode(c->reply, next);` |
| `ev_7883c62593eb` | call_site | `third_party/redis/src/networking.c:644` | `sds s = sdscatvprintf(sdsempty(),fmt,cpy);` |
| `ev_7893cfa26736` | call_site | `third_party/redis/src/dict.c:751` | `de->key = d->type->keyDup(d, key);` |
| `ev_78c187d957f8` | call_site | `third_party/redis/src/t_string.c:658` | `addReplyError(c, "decrement would overflow");` |
| `ev_78d0f9172552` | call_site | `third_party/redis/src/dict.c:1144` | `newde = encodeMaskedPtr(newentry, ENTRY_PTR_NO_VALUE);` |
| `ev_78f501b10b8a` | call_site | `third_party/redis/src/db.c:848` | `serverAssert(!((data->type != LLONG_MAX) && o));` |
| `ev_7907482fea3d` | call_site | `third_party/redis/src/db.c:1722` | `alsoPropagate(db->id,argv,2,PROPAGATE_AOF\|PROPAGATE_REPL);` |
| `ev_7915b814e831` | call_site | `third_party/redis/src/db.c:2270` | `return genericGetKeys(0, 1, 2, 1, argv, argc, result);` |
| `ev_7930216c63a3` | call_site | `third_party/redis/src/connection.h:270` | `return conn->type->sync_readline(conn, ptr, size, timeout);` |
| `ev_7959f95c2a36` | call_site | `third_party/redis/src/networking.c:2555` | `if (processMultibulkBuffer(c) != C_OK) break;` |
| `ev_796331d87272` | call_site | `third_party/redis/src/db.c:619` | `touchAllWatchedKeysInDb(&server.db[j], NULL);` |
| `ev_797993e158e1` | call_site | `third_party/redis/src/db.c:1482` | `robj *key = dictGetKey(de);` |
| `ev_798c5a5b9b01` | call_site | `third_party/redis/src/dict.c:762` | `assert(entryHasValue(de));` |
| `ev_7990e97f9b64` | call_site | `third_party/redis/src/db.c:255` | `incrRefCount(old);` |
| `ev_79ed3e586284` | call_site | `third_party/redis/src/db.c:369` | `signalDeletedKeyAsReady(db,key,val->type);` |
| `ev_79f12cc80a66` | call_site | `third_party/redis/src/db.c:763` | `addReplyError(c,"SELECT is not allowed in cluster mode");` |
| `ev_7a0cdacc5e10` | call_site | `third_party/redis/src/networking.c:721` | `tail = zrealloc_usable(tail, tail->used + sizeof(clientReplyBlock), &usable_size);` |
| `ev_7a2d9ac4626a` | call_site | `third_party/redis/src/networking.c:3969` | `clientHasPendingReplies(slave))` |
| `ev_7a398aa61dfc` | call_site | `third_party/redis/src/connection.h:160` | `return conn->type->accept(conn, accept_handler);` |
| `ev_7a8afee52d8c` | call_site | `third_party/redis/src/networking.c:1347` | `serverLog(LL_WARNING,` |
| `ev_7af4bf1dbb9b` | call_site | `third_party/redis/src/db.c:1316` | `selectDb(c,srcid); /* Back to the source DB */` |
| `ev_7b01bce9f4ff` | call_site | `third_party/redis/src/db.c:1555` | `scanDatabaseForReadyKeys(db2);` |
| `ev_7b03719b6f25` | call_site | `third_party/redis/src/networking.c:1086` | `len = ll2string(buf,64,ll);` |
| `ev_7b0bbd832421` | call_site | `third_party/redis/src/db.c:802` | `addReplyBulkCBuffer(c, key, sdslen(key));` |
| `ev_7b24e0d2348c` | call_site | `third_party/redis/src/t_string.c:396` | `rewriteClientCommandVector(c,2,aux,c->argv[1]);` |
| `ev_7b2a7cc68095` | call_site | `third_party/redis/src/db.c:1377` | `if (selectDb(c, dbid) == C_ERR) {` |
| `ev_7b2a7ef41439` | call_site | `third_party/redis/src/networking.c:605` | `addReplyErrorObject(c, reply);` |
| `ev_7b2e033f9d9f` | call_site | `third_party/redis/src/networking.c:1067` | `setDeferredReply(c, node, reply, sdslen(reply));` |
| `ev_7b3c8f7d234e` | call_site | `third_party/redis/src/ae_epoll.c:43` | `state->events = zmalloc(sizeof(struct epoll_event)*eventLoop->setsize);` |
| `ev_7b83b1b20dda` | call_site | `third_party/redis/src/db.c:2178` | `return cmd->getkeys_proc(cmd,argv,argc,result);` |
| `ev_7b8bcac4961b` | call_site | `third_party/redis/src/t_string.c:749` | `addReplyError(c,` |
| `ev_7b955e9d1f7d` | call_site | `third_party/redis/src/t_string.c:425` | `signalModifiedKey(c, c->db, c->argv[1]);` |
| `ev_7b9ae5ffc01f` | call_site | `third_party/redis/src/t_string.c:916` | `addReplyLongLong(c,arange_end);` |
| `ev_7ba81bae4279` | call_site | `third_party/redis/src/networking.c:1066` | `sds reply = sdscatprintf(sdsempty(), "$%d\r\n%s\r\n", (unsigned)sdslen(s), s);` |
| `ev_7bcedf819320` | call_site | `third_party/redis/src/rio.h:146` | `return r->flush(r);` |
| `ev_7c2e4e876d38` | call_site | `third_party/redis/src/db.c:1606` | `trackingInvalidateKeysOnFlush(1);` |
| `ev_7c48ece0d61a` | call_site | `third_party/redis/src/connection.h:418` | `return ct->configure(priv, reconfigure);` |
| `ev_7c58d0af0a82` | call_site | `third_party/redis/src/networking.c:1320` | `if (listLength(server.clients) + getClusterConnectionsCount()` |
| `ev_7c5a5fedfd45` | call_site | `third_party/redis/src/networking.c:4325` | `return handleClientsWithPendingWrites();` |
| `ev_7c5edb215518` | call_site | `third_party/redis/src/db.c:801` | `if (!keyIsExpired(c->db, &keyobj)) {` |
| `ev_7c6af7f10e47` | call_site | `third_party/redis/src/t_string.c:499` | `addReplyLongLong(c,sdslen(o->ptr));` |
| `ev_7ca0164147c8` | call_site | `third_party/redis/src/networking.c:3049` | `addReplyLongLong(c,c->id);` |
| `ev_7cf231c872c0` | call_site | `third_party/redis/src/dict.c:1474` | `_dictClear(d,0,callback);` |
| `ev_7d0a5681af8f` | call_site | `third_party/redis/src/networking.c:1975` | `serverLog(LL_VERBOSE,` |
| `ev_7d0c51d363b4` | call_site | `third_party/redis/src/ae.c:132` | `eventLoop->events = zrealloc(eventLoop->events,sizeof(aeFileEvent)*setsize);` |
| `ev_7d0fec1e18cd` | call_site | `third_party/redis/src/networking.c:4465` | `setIOPendingCount(j, count);` |
| `ev_7d2235a3e178` | call_site | `third_party/redis/src/networking.c:1884` | `serverAssert(o->used >= c->ref_block_pos);` |
| `ev_7d3289dad49f` | call_site | `third_party/redis/src/db.c:527` | `serverAssert(dbnum == -1);` |
| `ev_7d764a124481` | call_site | `third_party/redis/src/t_string.c:701` | `o = lookupKeyWrite(c->db,c->argv[1]);` |
| `ev_7d7676acad7a` | call_site | `third_party/redis/src/networking.c:1564` | `moduleNotifyUserChanged(c);` |
| `ev_7d989d81cabc` | call_site | `third_party/redis/src/networking.c:3794` | `mem += multiStateMemOverhead(c);` |
| `ev_7de05c4bf9d3` | call_site | `third_party/redis/src/bio.c:281` | `serverLog(LL_NOTICE,"Unable to reclaim page cache: %s", strerror(errno));` |
| `ev_7deecd6b6ec7` | call_site | `third_party/redis/src/networking.c:2001` | `freeClientAsync(c);` |
| `ev_7e0bf90a8ffb` | call_site | `third_party/redis/src/networking.c:68` | `serverAssertWithInfo(NULL,o,o->type == OBJ_STRING);` |
| `ev_7e15ce178348` | call_site | `third_party/redis/src/networking.c:2113` | `connSetWriteHandler(c->conn,NULL);` |
| `ev_7e4ef83db986` | call_site | `third_party/redis/src/networking.c:2310` | `addReplyError(c,` |
| `ev_7e76059240ac` | call_site | `third_party/redis/src/networking.c:3190` | `while ((ln = listNext(&li)) != NULL) {` |
| `ev_7ea113e941cc` | call_site | `third_party/redis/src/t_string.c:439` | `rewriteClientCommandArgument(c,0,shared.set);` |
| `ev_7eddcfc64a00` | call_site | `third_party/redis/src/t_string.c:494` | `signalModifiedKey(c,c->db,c->argv[1]);` |
| `ev_7eefb777b65b` | call_site | `third_party/redis/src/db.c:210` | `dbAddInternal(db, key, val, 0);` |
| `ev_7f2f7affff76` | call_site | `third_party/redis/src/networking.c:2949` | `if (validateClientAttr(val)==C_ERR) {` |
| `ev_7f7aaec9d95b` | call_site | `third_party/redis/src/networking.c:3926` | `freeClient(c);` |
| `ev_7fc0021c8616` | call_site | `third_party/redis/src/networking.c:1370` | `freeClient(connGetPrivateData(conn));` |
| `ev_7fc46de66dc4` | call_site | `third_party/redis/src/ae.c:311` | `zfree(te);` |
| `ev_8024582df05a` | call_site | `third_party/redis/src/networking.c:1176` | `if (prepareClientToWrite(dst) != C_OK)` |
| `ev_804f046e2b2d` | call_site | `third_party/redis/src/networking.c:1030` | `addReplyProto(c,"*-1\r\n",5);` |
| `ev_8058f8896b47` | call_site | `third_party/redis/src/bio.c:289` | `serverPanic("Wrong job type in bioProcessBackgroundJobs().");` |
| `ev_805a3a2bce5f` | call_site | `third_party/redis/src/t_string.c:773` | `if (getLongLongFromObjectOrReply(c,c->argv[j+1],&minmatchlen,NULL)` |
| `ev_805dce1f33bf` | call_site | `third_party/redis/src/networking.c:4131` | `serverAssert(ProcessingEventsWhileBlocked >= 0);` |
| `ev_806ae87acb9d` | call_site | `third_party/redis/src/t_string.c:731` | `if ((o = lookupKeyReadOrReply(c,c->argv[1],shared.czero)) == NULL \|\|` |
| `ev_807c39395393` | call_site | `third_party/redis/src/networking.c:192` | `initClientBlockingState(c);` |
| `ev_809ed62fe1af` | call_site | `third_party/redis/src/networking.c:3915` | `if ((c->reply_bytes == 0 && getClientType(c) != CLIENT_TYPE_SLAVE) \|\|` |
| `ev_80af5eec03ee` | call_site | `third_party/redis/src/networking.c:1574` | `ln = listSearchKey(server.clients_to_close,c);` |
| `ev_80b774d7e558` | call_site | `third_party/redis/src/dict.c:749` | `assert(!d->type->no_value);` |
| `ev_80be1fa55945` | call_site | `third_party/redis/src/db.c:1876` | `serverAssert(result->numkeys == 0); /* caller should initialize or reset it */` |
| `ev_80d7907c301f` | call_site | `third_party/redis/src/db.c:202` | `initObjectLRUOrLFU(val);` |
| `ev_80eea1a54595` | call_site | `third_party/redis/src/connection.h:324` | `return conn->type->is_local(conn);` |
| `ev_815655607c4c` | call_site | `third_party/redis/src/networking.c:1445` | `raxRemove(server.clients_index,(unsigned char*)&id,sizeof(id),NULL);` |
| `ev_8167af54ced0` | call_site | `third_party/redis/src/networking.c:2163` | `addReplyError(c,"Protocol error: unbalanced quotes in request");` |
| `ev_8171c5ed448c` | call_site | `third_party/redis/src/db.c:308` | `dbAddInternal(db,key,val,1);` |
| `ev_81a8416d4d0b` | call_site | `third_party/redis/src/networking.c:3259` | `if (clientSetNameOrReply(c,c->argv[2]) == C_OK)` |
| `ev_81b0851f98cf` | call_site | `third_party/redis/src/networking.c:3394` | `zfree(prefix);` |
| `ev_820dcdbad62e` | call_site | `third_party/redis/src/networking.c:4469` | `listRewind(io_threads_list[0],&li);` |
| `ev_8228a720fbda` | call_site | `third_party/redis/src/db.c:378` | `if (server.cluster_enabled) slotToKeyDelEntry(de, db);` |
| `ev_822a452fba08` | call_site | `third_party/redis/src/t_string.c:553` | `addReplyNull(c);` |
| `ev_8231dd9fa534` | call_site | `third_party/redis/src/t_string.c:785` | `addReplyError(c,` |
| `ev_8236717d1395` | call_site | `third_party/redis/src/networking.c:1294` | `moduleFireServerEvent(REDISMODULE_EVENT_CLIENT_CHANGE,` |
| `ev_82706aef2b46` | call_site | `third_party/redis/src/networking.c:4005` | `listRewind(server.postponed_clients, &li);` |
| `ev_828772c24eab` | call_site | `third_party/redis/src/networking.c:3150` | `type = getClientTypeByName(c->argv[i+1]->ptr);` |
| `ev_82c6539ba888` | call_site | `third_party/redis/src/networking.c:3946` | `while((ln = listNext(&li))) {` |
| `ev_831bb6c1430b` | call_site | `third_party/redis/src/networking.c:4564` | `sds ci = catClientInfoString(sdsempty(),c);` |
| `ev_83b4c8beb5ab` | call_site | `third_party/redis/src/adlist.c:282` | `if ((copy = listCreate()) == NULL)` |
| `ev_83e5390090c3` | call_site | `third_party/redis/src/connection.h:411` | `return ct->conn_create_accepted(fd, priv);` |
| `ev_841a2b016849` | call_site | `third_party/redis/src/networking.c:3053` | `o = sdscatlen(o,"\n",1);` |
| `ev_846e1b8eb811` | call_site | `third_party/redis/src/connection.h:317` | `return connAddr(conn, ip, ip_len, port, 0);` |
| `ev_847032d34b53` | call_site | `third_party/redis/src/connection.h:432` | `return listener->ct->listen(listener);` |
| `ev_8480898966bf` | call_site | `third_party/redis/src/networking.c:1497` | `if (c->flags & CLIENT_TRACKING) disableTracking(c);` |
| `ev_84fbe65e04d2` | call_site | `third_party/redis/src/networking.c:2890` | `if (validateClientAttr(name->ptr) == C_ERR) {` |
| `ev_852371b6c66f` | call_site | `third_party/redis/src/bio.c:193` | `bioSubmitJob(BIO_CLOSE_AOF, job);` |
| `ev_852a8d5b1df7` | call_site | `third_party/redis/src/dict.c:1142` | `dictEntryNoValue *entry = decodeEntryNoValue(de), *newentry;` |
| `ev_856c28a7817f` | call_site | `third_party/redis/src/t_string.c:467` | `o = createObject(OBJ_STRING,sdsnewlen(NULL, offset+sdslen(value)));` |
| `ev_8611f77a57ea` | call_site | `third_party/redis/src/rio.h:133` | `if (r->update_cksum) r->update_cksum(r,buf,bytes_to_read);` |
| `ev_8689c5ef8bce` | call_site | `third_party/redis/src/db.c:1334` | `if (lookupKeyWrite(dst,c->argv[1]) != NULL) {` |
| `ev_8697e52c2a5f` | call_site | `third_party/redis/src/dict.c:1411` | `if (DICTHT_SIZE(d->ht_size_exp[0]) == 0) return dictExpand(d, DICT_HT_INITIAL_SIZE);` |
| `ev_86a00d8df9a3` | call_site | `third_party/redis/src/networking.c:2330` | `ok = string2ll(c->querybuf+c->qb_pos+1,newline-(c->querybuf+c->qb_pos+1),&ll);` |
| `ev_86ab370e3789` | call_site | `third_party/redis/src/networking.c:3413` | `zfree(prefix);` |
| `ev_86c7a4ae6bf9` | call_site | `third_party/redis/src/networking.c:1308` | `serverLog(LL_VERBOSE,` |
| `ev_872dbd1a1a19` | call_site | `third_party/redis/src/db.c:682` | `if (getFlushCommandFlags(c,&flags) == C_ERR) return;` |
| `ev_8734db804634` | call_site | `third_party/redis/src/networking.c:2611` | `updateClientMemUsageAndBucket(c);` |
| `ev_875d0007807f` | call_site | `third_party/redis/src/dict.c:772` | `assert(entryHasValue(de));` |
| `ev_8762df9c32a2` | call_site | `third_party/redis/src/networking.c:3616` | `else if (server.cluster_enabled) addReplyBulkCString(c,"cluster");` |
| `ev_8776761a3ad9` | call_site | `third_party/redis/src/db.c:58` | `val->lru = (LFUGetTimeInMinutes()<<8) \| counter;` |
| `ev_87a3859fda00` | call_site | `third_party/redis/src/db.c:1382` | `selectDb(c,srcid); /* Back to the source DB */` |
| `ev_87c3b8c71016` | call_site | `third_party/redis/src/networking.c:3448` | `addReplyLongLong(c,c->client_tracking_redirection);` |
| `ev_87c4e0abfef3` | call_site | `third_party/redis/src/dict.c:787` | `assert(entryHasValue(de));` |
| `ev_87e1a5af9023` | call_site | `third_party/redis/src/db.c:225` | `dictEntry *de = dictAddRaw(db->dict, key, NULL);` |
| `ev_87f96c6d89a9` | call_site | `third_party/redis/src/t_string.c:491` | `if (sdslen(value) > 0) {` |
| `ev_87fd43ae537d` | call_site | `third_party/redis/src/rio.h:113` | `if (r->update_cksum) r->update_cksum(r,buf,bytes_to_write);` |
| `ev_880e1acaadab` | call_site | `third_party/redis/src/db.c:1928` | `if (!string2ll(keynum_str,sdslen(keynum_str),&numkeys) \|\| numkeys < 0) {` |
| `ev_8827c6e259da` | call_site | `third_party/redis/src/connection.h:376` | `return conn->type->get_peer_cert(conn);` |
| `ev_8828409d7ede` | call_site | `third_party/redis/src/db.c:404` | `return dbGenericDelete(db, key, server.lazyfree_lazy_server_del, DB_FLAG_KEY_DELETED);` |
| `ev_88e96ace4f1f` | call_site | `third_party/redis/src/db.c:348` | `decrRefCount(keyobj);` |
| `ev_892e3e111b61` | call_site | `third_party/redis/src/networking.c:3517` | `addReply(c,shared.ok);` |
| `ev_8949e4043a00` | call_site | `third_party/redis/src/t_string.c:408` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"expire",c->argv[1],c->db->id);` |
| `ev_8953a0ca44f5` | call_site | `third_party/redis/src/dict.c:576` | `dictSetNext(prevHe, dictGetNext(he));` |
| `ev_8958aa19789b` | call_site | `third_party/redis/src/networking.c:2675` | `freeClientAsync(c);` |
| `ev_8979f374950a` | call_site | `third_party/redis/src/db.c:1135` | `robj* typecheck = lookupKeyReadWithFlags(c->db, &kobj, LOOKUP_NOTOUCH\|LOOKUP_NONOTIFY);` |
| `ev_898fc7f66a6c` | call_site | `third_party/redis/src/db.c:1229` | `} else if (scriptIsEval()) {` |
| `ev_89bb74189a2a` | call_site | `third_party/redis/src/networking.c:2237` | `sdsfree(client);` |
| `ev_89c363603b24` | call_site | `third_party/redis/src/t_string.c:326` | `if ((o = lookupKeyReadOrReply(c,c->argv[1],shared.null[c->resp])) == NULL)` |
| `ev_89c63eace17e` | call_site | `third_party/redis/src/db.c:1579` | `scanDatabaseForDeletedKeys(activedb, newdb);` |
| `ev_89c91fdabcb8` | call_site | `third_party/redis/src/networking.c:2146` | `if (sdslen(c->querybuf)-c->qb_pos > PROTO_INLINE_MAX_SIZE) {` |
| `ev_89ce312d8681` | call_site | `third_party/redis/src/networking.c:1069` | `sdsfree(s);` |
| `ev_89e91dd54bfc` | call_site | `third_party/redis/src/db.c:1321` | `addReplyErrorObject(c,shared.sameobjecterr);` |
| `ev_8a083ed5ed75` | call_site | `third_party/redis/src/networking.c:2362` | `c->querybuf = sdsMakeRoomForNonGreedy(c->querybuf,ll+2-sdslen(c->querybuf));` |
| `ev_8a8cc8e32756` | call_site | `third_party/redis/src/networking.c:924` | `robj *o = createStringObjectFromLongDouble(d,1);` |
| `ev_8adc4dac304b` | call_site | `third_party/redis/src/networking.c:2927` | `int result = clientSetName(c, name, &err);` |
| `ev_8b536e0b17b0` | call_site | `third_party/redis/src/dict.c:647` | `dictFreeVal(d, he);` |
| `ev_8b8775833ede` | call_site | `third_party/redis/src/networking.c:2326` | `setProtocolError("expected $ but got something else",c);` |
| `ev_8b88f843a4e4` | call_site | `third_party/redis/src/networking.c:650` | `s = sdsmapchars(s, "\r\n", "  ",  2);` |
| `ev_8bb8f32da9dc` | call_site | `third_party/redis/src/networking.c:2072` | `listRelease(c->deferred_reply_errors);` |
| `ev_8bd8631146c5` | call_site | `third_party/redis/src/networking.c:1531` | `pubsubUnsubscribeAllPatterns(c,0);` |
| `ev_8becb4af35bf` | call_site | `third_party/redis/src/networking.c:3351` | `addReplyError(c,` |
| `ev_8bed16a2d7ca` | call_site | `third_party/redis/src/networking.c:2929` | `addReplyError(c, err);` |
| `ev_8c049d564eae` | call_site | `third_party/redis/src/networking.c:459` | `_addReplyToBufferOrList(c,s,sdslen(s));` |
| `ev_8c14b11d18f4` | call_site | `third_party/redis/src/t_string.c:948` | `if (objb) decrRefCount(objb);` |
| `ev_8c239ace6bb0` | call_site | `third_party/redis/src/dict.c:533` | `void *oldval = dictGetVal(existing);` |
| `ev_8c278be8f828` | call_site | `third_party/redis/src/networking.c:1698` | `sdsfree(c->sockname);` |
| `ev_8c39728e4452` | call_site | `third_party/redis/src/db.c:722` | `expireIfNeeded(c->db,c->argv[j],0);` |
| `ev_8c3f6ef14796` | call_site | `third_party/redis/src/networking.c:215` | `if (conn) linkClient(c);` |
| `ev_8c508b90e815` | call_site | `third_party/redis/src/networking.c:970` | `addReply(c,shared.czero);` |
| `ev_8c52caa84717` | call_site | `third_party/redis/src/t_string.c:366` | `if (parseExtendedStringArgumentsOrReply(c,&flags,&unit,&expire,COMMAND_GET) != C_OK) {` |
| `ev_8c8861c5ca75` | call_site | `third_party/redis/src/networking.c:59` | `case OBJ_ENCODING_RAW: return sdsZmallocSize(o->ptr);` |
| `ev_8c9fdb745b6d` | call_site | `third_party/redis/src/t_string.c:573` | `if (lookupKeyWrite(c->db,c->argv[j]) != NULL) {` |
| `ev_8cdf38571831` | call_site | `third_party/redis/src/db.c:726` | `signalModifiedKey(c,c->db,c->argv[j]);` |
| `ev_8d28f0880f9e` | call_site | `third_party/redis/src/db.c:934` | `serverAssert(o->type >= 0 && o->type < OBJ_TYPE_MAX);` |
| `ev_8d3587f0168d` | call_site | `third_party/redis/src/networking.c:913` | `addReplyProto(c,"(",1);` |
| `ev_8d482f30e7ce` | call_site | `third_party/redis/src/t_string.c:719` | `o = dbUnshareStringValue(c->db,c->argv[1],o);` |
| `ev_8d80c775b754` | call_site | `third_party/redis/src/db.c:1265` | `addReply(c,shared.czero);` |
| `ev_8d8c00beb623` | call_site | `third_party/redis/src/networking.c:889` | `const int dlen = d2string(dbuf+7,sizeof(dbuf)-7,d);` |
| `ev_8d8dc65c80dc` | call_site | `third_party/redis/src/db.c:1631` | `addReplyError(c,"DB index is out of range");` |
| `ev_8d93b9c60e7a` | call_site | `third_party/redis/src/networking.c:445` | `_addReplyToBufferOrList(c,buf,len);` |
| `ev_8dc8a55f381c` | call_site | `third_party/redis/src/networking.c:1777` | `listRewind(server.clients_to_close,&li);` |
| `ev_8dcb8e027b8f` | call_site | `third_party/redis/src/db.c:334` | `keyobj = createStringObject(key,sdslen(key));` |
| `ev_8df96fb596ff` | call_site | `third_party/redis/src/networking.c:2009` | `updateClientMemUsageAndBucket(c);` |
| `ev_8e0a35be25ec` | call_site | `third_party/redis/src/db.c:398` | `return dbGenericDelete(db, key, 1, DB_FLAG_KEY_DELETED);` |
| `ev_8e15e1e55caa` | call_site | `third_party/redis/src/networking.c:621` | `addReplyErrorLength(c,err,sdslen(err));` |
| `ev_8e429a5342ec` | call_site | `third_party/redis/src/db.c:2240` | `return genericGetKeys(1, 2, 3, 1, argv, argc, result);` |
| `ev_8e464db21c77` | call_site | `third_party/redis/src/networking.c:4273` | `serverAssert(server.io_threads_active == 0);` |
| `ev_8e7418746121` | call_site | `third_party/redis/src/networking.c:1618` | `dictRelease(c->pubsub_patterns);` |
| `ev_8e74de8e4218` | call_site | `third_party/redis/src/networking.c:3507` | `addReplyBulkCBuffer(c,ri.key,ri.key_len);` |
| `ev_8e9ca964cc37` | call_site | `third_party/redis/src/lazyfree.c:190` | `bioCreateLazyFreeJob(lazyFreeTrackingTable,1,tracking);` |
| `ev_8eaa53b6250c` | call_site | `third_party/redis/src/dict.c:744` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_8ed7560ad5bb` | call_site | `third_party/redis/src/adlist.c:93` | `if ((node = zmalloc(sizeof(*node))) == NULL)` |
| `ev_8efe32f161b1` | call_site | `third_party/redis/src/bio.c:145` | `serverLog(LL_WARNING, "Fatal: Can't initialize Background Jobs. Error message: %s", strerror(errno));` |
| `ev_8f17035919de` | call_site | `third_party/redis/src/networking.c:1688` | `listDelNode(c->mem_usage_bucket->clients, c->mem_usage_bucket_node);` |
| `ev_8f5aff8c04fd` | call_site | `third_party/redis/src/networking.c:4373` | `writeToClient(c,0);` |
| `ev_8f741e0a8aed` | call_site | `third_party/redis/src/t_string.c:550` | `addReplyNull(c);` |
| `ev_8fa966c2db54` | call_site | `third_party/redis/src/networking.c:1693` | `if (c->name) decrRefCount(c->name);` |
| `ev_8faa1ad91b3b` | call_site | `third_party/redis/src/networking.c:1288` | `freeClientAsync(c);` |
| `ev_8facdffa41e5` | call_site | `third_party/redis/src/networking.c:813` | `closeClientOnOutputBufferLimitReached(c, 1);` |
| `ev_8fc7867887a7` | call_site | `third_party/redis/src/ae.c:152` | `zfree(te);` |
| `ev_8fe18923ff9a` | call_site | `third_party/redis/src/networking.c:4181` | `redisSetCpuAffinity(server.server_cpulist);` |
| `ev_900e1c977d34` | call_site | `third_party/redis/src/db.c:1454` | `addReply(c,shared.cone);` |
| `ev_903535f7c6ec` | call_site | `third_party/redis/src/networking.c:3576` | `addAuthErrReply(c, err);` |
| `ev_9065226b3843` | call_site | `third_party/redis/src/t_string.c:407` | `signalModifiedKey(c, c->db, c->argv[1]);` |
| `ev_9067a080e791` | call_site | `third_party/redis/src/db.c:1805` | `if (isPausedActionsWithUpdate(PAUSE_ACTION_EXPIRE)) return 1;` |
| `ev_908088b53671` | call_site | `third_party/redis/src/networking.c:1133` | `while (help[blen]) addReplyStatus(c,help[blen++]);` |
| `ev_9080af14e547` | call_site | `third_party/redis/src/dict.c:1458` | `if (key == he_key \|\| dictCompareKeys(d, key, he_key)) {` |
| `ev_90843202edd3` | call_site | `third_party/redis/src/t_string.c:681` | `dbReplaceValue(c->db,c->argv[1],new);` |
| `ev_90a3e7f31eb8` | call_site | `third_party/redis/src/networking.c:698` | `sdsfree(s);` |
| `ev_90b7a66cd090` | call_site | `third_party/redis/src/networking.c:3588` | `addReplyError(c,"-NOAUTH HELLO must be called with the client already "` |
| `ev_90d9190687c3` | call_site | `third_party/redis/src/networking.c:3553` | `redactClientCommandArgument(c, j+1);` |
| `ev_90e9ca5befc3` | call_site | `third_party/redis/src/t_string.c:484` | `if (checkStringLength(c,offset,sdslen(value)) != C_OK)` |
| `ev_90f898223fa1` | call_site | `third_party/redis/src/t_string.c:758` | `objb = objb ? getDecodedObject(objb) : createStringObject("",0);` |
| `ev_90ff1cc7dddf` | call_site | `third_party/redis/src/db.c:1503` | `signalDeletedKeyAsReady(emptied, key, original_type);` |
| `ev_910cd55b712c` | call_site | `third_party/redis/src/db.c:545` | `tempDb[i].expires = dictCreate(&dbExpiresDictType);` |
| `ev_9119fa6010d0` | call_site | `third_party/redis/src/dict.c:1136` | `void *newkey = defragkey ? defragkey(dictGetKey(de)) : NULL;` |
| `ev_91571da46cc7` | call_site | `third_party/redis/src/networking.c:2029` | `while((ln = listNext(&li))) {` |
| `ev_916825381117` | call_site | `third_party/redis/src/networking.c:3752` | `serverAssertWithInfo(c,NULL,c->cmd != NULL);` |
| `ev_917f2d6f9df5` | call_site | `third_party/redis/src/db.c:882` | `if (val) listAddNodeTail(keys, val);` |
| `ev_91a4b863a704` | call_site | `third_party/redis/src/t_string.c:172` | `addReplyErrorExpireTime(c);` |
| `ev_91cd82ee8bbf` | call_site | `third_party/redis/src/networking.c:4403` | `listUnlinkNode(server.clients_pending_write, server.clients_pending_write->head);` |
| `ev_91d31f5ad725` | call_site | `third_party/redis/src/t_string.c:129` | `addReply(c, ok_reply ? ok_reply : shared.ok);` |
| `ev_91dbec6da29c` | call_site | `third_party/redis/src/networking.c:4480` | `pending += getIOPendingCount(j);` |
| `ev_91f9fabea6b0` | call_site | `third_party/redis/src/db.c:1290` | `renameGenericCommand(c,1);` |
| `ev_9211a474f587` | call_site | `third_party/redis/src/networking.c:372` | `tail = zmalloc_usable(size + sizeof(clientReplyBlock), &usable_size);` |
| `ev_9232604a3a21` | call_site | `third_party/redis/src/ae.c:145` | `zfree(eventLoop->events);` |
| `ev_931d62333653` | call_site | `third_party/redis/src/networking.c:2682` | `sdsfree(info);` |
| `ev_932e56dee340` | call_site | `third_party/redis/src/networking.c:3266` | `addReplyNull(c);` |
| `ev_93c74c9a3abd` | call_site | `third_party/redis/src/db.c:201` | `dictSetKey(db->dict, de, sdsdup(key->ptr));` |
| `ev_94b5c5fb9c00` | call_site | `third_party/redis/src/db.c:1264` | `decrRefCount(o);` |
| `ev_94f38d57fa99` | call_site | `third_party/redis/src/networking.c:1038` | `size_t len = stringObjectLen(obj);` |
| `ev_9516078eacbd` | call_site | `third_party/redis/src/networking.c:1342` | `if ((c = createClient(conn)) == NULL) {` |
| `ev_954ff55e34a0` | call_site | `third_party/redis/src/networking.c:2674` | `serverLog(LL_VERBOSE, "Reading from client: %s",connGetLastError(c->conn));` |
| `ev_9552ba9eaf22` | call_site | `third_party/redis/src/lazyfree.c:27` | `dictRelease(ht2);` |
| `ev_955c8d24b6e8` | call_site | `third_party/redis/src/t_string.c:165` | `int ret = getLongLongFromObjectOrReply(c, expire, milliseconds, NULL);` |
| `ev_959af9e15401` | call_site | `third_party/redis/src/t_string.c:41` | `if (mustObeyClient(c))` |
| `ev_962f86f14ccc` | call_site | `third_party/redis/src/networking.c:1367` | `serverLog(LL_WARNING,` |
| `ev_9651c725eef7` | call_site | `third_party/redis/src/db.c:923` | `moduleType *mt = moduleTypeLookupModuleByNameIgnoreCase(name);` |
| `ev_9652e5ab4a52` | call_site | `third_party/redis/src/networking.c:651` | `addReplyErrorLength(c,s,sdslen(s));` |
| `ev_968f0636ca91` | call_site | `third_party/redis/src/db.c:1676` | `return dictGetSignedIntegerVal(de);` |
| `ev_9696a4789567` | call_site | `third_party/redis/src/networking.c:3069` | `o = sdsempty();` |
| `ev_96a745c20c04` | call_site | `third_party/redis/src/networking.c:957` | `addReplyProto(c,shared.sethdr[ll]->ptr,hdr_len);` |
| `ev_96ec2df5d2ab` | call_site | `third_party/redis/src/db.c:1074` | `cursor = dictScan(ht, cursor, scanCallback, &data);` |
| `ev_9701fd2b1c5c` | call_site | `third_party/redis/src/networking.c:1251` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_972e7919d669` | call_site | `third_party/redis/src/ae.c:96` | `zfree(eventLoop);` |
| `ev_97640a109e12` | call_site | `third_party/redis/src/dict.c:356` | `dictSetNext(de, d->ht_table[1][h]);` |
| `ev_97b38df62301` | call_site | `third_party/redis/src/dict.c:1004` | `h = randomULong() & m;` |
| `ev_97bb5a14cb1e` | call_site | `third_party/redis/src/adlist.c:80` | `zfree(list);` |
| `ev_97c2a1caabed` | call_site | `third_party/redis/src/networking.c:4128` | `whileBlockedCron();` |
| `ev_97e0abdd2ecf` | call_site | `third_party/redis/src/db.c:522` | `if (server.cluster_enabled) slotToKeyFlush(server.db);` |
| `ev_9811bc80eb77` | call_site | `third_party/redis/src/networking.c:1739` | `freeClientAsync(c);` |
| `ev_981c0e0f0d9d` | call_site | `third_party/redis/src/networking.c:1695` | `if (c->lib_ver) decrRefCount(c->lib_ver);` |
| `ev_984e1db9efbd` | call_site | `third_party/redis/src/networking.c:1012` | `addReplyProto(c,"_\r\n",3);` |
| `ev_984fa87be077` | call_site | `third_party/redis/src/t_string.c:492` | `o->ptr = sdsgrowzero(o->ptr,offset+sdslen(value));` |
| `ev_987349a1c65d` | call_site | `third_party/redis/src/networking.c:3494` | `addReplyLongLong(c,c->client_tracking_redirection);` |
| `ev_9883af65b31a` | call_site | `third_party/redis/src/networking.c:313` | `putClientInPendingWriteQueue(c);` |
| `ev_98a32ef52742` | call_site | `third_party/redis/src/t_string.c:584` | `notifyKeyspaceEvent(NOTIFY_STRING,"set",c->argv[j],c->db->id);` |
| `ev_98bbd832887f` | call_site | `third_party/redis/src/t_string.c:479` | `addReplyLongLong(c,olen);` |
| `ev_98fc6c1ce134` | call_site | `third_party/redis/src/networking.c:3931` | `sdsfree(client);` |
| `ev_9910485166be` | call_site | `third_party/redis/src/connection.h:247` | `conn->type->shutdown(conn);` |
| `ev_9914ad5f5e58` | call_site | `third_party/redis/src/db.c:733` | `addReplyLongLong(c,numdel);` |
| `ev_993b875524e1` | call_site | `third_party/redis/src/networking.c:3945` | `listRewind(server.slaves,&li);` |
| `ev_998253c87b35` | call_site | `third_party/redis/src/db.c:333` | `key = dictGetKey(de);` |
| `ev_999b4f1cddd3` | call_site | `third_party/redis/src/db.c:723` | `int deleted  = lazy ? dbAsyncDelete(c->db,c->argv[j]) :` |
| `ev_99d4e346a196` | call_site | `third_party/redis/src/networking.c:1916` | `*nwritten = connWrite(c->conn, c->buf + c->sentlen, c->bufpos - c->sentlen);` |
| `ev_99d60dec134d` | call_site | `third_party/redis/src/dict.c:833` | `if (entryIsNoValue(de)) return decodeEntryNoValue(de)->next;` |
| `ev_99fa79050df9` | call_site | `third_party/redis/src/dict.c:1160` | `bucketref = dictGetNextRef(*bucketref);` |
| `ev_9a1b8e03f012` | call_site | `third_party/redis/src/networking.c:1165` | `freeClientAsync(dst);` |
| `ev_9a3c74e275b7` | call_site | `third_party/redis/src/db.c:1505` | `dictReleaseIterator(di);` |
| `ev_9a55f7985c67` | call_site | `third_party/redis/src/t_string.c:184` | `addReplyErrorExpireTime(c);` |
| `ev_9a86ab07bed4` | call_site | `third_party/redis/src/db.c:1142` | `listDelNode(keys, ln);` |
| `ev_9a96823f24f4` | call_site | `third_party/redis/src/t_string.c:464` | `if (checkStringLength(c,offset,sdslen(value)) != C_OK)` |
| `ev_9aa7f55317e9` | call_site | `third_party/redis/src/networking.c:2597` | `sdsrange(c->querybuf,c->repl_applied,-1);` |
| `ev_9aafba5d1a5c` | call_site | `third_party/redis/src/db.c:684` | `server.dirty += emptyData(c->db->id,flags \| EMPTYDB_NOFUNCTIONS,NULL);` |
| `ev_9ad3167d13e4` | call_site | `third_party/redis/src/networking.c:3798` | `mem += pubsubMemOverhead(c);` |
| `ev_9ad958549aed` | call_site | `third_party/redis/src/t_string.c:320` | `setGenericCommand(c,OBJ_PX,c->argv[1],c->argv[3],c->argv[2],UNIT_MILLISECONDS,NULL,NULL);` |
| `ev_9ae03c29d219` | call_site | `third_party/redis/src/networking.c:516` | `incrementErrorCount("ERR", 3);` |
| `ev_9b848275b280` | call_site | `third_party/redis/src/networking.c:978` | `serverAssert(length >= 0);` |
| `ev_9bb0a68ff44a` | call_site | `third_party/redis/src/dict.c:1059` | `_dictRehashStep(d);` |
| `ev_9bb513c2fa94` | call_site | `third_party/redis/src/networking.c:3079` | `o = catClientInfoString(o, cl);` |
| `ev_9bf054c96d3f` | call_site | `third_party/redis/src/networking.c:2955` | `if (sdslen(val)) {` |
| `ev_9c0b785673a4` | call_site | `third_party/redis/src/networking.c:2448` | `replicationFeedStreamFromMasterStream(c->querybuf+c->repl_applied,applied);` |
| `ev_9c30b52cf828` | call_site | `third_party/redis/src/ae.c:466` | `processed += processTimeEvents(eventLoop);` |
| `ev_9c58b8403da0` | call_site | `third_party/redis/src/adlist.c:126` | `if ((node = zmalloc(sizeof(*node))) == NULL)` |
| `ev_9c71d6b9b10d` | call_site | `third_party/redis/src/networking.c:120` | `client *c = zmalloc(sizeof(client));` |
| `ev_9c7e73a42e88` | call_site | `third_party/redis/src/db.c:228` | `dictSetVal(db->dict, de, val);` |
| `ev_9c8b9f6d4876` | call_site | `third_party/redis/src/db.c:1179` | `addReplyStatus(c, getObjectTypeName(o));` |
| `ev_9c9cd9ba9193` | call_site | `third_party/redis/src/dict.c:683` | `he = dictGetNext(he);` |
| `ev_9cadbdf65c13` | call_site | `third_party/redis/src/bio.c:129` | `bio_jobs[j] = listCreate();` |
| `ev_9ce677a4ba8b` | call_site | `third_party/redis/src/db.c:2097` | `keys = getKeysPrepareResult(result, stop - start);` |
| `ev_9d08c9a10bb2` | call_site | `third_party/redis/src/ae.c:85` | `if (aeApiCreate(eventLoop) == -1) goto err;` |
| `ev_9d0f3f436c7c` | call_site | `third_party/redis/src/networking.c:3620` | `addReplyBulkCString(c,"role");` |
| `ev_9d19b340d9cb` | call_site | `third_party/redis/src/networking.c:3405` | `enableTracking(c,redir,options,prefix,numprefix);` |
| `ev_9d58e84fde5d` | call_site | `third_party/redis/src/dict.c:187` | `size_t metasize = type->dictMetadataBytes ? type->dictMetadataBytes() : 0;` |
| `ev_9d6260694969` | call_site | `third_party/redis/src/db.c:1674` | `(de = dictFind(db->expires,key->ptr)) == NULL) return -1;` |
| `ev_9d790918160a` | call_site | `third_party/redis/src/networking.c:3189` | `listRewind(server.clients,&li);` |
| `ev_9d98de0499b4` | call_site | `third_party/redis/src/networking.c:4203` | `listRewind(io_threads_list[id],&li);` |
| `ev_9d9b836926c7` | call_site | `third_party/redis/src/networking.c:2235` | `serverLog(loglevel,` |
| `ev_9da205e8b0bc` | call_site | `third_party/redis/src/networking.c:1880` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_9da9fc41f9fd` | call_site | `third_party/redis/src/networking.c:3621` | `addReplyBulkCString(c,server.masterhost ? "replica" : "master");` |
| `ev_9dc0f22a61f6` | call_site | `third_party/redis/src/t_string.c:508` | `if (getLongLongFromObjectOrReply(c,c->argv[2],&start,NULL) != C_OK)` |
| `ev_9df18feefb4d` | call_site | `third_party/redis/src/t_string.c:414` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"persist",c->argv[1],c->db->id);` |
| `ev_9dff14afd9da` | call_site | `third_party/redis/src/db.c:1494` | `dictEntry *kde = dictFind(replaced_with->dict, key->ptr);` |
| `ev_9dff4cf0f2c4` | call_site | `third_party/redis/src/networking.c:1795` | `id = htonu64(id);` |
| `ev_9e0aaad05932` | call_site | `third_party/redis/src/networking.c:50` | `void *sh = sdsAllocPtr(s);` |
| `ev_9e31e413f57b` | call_site | `third_party/redis/src/dict.c:825` | `assert(entryHasValue(de));` |
| `ev_9e3a2d186bde` | call_site | `third_party/redis/src/db.c:799` | `if (allkeys \|\| stringmatchlen(pattern,plen,key,sdslen(key),0)) {` |
| `ev_9e853a227f9b` | call_site | `third_party/redis/src/db.c:618` | `scanDatabaseForDeletedKeys(&server.db[j], NULL);` |
| `ev_9e869ccb4ec2` | call_site | `third_party/redis/src/dict.c:647` | `dictFreeVal(d, he);` |
| `ev_9e98cb3d5064` | call_site | `third_party/redis/src/networking.c:1249` | `serverLog(LL_WARNING,` |
| `ev_9e9fe9e3e564` | call_site | `third_party/redis/src/lazyfree.c:167` | `bioCreateLazyFreeJob(lazyfreeFreeObject,1,obj);` |
| `ev_9edc65eb0a2c` | call_site | `third_party/redis/src/networking.c:3046` | `addReplyHelp(c, help);` |
| `ev_9f33e1e7fc2b` | call_site | `third_party/redis/src/dict.c:654` | `zfree(d->ht_table[htidx]);` |
| `ev_9f5550d8e9f5` | call_site | `third_party/redis/src/db.c:769` | `addReply(c,shared.ok);` |
| `ev_9f62b620c958` | call_site | `third_party/redis/src/networking.c:2164` | `setProtocolError("unbalanced quotes in inline request",c);` |
| `ev_9f7ca839d5e2` | call_site | `third_party/redis/src/db.c:1210` | `if (abortShutdown() == C_OK)` |
| `ev_9f9cb70dab4d` | call_site | `third_party/redis/src/db.c:437` | `robj *decoded = getDecodedObject(o);` |
| `ev_9fc3612f8b70` | call_site | `third_party/redis/src/networking.c:911` | `addReplyBulkCBuffer(c, num, len);` |
| `ev_9fe1514cea94` | call_site | `third_party/redis/src/db.c:2245` | `return genericGetKeys(0, 1, 2, 1, argv, argc, result);` |
| `ev_9fec39e2d1b5` | call_site | `third_party/redis/src/networking.c:1576` | `listDelNode(server.clients_to_close,ln);` |
| `ev_9ff3c9a08d99` | call_site | `third_party/redis/src/networking.c:2299` | `c->argv = zmalloc(sizeof(robj*)*c->argv_len);` |
| `ev_a029e355beaa` | call_site | `third_party/redis/src/dict.c:171` | `return entryIsNormal(de);` |
| `ev_a03863f40340` | call_site | `third_party/redis/src/ae.c:399` | `numevents = aeApiPoll(eventLoop, tvp);` |
| `ev_a075e04bea07` | call_site | `third_party/redis/src/dict.c:344` | `if (!entryIsKey(de)) zfree(decodeMaskedPtr(de));` |
| `ev_a0799a9a1114` | call_site | `third_party/redis/src/db.c:564` | `dictRelease(tempDb[i].dict);` |
| `ev_a0dd204499c2` | call_site | `third_party/redis/src/ae.c:192` | `aeApiDelEvent(eventLoop, fd, mask);` |
| `ev_a106c3e5b7fa` | call_site | `third_party/redis/src/db.c:375` | `freeObjAsync(key, dictGetVal(de), db->id);` |
| `ev_a16018b38921` | call_site | `third_party/redis/src/networking.c:931` | `addReplyProto(c,buf,len);` |
| `ev_a16416953989` | call_site | `third_party/redis/src/networking.c:3500` | `addReplyBulkCString(c,"prefixes");` |
| `ev_a16d46290086` | call_site | `third_party/redis/src/t_string.c:89` | `if (expire && getExpireMillisecondsOrReply(c, expire, flags, unit, &milliseconds) != C_OK) {` |
| `ev_a183c76b4971` | call_site | `third_party/redis/src/networking.c:3239` | `if (getLongLongFromObjectOrReply(c,c->argv[2],&id,NULL)` |
| `ev_a21d3cd264c8` | call_site | `third_party/redis/src/lazyfree.c:65` | `listRelease(blocks);` |
| `ev_a229c2c00573` | call_site | `third_party/redis/src/dict.c:932` | `dictIterator *iter = zmalloc(sizeof(*iter));` |
| `ev_a24c2fccc986` | call_site | `third_party/redis/src/t_string.c:669` | `if (checkType(c,o,OBJ_STRING)) return;` |
| `ev_a29280a7f4a4` | call_site | `third_party/redis/src/db.c:1447` | `if (expire != -1) setExpire(c, dst, newkey, expire);` |
| `ev_a2b6fed19e81` | call_site | `third_party/redis/src/t_string.c:812` | `addReplyError(c, "Insufficient memory, transient memory for LCS exceeds proto-max-bulk-len");` |
| `ev_a2d93b7d3cbe` | call_site | `third_party/redis/src/db.c:737` | `delGenericCommand(c,server.lazyfree_lazy_user_del);` |
| `ev_a31e85c32928` | call_site | `third_party/redis/src/db.c:2138` | `keys = getKeysPrepareResult(result, count);` |
| `ev_a327653c521d` | call_site | `third_party/redis/src/networking.c:2148` | `setProtocolError("too big inline request",c);` |
| `ev_a34d146d9271` | call_site | `third_party/redis/src/adlist.c:303` | `if (copy->free) copy->free(value);` |
| `ev_a36d4c552701` | call_site | `third_party/redis/src/networking.c:1509` | `serverAssert(ln != NULL);` |
| `ev_a382f09a16ac` | call_site | `third_party/redis/src/db.c:2378` | `if (sdslen(argv[3]->ptr) > 0) {` |
| `ev_a3d48235e944` | call_site | `third_party/redis/src/networking.c:864` | `serverAssert(c->resp >= 3);` |
| `ev_a3fc94c45f7f` | call_site | `third_party/redis/src/networking.c:2395` | `c->querybuf = sdsnewlen(SDS_NOINIT,c->bulklen+2);` |
| `ev_a408c88fa6c9` | call_site | `third_party/redis/src/db.c:1338` | `dbAdd(dst,c->argv[1],o);` |
| `ev_a42031368ec9` | call_site | `third_party/redis/src/networking.c:1619` | `dictRelease(c->pubsubshard_channels);` |
| `ev_a4300d183c82` | call_site | `third_party/redis/src/networking.c:2388` | `sdslen(c->querybuf) == (size_t)(c->bulklen+2))` |
| `ev_a45fca839a20` | call_site | `third_party/redis/src/dict.c:1462` | `he = dictGetNext(he);` |
| `ev_a48eee599d6e` | call_site | `third_party/redis/src/db.c:197` | `dbSetValue(db, key, val, 1, existing);` |
| `ev_a4ce89ef76ba` | call_site | `third_party/redis/src/networking.c:2032` | `listUnlinkNode(server.clients_pending_write,ln);` |
| `ev_a4dd96da2717` | call_site | `third_party/redis/src/networking.c:4343` | `listUnlinkNode(server.clients_pending_write, ln);` |
| `ev_a4ff834568c4` | call_site | `third_party/redis/src/t_string.c:914` | `addReplyArrayLen(c,2);` |
| `ev_a50311d698ac` | call_site | `third_party/redis/src/networking.c:1510` | `listDelNode(server.monitors,ln);` |
| `ev_a50a51611013` | call_site | `third_party/redis/src/t_string.c:720` | `o->ptr = sdscatlen(o->ptr,append->ptr,sdslen(append->ptr));` |
| `ev_a50c7db55d37` | call_site | `third_party/redis/src/dict.c:323` | `void *key = dictGetKey(de);` |
| `ev_a519cea2ff9d` | call_site | `third_party/redis/src/db.c:1276` | `signalModifiedKey(c,c->db,c->argv[2]);` |
| `ev_a524055c2ad1` | call_site | `third_party/redis/src/db.c:2152` | `serverPanic("Redis built-in command declared keys positions not matching the arity requirements.");` |
| `ev_a526bae69f83` | call_site | `third_party/redis/src/db.c:551` | `slotToKeyInit(tempDb);` |
| `ev_a5432aa65512` | call_site | `third_party/redis/src/networking.c:2334` | `setProtocolError("invalid bulk length",c);` |
| `ev_a54a69e64c63` | call_site | `third_party/redis/src/ae.c:229` | `te->when = getMonotonicUs() + milliseconds * 1000;` |
| `ev_a5bba9acc010` | call_site | `third_party/redis/src/db.c:1087` | `if (use_pattern && !stringmatchlen(pat, sdslen(pat), key, len, 0)) {` |
| `ev_a5c8c5cf5822` | call_site | `third_party/redis/src/db.c:1112` | `listAddNodeTail(keys, sdsnewlen(str, len));` |
| `ev_a5d23773b651` | call_site | `third_party/redis/src/db.c:152` | `serverAssert(!(flags & LOOKUP_WRITE));` |
| `ev_a5f25f9fca24` | call_site | `third_party/redis/src/networking.c:1636` | `unlinkClient(c);` |
| `ev_a5f48326beac` | call_site | `third_party/redis/src/networking.c:3361` | `addReplyError(c,` |
| `ev_a60887db4169` | call_site | `third_party/redis/src/dict.c:741` | `*plink = dictGetNext(he);` |
| `ev_a60fedbad3f6` | call_site | `third_party/redis/src/ae.c:436` | `fe->rfileProc(eventLoop,fd,fe->clientData,mask);` |
| `ev_a61a65e88e82` | call_site | `third_party/redis/src/networking.c:1700` | `zfree(c);` |
| `ev_a620d106fa37` | call_site | `third_party/redis/src/networking.c:3671` | `retainOriginalCommandVector(c);` |
| `ev_a6422dc94c20` | call_site | `third_party/redis/src/networking.c:212` | `listInitNode(&c->clients_pending_write_node, c);` |
| `ev_a64ffa20b65d` | assignment | `third_party/redis/src/lazyfree.c:190` | `bioCreateLazyFreeJob(lazyFreeTrackingTable,1,tracking);` |
| `ev_a6530d13761c` | call_site | `third_party/redis/src/networking.c:2977` | `clearClientConnectionState(c);` |
| `ev_a665edd1cec6` | call_site | `third_party/redis/src/db.c:1660` | `dictSetSignedIntegerVal(de,when);` |
| `ev_a68b2c2bb05b` | call_site | `third_party/redis/src/networking.c:1606` | `if (c->flags & CLIENT_BLOCKED) unblockClient(c, 1);` |
| `ev_a6d9e41055ea` | call_site | `third_party/redis/src/dict.c:664` | `_dictClear(d,1,NULL);` |
| `ev_a70978950304` | call_site | `third_party/redis/src/ae.c:144` | `aeApiFree(eventLoop);` |
| `ev_a709ff89fb1c` | call_site | `third_party/redis/src/networking.c:2260` | `serverAssertWithInfo(c,NULL,c->argc == 0);` |
| `ev_a79364436e66` | call_site | `third_party/redis/src/networking.c:197` | `c->pubsubshard_channels = dictCreate(&objectKeyPointerValueDictType);` |
| `ev_a7f6c69c0a0c` | call_site | `third_party/redis/src/db.c:1228` | `addReplyErrorObject(c, shared.slowmoduleerr);` |
| `ev_a8023cf07dc1` | call_site | `third_party/redis/src/networking.c:915` | `addReplyProto(c,"\r\n",2);` |
| `ev_a82636357b10` | call_site | `third_party/redis/src/dict.c:1399` | `return d->type->expandAllowed(` |
| `ev_a862abad6837` | call_site | `third_party/redis/src/db.c:362` | `robj *val = dictGetVal(de);` |
| `ev_a86a02856ee0` | call_site | `third_party/redis/src/db.c:2531` | `keys = getKeysPrepareResult(result, 1);` |
| `ev_a8b2f4d60b19` | call_site | `third_party/redis/src/db.c:2088` | `return moduleGetCommandChannelsViaAPI(cmd, argv, argc, result);` |
| `ev_a918f3bd99cd` | call_site | `third_party/redis/src/networking.c:621` | `addReplyErrorLength(c,err,sdslen(err));` |
| `ev_a92753b748a9` | call_site | `third_party/redis/src/db.c:876` | `val = sdsnewlen(buf, len);` |
| `ev_a92e6c511154` | call_site | `third_party/redis/src/networking.c:3554` | `redactClientCommandArgument(c, j+2);` |
| `ev_a942f93acac5` | call_site | `third_party/redis/src/networking.c:2430` | `reqresAppendResponse(c);` |
| `ev_a96ab495ef27` | call_site | `third_party/redis/src/networking.c:994` | `addReplyAggregateLen(c,length,prefix);` |
| `ev_a9f9a132c01e` | call_site | `third_party/redis/src/ae.c:94` | `zfree(eventLoop->events);` |
| `ev_aa06f716abc2` | call_site | `third_party/redis/src/db.c:360` | `dictEntry *de = dictTwoPhaseUnlinkFind(db->dict,key->ptr,&plink,&table);` |
| `ev_aa17f2bbbc07` | call_site | `third_party/redis/src/networking.c:3996` | `unblockPostponedClients();` |
| `ev_aa18bab08d48` | call_site | `third_party/redis/src/networking.c:1526` | `moduleNotifyUserChanged(c);` |
| `ev_aa1dcbccdaf5` | call_site | `third_party/redis/src/ae.c:444` | `fe->wfileProc(eventLoop,fd,fe->clientData,mask);` |
| `ev_aa39e7f76ed0` | call_site | `third_party/redis/src/db.c:1468` | `robj *value = dictGetVal(kde);` |
| `ev_aa6125c25f83` | call_site | `third_party/redis/src/lazyfree.c:179` | `db->expires = dictCreate(&dbExpiresDictType);` |
| `ev_aa6253514ee0` | call_site | `third_party/redis/src/dict.c:114` | `return siphash_nocase(buf,len,dict_hash_function_seed);` |
| `ev_aa86097f3bc4` | call_site | `third_party/redis/src/networking.c:1444` | `uint64_t id = htonu64(c->id);` |
| `ev_aa8fd4297cfe` | call_site | `third_party/redis/src/db.c:1082` | `while (setTypeNext(si, &str, &len, &llele) != -1) {` |
| `ev_aaa7965c27dc` | call_site | `third_party/redis/src/db.c:1211` | `addReply(c, shared.ok);` |
| `ev_aac1362cc262` | call_site | `third_party/redis/src/db.c:184` | `if (!o) addReplyOrErrorObject(c, reply);` |
| `ev_ab27bd7a8e9d` | call_site | `third_party/redis/src/dict.c:580` | `dictFreeUnlinkedEntry(d, he);` |
| `ev_ab52f7468ea4` | call_site | `third_party/redis/src/t_string.c:724` | `notifyKeyspaceEvent(NOTIFY_STRING,"append",c->argv[1],c->db->id);` |
| `ev_ab60b002d735` | call_site | `third_party/redis/src/ae_epoll.c:131` | `panic("aeApiPoll: epoll_wait, %s", strerror(errno));` |
| `ev_abe1006faa0e` | call_site | `third_party/redis/src/db.c:517` | `removed = emptyDbStructure(server.db, dbnum, async, callback);` |
| `ev_ac51e7755de6` | call_site | `third_party/redis/src/lazyfree.c:142` | `size_t effort = moduleGetFreeEffort(key, obj, dbid);` |
| `ev_aca802593ece` | call_site | `third_party/redis/src/networking.c:2182` | `sdsfreesplitres(argv,argc);` |
| `ev_acb823e164f5` | call_site | `third_party/redis/src/t_string.c:310` | `setGenericCommand(c,OBJ_SET_NX,c->argv[1],c->argv[2],NULL,0,shared.cone,shared.czero);` |
| `ev_acb9984553c0` | call_site | `third_party/redis/src/dict.c:694` | `return he ? dictGetVal(he) : NULL;` |
| `ev_acf09f6e5cc6` | call_site | `third_party/redis/src/t_string.c:97` | `found = (lookupKeyWrite(c->db,key) != NULL);` |
| `ev_ad37f361fbc7` | call_site | `third_party/redis/src/dict.c:1337` | `v = rev(v);` |
| `ev_ad3eefd9751a` | call_site | `third_party/redis/src/networking.c:2700` | `if (!(c->flags & CLIENT_MASTER) && sdslen(c->querybuf) > server.client_max_querybuf_len) {` |
| `ev_ad4513dd6e3c` | call_site | `third_party/redis/src/networking.c:695` | `sds s = sdscatvprintf(sdsempty(),fmt,ap);` |
| `ev_ad4836fe00b5` | call_site | `third_party/redis/src/networking.c:3439` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_ad597a8ab05d` | call_site | `third_party/redis/src/dict.c:322` | `nextde = dictGetNext(de);` |
| `ev_ad8ae4658a7f` | call_site | `third_party/redis/src/t_string.c:565` | `addReplyErrorArity(c);` |
| `ev_ada2661ab6f0` | call_site | `third_party/redis/src/networking.c:1010` | `addReplyProto(c,"$-1\r\n",5);` |
| `ev_adbc3f0ba877` | call_site | `third_party/redis/src/db.c:1097` | `unsigned char *p = lpFirst(o->ptr);` |
| `ev_ae39ff9faab1` | call_site | `third_party/redis/src/t_string.c:733` | `addReplyLongLong(c,stringObjectLen(o));` |
| `ev_ae5b9281bc2e` | call_site | `third_party/redis/src/db.c:133` | `notifyKeyspaceEvent(NOTIFY_KEY_MISS, "keymiss", key, db->id);` |
| `ev_ae6a15b01602` | call_site | `third_party/redis/src/networking.c:545` | `int ctype = getClientType(c);` |
| `ev_aecae5148c5d` | call_site | `third_party/redis/src/networking.c:1350` | `connClose(conn); /* May be already closed, just ignore errors */` |
| `ev_aed5540ec501` | call_site | `third_party/redis/src/lazyfree.c:221` | `atomicIncr(lazyfree_objects,listLength(blocks)+raxSize(index));` |
| `ev_aef963257222` | call_site | `third_party/redis/src/networking.c:1616` | `pubsubUnsubscribeAllPatterns(c,0);` |
| `ev_af0de47fbcac` | call_site | `third_party/redis/src/ae.c:171` | `if (aeApiAddEvent(eventLoop, fd, mask) == -1)` |
| `ev_af1ad51cdf13` | call_site | `third_party/redis/src/dict.c:534` | `dictSetVal(d, existing, val);` |
| `ev_af39ee92dccc` | call_site | `third_party/redis/src/t_string.c:744` | `obja = lookupKeyRead(c->db,c->argv[1]);` |
| `ev_af469f0f583e` | call_site | `third_party/redis/src/db.c:1169` | `addReplyLongLong(c,dictSize(c->db->dict));` |
| `ev_af5f2661d35a` | call_site | `third_party/redis/src/lazyfree.c:135` | `serverAssert(raxNext(&ri));` |
| `ev_afd22d946f45` | call_site | `third_party/redis/src/t_string.c:468` | `dbAdd(c->db,c->argv[1],o);` |
| `ev_affd15f225a3` | call_site | `third_party/redis/src/t_string.c:757` | `obja = obja ? getDecodedObject(obja) : createStringObject("",0);` |
| `ev_b0508392b951` | call_site | `third_party/redis/src/dict.c:970` | `iter->nextEntry = dictGetNext(iter->entry);` |
| `ev_b07955be5335` | call_site | `third_party/redis/src/networking.c:2912` | `incrRefCount(name);` |
| `ev_b0aa3fee0b1f` | call_site | `third_party/redis/src/db.c:573` | `zfree(tempDb);` |
| `ev_b0b85f0829e4` | call_site | `third_party/redis/src/networking.c:3612` | `addReplyLongLong(c,c->id);` |
| `ev_b11faa2f7a8e` | call_site | `third_party/redis/src/networking.c:456` | `sdsfree(s);` |
| `ev_b14c3bc08b57` | call_site | `third_party/redis/src/t_string.c:458` | `if (sdslen(value) == 0) {` |
| `ev_b15a0d36a22b` | call_site | `third_party/redis/src/t_string.c:818` | `addReplyError(c, "Insufficient memory, failed allocating transient memory for LCS");` |
| `ev_b166a3698631` | call_site | `third_party/redis/src/networking.c:1662` | `serverAssert(ln != NULL);` |
| `ev_b1cbf618e089` | call_site | `third_party/redis/src/db.c:1451` | `notifyKeyspaceEvent(NOTIFY_GENERIC,"copy_to",c->argv[2],dst->id);` |
| `ev_b1d1349fb85f` | call_site | `third_party/redis/src/db.c:1466` | `dictEntry *kde = dictFind(db->dict,key->ptr);` |
| `ev_b1d4dd241521` | call_site | `third_party/redis/src/dict.c:630` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_b1eec667d51d` | call_site | `third_party/redis/src/db.c:467` | `emptyDbAsync(&dbarray[j]);` |
| `ev_b1f0e9f0e7ea` | call_site | `third_party/redis/src/networking.c:3489` | `setDeferredSetLen(c,arraylen_ptr,numflags);` |
| `ev_b2a2167aef9b` | call_site | `third_party/redis/src/networking.c:1164` | `sds client = catClientInfoString(sdsempty(),dst);` |
| `ev_b2aa78640c3b` | call_site | `third_party/redis/src/adlist.c:301` | `if (listAddNodeTail(copy, value) == NULL) {` |
| `ev_b2c0862f1f32` | call_site | `third_party/redis/src/db.c:1272` | `dbAdd(c->db,c->argv[2],o);` |
| `ev_b3534e041834` | call_site | `third_party/redis/src/networking.c:1114` | `addReplyProto(c,s,len);` |
| `ev_b36a162bd270` | call_site | `third_party/redis/src/adlist.c:227` | `zfree(iter);` |
| `ev_b3729dcb1144` | assignment | `third_party/redis/src/networking.c:191` | `listSetDupMethod(c->reply,dupClientReplyValue);` |
| `ev_b385aee33d59` | call_site | `third_party/redis/src/networking.c:3561` | `if (validateClientName(clientname, &err) == C_ERR) {` |
| `ev_b3fd34820c25` | call_site | `third_party/redis/src/db.c:1345` | `signalModifiedKey(c,dst,c->argv[1]);` |
| `ev_b41442bb16fc` | call_site | `third_party/redis/src/t_string.c:631` | `signalModifiedKey(c,c->db,c->argv[1]);` |
| `ev_b44dba9aac7b` | call_site | `third_party/redis/src/networking.c:2205` | `zfree(argv);` |
| `ev_b4564eb78e53` | call_site | `third_party/redis/src/networking.c:3663` | `incrRefCount(c->argv[j]);` |
| `ev_b466264c9606` | call_site | `third_party/redis/src/lazyfree.c:200` | `bioCreateLazyFreeJob(lazyFreeLuaScripts,1,lua_scripts);` |
| `ev_b47dbe8ae263` | call_site | `third_party/redis/src/t_string.c:510` | `if (getLongLongFromObjectOrReply(c,c->argv[3],&end,NULL) != C_OK)` |
| `ev_b493ecb38fcd` | call_site | `third_party/redis/src/networking.c:3287` | `if (getTimeoutFromObjectOrReply(c,c->argv[2],&end,` |
| `ev_b4dd30cf7298` | call_site | `third_party/redis/src/networking.c:3089` | `o = getAllClientsInfoString(type);` |
| `ev_b509ef378061` | call_site | `third_party/redis/src/db.c:881` | `listAddNodeTail(keys, key);` |
| `ev_b518bbd260fc` | call_site | `third_party/redis/src/t_string.c:670` | `if (getLongDoubleFromObjectOrReply(c,o,&value,NULL) != C_OK \|\|` |
| `ev_b524227d359e` | call_site | `third_party/redis/src/db.c:122` | `updateLFU(val);` |
| `ev_b52747926e65` | call_site | `third_party/redis/src/networking.c:2278` | `serverAssertWithInfo(c,NULL,c->querybuf[c->qb_pos] == '*');` |
| `ev_b529d05818d4` | call_site | `third_party/redis/src/db.c:200` | `serverAssertWithInfo(NULL, key, de != NULL);` |
| `ev_b56261e81e08` | call_site | `third_party/redis/src/db.c:1009` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_b59e0b7b3efb` | call_site | `third_party/redis/src/t_string.c:179` | `*milliseconds += commandTimeSnapshot();` |
| `ev_b5b5bf2a7b1d` | call_site | `third_party/redis/src/t_string.c:574` | `addReply(c, shared.czero);` |
| `ev_b5c2335991b6` | call_site | `third_party/redis/src/networking.c:1525` | `clientSetDefaultAuth(c);` |
| `ev_b5eba8d966bd` | call_site | `third_party/redis/src/networking.c:3194` | `if (type != -1 && getClientType(client) != type) continue;` |
| `ev_b60a74449b2b` | call_site | `third_party/redis/src/networking.c:1615` | `pubsubUnsubscribeShardAllChannels(c, 0);` |
| `ev_b634c6fbb8c5` | call_site | `third_party/redis/src/t_string.c:661` | `incrDecrCommand(c,-incr);` |
| `ev_b692d0d93308` | call_site | `third_party/redis/src/networking.c:2701` | `sds ci = catClientInfoString(sdsempty(),c), bytes = sdsempty();` |
| `ev_b6944185ca32` | call_site | `third_party/redis/src/networking.c:1699` | `sdsfree(c->slave_addr);` |
| `ev_b69873deb102` | call_site | `third_party/redis/src/networking.c:4470` | `while((ln = listNext(&li))) {` |
| `ev_b6a4f68699cb` | call_site | `third_party/redis/src/ae_epoll.c:71` | `zfree(state);` |
| `ev_b6fa0decb1be` | call_site | `third_party/redis/src/dict.c:757` | `assert(entryHasValue(de));` |
| `ev_b6fce5be85bb` | call_site | `third_party/redis/src/t_string.c:732` | `checkType(c,o,OBJ_STRING)) return;` |
| `ev_b702d838bfd5` | call_site | `third_party/redis/src/networking.c:1147` | `sds cmd = sdsnew((char*) c->argv[0]->ptr);` |
| `ev_b708b96988d8` | call_site | `third_party/redis/src/t_string.c:612` | `addReplyError(c,"increment or decrement would overflow");` |
| `ev_b734a130a6f8` | call_site | `third_party/redis/src/networking.c:1405` | `while((ln = listNext(&li))) {` |
| `ev_b73d4f37d9e6` | call_site | `third_party/redis/src/db.c:2265` | `return genericGetKeys(0, 2, 3, 1, argv, argc, result);` |
| `ev_b7a93be696ca` | call_site | `third_party/redis/src/ae.c:287` | `monotime now = getMonotonicUs();` |
| `ev_b7d192bbe7c7` | call_site | `third_party/redis/src/networking.c:3061` | `type = getClientTypeByName(c->argv[3]->ptr);` |
| `ev_b7d70cabdf87` | call_site | `third_party/redis/src/t_string.c:944` | `zfree(lcs);` |
| `ev_b7de63ad3abd` | call_site | `third_party/redis/src/networking.c:3922` | `serverLog(LL_WARNING,` |
| `ev_b7f8ddba68a3` | call_site | `third_party/redis/src/networking.c:3688` | `argv = zmalloc(sizeof(robj*)*argc);` |
| `ev_b8327998213b` | call_site | `third_party/redis/src/networking.c:3192` | `if (addr && strcmp(getClientPeerId(client),addr) != 0) continue;` |
| `ev_b89224760791` | call_site | `third_party/redis/src/networking.c:196` | `c->pubsub_patterns = dictCreate(&objectKeyPointerValueDictType);` |
| `ev_b89502d2ba9f` | call_site | `third_party/redis/src/ae.c:133` | `eventLoop->fired = zrealloc(eventLoop->fired,sizeof(aeFiredEvent)*setsize);` |
| `ev_b8b445008780` | call_site | `third_party/redis/src/dict.c:399` | `while(dictRehash(d,100)) {` |
| `ev_b8bce1b9c7fc` | call_site | `third_party/redis/src/networking.c:849` | `setDeferredAggregateLen(c,node,length,'*');` |
| `ev_b8e4abad0f12` | call_site | `third_party/redis/src/t_string.c:605` | `o = lookupKeyWrite(c->db,c->argv[1]);` |
| `ev_b9260b05d4a1` | call_site | `third_party/redis/src/networking.c:97` | `raxInsert(server.clients_index,(unsigned char*)&id,sizeof(id),c,NULL);` |
| `ev_b9f82c324fc2` | call_site | `third_party/redis/src/networking.c:1480` | `serverAssert(io_threads_op == IO_THREADS_OP_IDLE);` |
| `ev_ba09b46f5d96` | call_site | `third_party/redis/src/db.c:1090` | `listAddNodeTail(keys, sdsnewlen(key, len));` |
| `ev_ba0f78c9b667` | call_site | `third_party/redis/src/adlist.c:129` | `listLinkNodeTail(list, node);` |
| `ev_ba3f38cdf9d7` | call_site | `third_party/redis/src/db.c:262` | `decrRefCount(old);` |
| `ev_ba7328591dad` | call_site | `third_party/redis/src/networking.c:2281` | `addReplyError(c,"Protocol error: invalid multibulk length");` |
| `ev_ba79ead8cc96` | call_site | `third_party/redis/src/networking.c:2681` | `serverLog(LL_VERBOSE, "Client closed connection %s", info);` |
| `ev_ba7b567d71c8` | call_site | `third_party/redis/src/dict.c:814` | `assert(entryHasValue(de));` |
| `ev_baae1f00f3ae` | call_site | `third_party/redis/src/lazyfree.c:66` | `raxFree(index);` |
| `ev_bac2168559dc` | call_site | `third_party/redis/src/dict.c:429` | `if (!d->type->no_value) dictSetVal(d, entry, val);` |
| `ev_bacadf21e1c7` | call_site | `third_party/redis/src/networking.c:1369` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_bb1f7cb058e5` | call_site | `third_party/redis/src/dict.c:648` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_bb259a85f1fa` | call_site | `third_party/redis/src/db.c:1625` | `if (getIntFromObjectOrReply(c, c->argv[2], &id2,` |
| `ev_bb37c39c7d86` | call_site | `third_party/redis/src/ae.c:456` | `fe->rfileProc(eventLoop,fd,fe->clientData,mask);` |
| `ev_bb4b035b3a2b` | call_site | `third_party/redis/src/db.c:1308` | `if (getIntFromObjectOrReply(c, c->argv[2], &dbid, NULL) != C_OK)` |
| `ev_bb73ed23c0d5` | call_site | `third_party/redis/src/dict.c:401` | `if (timeInMilliseconds()-start > ms) break;` |
| `ev_bba78f38e2a6` | call_site | `third_party/redis/src/bio.c:296` | `listDelNode(bio_jobs[worker], ln);` |
| `ev_bbaf9c06b890` | call_site | `third_party/redis/src/t_string.c:386` | `addReplyBulk(c,o);` |
| `ev_bbb8b2a3d342` | call_site | `third_party/redis/src/networking.c:1475` | `listUnlinkNode(server.clients_pending_write, &c->clients_pending_write_node);` |
| `ev_bbd5ff6483bd` | call_site | `third_party/redis/src/networking.c:2183` | `serverLog(LL_WARNING,"WARNING: Receiving inline protocol from master, master stream corruption? Closing the master connection and discarding the cached master.");` |
| `ev_bbdbae75e5a1` | call_site | `third_party/redis/src/networking.c:505` | `listAddNodeTail(c->deferred_reply_errors, sdsnewlen(s, len));` |
| `ev_bbfe63ac0228` | call_site | `third_party/redis/src/networking.c:2265` | `if (sdslen(c->querybuf)-c->qb_pos > PROTO_INLINE_MAX_SIZE) {` |
| `ev_bc123b1a1c5f` | call_site | `third_party/redis/src/networking.c:3055` | `sdsfree(o);` |
| `ev_bc2056b9df7e` | call_site | `third_party/redis/src/networking.c:1588` | `replicationCacheMaster(c);` |
| `ev_bc306f7430aa` | call_site | `third_party/redis/src/networking.c:2689` | `qblen = sdslen(c->querybuf);` |
| `ev_bc69f12828fa` | call_site | `third_party/redis/src/networking.c:652` | `afterErrorReply(c,s,sdslen(s),flags);` |
| `ev_bc7a8c7be7fd` | call_site | `third_party/redis/src/db.c:766` | `if (selectDb(c,id) == C_ERR) {` |
| `ev_bc866b3ecf81` | call_site | `third_party/redis/src/networking.c:989` | `addReplyAggregateLen(c,length,prefix);` |
| `ev_bcb58ccec031` | call_site | `third_party/redis/src/adlist.c:185` | `if (list->free) list->free(node->value);` |
| `ev_bcd536bfd88f` | call_site | `third_party/redis/src/t_string.c:421` | `if (getGenericCommand(c) == C_ERR) return;` |
| `ev_bce73498ee7c` | call_site | `third_party/redis/src/networking.c:1624` | `freeReplicaReferencedReplBuffer(c);` |
| `ev_bcfb8853b448` | call_site | `third_party/redis/src/networking.c:1467` | `connClose(c->conn);` |
| `ev_bd1f15772dfa` | call_site | `third_party/redis/src/networking.c:3074` | `sdsfree(o);` |
| `ev_bd2b75702f9c` | call_site | `third_party/redis/src/t_string.c:634` | `addReplyLongLong(c, value);` |
| `ev_bd338dcb0add` | call_site | `third_party/redis/src/networking.c:4329` | `if (!server.io_threads_active) startThreadedIO();` |
| `ev_bd45936c117a` | call_site | `third_party/redis/src/db.c:1530` | `scanDatabaseForDeletedKeys(db2, db1);` |
| `ev_bd716af4de40` | call_site | `third_party/redis/src/dict.c:374` | `_dictReset(d, 1);` |
| `ev_bd833f157197` | call_site | `third_party/redis/src/dict.c:1422` | `if (!dictTypeExpandAllowed(d))` |
| `ev_bd970c16447b` | call_site | `third_party/redis/src/db.c:1154` | `addReplyBulkCBuffer(c, key, sdslen(key));` |
| `ev_bdba8941766a` | call_site | `third_party/redis/src/networking.c:4336` | `while((ln = listNext(&li))) {` |
| `ev_bdea65cb32b5` | call_site | `third_party/redis/src/networking.c:2717` | `beforeNextClient(c);` |
| `ev_bdf2bdaff46f` | call_site | `third_party/redis/src/networking.c:979` | `addReplyLongLongWithPrefix(c,length,prefix);` |
| `ev_bdff5dad8d49` | call_site | `third_party/redis/src/networking.c:2184` | `setProtocolError("Master using the inline protocol. Desync?",c);` |
| `ev_be839a0f3fd8` | call_site | `third_party/redis/src/bio.c:215` | `redisSetCpuAffinity(server.bio_cpulist);` |
| `ev_be89fcaefc64` | call_site | `third_party/redis/src/t_string.c:936` | `addReplyLongLong(c,LCS(alen,blen));` |
| `ev_bf25647921a5` | call_site | `third_party/redis/src/db.c:1103` | `str = lpGet(p, &len, intbuf);` |
| `ev_bf4011944d83` | call_site | `third_party/redis/src/db.c:898` | `addReplyError(c, "invalid cursor");` |
| `ev_bf4403c7325e` | call_site | `third_party/redis/src/networking.c:4564` | `sds ci = catClientInfoString(sdsempty(),c);` |
| `ev_bf5590371781` | call_site | `third_party/redis/src/networking.c:129` | `connKeepAlive(conn,server.tcpkeepalive);` |
| `ev_bf6d350c7966` | call_site | `third_party/redis/src/networking.c:3337` | `prefix = zrealloc(prefix,sizeof(robj*)*(numprefix+1));` |
| `ev_bfa720fdbab3` | call_site | `third_party/redis/src/t_string.c:451` | `addReplyError(c,"offset is out of range");` |
| `ev_bfbe8aa1e0d6` | call_site | `third_party/redis/src/networking.c:3746` | `incrRefCount(newval);` |
| `ev_bfcb788257e5` | call_site | `third_party/redis/src/dict.c:833` | `if (entryIsNoValue(de)) return decodeEntryNoValue(de)->next;` |
| `ev_bfdeaeb6039d` | call_site | `third_party/redis/src/db.c:1630` | `if (dbSwapDatabases(id1,id2) == C_ERR) {` |
| `ev_bffa4485ca09` | call_site | `third_party/redis/src/networking.c:2323` | `addReplyErrorFormat(c,` |
| `ev_c00079ee50dc` | call_site | `third_party/redis/src/networking.c:3312` | `if (getLongLongFromObjectOrReply(c,c->argv[j],&redir,NULL) !=` |
| `ev_c06633aa35b1` | call_site | `third_party/redis/src/networking.c:4008` | `unblockClient(c, 1);` |
| `ev_c06f0277cbbb` | call_site | `third_party/redis/src/networking.c:2859` | `listRewind(server.clients,&li);` |
| `ev_c09a027dfd9f` | call_site | `third_party/redis/src/db.c:753` | `addReplyLongLong(c,count);` |
| `ev_c0d8860c81f6` | call_site | `third_party/redis/src/db.c:1683` | `dbGenericDelete(db,keyobj,server.lazyfree_lazy_expire,DB_FLAG_KEY_EXPIRED);` |
| `ev_c0e3f534bbe1` | call_site | `third_party/redis/src/t_string.c:467` | `o = createObject(OBJ_STRING,sdsnewlen(NULL, offset+sdslen(value)));` |
| `ev_c0e418a2a629` | call_site | `third_party/redis/src/dict.c:487` | `assert(entryIsKey(entry));` |
| `ev_c1254570635e` | call_site | `third_party/redis/src/t_string.c:671` | `getLongDoubleFromObjectOrReply(c,c->argv[2],&incr,NULL) != C_OK)` |
| `ev_c15bf2a52e22` | call_site | `third_party/redis/src/networking.c:4099` | `updateCachedTime(0);` |
| `ev_c1925afcfbf0` | call_site | `third_party/redis/src/dict.c:681` | `if (key == he_key \|\| dictCompareKeys(d, key, he_key))` |
| `ev_c1ab576ebc28` | call_site | `third_party/redis/src/lazyfree.c:36` | `freeTrackingRadixTree(rt);` |
| `ev_c1c110d5c805` | call_site | `third_party/redis/src/dict.c:487` | `assert(entryIsKey(entry));` |
| `ev_c1cde283c8b4` | call_site | `third_party/redis/src/networking.c:233` | `freeClientAsync(c);` |
| `ev_c1e19d56da56` | call_site | `third_party/redis/src/networking.c:1166` | `serverLog(LL_WARNING,"Client %s scheduled to be closed ASAP for overcoming of output buffer limits.", client);` |
| `ev_c1f7933095a4` | call_site | `third_party/redis/src/dict.c:630` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_c20372fdca4d` | call_site | `third_party/redis/src/networking.c:3306` | `addReplyError(c,"A client can only redirect to a single "` |
| `ev_c26fe655adac` | call_site | `third_party/redis/src/db.c:266` | `dictSetVal(db->dict, de, val);` |
| `ev_c277a0cf5705` | call_site | `third_party/redis/src/adlist.c:294` | `listRelease(copy);` |
| `ev_c2a1e75c51dc` | call_site | `third_party/redis/src/networking.c:1404` | `listRewind(server.slaves,&li);` |
| `ev_c32ec901998f` | call_site | `third_party/redis/src/dict.c:1140` | `assert(entryIsKey(*bucketref));` |
| `ev_c367a5808807` | call_site | `third_party/redis/src/ae_epoll.c:45` | `zfree(state);` |
| `ev_c38e00812ea2` | call_site | `third_party/redis/src/networking.c:3456` | `addReplyBulkCString(c,"flags");` |
| `ev_c38e8c756e4d` | call_site | `third_party/redis/src/networking.c:3290` | `addReply(c,shared.ok);` |
| `ev_c3d2b831fedd` | call_site | `third_party/redis/src/networking.c:3417` | `addReplyError(c,"CLIENT CACHING can be called only when the "` |
| `ev_c3ef7bdece23` | call_site | `third_party/redis/src/networking.c:1963` | `zmalloc_used_memory() < server.maxmemory) &&` |
| `ev_c3f89f31553e` | call_site | `third_party/redis/src/db.c:664` | `rdbSave(SLAVE_REQ_NONE,server.rdb_filename,rsiptr,RDBFLAGS_NONE);` |
| `ev_c4016875afc8` | call_site | `third_party/redis/src/networking.c:3713` | `serverAssertWithInfo(c,NULL,c->cmd != NULL);` |
| `ev_c40e0819d430` | call_site | `third_party/redis/src/dict.c:724` | `void *de_key = dictGetKey(*ref);` |
| `ev_c459ee82f3dc` | call_site | `third_party/redis/src/dict.c:475` | `size_t metasize = dictEntryMetadataSize(d);` |
| `ev_c46293294626` | call_site | `third_party/redis/src/networking.c:70` | `case OBJ_ENCODING_RAW: return sdslen(o->ptr);` |
| `ev_c46a89207803` | call_site | `third_party/redis/src/networking.c:2659` | `c->querybuf = sdsMakeRoomForNonGreedy(c->querybuf, readlen);` |
| `ev_c4703d794a13` | call_site | `third_party/redis/src/networking.c:3614` | `addReplyBulkCString(c,"mode");` |
| `ev_c4c71bfbe0ed` | call_site | `third_party/redis/src/dict.c:1138` | `if (entryIsKey(de)) {` |
| `ev_c4d48f76999b` | call_site | `third_party/redis/src/ae.c:71` | `monotonicInit();    /* just in case the calling app didn't initialize */` |
| `ev_c4d573d22085` | call_site | `third_party/redis/src/db.c:1108` | `p = lpNext(o->ptr, p);` |
| `ev_c4ecf19288b8` | call_site | `third_party/redis/src/networking.c:1129` | `addReplyStatusFormat(c,` |
| `ev_c51ad09ec85a` | call_site | `third_party/redis/src/networking.c:1066` | `sds reply = sdscatprintf(sdsempty(), "$%d\r\n%s\r\n", (unsigned)sdslen(s), s);` |
| `ev_c59e3e0f73d7` | call_site | `third_party/redis/src/networking.c:131` | `connSetPrivateData(conn, c);` |
| `ev_c5a5ee3d1c10` | call_site | `third_party/redis/src/networking.c:4567` | `sdsfree(ci);` |
| `ev_c5ad601eba25` | call_site | `third_party/redis/src/networking.c:1208` | `afterErrorReply(c, err, sdslen(err), 0);` |
| `ev_c5d3bda7a4cd` | call_site | `third_party/redis/src/adlist.c:46` | `if ((list = zmalloc(sizeof(*list))) == NULL)` |
| `ev_c5fd760eba89` | call_site | `third_party/redis/src/networking.c:3492` | `addReplyBulkCString(c,"redirect");` |
| `ev_c615d784824c` | call_site | `third_party/redis/src/networking.c:1059` | `addReplyLongLongWithPrefix(c,sdslen(s),'$');` |
| `ev_c62d2b3506e8` | call_site | `third_party/redis/src/networking.c:2285` | `addReplyError(c, "Protocol error: unauthenticated multibulk length");` |
| `ev_c65891142f08` | call_site | `third_party/redis/src/networking.c:1005` | `addReplyAggregateLen(c,length,'>');` |
| `ev_c68d23598c93` | call_site | `third_party/redis/src/networking.c:91` | `listAddNodeTail(server.clients,c);` |
| `ev_c699e88d6e04` | call_site | `third_party/redis/src/networking.c:2333` | `addReplyError(c,"Protocol error: invalid bulk length");` |
| `ev_c6d65a9c2947` | call_site | `third_party/redis/src/networking.c:2379` | `c->argv = zrealloc(c->argv, sizeof(robj*)*c->argv_len);` |
| `ev_c6e4592a78a3` | call_site | `third_party/redis/src/networking.c:3264` | `addReplyBulk(c,c->name);` |
| `ev_c78c302c0625` | call_site | `third_party/redis/src/networking.c:3215` | `addReplyLongLong(c,killed);` |
| `ev_c7ab4e6f972e` | call_site | `third_party/redis/src/networking.c:3407` | `disableTracking(c);` |
| `ev_c7bd4123446e` | call_site | `third_party/redis/src/dict.c:497` | `entry = zmalloc(sizeof(*entry) + metasize);` |
| `ev_c7c3658919c1` | call_site | `third_party/redis/src/t_string.c:459` | `addReply(c,shared.czero);` |
| `ev_c7c7c981efbd` | call_site | `third_party/redis/src/dict.c:190` | `memset(dictMetadata(d), 0, metasize);` |
| `ev_c7d501b39ed4` | call_site | `third_party/redis/src/db.c:1525` | `touchAllWatchedKeysInDb(db1, db2);` |
| `ev_c7ec446f489b` | call_site | `third_party/redis/src/networking.c:2215` | `sds client = catClientInfoString(sdsempty(),c);` |
| `ev_c7ee722a3125` | call_site | `third_party/redis/src/lazyfree.c:135` | `serverAssert(raxNext(&ri));` |
| `ev_c813ef9a9d9c` | call_site | `third_party/redis/src/networking.c:2279` | `ok = string2ll(c->querybuf+1+c->qb_pos,newline-(c->querybuf+1+c->qb_pos),&ll);` |
| `ev_c83d4daa0c3e` | call_site | `third_party/redis/src/t_string.c:913` | `addReplyArrayLen(c,2+withmatchlen);` |
| `ev_c8605e341339` | call_site | `third_party/redis/src/db.c:1136` | `if (!typecheck \|\| !objectTypeCompare(typecheck, type)) {` |
| `ev_c8bf932dd23d` | call_site | `third_party/redis/src/db.c:1105` | `p = lpNext(o->ptr, p);` |
| `ev_c8c6db1c6463` | call_site | `third_party/redis/src/networking.c:860` | `setDeferredAggregateLen(c,node,length,prefix);` |
| `ev_c8f54c823f03` | call_site | `third_party/redis/src/db.c:1810` | `key = createStringObject(key->ptr, sdslen(key->ptr));` |
| `ev_c908082447c2` | call_site | `third_party/redis/src/t_string.c:455` | `o = lookupKeyWrite(c->db,c->argv[1]);` |
| `ev_c92a9b092aa7` | call_site | `third_party/redis/src/dict.c:458` | `if (d->type->keyDup) key = d->type->keyDup(d, key);` |
| `ev_c92ae3fd0a52` | call_site | `third_party/redis/src/db.c:2017` | `return moduleGetCommandKeysViaAPI(cmd,argv,argc,result);` |
| `ev_c9755f52b731` | call_site | `third_party/redis/src/connection.h:286` | `return conn->type->addr(conn, ip, ip_len, port, remote);` |
| `ev_c98ae61ce6fe` | call_site | `third_party/redis/src/networking.c:3948` | `int can_receive_writes = connHasWriteHandler(slave->conn) \|\|` |
| `ev_c99f26162df2` | call_site | `third_party/redis/src/db.c:2490` | `keys = getKeysPrepareResult(result, num);` |
| `ev_c9ffc3516bc6` | call_site | `third_party/redis/src/db.c:1154` | `addReplyBulkCBuffer(c, key, sdslen(key));` |
| `ev_ca2c0566ba0b` | call_site | `third_party/redis/src/networking.c:57` | `serverAssertWithInfo(NULL,o,o->type == OBJ_STRING);` |
| `ev_ca4b4842099b` | call_site | `third_party/redis/src/db.c:177` | `robj *o = lookupKeyRead(c->db, key);` |
| `ev_ca5c6045bbb5` | call_site | `third_party/redis/src/networking.c:3457` | `void *arraylen_ptr = addReplyDeferredLen(c);` |
| `ev_ca5d22ce42cb` | call_site | `third_party/redis/src/networking.c:3341` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_caef9da841bc` | call_site | `third_party/redis/src/t_string.c:791` | `if (sdslen(a) >= UINT32_MAX-1 \|\| sdslen(b) >= UINT32_MAX-1) {` |
| `ev_caf4c36bcfd8` | call_site | `third_party/redis/src/db.c:1411` | `expire = getExpire(c->db,key);` |
| `ev_cb8c5556684c` | call_site | `third_party/redis/src/t_string.c:309` | `c->argv[2] = tryObjectEncoding(c->argv[2]);` |
| `ev_cba793aa77fa` | call_site | `third_party/redis/src/db.c:1340` | `incrRefCount(o);` |
| `ev_cbc1d4e1646f` | call_site | `third_party/redis/src/t_string.c:304` | `c->argv[2] = tryObjectEncoding(c->argv[2]);` |
| `ev_cbc34c85e552` | call_site | `third_party/redis/src/dict.c:1368` | `dictDefragBucket(d, &d->ht_table[htidx1][v & m1], defragfns);` |
| `ev_cbcd9058e5cc` | call_site | `third_party/redis/src/networking.c:1558` | `moduleFireServerEvent(REDISMODULE_EVENT_CLIENT_CHANGE,` |
| `ev_cbe0da2227da` | call_site | `third_party/redis/src/networking.c:459` | `_addReplyToBufferOrList(c,s,sdslen(s));` |
| `ev_cc08bb37cca4` | call_site | `third_party/redis/src/networking.c:488` | `if (!len \|\| s[0] != '-') addReplyProto(c,"-ERR ",5);` |
| `ev_cc120a9c50d1` | call_site | `third_party/redis/src/db.c:469` | `dictEmpty(dbarray[j].dict,callback);` |
| `ev_cc3eb6f993b7` | call_site | `third_party/redis/src/networking.c:1839` | `*nwritten = connWritev(c->conn, iov, iovcnt);` |
| `ev_cc4c18a04152` | call_site | `third_party/redis/src/dict.c:819` | `assert(entryHasValue(de));` |
| `ev_cc739708f1b9` | call_site | `third_party/redis/src/networking.c:3390` | `addReplyError(c,` |
| `ev_cc797346d296` | call_site | `third_party/redis/src/networking.c:1567` | `zfree(c->module_blocked_client);` |
| `ev_cc7a903ba2a0` | call_site | `third_party/redis/src/networking.c:524` | `incrementErrorCount("ERR", 3);` |
| `ev_ccabce0283bc` | call_site | `third_party/redis/src/networking.c:865` | `setDeferredAggregateLen(c,node,length,'\|');` |
| `ev_cce824b30739` | call_site | `third_party/redis/src/db.c:1815` | `decrRefCount(key);` |
| `ev_cd06a8473e8c` | call_site | `third_party/redis/src/db.c:1173` | `addReplyLongLong(c,server.lastsave);` |
| `ev_cd375709eb90` | call_site | `third_party/redis/src/networking.c:2674` | `serverLog(LL_VERBOSE, "Reading from client: %s",connGetLastError(c->conn));` |
| `ev_cdab3fc4fb1e` | call_site | `third_party/redis/src/networking.c:1866` | `listDelNode(c->reply, next);` |
| `ev_cdd08b67ccf3` | call_site | `third_party/redis/src/adlist.c:184` | `listUnlinkNode(list, node);` |
| `ev_cddb70fd9512` | call_site | `third_party/redis/src/dict.c:1373` | `fn(privdata, de);` |
| `ev_ce0f795365c1` | call_site | `third_party/redis/src/connection.h:227` | `return conn->type->set_write_handler(conn, func, 0);` |
| `ev_ce5e35057587` | call_site | `third_party/redis/src/networking.c:2957` | `incrRefCount(valob);` |
| `ev_ce9d79f0c1fd` | call_site | `third_party/redis/src/networking.c:4265` | `serverLog(LL_WARNING,` |
| `ev_ceee5d027588` | call_site | `third_party/redis/src/networking.c:801` | `listDelNode(c->reply,ln);` |
| `ev_cf17bf7003a2` | call_site | `third_party/redis/src/networking.c:1077` | `addReplyBulkCBuffer(c,s,strlen(s));` |
| `ev_cf1bd8153a65` | call_site | `third_party/redis/src/t_string.c:422` | `if (dbSyncDelete(c->db, c->argv[1])) {` |
| `ev_cf31e5e96b90` | call_site | `third_party/redis/src/dict.c:767` | `assert(entryHasValue(de));` |
| `ev_cfc09103a9aa` | call_site | `third_party/redis/src/networking.c:3676` | `decrRefCount(c->original_argv[argc]);` |
| `ev_d026e93f3efd` | call_site | `third_party/redis/src/networking.c:1206` | `while((ln = listNext(&li))) {` |
| `ev_d03a83119e80` | call_site | `third_party/redis/src/networking.c:1252` | `freeClientAsync(c);` |
| `ev_d049f7eedc2e` | call_site | `third_party/redis/src/networking.c:4334` | `listRewind(server.clients_pending_write,&li);` |
| `ev_d04df75c10ef` | call_site | `third_party/redis/src/t_string.c:477` | `olen = stringObjectLen(o);` |
| `ev_d0550eb69861` | call_site | `third_party/redis/src/db.c:741` | `delGenericCommand(c,1);` |
| `ev_d057e2723604` | call_site | `third_party/redis/src/t_string.c:94` | `if (getGenericCommand(c) == C_ERR) return;` |
| `ev_d058dea64a51` | call_site | `third_party/redis/src/t_string.c:692` | `rewriteClientCommandArgument(c,0,shared.set);` |
| `ev_d0d7431e4f1a` | call_site | `third_party/redis/src/db.c:1346` | `notifyKeyspaceEvent(NOTIFY_GENERIC,` |
| `ev_d100d2dff5af` | call_site | `third_party/redis/src/db.c:1261` | `expire = getExpire(c->db,c->argv[1]);` |
| `ev_d12550124753` | call_site | `third_party/redis/src/networking.c:562` | `serverLog(LL_WARNING,"== CRITICAL == This %s is sending an error "` |
| `ev_d15c6a39ebbe` | call_site | `third_party/redis/src/networking.c:1124` | `sds cmd = sdsnew((char*) c->argv[0]->ptr);` |
| `ev_d1a5fc7ade29` | call_site | `third_party/redis/src/networking.c:521` | `incrementErrorCount(s+1, errEndPos-1);` |
| `ev_d1e94e0419b8` | call_site | `third_party/redis/src/networking.c:1626` | `freeClientOriginalArgv(c);` |
| `ev_d21c31060748` | call_site | `third_party/redis/src/t_string.c:484` | `if (checkStringLength(c,offset,sdslen(value)) != C_OK)` |
| `ev_d23d33350071` | call_site | `third_party/redis/src/dict.c:344` | `if (!entryIsKey(de)) zfree(decodeMaskedPtr(de));` |
| `ev_d23d865627cf` | call_site | `third_party/redis/src/t_string.c:598` | `msetGenericCommand(c,1);` |
| `ev_d273ac8ab34f` | call_site | `third_party/redis/src/db.c:1312` | `addReplyError(c,"DB index is out of range");` |
| `ev_d27567b55468` | call_site | `third_party/redis/src/t_string.c:48` | `addReplyError(c,"string exceeds maximum allowed size (proto-max-bulk-len)");` |
| `ev_d3557b97b652` | call_site | `third_party/redis/src/db.c:120` | `if (!hasActiveChildProcess() && !(flags & LOOKUP_NOTOUCH)){` |
| `ev_d36dc3ce5b15` | call_site | `third_party/redis/src/db.c:1084` | `len = ll2string(buf, sizeof(buf), llele);` |
| `ev_d3bff74ce13c` | call_site | `third_party/redis/src/t_string.c:426` | `notifyKeyspaceEvent(NOTIFY_GENERIC, "del", c->argv[1], c->db->id);` |
| `ev_d3e241455c5f` | call_site | `third_party/redis/src/networking.c:3145` | `if (getRangeLongFromObjectOrReply(c, c->argv[i+1], 1, LONG_MAX, &tmp,` |
| `ev_d3e8c67c9386` | call_site | `third_party/redis/src/networking.c:3373` | `addReplyError(c,` |
| `ev_d403f461b4d8` | call_site | `third_party/redis/src/lazyfree.c:210` | `bioCreateLazyFreeJob(lazyFreeFunctionsCtx,1,functions_lib_ctx);` |
| `ev_d494b10b6283` | call_site | `third_party/redis/src/networking.c:1529` | `pubsubUnsubscribeAllChannels(c,0);` |
| `ev_d49aba731381` | call_site | `third_party/redis/src/dict.c:596` | `return dictGenericDelete(ht,key,0) ? DICT_OK : DICT_ERR;` |
| `ev_d4aa1701c2df` | call_site | `third_party/redis/src/networking.c:2857` | `sds o = sdsnewlen(SDS_NOINIT,200*listLength(server.clients));` |
| `ev_d4c76f27c79e` | call_site | `third_party/redis/src/db.c:874` | `int len = ld2string(buf, sizeof(buf), *(double *)dictGetVal(de), LD_STR_AUTO);` |
| `ev_d4db94b49b73` | call_site | `third_party/redis/src/t_string.c:715` | `if (checkStringLength(c,stringObjectLen(o),sdslen(append->ptr)) != C_OK)` |
| `ev_d4de32110037` | call_site | `third_party/redis/src/dict.c:1457` | `void *he_key = dictGetKey(he);` |
| `ev_d4ecda8cc54b` | call_site | `third_party/redis/src/networking.c:2688` | `sdsIncrLen(c->querybuf,nread);` |
| `ev_d525c16f3462` | call_site | `third_party/redis/src/dict.c:326` | `h = dictHashKey(d, key) & DICTHT_SIZE_MASK(d->ht_size_exp[1]);` |
| `ev_d532c5ba271c` | call_site | `third_party/redis/src/networking.c:438` | `_addReplyToBufferOrList(c,obj->ptr,sdslen(obj->ptr));` |
| `ev_d53eaf711d84` | call_site | `third_party/redis/src/dict.c:564` | `if (dictIsRehashing(d)) _dictRehashStep(d);` |
| `ev_d588c8c15298` | call_site | `third_party/redis/src/networking.c:1208` | `afterErrorReply(c, err, sdslen(err), 0);` |
| `ev_d594d9cb4799` | call_site | `third_party/redis/src/networking.c:2623` | `if (postponeClientRead(c)) return;` |
| `ev_d5a2aaff46a7` | call_site | `third_party/redis/src/networking.c:4067` | `updatePausedActions();` |
| `ev_d60416454772` | call_site | `third_party/redis/src/dict.c:1183` | `if (count == 0) return dictGetRandomKey(d);` |
| `ev_d62de808f87a` | call_site | `third_party/redis/src/dict.c:799` | `if (entryIsNoValue(de)) return decodeEntryNoValue(de)->key;` |
| `ev_d6610219a78f` | call_site | `third_party/redis/src/db.c:1385` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_d67d4defae24` | call_site | `third_party/redis/src/networking.c:604` | `if (sdslen(rep) > 1 && rep[0] == '-') {` |
| `ev_d68433120ccb` | assignment | `third_party/redis/src/lazyfree.c:200` | `bioCreateLazyFreeJob(lazyFreeLuaScripts,1,lua_scripts);` |
| `ev_d69a2dd2eeeb` | call_site | `third_party/redis/src/t_string.c:434` | `setKey(c,c->db,c->argv[1],c->argv[2],0);` |
| `ev_d6b786ef2b0d` | call_site | `third_party/redis/src/networking.c:2667` | `readlen = sdsavail(c->querybuf);` |
| `ev_d6d3d3a6905e` | call_site | `third_party/redis/src/dict.c:742` | `dictFreeKey(d, he);` |
| `ev_d6e680fe5175` | call_site | `third_party/redis/src/networking.c:401` | `if (getClientType(c) == CLIENT_TYPE_SLAVE) {` |
| `ev_d73c05712273` | call_site | `third_party/redis/src/db.c:1081` | `setTypeIterator *si = setTypeInitIterator(o);` |
| `ev_d766c67f5398` | call_site | `third_party/redis/src/networking.c:1059` | `addReplyLongLongWithPrefix(c,sdslen(s),'$');` |
| `ev_d77525c6ba71` | call_site | `third_party/redis/src/dict.c:782` | `assert(entryHasValue(de));` |
| `ev_d78763464933` | call_site | `third_party/redis/src/db.c:1256` | `addReply(c,nx ? shared.czero : shared.ok);` |
| `ev_d7c5692b2410` | call_site | `third_party/redis/src/networking.c:1679` | `if (c->flags & CLIENT_MASTER) replicationHandleMasterDisconnection();` |
| `ev_d84f89bf5822` | call_site | `third_party/redis/src/networking.c:3462` | `addReplyBulkCString(c,"bcast");` |
| `ev_d86a1d953ddf` | call_site | `third_party/redis/src/dict.c:154` | `assert(((uintptr_t)ptr & ENTRY_PTR_MASK) == 0);` |
| `ev_d88800bbbc03` | call_site | `third_party/redis/src/bio.c:280` | `if (reclaimFilePageCache(job->fd_args.fd, 0, 0) == -1) {` |
| `ev_d8a86350330e` | call_site | `third_party/redis/src/db.c:1213` | `addReplyError(c, "No shutdown in progress.");` |
| `ev_d8d2724f5c6f` | call_site | `third_party/redis/src/db.c:1165` | `scanGenericCommand(c,NULL,cursor);` |
| `ev_d9001d1943e9` | call_site | `third_party/redis/src/ae.c:379` | `eventLoop->beforesleep(eventLoop);` |
| `ev_d90bdfe578d0` | call_site | `third_party/redis/src/networking.c:926` | `decrRefCount(o);` |
| `ev_d91914003bf5` | call_site | `third_party/redis/src/networking.c:1824` | `while ((next = listNext(&iter)) && iovcnt < iovmax && iov_bytes_len < NET_MAX_WRITES_PER_EVENT) {` |
| `ev_d9354c080553` | call_site | `third_party/redis/src/networking.c:999` | `addReplyAggregateLen(c,length,'\|');` |
| `ev_d96dc5daa954` | call_site | `third_party/redis/src/dict.c:809` | `assert(entryHasValue(de));` |
| `ev_d9d2088fd5ac` | call_site | `third_party/redis/src/t_string.c:649` | `incrDecrCommand(c,incr);` |
| `ev_d9ecb922ed2e` | call_site | `third_party/redis/src/db.c:1726` | `decrRefCount(argv[1]);` |
| `ev_da02db26e331` | call_site | `third_party/redis/src/db.c:1658` | `serverAssertWithInfo(NULL,key,kde != NULL);` |
| `ev_da10f9cd548c` | call_site | `third_party/redis/src/db.c:1481` | `while((de = dictNext(di)) != NULL) {` |
| `ev_da28d2dbbf65` | call_site | `third_party/redis/src/networking.c:751` | `reqresSaveClientReplyOffset(c);` |
| `ev_da85a2986b77` | call_site | `third_party/redis/src/db.c:1576` | `touchAllWatchedKeysInDb(activedb, newdb);` |
| `ev_da8de070d44d` | call_site | `third_party/redis/src/db.c:365` | `incrRefCount(val);` |
| `ev_dabb61598158` | call_site | `third_party/redis/src/dict.c:549` | `entry = dictAddRaw(d,key,&existing);` |
| `ev_dafc3ef3f826` | call_site | `third_party/redis/src/db.c:375` | `freeObjAsync(key, dictGetVal(de), db->id);` |
| `ev_db1bc6ab10c4` | call_site | `third_party/redis/src/db.c:1391` | `addReplyError(c,"Copying to another database is not allowed in cluster mode");` |
| `ev_db99761e6c20` | call_site | `third_party/redis/src/db.c:1348` | `notifyKeyspaceEvent(NOTIFY_GENERIC,` |
| `ev_db9db9ba154a` | call_site | `third_party/redis/src/dict.c:343` | `assert(entryIsKey(key));` |
| `ev_dc083aee48d9` | call_site | `third_party/redis/src/lazyfree.c:160` | `size_t free_effort = lazyfreeGetFreeEffort(key,obj,dbid);` |
| `ev_dc69485a988a` | call_site | `third_party/redis/src/dict.c:573` | `if (key == he_key \|\| dictCompareKeys(d, key, he_key)) {` |
| `ev_dc8981acb078` | call_site | `third_party/redis/src/networking.c:502` | `c->deferred_reply_errors = listCreate();` |
| `ev_dcbde6199b3b` | call_site | `third_party/redis/src/dict.c:396` | `long long start = timeInMilliseconds();` |
| `ev_dcdda44418d7` | call_site | `third_party/redis/src/db.c:1715` | `incrRefCount(argv[0]);` |
| `ev_dce8dbd686b8` | call_site | `third_party/redis/src/db.c:279` | `dbSetValue(db, key, val, 0, NULL);` |
| `ev_dd205495781a` | call_site | `third_party/redis/src/db.c:89` | `dictEntry *de = dictFind(db->dict,key->ptr);` |
| `ev_dd47b7eb99d3` | call_site | `third_party/redis/src/db.c:1434` | `newobj = moduleTypeDupOrReply(c, key, newkey, dst->id, o);` |
| `ev_dd98aa948272` | call_site | `third_party/redis/src/networking.c:2273` | `if (newline-(c->querybuf+c->qb_pos) > (ssize_t)(sdslen(c->querybuf)-c->qb_pos-2))` |
| `ev_dde377fcff44` | call_site | `third_party/redis/src/dict.c:166` | `return decodeMaskedPtr(de);` |
| `ev_ddea802f9f4e` | call_site | `third_party/redis/src/t_string.c:381` | `if (expire && getExpireMillisecondsOrReply(c, expire, flags, unit, &milliseconds) != C_OK) {` |
| `ev_de442268fd8c` | call_site | `third_party/redis/src/networking.c:651` | `addReplyErrorLength(c,s,sdslen(s));` |
| `ev_de6177ecc220` | call_site | `third_party/redis/src/db.c:1087` | `if (use_pattern && !stringmatchlen(pat, sdslen(pat), key, len, 0)) {` |
| `ev_de647213c494` | call_site | `third_party/redis/src/networking.c:1047` | `addReplyProto(c,"\r\n",2);` |
| `ev_de8c06cad202` | call_site | `third_party/redis/src/networking.c:2219` | `if (sdslen(c->querybuf)-c->qb_pos < PROTO_DUMP_LEN) {` |
| `ev_de9952f16626` | call_site | `third_party/redis/src/networking.c:3912` | `serverAssert(c->reply_bytes < SIZE_MAX-(1024*64));` |
| `ev_dea709f0838a` | call_site | `third_party/redis/src/dict.c:1178` | `unsigned int count = dictGetSomeKeys(d,entries,GETFAIR_NUM_ENTRIES);` |
| `ev_deda960d182e` | call_site | `third_party/redis/src/networking.c:3787` | `mem += sdsZmallocSize(c->querybuf);` |
| `ev_dee68da842c6` | call_site | `third_party/redis/src/networking.c:1585` | `serverLog(LL_NOTICE,"Connection with master lost.");` |
| `ev_df330ce893ac` | call_site | `third_party/redis/src/db.c:1137` | `listDelNode(keys, ln);` |
| `ev_df451c057f93` | call_site | `third_party/redis/src/networking.c:869` | `serverAssert(c->resp >= 3);` |
| `ev_df5b8ccc79e6` | call_site | `third_party/redis/src/networking.c:4282` | `handleClientsWithPendingReadsUsingThreads();` |
| `ev_df7941e6a75b` | call_site | `third_party/redis/src/db.c:781` | `addReplyBulk(c,key);` |
| `ev_df7c595973bd` | call_site | `third_party/redis/src/db.c:797` | `sds key = dictGetKey(de);` |
| `ev_dfc6eebafc6c` | call_site | `third_party/redis/src/networking.c:1669` | `refreshGoodSlavesCount();` |
| `ev_dff4883c27ea` | call_site | `third_party/redis/src/networking.c:2705` | `sdsfree(ci);` |
| `ev_e00642d76b9a` | call_site | `third_party/redis/src/networking.c:2751` | `c->peerid = sdsnew(peerid);` |
| `ev_e01cc49862bd` | call_site | `third_party/redis/src/networking.c:3918` | `sds client = catClientInfoString(sdsempty(),c);` |
| `ev_e05d8d72d46d` | call_site | `third_party/redis/src/db.c:347` | `if (expireIfNeeded(db,keyobj,0)) {` |
| `ev_e0a2e7a0c11d` | call_site | `third_party/redis/src/db.c:382` | `if (dictSize(db->expires) > 0) dictDelete(db->expires,key->ptr);` |
| `ev_e0c0fb67fe5e` | call_site | `third_party/redis/src/db.c:1659` | `de = dictAddOrFind(db->expires,dictGetKey(kde));` |
| `ev_e111897e1350` | call_site | `third_party/redis/src/t_string.c:757` | `obja = obja ? getDecodedObject(obja) : createStringObject("",0);` |
| `ev_e16f119d3a38` | call_site | `third_party/redis/src/networking.c:2362` | `c->querybuf = sdsMakeRoomForNonGreedy(c->querybuf,ll+2-sdslen(c->querybuf));` |
| `ev_e1b3832c9ee8` | call_site | `third_party/redis/src/db.c:264` | `old = dictGetVal(de);` |
| `ev_e1b66a722b5e` | call_site | `third_party/redis/src/db.c:751` | `if (lookupKeyReadWithFlags(c->db,c->argv[j],LOOKUP_NOTOUCH)) count++;` |
| `ev_e1f69dc3275d` | call_site | `third_party/redis/src/networking.c:216` | `initClientMultiState(c);` |
| `ev_e21975271368` | call_site | `third_party/redis/src/db.c:1408` | `addReply(c,shared.czero);` |
| `ev_e223031f1bfc` | call_site | `third_party/redis/src/networking.c:2910` | `if (c->name) decrRefCount(c->name);` |
| `ev_e27e4dd88f9c` | call_site | `third_party/redis/src/networking.c:4390` | `while((ln = listNext(&li))) {` |
| `ev_e2a0ebb331f1` | call_site | `third_party/redis/src/networking.c:1246` | `client *c = connGetPrivateData(conn);` |
| `ev_e2a80b5c3d4f` | call_site | `third_party/redis/src/networking.c:1040` | `addReplyLongLongWithPrefix(c,len,'$');` |
| `ev_e2b393d1fb83` | call_site | `third_party/redis/src/dict.c:498` | `assert(entryIsNormal(entry)); /* Check alignment of allocation */` |
| `ev_e31f91ecc393` | call_site | `third_party/redis/src/t_string.c:412` | `signalModifiedKey(c, c->db, c->argv[1]);` |
| `ev_e32a410a63f6` | call_site | `third_party/redis/src/dict.c:1140` | `assert(entryIsKey(*bucketref));` |
| `ev_e355008bf803` | call_site | `third_party/redis/src/db.c:1687` | `signalModifiedKey(NULL, db, keyobj);` |
| `ev_e359c9c3db74` | call_site | `third_party/redis/src/networking.c:1345` | `connFormatAddr(conn, addr, sizeof(addr), 1);` |
| `ev_e3c3d8177eff` | call_site | `third_party/redis/src/t_string.c:583` | `setKey(c, c->db, c->argv[j], c->argv[j + 1], setkey_flags);` |
| `ev_e3d1d6c7e258` | call_site | `third_party/redis/src/t_string.c:606` | `if (checkType(c,o,OBJ_STRING)) return;` |
| `ev_e3ef23259006` | call_site | `third_party/redis/src/db.c:1432` | `case OBJ_STREAM: newobj = streamDup(o); break;` |
| `ev_e3fab4e6791f` | call_site | `third_party/redis/src/t_string.c:492` | `o->ptr = sdsgrowzero(o->ptr,offset+sdslen(value));` |
| `ev_e43f72faa638` | call_site | `third_party/redis/src/t_string.c:685` | `notifyKeyspaceEvent(NOTIFY_STRING,"incrbyfloat",c->argv[1],c->db->id);` |
| `ev_e45e74dbb830` | call_site | `third_party/redis/src/networking.c:2267` | `setProtocolError("too big mbulk count string",c);` |
| `ev_e4ac202076eb` | call_site | `third_party/redis/src/networking.c:4493` | `serverAssert(!(c->flags & CLIENT_BLOCKED));` |
| `ev_e5049e628961` | call_site | `third_party/redis/src/db.c:2275` | `return genericGetKeys(0, 2, 3, 1, argv, argc, result);` |
| `ev_e52688256a92` | call_site | `third_party/redis/src/db.c:1777` | `if (!keyIsExpired(db,key)) return 0;` |
| `ev_e539172d7f22` | call_site | `third_party/redis/src/dict.c:344` | `if (!entryIsKey(de)) zfree(decodeMaskedPtr(de));` |
| `ev_e53aab7268cf` | call_site | `third_party/redis/src/db.c:1120` | `serverPanic("Not handled encoding in SCAN.");` |
| `ev_e543fd7abe46` | call_site | `third_party/redis/src/dict.c:1149` | `assert(entryIsNormal(de));` |
| `ev_e55ad1bd9aa2` | call_site | `third_party/redis/src/db.c:1374` | `if (getIntFromObjectOrReply(c, c->argv[j+1], &dbid, NULL) != C_OK)` |
| `ev_e579018ac224` | call_site | `third_party/redis/src/dict.c:490` | `entry = createEntryNoValue(key, *bucket);` |
| `ev_e652fc4b0526` | call_site | `third_party/redis/src/bio.c:197` | `bio_job *job = zmalloc(sizeof(*job));` |
| `ev_e66d202e683a` | call_site | `third_party/redis/src/dict.c:793` | `assert(entryHasValue(de));` |
| `ev_e68194783368` | call_site | `third_party/redis/src/networking.c:3504` | `raxStart(&ri,c->client_tracking_prefixes);` |
| `ev_e682f22c2ee7` | assignment | `third_party/redis/src/lazyfree.c:181` | `bioCreateLazyFreeJob(lazyfreeFreeDatabase,2,oldht1,oldht2);` |
| `ev_e6942d90f1fa` | call_site | `third_party/redis/src/networking.c:2978` | `addReplyStatus(c,"RESET");` |
| `ev_e69fd706d30a` | call_site | `third_party/redis/src/networking.c:1087` | `addReplyBulkCBuffer(c,buf,len);` |
| `ev_e6a93398ae70` | call_site | `third_party/redis/src/db.c:984` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_e6bf7fe39584` | call_site | `third_party/redis/src/dict.c:1475` | `_dictClear(d,1,callback);` |
| `ev_e6e3a695da30` | call_site | `third_party/redis/src/networking.c:1251` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_e6ff3212a78e` | call_site | `third_party/redis/src/db.c:2008` | `int ret = getKeysUsingKeySpecs(cmd,argv,argc,search_flags,result);` |
| `ev_e733e523c2a7` | call_site | `third_party/redis/src/networking.c:839` | `setDeferredReply(c, node, shared.sethdr[length]->ptr, hdr_len);` |
| `ev_e7737e51d8be` | call_site | `third_party/redis/src/lazyfree.c:137` | `effort += raxSize(s->cgroups)*(1+raxSize(cg->pel));` |
| `ev_e7da4058e210` | call_site | `third_party/redis/src/networking.c:4078` | `updatePausedActions();` |
| `ev_e7dc5a0c662b` | call_site | `third_party/redis/src/t_string.c:539` | `addReplyBulkCBuffer(c,(char*)str+start,end-start+1);` |
| `ev_e7eecf08ead0` | call_site | `third_party/redis/src/bio.c:287` | `job->free_args.free_fn(job->free_args.free_args);` |
| `ev_e86aef2bf6d3` | call_site | `third_party/redis/src/networking.c:831` | `setDeferredReply(c, node, shared.mbulkhdr[length]->ptr, hdr_len);` |
| `ev_e8c2b5fba4a7` | call_site | `third_party/redis/src/t_string.c:512` | `if ((o = lookupKeyReadOrReply(c,c->argv[1],shared.emptybulk)) == NULL \|\|` |
| `ev_e8c6a3f0129a` | call_site | `third_party/redis/src/dict.c:1021` | `while(listele--) he = dictGetNext(he);` |
| `ev_e8d3d1a2aea0` | call_site | `third_party/redis/src/rio.h:114` | `if (r->write(r,buf,bytes_to_write) == 0) {` |
| `ev_e8f61ddc165a` | call_site | `third_party/redis/src/db.c:860` | `if (!stringmatchlen(data->pattern, sdslen(data->pattern), keysds, sdslen(keysds), 0)) {` |
| `ev_e904dde330f9` | call_site | `third_party/redis/src/networking.c:1366` | `if (connGetState(conn) == CONN_STATE_ERROR)` |
| `ev_e919b52d74f3` | call_site | `third_party/redis/src/networking.c:3253` | `addReply(c,shared.cone);` |
| `ev_e93790ece6e8` | call_site | `third_party/redis/src/networking.c:2553` | `if (processInlineBuffer(c) != C_OK) break;` |
| `ev_e966de232cb4` | call_site | `third_party/redis/src/networking.c:3152` | `addReplyErrorFormat(c,"Unknown client type '%s'",` |
| `ev_e9ac851dcdce` | call_site | `third_party/redis/src/dict.c:1596` | `l = _dictGetStatsHt(buf,bufsize,d,0,full);` |
| `ev_e9c09fe4cacc` | call_site | `third_party/redis/src/networking.c:3248` | `unblockClientOnError(target,` |
| `ev_e9c933a0fe45` | call_site | `third_party/redis/src/networking.c:2764` | `genClientAddrString(c,sockname,sizeof(sockname),0);` |
| `ev_e9f78b848502` | call_site | `third_party/redis/src/db.c:435` | `serverAssert(o->type == OBJ_STRING);` |
| `ev_ea737bd2c001` | call_site | `third_party/redis/src/networking.c:568` | `showLatestBacklog();` |
| `ev_ea744d68f170` | call_site | `third_party/redis/src/networking.c:2392` | `sdsIncrLen(c->querybuf,-2); /* remove CRLF */` |
| `ev_ea8a09a71e1c` | call_site | `third_party/redis/src/networking.c:998` | `serverAssert(c->resp >= 3);` |
| `ev_ea8fe6093856` | call_site | `third_party/redis/src/networking.c:1003` | `serverAssert(c->resp >= 3);` |
| `ev_eabd48cc7bc3` | call_site | `third_party/redis/src/networking.c:3736` | `c->argv = zrealloc(c->argv,sizeof(robj*)*(i+1));` |
| `ev_eac5d336562c` | call_site | `third_party/redis/src/networking.c:2522` | `while(c->qb_pos < sdslen(c->querybuf)) {` |
| `ev_ead3f1bfa09e` | call_site | `third_party/redis/src/db.c:1659` | `de = dictAddOrFind(db->expires,dictGetKey(kde));` |
| `ev_eadd9c28b43a` | call_site | `third_party/redis/src/ae_epoll.c:70` | `zfree(state->events);` |
| `ev_eb09f3a91395` | call_site | `third_party/redis/src/db.c:2255` | `return genericGetKeys(0, 2, 3, 1, argv, argc, result);` |
| `ev_eb3f1114c72e` | call_site | `third_party/redis/src/db.c:259` | `moduleNotifyKeyUnlink(key,old,db->id,DB_FLAG_KEY_OVERWRITE);` |
| `ev_eb4eecec5e77` | call_site | `third_party/redis/src/networking.c:4239` | `io_threads_list[i] = listCreate();` |
| `ev_eb65f9ded76d` | call_site | `third_party/redis/src/db.c:724` | `dbSyncDelete(c->db,c->argv[j]);` |
| `ev_ebc7616015d2` | call_site | `third_party/redis/src/ae.c:331` | `retval = te->timeProc(eventLoop, id, te->clientData);` |
| `ev_ebc9b01a3c17` | call_site | `third_party/redis/src/db.c:2294` | `keys = getKeysPrepareResult(result, 1);` |
| `ev_ebdf315ad264` | call_site | `third_party/redis/src/adlist.c:326` | `listRewind(list, &iter);` |
| `ev_ec27c0f2cc32` | call_site | `third_party/redis/src/t_string.c:934` | `setDeferredArrayLen(c,arraylenptr,arraylen);` |
| `ev_ec5b33c69aba` | call_site | `third_party/redis/src/adlist.c:329` | `if (list->match(node->value, key)) {` |
| `ev_ec64e971192f` | call_site | `third_party/redis/src/networking.c:1045` | `addReplyBulkLen(c,obj);` |
| `ev_ec76d5181800` | call_site | `third_party/redis/src/networking.c:4565` | `serverLog(LL_NOTICE, "Evicting client: %s", ci);` |
| `ev_ec839420aa26` | call_site | `third_party/redis/src/db.c:272` | `db->dict->type->valDestructor(db->dict, old);` |
| `ev_ecba165a05fa` | call_site | `third_party/redis/src/dict.c:110` | `return siphash(key,len,dict_hash_function_seed);` |
| `ev_ecd13711bf35` | call_site | `third_party/redis/src/networking.c:1737` | `sdsfree(info);` |
| `ev_ed2ee65ac965` | call_site | `third_party/redis/src/networking.c:489` | `addReplyProto(c,s,len);` |
| `ev_ed339e6fadd5` | call_site | `third_party/redis/src/networking.c:2282` | `setProtocolError("invalid mbulk count",c);` |
| `ev_ed3c28db4c64` | call_site | `third_party/redis/src/networking.c:3729` | `retainOriginalCommandVector(c);` |
| `ev_ed617bbc86c3` | call_site | `third_party/redis/src/networking.c:1614` | `pubsubUnsubscribeAllChannels(c,0);` |
| `ev_ed9a90986887` | call_site | `third_party/redis/src/networking.c:2160` | `argv = sdssplitargs(aux,&argc);` |
| `ev_edda40d55e1b` | call_site | `third_party/redis/src/networking.c:647` | `s = sdstrim(s, "\r\n");` |
| `ev_ee0986e8dfb1` | call_site | `third_party/redis/src/networking.c:3234` | `addReplyError(c,` |
| `ev_ee1de2e98082` | call_site | `third_party/redis/src/db.c:810` | `setDeferredArrayLen(c,replylen,numkeys);` |
| `ev_ee2ce2b58c4d` | call_site | `third_party/redis/src/networking.c:1764` | `freeClient(c);` |
| `ev_ee7349c101ca` | call_site | `third_party/redis/src/networking.c:1369` | `connGetLastError(conn), getClientPeerId(c), getClientSockname(c));` |
| `ev_ee78884d3606` | call_site | `third_party/redis/src/db.c:1725` | `decrRefCount(argv[0]);` |
| `ev_ee8a3f40f98f` | call_site | `third_party/redis/src/dict.c:718` | `h = dictHashKey(d, key);` |
| `ev_eedec229a457` | call_site | `third_party/redis/src/dict.c:236` | `signed char new_ht_size_exp = _dictNextExp(size);` |
| `ev_ef03be1d7981` | call_site | `third_party/redis/src/ae.c:146` | `zfree(eventLoop->fired);` |
| `ev_ef3be3e1f909` | call_site | `third_party/redis/src/networking.c:3608` | `addReplyBulkCString(c,"proto");` |
| `ev_ef403958ac7b` | call_site | `third_party/redis/src/networking.c:914` | `addReplyProto(c,num,len);` |
| `ev_ef7a6d54e2dc` | call_site | `third_party/redis/src/t_string.c:858` | `if (computelcs) result = sdsnewlen(SDS_NOINIT,idx);` |
| `ev_ef8da853b265` | call_site | `third_party/redis/src/networking.c:3321` | `if (lookupClientByID(redir) == NULL) {` |
| `ev_efa3e538394b` | call_site | `third_party/redis/src/db.c:57` | `counter = LFULogIncr(counter);` |
| `ev_efb7b06285b6` | call_site | `third_party/redis/src/networking.c:3541` | `addReplyError(c,"-NOPROTO unsupported protocol version");` |
| `ev_efddce6ba22b` | call_site | `third_party/redis/src/t_string.c:638` | `incrDecrCommand(c,1);` |
| `ev_efe33d73cab8` | call_site | `third_party/redis/src/db.c:1463` | `dictIterator *di = dictGetSafeIterator(db->blocking_keys);` |
| `ev_f02411c59f8a` | call_site | `third_party/redis/src/networking.c:3281` | `addReplyError(c,` |
| `ev_f06a823e959a` | call_site | `third_party/redis/src/db.c:335` | `if (dictFind(db->expires,key)) {` |
| `ev_f06e799aa5fd` | call_site | `third_party/redis/src/networking.c:3164` | `addReplyErrorFormat(c,"No such user '%s'",` |
| `ev_f0758a7140bd` | call_site | `third_party/redis/src/dict.c:933` | `dictInitIterator(iter, d);` |
| `ev_f07b6dc52759` | call_site | `third_party/redis/src/db.c:2180` | `return getKeysUsingLegacyRangeSpec(cmd,argv,argc,result);` |
| `ev_f0932c3a8ea2` | call_site | `third_party/redis/src/t_string.c:148` | `replaceClientCommandVector(c, argc, argv);` |
| `ev_f0d94b27f340` | call_site | `third_party/redis/src/networking.c:3308` | `zfree(prefix);` |
| `ev_f0e495bbc76d` | call_site | `third_party/redis/src/dict.c:762` | `assert(entryHasValue(de));` |
| `ev_f0ee9cd17273` | call_site | `third_party/redis/src/dict.c:757` | `assert(entryHasValue(de));` |
| `ev_f1158b4394a5` | call_site | `third_party/redis/src/networking.c:2954` | `if (*destvar) decrRefCount(*destvar);` |
| `ev_f11cd568e79b` | call_site | `third_party/redis/src/db.c:874` | `int len = ld2string(buf, sizeof(buf), *(double *)dictGetVal(de), LD_STR_AUTO);` |
| `ev_f12c706a0b65` | call_site | `third_party/redis/src/db.c:977` | `if (getLongFromObjectOrReply(c, c->argv[i+1], &count, NULL)` |
| `ev_f1383e6a114b` | call_site | `third_party/redis/src/networking.c:668` | `addReplyErrorFormatInternal(c, 0, fmt, ap);` |
| `ev_f14575344784` | call_site | `third_party/redis/src/networking.c:4503` | `updateClientMemUsageAndBucket(c);` |
| `ev_f184c9fd9e8d` | call_site | `third_party/redis/src/dict.c:814` | `assert(entryHasValue(de));` |
| `ev_f1885360788c` | call_site | `third_party/redis/src/networking.c:3444` | `addReply(c,shared.ok);` |
| `ev_f19ca50db9b4` | call_site | `third_party/redis/src/networking.c:133` | `c->buf = zmalloc_usable(PROTO_REPLY_CHUNK_BYTES, &c->buf_usable_size);` |
| `ev_f1d9675082aa` | call_site | `third_party/redis/src/t_string.c:411` | `if (removeExpire(c->db, c->argv[1])) {` |
| `ev_f1ffbc2f78c4` | call_site | `third_party/redis/src/networking.c:3241` | `struct client *target = lookupClientByID(id);` |
| `ev_f210ebf6511f` | call_site | `third_party/redis/src/db.c:1237` | `blockClientShutdown(c);` |
| `ev_f2175c13f861` | call_site | `third_party/redis/src/db.c:1339` | `if (expire != -1) setExpire(c,dst,c->argv[1],expire);` |
| `ev_f230ec6509ef` | call_site | `third_party/redis/src/networking.c:3921` | `freeClientAsync(c);` |
| `ev_f25465522c8d` | call_site | `third_party/redis/src/dict.c:1372` | `next = dictGetNext(de);` |
| `ev_f266d1185026` | call_site | `third_party/redis/src/networking.c:1054` | `addReplyProto(c,"\r\n",2);` |
| `ev_f2671b356293` | call_site | `third_party/redis/src/networking.c:2765` | `c->sockname = sdsnew(sockname);` |
| `ev_f2883cfe57c7` | call_site | `third_party/redis/src/networking.c:685` | `addReplyProto(c,"\r\n",2);` |
| `ev_f288b3c812ee` | call_site | `third_party/redis/src/db.c:799` | `if (allkeys \|\| stringmatchlen(pattern,plen,key,sdslen(key),0)) {` |
| `ev_f2ca5a22eab6` | call_site | `third_party/redis/src/networking.c:592` | `addReply(c, err);` |
| `ev_f2d41f84db61` | call_site | `third_party/redis/src/db.c:153` | `return lookupKey(db, key, flags);` |
| `ev_f2d55df48c3d` | call_site | `third_party/redis/src/db.c:1275` | `signalModifiedKey(c,c->db,c->argv[1]);` |
| `ev_f2dc3ebb341c` | call_site | `third_party/redis/src/db.c:205` | `if (server.cluster_enabled) slotToKeyAddEntry(de, db);` |
| `ev_f30a0647ce48` | call_site | `third_party/redis/src/networking.c:3482` | `addReplyBulkCString(c,"noloop");` |
| `ev_f30c0028595c` | call_site | `third_party/redis/src/networking.c:819` | `serverAssert(length >= 0);` |
| `ev_f319e51596ef` | call_site | `third_party/redis/src/dict.c:777` | `assert(entryHasValue(de));` |
| `ev_f328b21c374b` | call_site | `third_party/redis/src/networking.c:2431` | `resetClient(c);` |
| `ev_f32a933ab9aa` | call_site | `third_party/redis/src/networking.c:882` | `addReplyProto(c,dbuf,dlen+3);` |
| `ev_f3654d89f68a` | call_site | `third_party/redis/src/networking.c:4215` | `setIOPendingCount(id, 0);` |
| `ev_f3833e736e8b` | call_site | `third_party/redis/src/db.c:1260` | `incrRefCount(o);` |
| `ev_f389bdde9594` | call_site | `third_party/redis/src/db.c:261` | `signalDeletedKeyAsReady(db,key,old->type);` |
| `ev_f390d66f5aff` | call_site | `third_party/redis/src/t_string.c:642` | `incrDecrCommand(c,-1);` |
| `ev_f3ab53c61b35` | call_site | `third_party/redis/src/networking.c:1515` | `serverAssert(!(c->flags &(CLIENT_SLAVE\|CLIENT_MASTER)));` |
| `ev_f3c26c23d3f5` | call_site | `third_party/redis/src/db.c:1149` | `addReplyBulkLongLong(c,cursor);` |
| `ev_f454ac3ed8a9` | call_site | `third_party/redis/src/dict.c:1289` | `return dictScanDefrag(d, v, fn, NULL, privdata);` |
| `ev_f4550338ae89` | call_site | `third_party/redis/src/db.c:1526` | `touchAllWatchedKeysInDb(db2, db1);` |
| `ev_f45aeac81420` | call_site | `third_party/redis/src/networking.c:4207` | `writeToClient(c,0);` |
| `ev_f48ac663e6fc` | call_site | `third_party/redis/src/ae.c:496` | `aeProcessEvents(eventLoop, AE_ALL_EVENTS\|` |
| `ev_f48c8f6676d2` | call_site | `third_party/redis/src/networking.c:424` | `size_t reply_len = _addReplyToBuffer(c,s,len);` |
| `ev_f48cfb3ed094` | call_site | `third_party/redis/src/dict.c:926` | `assert(iter->fingerprint == dictFingerprint(iter->d));` |
| `ev_f4a4845544db` | call_site | `third_party/redis/src/networking.c:1075` | `addReplyNull(c);` |
| `ev_f4c87d382c19` | call_site | `third_party/redis/src/db.c:514` | `signalFlushedDb(dbnum, async);` |
| `ev_f4cc7b84052a` | call_site | `third_party/redis/src/db.c:871` | `val = dictGetVal(de);` |
| `ev_f4ee629653fb` | call_site | `third_party/redis/src/networking.c:4204` | `while((ln = listNext(&li))) {` |
| `ev_f52762d5db56` | call_site | `third_party/redis/src/db.c:1328` | `addReply(c,shared.czero);` |
| `ev_f531af8c54e1` | call_site | `third_party/redis/src/dict.c:938` | `dictIterator *i = dictGetIterator(d);` |
| `ev_f55056689f0a` | call_site | `third_party/redis/src/networking.c:2201` | `c->argv[c->argc] = createObject(OBJ_STRING,argv[j]);` |
| `ev_f5550e099496` | call_site | `third_party/redis/src/db.c:440` | `dbReplaceValue(db,key,o);` |
| `ev_f5800473a813` | call_site | `third_party/redis/src/networking.c:2617` | `client *c = connGetPrivateData(conn);` |
| `ev_f5865ae4b995` | call_site | `third_party/redis/src/networking.c:3784` | `size_t mem = getClientOutputBufferMemoryUsage(c);` |
| `ev_f5a749cfd2b0` | call_site | `third_party/redis/src/dict.c:426` | `dictEntry *entry = dictAddRaw(d,key,NULL);` |
| `ev_f5cf8639d68f` | call_site | `third_party/redis/src/t_string.c:555` | `addReplyBulk(c,o);` |
| `ev_f5d21bff123d` | call_site | `third_party/redis/src/networking.c:3340` | `zfree(prefix);` |
| `ev_f5ee10fee9a3` | call_site | `third_party/redis/src/networking.c:2750` | `genClientAddrString(c,peerid,sizeof(peerid),1);` |
| `ev_f604da42551c` | assignment | `third_party/redis/src/lazyfree.c:167` | `bioCreateLazyFreeJob(lazyfreeFreeObject,1,obj);` |
| `ev_f6254e6793c5` | call_site | `third_party/redis/src/networking.c:3611` | `addReplyBulkCString(c,"id");` |
| `ev_f63e973ee8dd` | call_site | `third_party/redis/src/dict.c:193` | `_dictInit(d,type);` |
| `ev_f68a82d929e7` | call_site | `third_party/redis/src/networking.c:3615` | `if (server.sentinel_mode) addReplyBulkCString(c,"sentinel");` |
| `ev_f6ab9b509b96` | call_site | `third_party/redis/src/networking.c:85` | `zfree(o);` |
| `ev_f6cc27a8d406` | call_site | `third_party/redis/src/bio.c:225` | `serverLog(LL_WARNING,` |
| `ev_f6d5a08b3f66` | call_site | `third_party/redis/src/db.c:759` | `if (getIntFromObjectOrReply(c, c->argv[1], &id, NULL) != C_OK)` |
| `ev_f6d827af31c5` | call_site | `third_party/redis/src/networking.c:689` | `addReplyStatusLength(c,status,strlen(status));` |
| `ev_f6def913d1a1` | call_site | `third_party/redis/src/dict.c:473` | `assert(bucket >= &d->ht_table[htidx][0] &&` |
| `ev_f6e28665f1a5` | call_site | `third_party/redis/src/networking.c:1370` | `freeClient(connGetPrivateData(conn));` |
| `ev_f6fddc16612d` | call_site | `third_party/redis/src/dict.c:798` | `if (entryIsKey(de)) return (void*)de;` |
| `ev_f731f76d9813` | call_site | `third_party/redis/src/db.c:659` | `server.dirty += emptyData(-1,flags,NULL);` |
| `ev_f747091a8672` | call_site | `third_party/redis/src/networking.c:1365` | `if (connAccept(conn, clientAcceptHandler) == C_ERR) {` |
| `ev_f76ce303278a` | call_site | `third_party/redis/src/networking.c:623` | `sdsfree(err);` |
| `ev_f79a1ccce0b0` | call_site | `third_party/redis/src/networking.c:2309` | `if (sdslen(c->querybuf)-c->qb_pos > PROTO_INLINE_MAX_SIZE) {` |
| `ev_f7a8d295eb92` | call_site | `third_party/redis/src/networking.c:1136` | `addReplyStatus(c,"    Print this help.");` |
| `ev_f7d6c005e603` | call_site | `third_party/redis/src/t_string.c:398` | `notifyKeyspaceEvent(NOTIFY_GENERIC, "del", c->argv[1], c->db->id);` |
| `ev_f830573ec491` | call_site | `third_party/redis/src/db.c:528` | `functionsLibCtxClearCurrent(async);` |
| `ev_f853bfe7e97b` | call_site | `third_party/redis/src/networking.c:3644` | `if (connAddrPeerName(c->conn, ip, sizeof(ip), &port) == -1) {` |
| `ev_f8922f5480d4` | call_site | `third_party/redis/src/networking.c:1552` | `freeClientAsync(c);` |
| `ev_f89ed78add92` | call_site | `third_party/redis/src/networking.c:2171` | `if (querylen == 0 && getClientType(c) == CLIENT_TYPE_SLAVE)` |
| `ev_f8cd572ebf5a` | call_site | `third_party/redis/src/db.c:604` | `touchWatchedKey(db,key);` |
| `ev_f8d133864392` | call_site | `third_party/redis/src/db.c:247` | `serverAssertWithInfo(NULL,key,de != NULL);` |
| `ev_f8ed9e850d30` | call_site | `third_party/redis/src/db.c:1880` | `serverAssert(spec->begin_search_type != KSPEC_BS_INVALID);` |
| `ev_f96ac5c2c6e7` | call_site | `third_party/redis/src/dict.c:200` | `_dictReset(d, 0);` |
| `ev_f96e61845c16` | call_site | `third_party/redis/src/networking.c:890` | `int digits = digits10(dlen);` |
| `ev_f978dac39cee` | call_site | `third_party/redis/src/db.c:227` | `initObjectLRUOrLFU(val);` |
| `ev_f9a53ae22b11` | call_site | `third_party/redis/src/adlist.c:67` | `zfree(current);` |
| `ev_f9b4efeff26f` | call_site | `third_party/redis/src/networking.c:3853` | `unsigned long used_mem = getClientOutputBufferMemoryUsage(c);` |
| `ev_f9c46f030b9f` | call_site | `third_party/redis/src/networking.c:2534` | `if (isInsideYieldingLongCommand() && c->flags & CLIENT_MASTER) break;` |
| `ev_f9e7cc2323b9` | call_site | `third_party/redis/src/db.c:1262` | `if (lookupKeyWrite(c->db,c->argv[2]) != NULL) {` |
| `ev_fa1dd15fed66` | call_site | `third_party/redis/src/networking.c:1517` | `if (c->flags & CLIENT_TRACKING) disableTracking(c);` |
| `ev_fa44f6950541` | call_site | `third_party/redis/src/t_string.c:687` | `addReplyBulk(c,new);` |
| `ev_fa64c51f1178` | call_site | `third_party/redis/src/networking.c:1053` | `addReplyProto(c,p,len);` |
| `ev_fa64eac03c7b` | call_site | `third_party/redis/src/ae.c:74` | `eventLoop->events = zmalloc(sizeof(aeFileEvent)*setsize);` |
| `ev_fa9104bdbc6e` | call_site | `third_party/redis/src/dict.c:847` | `if (entryIsNoValue(de)) {` |
| `ev_fabc2682bdcf` | call_site | `third_party/redis/src/networking.c:2886` | `int len = (name != NULL) ? sdslen(name->ptr) : 0;` |
| `ev_faee843fa79b` | call_site | `third_party/redis/src/networking.c:127` | `connEnableTcpNoDelay(conn);` |
| `ev_faf0c2e88cbb` | call_site | `third_party/redis/src/networking.c:2042` | `if (writeToClient(c,0) == C_ERR) continue;` |
| `ev_faf4ea597302` | call_site | `third_party/redis/src/t_string.c:447` | `if (getLongFromObjectOrReply(c,c->argv[2],&offset,NULL) != C_OK)` |
| `ev_fb15d4183443` | call_site | `third_party/redis/src/t_string.c:778` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_fb232f569563` | call_site | `third_party/redis/src/networking.c:460` | `sdsfree(s);` |
| `ev_fbdd33d6e652` | call_site | `third_party/redis/src/networking.c:3609` | `addReplyLongLong(c,c->resp);` |
| `ev_fc1737ab844f` | call_site | `third_party/redis/src/t_string.c:112` | `setKey(c,c->db,key,val,setkey_flags);` |
| `ev_fc2a5a9bd319` | call_site | `third_party/redis/src/networking.c:380` | `closeClientOnOutputBufferLimitReached(c, 1);` |
| `ev_fc4ed89698fa` | call_site | `third_party/redis/src/networking.c:1508` | `ln = listSearchKey(server.monitors,c);` |
| `ev_fc5e8aa16d52` | call_site | `third_party/redis/src/dict.c:477` | `assert(!metasize); /* Entry metadata + no value not supported. */` |
| `ev_fc606e7f0f76` | call_site | `third_party/redis/src/db.c:1106` | `if (use_pattern && !stringmatchlen(pat, sdslen(pat), (char *)str, len, 0)) {` |
| `ev_fc792bd8b3e9` | call_site | `third_party/redis/src/networking.c:2983` | `addReply(c,shared.ok);` |
| `ev_fc9aac1d6a13` | call_site | `third_party/redis/src/networking.c:3506` | `while(raxNext(&ri)) {` |
| `ev_fcd7fca590e7` | call_site | `third_party/redis/src/lazyfree.c:132` | `raxSeek(&ri,"^",NULL,0);` |
| `ev_fce61b5936ae` | call_site | `third_party/redis/src/networking.c:1333` | `if (connWrite(conn,err,strlen(err)) == -1) {` |
| `ev_fcf7e96515ca` | call_site | `third_party/redis/src/dict.c:744` | `if (!entryIsKey(he)) zfree(decodeMaskedPtr(he));` |
| `ev_fd1ca3c374c0` | call_site | `third_party/redis/src/networking.c:1307` | `connFormatAddr(conn, laddr, sizeof(addr), 0);` |
| `ev_fd332391bb01` | call_site | `third_party/redis/src/networking.c:4231` | `serverLog(LL_WARNING,"Fatal: too many I/O threads configured. "` |
| `ev_fd380facdc85` | call_site | `third_party/redis/src/dict.c:353` | `dictSetNext(de, d->ht_table[1][h]);` |
| `ev_fd44363c5cde` | call_site | `third_party/redis/src/dict.c:500` | `memset(dictEntryMetadata(entry), 0, metasize);` |
| `ev_fd83c1691922` | call_site | `third_party/redis/src/db.c:178` | `if (!o) addReplyOrErrorObject(c, reply);` |
| `ev_fd9783e9f089` | call_site | `third_party/redis/src/networking.c:3410` | `addReplyErrorObject(c,shared.syntaxerr);` |
| `ev_fdb5cd7fdf7a` | call_site | `third_party/redis/src/db.c:1326` | `o = lookupKeyWrite(c->db,c->argv[1]);` |
| `ev_fddecf2dc807` | call_site | `third_party/redis/src/dict.c:1136` | `void *newkey = defragkey ? defragkey(dictGetKey(de)) : NULL;` |
| `ev_fde58ae29457` | call_site | `third_party/redis/src/t_string.c:390` | `if (((flags & OBJ_PXAT) \|\| (flags & OBJ_EXAT)) && checkAlreadyExpired(milliseconds)) {` |
| `ev_fe1ad769ba6d` | call_site | `third_party/redis/src/t_string.c:594` | `msetGenericCommand(c,0);` |
| `ev_fe242f856fc9` | call_site | `third_party/redis/src/networking.c:2499` | `if (processCommandAndResetClient(c) == C_ERR) {` |
| `ev_fe632a4d48b5` | call_site | `third_party/redis/src/networking.c:4197` | `serverAssert(getIOPendingCount(id) != 0);` |
| `ev_fe78b73c2f55` | call_site | `third_party/redis/src/bio.c:187` | `bio_job *job = zmalloc(sizeof(*job));` |
| `ev_fe8c1bb9d0dc` | call_site | `third_party/redis/src/t_string.c:707` | `totlen = stringObjectLen(c->argv[2]);` |
| `ev_fe90d4bbac8a` | call_site | `third_party/redis/src/lazyfree.c:225` | `raxFree(index);` |
| `ev_fe90f6a98a5d` | call_site | `third_party/redis/src/db.c:229` | `if (server.cluster_enabled) slotToKeyAddEntry(de, db);` |
| `ev_fe9815373ee5` | call_site | `third_party/redis/src/networking.c:2945` | `addReplyErrorFormat(c,"Unrecognized option '%s'", attr);` |
| `ev_fed7ba36bcba` | call_site | `third_party/redis/src/lazyfree.c:53` | `size_t len = functionsLibCtxfunctionsLen(functions_lib_ctx);` |
| `ev_ff0b48350fae` | call_site | `third_party/redis/src/networking.c:259` | `listLinkNodeHead(server.clients_pending_write, &c->clients_pending_write_node);` |
| `ev_ff5c24e6c1db` | call_site | `third_party/redis/src/db.c:2260` | `return genericGetKeys(0, 1, 2, 1, argv, argc, result);` |
| `ev_ff75200ff0e2` | call_site | `third_party/redis/src/networking.c:2864` | `o = sdscatlen(o,"\n",1);` |
| `ev_ff9867e40ed4` | call_site | `third_party/redis/src/db.c:169` | `return lookupKey(db, key, flags \| LOOKUP_WRITE);` |
| `ev_ffa537625d02` | call_site | `third_party/redis/src/networking.c:1032` | `addReplyProto(c,"_\r\n",3);` |
| `ev_ffb1668209fd` | call_site | `third_party/redis/src/lazyfree.c:131` | `raxStart(&ri,s->cgroups);` |
| `ev_ffbaa2a0d24a` | call_site | `third_party/redis/src/networking.c:312` | `if (!clientHasPendingReplies(c) && io_threads_op == IO_THREADS_OP_IDLE)` |
| `ev_ffce7d358520` | call_site | `third_party/redis/src/db.c:2004` | `int has_varflags = (getAllKeySpecsFlags(cmd, 0) & CMD_KEY_VARIABLE_FLAGS);` |
