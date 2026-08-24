const pptxgen = require('/Users/andye/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Code Reverse Agent';
pptx.lang = 'zh-CN';
pptx.title = '逆向分析入门：为什么调用链很难';
pptx.theme = { headFontFace: 'STHeiti', bodyFontFace: 'STHeiti', lang: 'zh-CN' };
const C = { bg:'F7FAFC', ink:'102A43', muted:'52606D', teal:'0B7285', green:'1F7A5C', amber:'B7791F', line:'CBD5E1', panel:'FFFFFF', soft:'E6FFFA', paleAmber:'FFF4D6' };
function base(){const s=pptx.addSlide();s.background={color:C.bg};s.addShape(pptx.ShapeType.line,{x:0.45,y:7.12,w:12.4,h:0,line:{color:C.line,width:1}});s.addText('逆向分析入门',{x:0.5,y:7.2,w:2,h:0.14,fontSize:7,color:C.muted,margin:0});return s;}
function title(s,t,sub=''){s.addText(t,{x:0.62,y:0.38,w:11.7,h:0.42,fontSize:25,bold:true,color:C.ink,margin:0});if(sub)s.addText(sub,{x:0.65,y:0.91,w:11.6,h:0.28,fontSize:11,color:C.muted,margin:0});}
function box(s,x,y,w,h,txt,o={}){s.addShape(pptx.ShapeType.roundRect,{x,y,w,h,rectRadius:0.04,fill:{color:o.fill||C.panel},line:{color:o.line||C.line,width:1}});s.addText(txt,{x:x+0.12,y:y+0.1,w:w-0.24,h:h-0.2,fontSize:o.size||14,bold:!!o.bold,color:o.color||C.ink,align:o.align||'center',valign:'mid',margin:0.02,fit:'shrink'});}
function arrow(s,x1,y1,x2,y2,color=C.teal,dash='solid'){s.addShape(pptx.ShapeType.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:1.5,endArrowType:'triangle',dashType:dash}});}
function bullets(s,arr,x,y,w,h,size=17){s.addText(arr.map(v=>({text:v,options:{bullet:{indent:14},breakLine:true}})),{x,y,w,h,fontSize:size,color:C.ink,breakLine:false,margin:0.05,paraSpaceAfterPt:12,fit:'shrink'});}

// 1. 总览
{const s=base();s.addText('为什么调用链很难？',{x:0.75,y:1.08,w:8,h:0.7,fontSize:38,bold:true,color:C.ink,margin:0});s.addText('从模块架构分层看函数调用、异步回调链和复杂宏',{x:0.8,y:2.0,w:10.8,h:0.42,fontSize:20,color:C.teal,margin:0});s.addText('面向初学者：先分清三种“箭头”，再看如何逆向还原真实执行路径。',{x:0.82,y:2.72,w:10.8,h:0.3,fontSize:13,color:C.muted,margin:0});box(s,0.82,4.15,3.45,1.0,'普通函数调用\n现在进入，等返回',{fill:C.soft,color:C.teal,bold:true,size:17});box(s,4.95,4.15,3.45,1.0,'异步回调链\n现在登记，未来触发',{fill:'EAF7EE',color:C.green,bold:true,size:17});box(s,9.08,4.15,3.45,1.0,'复杂宏定义\n编译前改写代码',{fill:C.paleAmber,color:C.amber,bold:true,size:17});s.addText('逆向分析要回答：箭头为什么存在？何时成立？证据在哪里？',{x:0.85,y:6.02,w:11.5,h:0.34,fontSize:15,bold:true,color:C.teal,margin:0});}

