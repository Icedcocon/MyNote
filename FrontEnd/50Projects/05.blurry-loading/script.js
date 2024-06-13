bg = document.querySelector('.bg')
loading = document.querySelector('.loading-text')

let fun = setInterval(bluring, 30)
let val = 1

function bluring(){
    val++
    if (val > 99) {
        clearInterval(fun)
    } 
    loading.innerText = `${val}%`
    loading.style.opacity = `${scale(val,0,100,1,0)}`
    bg.style.filter = `blur(${scale(val,0,100,30,0)}px)`
}

function scale(num, in_min, in_max, out_min, out_max){
    return (num-in_min)/(in_max-in_min)*(out_max-out_min) + out_min
}