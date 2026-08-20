const pptxgen = require('/Users/andye/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pptxgenjs');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Code Reverse Agent';
pptx.subject = '代码逆向 Agent 设计与 Demo';
pptx.title = '代码逆向 Agent';
pptx.company = 'OpenAI';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Aptos',
  lang: 'zh-CN'
};
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: '0B1020' },
  objects: [
    { rect: { x: 0, y: 7.18, w: 13.333, h: 0.32, fill: { color: '111A33' }, line: { color: '111A33' } } },
    { text: { text: 'Code Reverse Agent  |  libuv + Redis', options: { x: 0.45, y: 7.24, w: 5, h: 0.12, fontFace: 'Aptos', fontSize: 6.5, color: '8190B5', margin: 0 } } }
  ],
  slideNumber: { x: 12.55, y: 7.22, color: '8190B5', fontFace: 'Aptos', fontSize: 7 }
});

const C = { bg:'0B1020', panel:'131C35', panel2:'182544', text:'F5F7FF', muted:'AAB6D3', cyan:'45D6E8', green:'6CE5A0', amber:'FFC857', red:'FF6B7A', line:'344363' };
function title(slide, t, sub='') {
  slide.addText(t, { x:0.55, y:0.34, w:9.5, h:0.45, fontSize:24, bold:true, color:C.text, margin:0 });
  if (sub) slide.addText(sub, { x:0.58, y:0.86, w:11.6, h:0.28, fontSize:10.5, color:C.muted, margin:0 });
}
function box(slide, x,y,w,h, label, opts={}) {
  slide.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.06,fill:{color:opts.fill||C.panel},line:{color:opts.line||C.line,width:1}});
  slide.addText(label,{x:x+0.12,y:y+0.12,w:w-0.24,h:h-0.24,fontSize:opts.size||12,bold:!!opts.bold,color:opts.color||C.text,align:opts.align||'center',valign:'mid',margin:0.04,breakLine:false,fit:'shrink'});
}
function arrow(slide,x1,y1,x2,y2,color=C.cyan,dash='solid') {
  slide.addShape(pptx.ShapeType.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:1.6,beginArrowType:'none',endArrowType:'triangle',dashType:dash}});
}
function bullets(slide, items, x,y,w,h, size=15) {
  slide.addText(items.map(v=>({text:v,options:{bullet:{indent:14},breakLine:true}})),{x,y,w,h,fontSize:size,color:C.text,breakLine:false,margin:0.05,paraSpaceAfterPt:10,fit:'shrink'});
}

// 1
{
  const s=pptx.addSlide('MASTER');
  s.addText('代码逆向 Agent',{x:0.7,y:1.15,w:8.8,h:0.85,fontSize:38,bold:true,color:C.text,margin:0});
  s.addText('从源码到可审计的调用关系图',{x:0.75,y:2.1,w:8,h:0.45,fontSize:21,color:C.cyan,margin:0});
  s.addText('libuv / Redis 源码结构剖析 · Subagent 架构 · JSON 契约 · Demo 验证',{x:0.76,y:2.75,w:10.2,h:0.3,fontSize:12,color:C.muted,margin:0});
  box(s,0.75,4.25,3.45,1.0,'直接调用\ndirect_call',{fill:C.panel2,color:C.cyan,size:17,bold:true});
  box(s,4.95,4.25,3.45,1.0,'异步回调\ncallback_edge',{fill:C.panel2,color:C.green,size:17,bold:true});
  box(s,9.15,4.25,3.45,1.0,'宏 / 平台\nbuild profile',{fill:C.panel2,color:C.amber,size:17,bold:true});
  s.addText('目标：像专家一样阅读代码，同时保留每个结论的源码证据、配置条件和置信度。',{x:0.78,y:6.0,w:11.6,h:0.35,fontSize:14,color:C.text,margin:0});
}

