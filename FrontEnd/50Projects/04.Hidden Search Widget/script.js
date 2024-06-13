button = document.getElementById("search")
search = document.querySelector(".search")
input = document.querySelector(".search .input")

button.addEventListener("click",()=>{
    search.classList.toggle("active")
    input.focus()
})