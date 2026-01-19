document.addEventListener("DOMContentLoaded",function(){const C=document.getElementById("calculate-btn"),w=document.getElementById("cost-results"),i=document.getElementById("files-count"),c=document.getElementById("file-size"),r=document.getElementById("translation-enabled"),v=document.getElementById("dm-calls"),m=document.getElementById("md-calls"),u=document.getElementById("viewer-calls"),d=document.getElementById("users-count"),g=document.getElementById("sessions-count"),o={dataManagement:.02,modelDerivative:.05,viewer:.01,storage:.1};function l(){const e=parseInt(i.value)||0,s=parseFloat(c.value)||0,a=r.checked,t=parseInt(v.value)||0,n=parseInt(m.value)||0,$=parseInt(u.value)||0,h=parseInt(d.value)||0,E=parseInt(g.value)||0,p=e*t*o.dataManagement,x=a?e*n*o.modelDerivative:0,f=e*$*o.viewer,b=e*s/1024*o.storage,y=p+x+f+b,F=y*12,B=e*(t+(a?n:0)),S=h*E,M=e*s/1024;I({monthly:y,annual:F,breakdown:{dataManagement:p,modelDerivative:x,viewer:f,storage:b},usage:{apiCalls:B,sessions:S,storage:M}})}function I(e){const{monthly:s,annual:a,breakdown:t,usage:n}=e;w.innerHTML=`
          <!-- Cost Summary -->
          <div class="bg-gradient-to-r from-raps-blue to-raps-purple text-white rounded-lg p-6">
            <h3 class="text-lg font-semibold mb-4">💰 Cost Summary</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-2xl font-bold">$${s.toFixed(2)}</div>
                <div class="text-sm opacity-90">per month</div>
              </div>
              <div>
                <div class="text-2xl font-bold">$${a.toFixed(2)}</div>
                <div class="text-sm opacity-90">per year</div>
              </div>
            </div>
          </div>

          <!-- Cost Breakdown -->
          <div class="bg-white border rounded-lg p-6">
            <h3 class="font-semibold mb-4">📊 Monthly Cost Breakdown</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span>Data Management APIs:</span>
                <span class="font-mono">$${t.dataManagement.toFixed(2)}</span>
              </div>
              <div class="flex justify-between">
                <span>Model Derivative:</span>
                <span class="font-mono">$${t.modelDerivative.toFixed(2)}</span>
              </div>
              <div class="flex justify-between">
                <span>Viewer Sessions:</span>
                <span class="font-mono">$${t.viewer.toFixed(2)}</span>
              </div>
              <div class="flex justify-between">
                <span>Storage:</span>
                <span class="font-mono">$${t.storage.toFixed(2)}</span>
              </div>
              <div class="border-t pt-2 flex justify-between font-semibold">
                <span>Total:</span>
                <span class="font-mono">$${s.toFixed(2)}</span>
              </div>
            </div>
          </div>

          <!-- Usage Statistics -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h3 class="font-semibold mb-4">📈 Monthly Usage</h3>
            <div class="grid grid-cols-3 gap-4 text-center text-sm">
              <div>
                <div class="text-2xl font-bold text-raps-blue">${n.apiCalls.toLocaleString()}</div>
                <div class="text-gray-600">API Calls</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-raps-blue">${n.sessions.toLocaleString()}</div>
                <div class="text-gray-600">Viewer Sessions</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-raps-blue">${n.storage.toFixed(1)}</div>
                <div class="text-gray-600">GB Storage</div>
              </div>
            </div>
          </div>

          <!-- Cost Per File -->
          <div class="bg-yellow-50 rounded-lg p-4">
            <h4 class="font-semibold mb-2 text-orange-800">💡 Per-File Economics</h4>
            <div class="text-sm text-orange-700">
              <div>Cost per file: <strong>$${(s/parseInt(i.value)).toFixed(3)}</strong></div>
              <div>Annual cost per user: <strong>$${(a/parseInt(d.value)).toFixed(2)}</strong></div>
            </div>
          </div>
        `}C.addEventListener("click",l),[i,c,v,m,u,d,g].forEach(e=>{e.addEventListener("input",l)}),r.addEventListener("change",l),l()});
