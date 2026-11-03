// Trusted mouse and keyboard input through the DevTools protocol (pointer capture and double click behave as with a real mouse).
// Run: node tests/real_input.js ../lectures/lecture-1/presentation.html
const {spawn}=require('child_process'),fs=require('fs'),os=require('os'),path=require('path');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const dir=fs.mkdtempSync(path.join(process.env.TMPDIR||os.tmpdir(),'ri'));
const ch=spawn(CHROME,['--headless=new','--disable-gpu','--no-sandbox','--remote-debugging-port=0',`--user-data-dir=${dir}`,'--window-size=1280,764','about:blank'],{stdio:['ignore','ignore','pipe']});
const done=(c)=>{try{ch.kill();}catch(e){}setTimeout(()=>{try{fs.rmSync(dir,{recursive:true,force:true});}catch(e){}process.exit(c);},800);};
let buf='';ch.stderr.on('data',async d=>{buf+=d;const m=/ws:\/\/[^\s]+/.exec(buf);if(!m||run.started)return;run.started=1;run(m[0]).catch(e=>{console.log('ERR',e);done(1);});});
async function run(bws){
 const list=await (await fetch(bws.replace('ws://','http://').replace(/\/devtools.*/,'/json/list'))).json();
 const ws=new WebSocket(list.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
 let id=0;const pend={};ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pend[m.id]){pend[m.id](m);delete pend[m.id];}};
 const cmd=(method,params={})=>new Promise(r=>{const i=++id;pend[i]=r;ws.send(JSON.stringify({id:i,method,params}));});
 const ev=async x=>(await cmd('Runtime.evaluate',{expression:x,returnByValue:true,awaitPromise:true})).result.result.value;
 await cmd('Page.enable');await cmd('Page.navigate',{url:'file://'+path.resolve(process.argv[2])});await new Promise(r=>setTimeout(r,2500));
 await ev(`document.head.insertAdjacentHTML('beforeend','<style>*{transition:none!important;animation:none!important}</style>');window.__deck.go('q-fv');1`);
 const at=async(s,a)=>ev(`(()=>{const r=document.querySelector('#${s} td[data-a="${a}"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`);
 const mouse=async(type,[x,y],clickCount=1)=>cmd('Input.dispatchMouseEvent',{type,x,y,button:'left',buttons:type==='mouseReleased'?0:1,clickCount});
 const click=async(p,n=1)=>{for(let k=1;k<=n;k++){await mouse('mousePressed',p,k);await mouse('mouseReleased',p,k);}};
 const key=async(k,code,text)=>{await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:k,code:code||k,windowsVirtualKeyCode:{Enter:13,F2:113,Escape:27,ArrowRight:39,ArrowLeft:37}[k]||0,text});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:k,code:code||k});};
 const type=async t=>{for(const c of t)await cmd('Input.insertText',{text:c});};
 const R={};
 // a student fills the FV template of question 1: the data by typing and Enter, the formula by clicking the cells
 // the template labels appear click by click first (six build steps)
 for(let k=0;k<6;k++)await ev(`window.__deck.next();1`);
 await click(await at('q-fv','C2'));for(const v of ['5%','3','0','50000']){await type(v);await key('Enter');}
 await type('=FV(');await click(await at('q-fv','C2'));await type(',');await click(await at('q-fv','C3'));await type(',');await click(await at('q-fv','C4'));await type(',');await click(await at('q-fv','C5'));await type(')');
 R.typed=await ev(`document.querySelector('#q-fv .xl-in')&&document.querySelector('#q-fv .xl-in').value`);await key('Enter');
 await click(await ev(`(()=>{const r=document.querySelector('#q-fv [data-x="check"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`));
 R.fv=await ev(`document.querySelector('#q-fv .xl-fb').textContent`);R.fvok=await ev(`!!document.querySelector('#q-fv .xl-ok')`);
 // a wrong formula: the arguments swapped, and the specific message
 await click(await at('q-fv','C6'));await type('=FV(C2,C3,C5,C4)');await key('Enter');
 await click(await ev(`(()=>{const r=document.querySelector('#q-fv [data-x="check"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`));
 R.trap=await ev(`document.querySelector('#q-fv .xl-fb').textContent`);
 // question 1 year by year: type B5 and C5, then drag the fill handle over B5:C5 down to row 7
 await ev(`window.__deck.go('q-1');1`);for(let k=0;k<3;k++)await ev(`window.__deck.next();1`);
 await click(await at('q-1','B1'));await type('5%');await key('Enter');
 for(const [a,v] of [['A4','0'],['A5','1'],['A6','2'],['A7','3'],['C4','50000']]){await click(await at('q-1',a));await type(v);await key('Enter');}
 await click(await at('q-1','B5'));await type('=C4*$B$1');await key('Enter');await click(await at('q-1','C5'));await type('=C4+B5');await key('Enter');
 const b5=await at('q-1','B5'),c5=await at('q-1','C5');await mouse('mousePressed',b5);await cmd('Input.dispatchMouseEvent',{type:'mouseMoved',x:c5[0],y:c5[1],button:'left',buttons:1});await mouse('mouseReleased',c5);
 const fh=await ev(`(()=>{const r=document.querySelector('#q-1 .xl-fh').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`),c7=await at('q-1','C7');
 R.name=await ev(`document.querySelector('#q-1 .xl-name').textContent`);R.dbg=await ev(`(()=>{const h=document.querySelector('#q-1 .xl-fh'),t=h.closest('td'),r=h.getBoundingClientRect(),q=t.getBoundingClientRect(),w=h.closest('.xl-wrap').getBoundingClientRect();return {h:[r.left,r.top,r.width,r.height],td:[t.dataset.a,q.left,q.top,q.width,q.height],wrap:[w.left,w.top,w.right,w.bottom],cs:getComputedStyle(h).display+' '+getComputedStyle(t).position,atTd:(e=>e&&e.tagName+'.'+e.className+'.'+(e.dataset&&e.dataset.a))(document.elementFromPoint(q.left+q.width/2,q.top+q.height/2)),atH:(e=>e&&e.tagName+'.'+e.className)(document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)),pe:getComputedStyle(t).pointerEvents+' '+getComputedStyle(h).pointerEvents};})()`);R.fh=fh;R.c7=c7;R.under=await ev('(()=>{const e=document.elementFromPoint('+fh[0]+','+fh[1]+');return e&&(e.tagName+"."+e.className);})()');
 await mouse('mousePressed',fh);for(let k=1;k<=6;k++)await cmd('Input.dispatchMouseEvent',{type:'mouseMoved',x:fh[0],y:fh[1]+(c7[1]-fh[1])*k/6,button:'left',buttons:1});await mouse('mouseReleased',[fh[0],c7[1]]);
 R.fill=await ev(`[document.querySelector('#q-1 .sheet').__api.raw('B7'),document.querySelector('#q-1 .sheet').__api.raw('C7')]`);
 await click(await ev(`(()=>{const r=document.querySelector('#q-1 [data-x="check"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`));
 R.q1=await ev(`document.querySelector('#q-1 .xl-fb').textContent`);R.q1ok=await ev(`!!document.querySelector('#q-1 .xl-ok')`);
 R.err=await ev(`document.documentElement.getAttribute('data-err')`);
 console.log(JSON.stringify(R,null,1));
 const pass=R.typed==='=FV(C2,C3,C4,C5)'&&R.fvok&&/הסדר של הארגומנטים/.test(R.trap)&&R.fill[0]==='=C6*$B$1'&&R.fill[1]==='=C6+B7'&&R.q1ok;
 console.log(pass?'REAL INPUT: PASS':'REAL INPUT: FAIL');done(pass?0:1);}
setTimeout(()=>{console.log('timeout');done(1);},120000);
