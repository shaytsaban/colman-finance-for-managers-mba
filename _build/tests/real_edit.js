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

 const SID=process.argv[3]||'q-4';
 await ev(`document.head.insertAdjacentHTML('beforeend','<style>*{transition:none!important;animation:none!important}</style>');window.__deck.go('${SID}');1`);
 const at=async(s,a)=>ev(`(()=>{const r=document.querySelector('#${s} td[data-a="${a}"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`);
 const mouse=async(type,[x,y],clickCount=1)=>cmd('Input.dispatchMouseEvent',{type,x,y,button:'left',buttons:type==='mouseReleased'?0:1,clickCount});
 const click=async(p,n=1)=>{for(let k=1;k<=n;k++){await mouse('mousePressed',p,k);await mouse('mouseReleased',p,k);}};
 const VK={Enter:13,F2:113,Escape:27,ArrowRight:39,ArrowLeft:37,Home:36,End:35,Backspace:8,Delete:46,c:67,v:86,z:90};
 const key=async(k,mods=0)=>{await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:k,code:k.length===1?'Key'+k.toUpperCase():k,windowsVirtualKeyCode:VK[k]||0,nativeVirtualKeyCode:VK[k]||0,modifiers:mods});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:k,code:k.length===1?'Key'+k.toUpperCase():k,windowsVirtualKeyCode:VK[k]||0,modifiers:mods});};
 const type=async t=>{for(const c of t)await cmd('Input.insertText',{text:c});};
 const raw=a=>ev(`document.querySelector('#${SID} .sheet').__api.raw('${a}')`);
 const inp=()=>ev(`(()=>{const i=document.querySelector('#${SID} .xl-in');return i?{v:i.value,s:i.selectionStart,act:document.activeElement===i}:null;})()`);
 const R={};
 await click(await at(SID,'C2'));for(const v of ['0.25%','=4*12','-1000','0']){await type(v);await key('Enter');}
 await type('=FV(C2,C3,C4,C5)');await key('Enter');
 // 1. a real double click opens the cell for editing, with its formula
 await click(await at(SID,'C6'),2);await new Promise(r=>setTimeout(r,150));R.dbl=await inp();
 // 2. typing inside a formula: End, three arrows to the left, then a character; the text must stay in order
 await key('End');for(let k=0;k<3;k++)await key('ArrowLeft');await type('9');R.mid=await inp();await key('Backspace');R.back=await inp();
 // a click inside the text places the caret there; typing goes to that place
 const box=await ev(`(()=>{const r=document.querySelector('#${SID} .xl-in').getBoundingClientRect();return [r.left,r.top,r.width,r.height];})()`);
 await click([box[0]+box[2]/2,box[1]+box[3]/2]);R.clickIn=await inp();await type('7');R.afterClick=await inp();await key('Escape');R.kept=await raw('C6');
 // 3. copy a block of four cells and paste it one column to the left
 const c2=await at(SID,'C2'),c5=await at(SID,'C5');await mouse('mousePressed',c2);await cmd('Input.dispatchMouseEvent',{type:'mouseMoved',x:c5[0],y:c5[1],button:'left',buttons:1});await mouse('mouseReleased',c5);
 R.sel=await ev(`document.querySelector('#${SID} .xl-name').textContent`);
 await key('c',4);await click(await at(SID,'D2'));await key('v',4);
 R.paste=[await raw('D2'),await raw('D3'),await raw('D4'),await raw('D5')];
 await key('z',4);R.undo=[await raw('D2'),await raw('D3'),await raw('D4'),await raw('D5')];
 // the formula bar shows a formula without letters left to right (=4*12, never 12*4=)
 await click(await at(SID,'C3'));R.bar=await ev(`(()=>{const b=document.querySelector('#${SID} .xl-bar');return b.value+' '+getComputedStyle(b).direction;})()`);
 R.err=await ev(`document.documentElement.getAttribute('data-err')`);

 console.log(JSON.stringify(R,null,1));
 const pass=R.dbl&&R.dbl.v==='=FV(C2,C3,C4,C5)'&&R.dbl.act&&R.mid.v==='=FV(C2,C3,C4,9C5)'&&R.back.v==='=FV(C2,C3,C4,C5)'&&R.afterClick&&R.afterClick.v.length===17&&R.kept==='=FV(C2,C3,C4,C5)'&&R.paste.join('|')==='0.25%|=4*12|-1000|0'&&R.undo.every(x=>x==null||x==='')&&R.bar==='=4*12 ltr';
 console.log(pass?'REAL EDIT: PASS':'REAL EDIT: FAIL');done(pass?0:1);}
setTimeout(()=>{console.log('timeout');done(1);},120000);