// 2
{
  const s=pptx.addSlide('MASTER'); title(s,'为什么普通调用图不够','逆向分析的难点集中在“运行时关系”而非函数名列表');
  const rows=[['静态调用','A 调用 B','可由 AST / IR 直接确认'],['异步回调','注册点 → 事件 → callback','必须保留事件源、线程和队列'],['函数指针','类型 + 赋值流 + 注册 API','结果可能是候选集合'],['编译宏','Linux / macOS / Windows','同一逻辑有多套实现']];
  rows.forEach((r,i)=>{const y=1.45+i*1.15;box(s,0.7,y,2.15,0.72,r[0],{fill:C.panel2,color:i===1?C.green:i===2?C.amber:C.cyan,size:14,bold:true});box(s,3.15,y,3.3,0.72,r[1],{fill:C.panel,color:C.text,size:13});box(s,6.85,y,5.75,0.72,r[2],{fill:C.panel,color:C.muted,size:13,align:'left'});});
  s.addShape(pptx.ShapeType.line,{x:3.0,y:1.2,w:0,h:4.8,line:{color:C.line,width:1}});
  s.addShape(pptx.ShapeType.line,{x:6.7,y:1.2,w:0,h:4.8,line:{color:C.line,width:1}});
  s.addText('事实层：Evidence Graph',{x:0.75,y:6.25,w:3.1,h:0.3,fontSize:16,bold:true,color:C.cyan,margin:0});
  s.addText('报告、自然语言和图形都从事实层派生，不把模型猜测当作源码事实。',{x:3.15,y:6.25,w:8.9,h:0.3,fontSize:13,color:C.text,margin:0});
}

// 3
{
  const s=pptx.addSlide('MASTER'); title(s,'libuv：事件循环与生命周期','Unix / Windows 实现分层；loop、watcher、request 共同推进状态机');
  box(s,0.65,1.35,2.1,0.8,'uv_run',{fill:C.panel2,color:C.cyan,bold:true,size:18});
  box(s,3.25,1.35,2.3,0.8,'阶段调度\npending / prepare',{fill:C.panel,size:13});
  box(s,6.1,1.35,2.3,0.8,'uv__io_poll\nepoll / kqueue',{fill:C.panel,size:13});
  box(s,8.95,1.35,2.75,0.8,'watcher.callback',{fill:C.panel2,color:C.green,bold:true,size:15});
  arrow(s,2.75,1.75,3.2,1.75); arrow(s,5.6,1.75,6.05,1.75); arrow(s,8.45,1.75,8.9,1.75);
  box(s,1.05,3.35,2.8,0.82,'handle init / start',{fill:C.panel,size:14});
  box(s,5.25,3.35,2.8,0.82,'worker / async completion',{fill:C.panel,size:14});
  box(s,9.45,3.35,2.8,0.82,'uv_close + close_cb',{fill:C.panel,size:14});
  arrow(s,3.9,3.76,5.15,3.76,C.green,'dash'); arrow(s,8.1,3.76,9.35,3.76,C.green,'dash');
  s.addText('关键建模：注册点、触发点、回调点必须是三类独立证据；uv_close 是延迟关闭语义。',{x:0.9,y:5.45,w:11.6,h:0.45,fontSize:15,color:C.text,margin:0});
  s.addText('源码区域：include/uv.h · src/uv-common.c · src/unix/* · src/win/* · test/',{x:0.9,y:6.12,w:11.2,h:0.3,fontSize:11,color:C.muted,margin:0});
}

