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
 await click(await at(SID,'C2'));for(const v of ['1%','=5*12','-1000','0']){await type(v);await key('Enter');}
 const keyRaw=async(k,code,vk,mods)=>{await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:k,code,windowsVirtualKeyCode:vk,nativeVirtualKeyCode:vk,modifiers:mods});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:k,code,windowsVirtualKeyCode:vk,modifiers:mods});};
 const drag=async(a,b)=>{const p=await at(SID,a),q=await at(SID,b);await mouse('mousePressed',p);await cmd('Input.dispatchMouseEvent',{type:'mouseMoved',x:q[0],y:q[1],button:'left',buttons:1});await mouse('mouseReleased',q);};
 for(const [tag,ck,vk,mod] of [['latinCtrl','c','v',2],['latinCmd','c','v',4],['hebrewCtrl','ב','ה',2],['hebrewCmd','ב','ה',4]]){
  await drag('C2','C5');await keyRaw(ck,'KeyC',67,mod);await click(await at(SID,'D2'));await keyRaw(vk,'KeyV',86,mod);
  R[tag]=[await raw('D2'),await raw('D3'),await raw('D4'),await raw('D5')].join('|');
  await drag('D2','D5');await key('Delete');}
 // paste, then the formula in both columns, and the sheet's own check
 await drag('C2','C5');await keyRaw('c','KeyC',67,2);await click(await at(SID,'D2'));await keyRaw('v','KeyV',86,2);
 await click(await at(SID,'D5'));await type('-30000');await key('Enter');
 await click(await at(SID,'C6'));await type('=FV(C2,C3,C4,C5)');await key('Enter');await click(await at(SID,'C6'));await keyRaw('c','KeyC',67,2);await click(await at(SID,'D6'));await keyRaw('v','KeyV',86,2);
 R.d6=await raw('D6');
 await click(await ev(`(()=>{const r=document.querySelector('#${SID} [data-x="check"]').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];})()`));
 R.ok=await ev(`!!document.querySelector('#${SID} .xl-ok')`);R.fb=await ev(`document.querySelector('#${SID} .xl-fb').textContent.slice(0,120)`);
 console.log(JSON.stringify(R,null,1));
 const want='1%|=5*12|-1000|0';const pass=['latinCtrl','latinCmd','hebrewCtrl','hebrewCmd'].every(k=>R[k]===want)&&R.d6==='=FV(D2,D3,D4,D5)'&&R.ok;
 console.log(pass?'REAL PASTE: PASS':'REAL PASTE: FAIL');done(pass?0:1);}
setTimeout(()=>{console.log('timeout');done(1);},120000);
