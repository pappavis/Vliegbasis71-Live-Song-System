document.addEventListener("DOMContentLoaded",()=>{

console.log("🎸 Vliegbasis71 Live Song System");

const headers=document.querySelectorAll("h2");

headers.forEach(h=>{

h.addEventListener("mouseenter",()=>{

h.style.transition="0.3s";

h.style.transform="translateX(6px)";

});

h.addEventListener("mouseleave",()=>{

h.style.transform="translateX(0px)";

});

});

});
console.log("Vliegbasis71 loaded");