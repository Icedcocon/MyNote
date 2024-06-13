boxes = document.querySelectorAll(".box")

boxes.forEach(box => {
    box.addEventListener("mouseover",()=>{
        removeActive()
        box.classList.add("active")
    })
});

function removeActive(){
    boxes.forEach(box=>{
        box.classList.remove("active")
    })
}