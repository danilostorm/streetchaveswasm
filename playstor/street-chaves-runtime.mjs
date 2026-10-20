/* Street Chaves: first-party local WASM title displayed inside PlayStor native G4.3 player.
 * A same-origin frame isolates Pygbag's global SDL bootstrap from PlayStor's
 * other emulators; no external site/player and no secondary domain.
 */
const ROOT='/pc-web/street-chaves/';
export async function createStreetChavesRuntime({game,stage}){
  if(game?.platform!=='windows'||game?.web_runtime!=='street-chaves-wasm'||!stage)throw Error('Street Chaves: integração inválida');
  const holder=document.createElement('div');
  holder.className='playstor-pc-web-host playstor-street-chaves-host';
  holder.style.cssText='position:absolute;inset:0;overflow:hidden;background:#02040a;display:flex;align-items:center;justify-content:center';
  const iframe=document.createElement('iframe');
  iframe.title='Street Chaves · PlayStor WebAssembly';
  iframe.className='playstor-street-chaves-frame';
  iframe.src=ROOT+'index.html?v=20261019-native1';
  iframe.referrerPolicy='same-origin';
  iframe.setAttribute('sandbox','allow-scripts allow-same-origin allow-pointer-lock');
  iframe.setAttribute('allow','gamepad; autoplay; fullscreen');
  iframe.setAttribute('allowfullscreen','');
  iframe.style.cssText='width:100%;height:100%;border:0;display:block;background:#02040a;';
  holder.append(iframe);stage.append(holder);
  let ended=false,status='loading';
  const loaded=new Promise((resolve,reject)=>{
    iframe.addEventListener('load',resolve,{once:true});
    iframe.addEventListener('error',()=>reject(Error('Falha ao carregar Street Chaves no PlayStor')),{once:true});
  });
  function send(action,extras={}){
    if(ended||!iframe.contentWindow)return;
    iframe.contentWindow.postMessage({channel:'playstor-street-chaves',action,...extras},location.origin);
  }
  return {
    isPCWeb:true,
    getStatus:()=>ended?'terminated':status,
    getFrame:()=>iframe,
    async start(){
      await Promise.race([loaded,new Promise((_,reject)=>setTimeout(()=>reject(Error('Street Chaves demorou para abrir')),20000))]);
      if(ended)return;
      status='running';
      iframe.focus({preventScroll:true});
    },
    // Keyboard and physical gamepads go directly to Pygame in its frame.
    // Virtual controller inputs from PlayStor are forwarded to the local game.
    pressDown({button}){send('input',{button,down:true})},
    pressUp({button}){send('input',{button,down:false})},
    async pause(){status='paused';send('input',{button:'l2',down:true});send('input',{button:'l2',down:false})},
    async resume(){status='running';send('input',{button:'l2',down:true});send('input',{button:'l2',down:false});iframe.focus({preventScroll:true})},
    async saveState(){return null},async saveSRAM(){return null},
    async loadState(){throw Error('Street Chaves não oferece save state.')},
    setPresentation(settings={}){iframe.style.filter='saturate('+Math.max(50,Math.min(150,Number(settings.saturation)||100))+'%)'},
    getVideoCanvas:()=>null,
    exit(){if(ended)return;ended=true;status='terminated';iframe.src='about:blank';holder.remove()},
  };
}
