document.addEventListener("DOMContentLoaded",function(){const o=document.getElementById("urn-input"),g=document.getElementById("token-input"),m=document.getElementById("debug-btn"),a=document.getElementById("debug-results");function l(s){return/^urn:adsk\./.test(s)}function v(s){try{let e=s.replace(/-/g,"+").replace(/_/g,"/");for(;e.length%4;)e+="=";return atob(e)}catch{return null}}function f(s){const e={original:s.trim(),isEncoded:!1,isValidUrn:!1,decoded:null,issues:[],recommendations:[]};if(!s.trim())return e.issues.push("No URN provided"),e;if(s.startsWith("urn:"))e.decoded=s,l(s)?e.isValidUrn=!0:e.issues.push("URN format appears invalid");else{e.isEncoded=!0;const t=v(s);t?(e.decoded=t,l(t)?e.isValidUrn=!0:e.issues.push("Decoded URN does not match expected format")):(e.issues.push("Invalid Base64 encoding"),e.recommendations.push("Verify the URN is properly encoded"))}return e.decoded&&(!e.decoded.includes("objects:os.object:")&&!e.decoded.includes("wipprod:")&&!e.decoded.includes("fs.file:")&&(e.issues.push("URN type may not support translation"),e.recommendations.push("Ensure URN points to a translatable file type")),e.decoded.length>500&&e.issues.push("URN unusually long - may indicate corruption")),e}function x(s,e){const{original:t,isEncoded:u,isValidUrn:r,decoded:n,issues:p,recommendations:b}=s;let d=`
          <!-- URN Analysis -->
          <div class="bg-white border rounded-lg p-4">
            <h3 class="font-semibold mb-3 flex items-center">
              ${r?"✅":"❌"} URN Analysis
            </h3>
            <div class="space-y-2 text-sm">
              <div><strong>Format:</strong> ${u?"Base64 Encoded":"Plain URN"}</div>
              <div><strong>Valid URN:</strong> ${r?"Yes":"No"}</div>
              ${n?`<div><strong>Decoded:</strong><br><code class="text-xs break-all">${n}</code></div>`:""}
            </div>
          </div>
        `;p.length>0&&(d+=`
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
              <h3 class="font-semibold mb-3 text-red-800">⚠️ Issues Found</h3>
              <ul class="space-y-1 text-sm text-red-700">
                ${p.map(i=>`<li>• ${i}</li>`).join("")}
              </ul>
            </div>
          `),b.length>0&&(d+=`
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 class="font-semibold mb-3 text-yellow-800">💡 Recommendations</h3>
              <ul class="space-y-1 text-sm text-yellow-700">
                ${b.map(i=>`<li>• ${i}</li>`).join("")}
              </ul>
            </div>
          `),r&&(d+=`
            <div class="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 class="font-semibold mb-3 text-green-800">✅ Next Steps</h3>
              <div class="space-y-2 text-sm text-green-700">
                <p><strong>API Endpoint:</strong></p>
                <code class="block text-xs bg-white p-2 rounded">GET /modelderivative/v2/designdata/${u?t:btoa(t).replace(/=/g,"")}/manifest</code>
                
                <p class="pt-2"><strong>Required Scopes:</strong></p>
                <div class="flex flex-wrap gap-1">
                  <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">viewables:read</span>
                  <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">data:read</span>
                </div>
                
                ${e?"":`
                <p class="pt-2"><strong>With RAPS:</strong></p>
                <code class="block text-xs bg-gray-800 text-green-400 p-2 rounded">raps translate status "${n||t}"</code>
                `}
              </div>
            </div>
          `),e||(d+=`
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 class="font-semibold mb-3 text-blue-800">🔑 Live Testing</h3>
              <p class="text-sm text-blue-700 mb-2">
                To test actual translation status, provide an access token above or use RAPS CLI:
              </p>
              <code class="block text-xs bg-gray-800 text-green-400 p-2 rounded">
                raps auth login --scopes "viewables:read data:read"<br>
                raps translate status "${n||t}"
              </code>
            </div>
          `),a.innerHTML=d}function c(){const s=o.value.trim(),e=g.value.trim();if(!s){a.innerHTML='<div class="text-red-600 text-center py-8">Please enter a URN or Object ID</div>';return}const t=f(s);x(t,!!e)}m.addEventListener("click",c),o.addEventListener("input",()=>{o.value.trim()&&c()})});
