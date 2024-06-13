left = document.querySelector(".split.left")
right = document.querySelector(".split.right")
container = document.querySelector(".container")

left.addEventListener("mouseenter",(event)=>{
    container.classList.add("hover-left")
    container.classList.remove("hover-right")
})

right.addEventListener("mouseenter",(event)=>{
    container.classList.add("hover-right")
    container.classList.remove("hover-left")
})