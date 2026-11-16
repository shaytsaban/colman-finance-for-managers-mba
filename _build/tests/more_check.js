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
 R.more=await ev(`(()=>{const out=[];const st=document.getElementById('stage').getBoundingClientRect(),k=st.width/1280;document.querySelectorAll('details.more').forEach(d=>{const sl=d.closest('.slide');window.__deck.go(sl.id);window.__deck.setAll(sl,true);d.open=true;const r=d.querySelector('.mb').getBoundingClientRect();const l=(r.left-st.left)/k,rt=(r.right-st.left)/k,t=(r.top-st.top)/k,bt=(r.bottom-st.top)/k;const ok=l>=8&&rt<=1272&&t>=4&&bt<=712;out.push((ok?'ok ':'OUT ')+sl.id+' '+d.querySelector('summary').textContent.slice(0,22)+' ['+[l,t,rt,bt].map(Math.round).join(',')+']');d.open=false;});return out;})()`);
 console.log(R.more.join('\n'));const bad=R.more.filter(x=>x.startsWith('OUT')).length;console.log(bad?'MORE: FAIL '+bad:'MORE: PASS '+R.more.length);done(bad?1:0);}
setTimeout(()=>done(1),60000);
