function vh(v) {
    var h = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
    return (v * h) / 100;
  }
  
function vw(v) {
    var w = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
    return (v * w) / 100;
}




let canvas;
let board;
let width;
let height;
let new_map = false;
let valid_map = false
let paths = Array();
let pg;
const max_size = 150;
let actual_speed = 5;
let canvas_div = document.getElementById('p5_canvas')
let restart = document.getElementById('restart')
let play = document.getElementById('play')
let clear = document.getElementById('clear')

let play_state = true


function setup(){
    canvas = createCanvas(0,0)
    canvas.parent('p5_canvas')



}


let restart_paths = function(){ 
    paths.forEach(path => {
        path.restart()
    })
}

let play_paths = function(){
    play_state = ! play_state
    play.textContent = play_state ? "Detener" : "Reanudar"
    console.log(play_state ? "Detener" : "Reanudar")
}

let clear_paths = function(){
    background(255)
    paths.forEach(path=>{
        path.clear()
    })
    Path.car_color=0
    paths = []
}

let change_speed = function(e){
    paths.forEach(path => {
        path.tick_speed = parseInt(speed.value)
    })
}
restart.addEventListener("click", restart_paths)
play.addEventListener("click", play_paths)
clear.addEventListener("click", clear_paths)

let speed = document.getElementById("speed")
let pa = document.getElementById("pa")

speed.onchange = change_speed


function draw(){

    if (new_map){
        valid_map = true
        new_map = false
        pg = createGraphics(width, height)
        board.show(pg)
        resizeCanvas(width, height)
        canvas.height = height  
        canvas.width = width

    }
    if (valid_map){
        image(pg, 0, 0, width, height)
    }
    if (play_state){
        paths.forEach(path => {
            path.show()
        });
    }

    

}

let load_map = function(text) {
    var lines = text.split(/[\r\n]+/g);
    var map_size = lines[0].split(',').map(element => {
        return parseInt(element);
    });
    
    if (map_size[0] && map_size[1]) {
        lines = lines.slice(1, lines.length);
        let matrix = lines.map(e => {
            return e.split('').map(el => {
                // Devolver el carácter directamente
                return el; // Ahora la matriz contendrá 'I', 'G', '@', '.', 'H', 'A'
            });
        });

        let cols = map_size[0];
        let rows = map_size[1];
        let max_dim = Math.max(rows, cols);
        console.log(max_dim);
        console.log(rows, cols);
        height = vw(max_size * rows / max_dim);
        width = vh(max_size * cols / max_dim);
        console.log(height, width);
        let square_size = width / cols;
        console.log(square_size);
        
        // Crear el tablero con la nueva matriz
        board = new Board(rows, cols, square_size, matrix);
        new_map = true;
    }
};



let load_path = function(text){
    let problem = JSON.parse(text)
    problem.forEach(path => {
        let new_path = new Path(path.start, path.goal, path.path, path.velocity, board.square_size, canvas_div, actual_speed)
        paths.push(new_path)
    })

    
}

let read_and_apply = function(id, fn){
    var fileInput = document.getElementById(id);
    fileInput.addEventListener('change', function(e) {
        var file = fileInput.files[0];
        
        var reader = new FileReader();
        reader.onload = function(e) {
            fn(reader.result)
        }
        reader.readAsText(file);    
        
    });
    fileInput.addEventListener('click', (e)=>{
        fileInput.value = ""
    })
    
}
window.onload = function() {
    read_and_apply('mapFileInput', load_map)
    read_and_apply('pathFileInput', load_path)
}