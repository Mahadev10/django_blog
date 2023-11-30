const closeElements = document.querySelectorAll(".alert-close")
closeElements.forEach((ele)=>{
    ele.addEventListener("click",()=>{
        ele.parentElement.parentElement.parentElement.remove();
    })
})