// 2. 三类难点
{const s=base();title(s,'三类关系，三种分析难点','不能只把所有关系都画成 A -> B');const rows=[['普通调用','main -> add','直接可见，但函数指针会隐藏终点。',C.soft,C.teal],['异步回调','注册 -> 事件 -> callback','中间隔着时间、线程、队列，当前栈看不到未来。','EAF7EE',C.green],['复杂宏','源码 -> 预处理后代码','不同平台和宏开关可能生成不同调用图。',C.paleAmber,C.amber]];rows.forEach((r,i)=>{const y=1.45+i*1.3;box(s,0.75,y,2.25,0.82,r[0],{fill:r[3],color:r[4],bold:true,size:16});box(s,3.35,y,3.05,0.82,r[1],{fill:C.panel,bold:true,size:14});box(s,6.85,y,5.65,0.82,r[2],{fill:C.panel,color:C.muted,size:13,align:'left'});});s.addText('所以调用图至少要区分：direct_call、callback_edge、implementation_of。',{x:0.85,y:5.75,w:11.5,h:0.38,fontSize:16,bold:true,color:C.ink,margin:0});s.addText('初学者记忆：直接调用看“现在”，回调看“未来”，宏看“编译后”。',{x:0.85,y:6.25,w:11.5,h:0.3,fontSize:14,color:C.teal,margin:0});}

// 3. 模块分层与调用链
{const s=base();title(s,'模块分层：源码目录不等于运行时路径','回调和平台实现会把原本分开的层重新连接起来');const arr=[['网络层','注册 read callback'],['事件层','等待 socket 就绪'],['处理层','解析请求 / 执行命令'],['输出层','发送响应 / 关闭']];arr.forEach((v,i)=>{const x=0.62+i*3.18;box(s,x,1.45,2.65,0.95,v[0]+'\n'+v[1],{fill:i===1?'EAF7EE':C.panel,color:i===1?C.green:C.ink,bold:true,size:14});if(i<3)arrow(s,x+2.72,1.92,x+3.08,1.92,i===1?C.green:C.teal,i===1?'dash':'solid');});s.addText('简化调用链',{x:0.8,y:2.85,w:2,h:0.25,fontSize:13,bold:true,color:C.muted,margin:0});box(s,0.85,3.3,2.0,0.7,'aeMain / uv_run',{fill:C.soft,color:C.teal,bold:true,size:14});box(s,3.35,3.3,2.0,0.7,'aeApiPoll / io_poll',{fill:C.panel,size:13});box(s,5.85,3.3,2.0,0.7,'回调 callback',{fill:'EAF7EE',color:C.green,bold:true,size:14});box(s,8.35,3.3,2.0,0.7,'parser / command',{fill:C.panel,size:13});box(s,10.85,3.3,1.7,0.7,'reply',{fill:C.panel,size:14});arrow(s,2.92,3.65,3.28,3.65);arrow(s,5.42,3.65,5.78,3.65,C.green,'dash');arrow(s,7.92,3.65,8.28,3.65);arrow(s,10.42,3.65,10.78,3.65);bullets(s,['回调：不是当前函数直接调用，而是事件发生后再回到上层。','宏 / 平台：epoll、kqueue、select 可能是同一抽象的不同实现。','函数指针：终点可能在结构体字段或外部模块里。'],0.95,4.7,11.2,1.55,16);}

// 4. 分析方法
{const s=base();title(s,'初学者的四步分析法','先把问题变小，再让每条结论可复核');const steps=[['1','选一个入口','uv_run、aeMain 或网络 API'],['2','追三件事','谁注册？谁触发？谁执行？'],['3','固定配置','commit、平台、编译宏、生成步骤'],['4','保留证据','文件、行号、边类型、置信度']];steps.forEach((v,i)=>{const y=1.35+i*0.98;box(s,0.95,y,0.62,0.58,v[0],{fill:C.teal,color:'FFFFFF',bold:true,size:18});box(s,1.85,y,2.15,0.58,v[1],{fill:C.panel,bold:true,size:14,align:'left'});box(s,4.3,y,7.65,0.58,v[2],{fill:C.panel,color:C.muted,size:14,align:'left'});});box(s,1.55,5.55,10.2,0.88,'不能唯一确定时：输出候选集合和置信度，不要把猜测写成事实。',{fill:C.soft,color:C.teal,bold:true,size:18});s.addText('一句话总结：函数调用看栈，异步回调看事件，复杂宏看预处理结果。',{x:1.0,y:6.65,w:11.3,h:0.3,fontSize:15,color:C.ink,align:'center',margin:0});}

pptx.writeFile({fileName:'/Users/andye/Documents/ChatGPT/8.18huawei/Code-Reverse-Agent-汇报.pptx'});
