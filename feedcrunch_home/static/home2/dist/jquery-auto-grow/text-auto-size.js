(function(){"use strict";var e=/\s/g;var t=/>/g;var i=/</g;function n(n){return n.replace(e,"&nbsp;").replace(t,"&lt;").replace(i,"&gt;")}var o=document.createElement("div");o.style.cssText="box-sizing:content-box;display:inline-block;height:0;overflow:hidden;position:absolute;top:0;visibility:hidden;white-space:nowrap;";document.body.appendChild(o);function l(e,t){e.style.boxSizing="content-box";var i=window.getComputedStyle(e);var l="font-family:"+i.fontFamily+";font-size:"+i.fontSize;function r(t){t=t||e.value||e.getAttribute("placeholder")||"";o.style.cssText+=l;o.innerHTML=n(t);var i=window.getComputedStyle(o).width;e.style.width=i;return i}e.addEventListener("input",function(){r()});var d=r();if(t&&t.minWidth&&d!=="0px"){e.style.minWidth=d}return r}if(typeof module=="object"){module.exports=l}else{window.autosizeInput=l}})();
