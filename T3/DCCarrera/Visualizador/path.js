class Path {
    static car_color = 0
    static colors = [
        "#f44336",
        "#9c27b0",
        "#3f51b5",
        "#2196f3",
        "#009688",
        "#4caf50",
        "#cddc39",
        "#ff9800",
        "#4e342e",
    ]
    constructor(start, goal, path, velocity, sq_size, canvas, actual_speed){

        this.start = start
        this.goal = goal
        this.path = path
        this.velocity = velocity
        this.square_size = sq_size
        this.start_color = Path.colors[Path.car_color]
        this.goal_color = Path.colors[Path.car_color]
        this.path_color = Path.colors[Path.car_color]
        this.car = new Car(Path.car_color, sq_size)
        Path.car_color = (Path.car_color + 1 )%9
        this.index = 0
        this.max_ticks = 20
        this.tick_speed = actual_speed
        this.tick = 0
        this.finish = false
        this.stop = false
        this.canvas = canvas
        this.offset = 0
        this.canvas.appendChild(this.car.img)
        this.assign_points()

    }
    assign_points(){
        this.p1 = this.path[this.index]
        this.p2 = this.path[this.index+1]
        if (this.index >= this.path.length-1){
            this.finish = true
            this.index = this.path_length-2
        }

    }
    draw_line(pos, color){
        stroke(color)
        fill(color)
        rect(pos[0]*this.square_size  , pos[1]*this.square_size , this.square_size , this.square_size )
    }

    calc_position(){
        let x = this.p1[0] + (this.p2[0] - this.p1[0])*this.tick/this.max_ticks
        let y = this.p1[1] + (this.p2[1] - this.p1[1])*this.tick/this.max_ticks
        let out = [x*this.square_size - this.offset, y*this.square_size - this.offset]
        return out
    }
    calc_angle(){
        let vector = [this.p2[0] - this.p1[0], this.p2[1] - this.p1[1]]
        let angle = Math.atan2(vector[1], vector[0])*180/Math.PI + 90
        return angle
    }
    show(){

        this.draw_line(this.start, this.start_color)

        this.draw_line(this.goal, this.goal_color)
        this.path.slice(0, this.path.length-1).forEach((pos, i) => {
            stroke(this.path_color)
            line(pos[0]*this.square_size + this.square_size/2,  pos[1]*this.square_size + this.square_size/2, this.path[i+1][0]*this.square_size + this.square_size/2, this.path[i+1][1]*this.square_size + this.square_size/2)
        });

        if (!this.finish){
            this.car.show(this.calc_position(),this.calc_angle())
            this.tick += this.tick_speed;
            if (this.tick>=this.max_ticks-1){
    
                this.tick = 0
                this.index +=1
                this.assign_points()
            }
            
        }
    }

    restart(){
        this.index = 0
        this.tick = 0
        this.finish = false
        this.assign_points()
        this.show()
    }
    clear(){
        this.canvas.removeChild(this.car.img)
    }

    // play(){
    //     this.stop = !this.stop
    // }

}