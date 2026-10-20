const {chromium}=require('/app/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1200,height:850}});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:3086/pc-web/street-chaves/CREDITS.txt',{waitUntil:'domcontentloaded',timeout:22000});
 await page.setContent('<html><body style="margin:0;background:#080a14"><main id="stage" style="position:relative;width:1080px;height:740px;"></main></body></html>');
 const info=await page.evaluate(async()=>{
  const {createStreetChavesRuntime}=await import('/stormgames/street-chaves-runtime.mjs');
  window.streetChavesNative=await createStreetChavesRuntime({game:{id:680,title:'Street Chaves Remaster',platform:'windows',web_runtime:'street-chaves-wasm'},stage:document.getElementById('stage')});
  await window.streetChavesNative.start();
  return {status:window.streetChavesNative.getStatus(),iframeSrc:window.streetChavesNative.getFrame().getAttribute('src')};
 });
 console.log('LIVE_NATIVE',JSON.stringify(info));
 const frame=page.frameLocator('.playstor-street-chaves-frame');
 await frame.locator('#playstor-launch-hint').click({timeout:30000});
 await page.waitForTimeout(18000);
 const status=await frame.locator('#canvas').evaluate(c=>({width:c.width,height:c.height,visible:getComputedStyle(c).display,screenTitle:document.title,hiddenDebug:getComputedStyle(document.querySelector('#pyconsole')).display}));
 console.log('LIVE_WASM',JSON.stringify(status));
 await page.screenshot({path:'/out/screenshot-live-playstor.png'});
 await page.evaluate(()=>window.streetChavesNative.exit());
 console.log('FINAL_STATUS',await page.evaluate(()=>window.streetChavesNative.getStatus()));
 console.log('PAGE_ERRORS',JSON.stringify(errors));
 await browser.close();
})().catch(e=>{console.error('LIVE_TEST_FAIL',e.stack||e);process.exit(1)});