// 4
{
  const s=pptx.addSlide('MASTER'); title(s,'Redis：从 socket 事件到命令执行','事件抽象层保持稳定，平台 backend 和业务状态机分别建模');
  const chain=['aeMain','aeProcessEvents','aeApiPoll','readQueryFromClient','processInputBuffer','processCommand'];
  chain.forEach((v,i)=>{const x=0.6+i*2.1;box(s,x,1.55,1.75,0.88,v,{fill:i===3?C.panel2:C.panel,color:i===3?C.green:C.text,bold:i===0||i===5,size:i===3?12:11}); if(i<chain.length-1) arrow(s,x+1.78,1.99,x+2.02,1.99);});
  box(s,1.0,3.65,2.8,0.8,'epoll / kqueue / select',{fill:C.panel2,color:C.amber,size:14,bold:true});
  box(s,5.25,3.65,2.8,0.8,'RESP 解析 + client state',{fill:C.panel,size:14});
  box(s,9.5,3.65,2.8,0.8,'command table / module API',{fill:C.panel2,color:C.cyan,size:14});
  arrow(s,3.9,4.05,5.15,4.05,C.amber,'dash'); arrow(s,8.15,4.05,9.4,4.05,C.amber,'dash');
  s.addText('异步边：file event、time event、BIO 后台任务、Module 回调；fork / replication 需要跨进程状态标记。',{x:0.82,y:5.55,w:11.8,h:0.42,fontSize:14,color:C.text,margin:0});
  s.addText('源码区域：src/server.c · src/ae*.c · src/networking.c · src/commands/ · src/rdb.c · src/aof.c · src/module.c',{x:0.82,y:6.18,w:11.8,h:0.3,fontSize:10.5,color:C.muted,margin:0});
}

// 5
{
  const s=pptx.addSlide('MASTER'); title(s,'Subagent 组织：一个事实层，多个专项分析器','编排器管理依赖、缓存、超时和结果合并；Agent 之间只交换结构化 artifact');
  box(s,4.65,1.15,4.0,0.72,'Orchestrator',{fill:C.panel2,color:C.cyan,bold:true,size:18});
  const agents=[['Repository\nIndexer',0.55,2.55,C.text],['Build / Macro\nAnalyzer',2.95,2.55,C.amber],['Call Graph\nAnalyzer',5.35,2.55,C.cyan],['Function Pointer\nResolver',7.75,2.55,C.green],['Async Event\nTracer',10.15,2.55,C.green]];
  agents.forEach(([t,x,y,c])=>{box(s,x,y,1.95,0.9,t,{fill:C.panel,color:c,size:12,bold:true});arrow(s,6.65,1.88,x+0.98,2.48,c,'dash');});
  box(s,2.0,4.45,2.85,0.78,'Architecture\nSynthesizer',{fill:C.panel2,color:C.cyan,size:14,bold:true});
  box(s,5.25,4.45,2.85,0.78,'Natural Language\nAnalyst',{fill:C.panel2,color:C.text,size:14,bold:true});
  box(s,8.5,4.45,2.85,0.78,'Verification\nAgent',{fill:C.panel2,color:C.green,size:14,bold:true});
  arrow(s,3.1,3.5,3.35,4.38);arrow(s,6.3,3.5,6.65,4.38);arrow(s,9.0,3.5,9.85,4.38);arrow(s,4.9,4.84,5.15,4.84);arrow(s,8.15,4.84,8.4,4.84);
  s.addText('规则：Agent 不覆盖他人结果；冲突保留双方证据并降低置信度。artifact 用内容哈希寻址，可增量复用。',{x:0.85,y:6.13,w:11.9,h:0.3,fontSize:13,color:C.text,margin:0});
}

// 6
{
  const s=pptx.addSlide('MASTER'); title(s,'JSON 契约：让结果可组合、可复核','请求锁定仓库、commit、编译配置和查询范围；结果必须带 evidence');
  box(s,0.65,1.35,5.75,4.55,'AnalysisRequest\n\nrepository.url\nrepository.commit\nbuild_profiles[]\nquery.entry_symbols\nquery.include_async\nquery.include_function_pointers',{fill:C.panel2,color:C.text,size:15,align:'left'});
  box(s,6.95,1.35,5.75,4.55,'AgentResult\n\nstatus: success | partial | failed\nfindings[].kind\nfindings[].confidence\nfindings[].condition\nfindings[].execution_context\nevidence[].file + line',{fill:C.panel2,color:C.text,size:15,align:'left'});
  arrow(s,6.55,3.6,6.85,3.6,C.cyan);
  s.addText('契约原则：不确定性显式化，配置条件附着在边上，缺失信息进入 warnings。',{x:0.9,y:6.25,w:11.5,h:0.3,fontSize:14,color:C.cyan,margin:0});
}

