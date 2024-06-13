openBtn = document.getElementById("open")
closeBtn = document.getElementById("close")
container = document.querySelector(".container")

openBtn.addEventListener("click", ()=>{
    container.classList.add("show-nav")
})

closeBtn.addEventListener("click", ()=>{
    container.classList.remove("show-nav")
})