class Car {
    constructor(color, square_size){
        this.img = document.createElement('img')
        let filename = `assets/car${color}.png`
        console.log("Square size", square_size)
        console.log("filename", filename)
        this.img.src = filename
        let squares = 2
        let factor = 25/square_size / squares
        this.img.style.width = Math.round(17/factor)
        this.img.style.height =  Math.round(25/factor)
        this.img.style.position = "absolute"
        this.img.style.top = 0
        this.img.style.left = 0
        this.img.style.zIndex = 999
    }
    show(pos, angle) {
        this.img.style.top = pos[1]- 5 + 'px';
        this.img.style.left = pos[0] + 'px';
        this.img.style.transform = `rotate(${angle}deg)`;
    }
}