// 7
{
  const s=pptx.addSlide('MASTER'); title(s,'Demo 验证：两条关键链路','先用人工复核 fixture 固定输出形态，再接 AST / IR / compile database 适配器');
  box(s,0.7,1.35,5.75,0.75,'libuv / uv_run',{fill:C.panel2,color:C.cyan,bold:true,size:17});
  const l1=['uv_run','uv__io_poll','watcher.callback','uv__run_closing_handles'];
  l1.forEach((v,i)=>{const x=0.95+i*1.45;box(s,x,2.55,1.25,0.72,v,{fill:i===2?C.panel2:C.panel,color:i===2?C.green:C.text,size:10,bold:i===0});if(i<l1.length-1)arrow(s,x+1.27,2.91,x+1.42,2.91,i===1?C.green:C.cyan,'solid');});
  box(s,6.9,1.35,5.75,0.75,'Redis / client command',{fill:C.panel2,color:C.cyan,bold:true,size:17});
  const l2=['aeMain','aeApiPoll','readQueryFromClient','processCommand'];
  l2.forEach((v,i)=>{const x=7.15+i*1.4;box(s,x,2.55,1.2,0.72,v,{fill:i===2?C.panel2:C.panel,color:i===2?C.green:C.text,size:9.5,bold:i===0});if(i<l2.length-1)arrow(s,x+1.22,2.91,x+1.37,2.91,i===1?C.green:C.cyan,'solid');});
  box(s,1.2,4.45,3.1,0.72,'每条边：kind + evidence',{fill:C.panel,size:14});
  box(s,5.1,4.45,3.1,0.72,'回调边：event + thread',{fill:C.panel,size:14});
  box(s,9.0,4.45,3.1,0.72,'宏差异：profile 条件',{fill:C.panel,size:14});
  s.addText('Demo 输出：JSON 结果 + Mermaid 图 + 自然语言结论。fixture 行号为占位，真实适配器必须替换成精确源码位置。',{x:0.9,y:6.12,w:11.7,h:0.3,fontSize:13,color:C.muted,margin:0});
}

// 8
{
  const s=pptx.addSlide('MASTER'); title(s,'验收指标与下一步','把“看起来合理”升级为可重复、可审计、可回归');
  const metrics=[['关键入口链覆盖率','≥ 90%',C.cyan],['回调映射准确率','≥ 85%',C.green],['函数指针召回率','≥ 80%',C.amber],['报告证据覆盖率','100%',C.cyan],['同 commit 结果稳定','100%',C.green]];
  metrics.forEach((m,i)=>{const y=1.25+i*0.85;box(s,0.8,y,4.0,0.55,m[0],{fill:C.panel,size:13,align:'left'});box(s,5.0,y,1.55,0.55,m[1],{fill:C.panel2,color:m[2],bold:true,size:16});});
  box(s,7.45,1.25,4.9,3.8,'实施路线\n\n1  固定 libuv / Redis commit\n2  接入 AST / IR 与编译数据库\n3  构建 Evidence Graph\n4  增加回调、函数指针、宏分析\n5  接入 NL 问答与图形导出\n6  GitHub Actions 回归验证',{fill:C.panel2,color:C.text,size:15,align:'left'});
  s.addText('交付物：GitHub Demo · JSON Schema · 示例报告 · 调用关系图 · PPT · 演示脚本',{x:0.85,y:6.25,w:11.8,h:0.3,fontSize:15,color:C.cyan,margin:0});
}

pptx.writeFile({ fileName: '/Users/andye/Documents/ChatGPT/8.18huawei/Code-Reverse-Agent-汇报.pptx' });
