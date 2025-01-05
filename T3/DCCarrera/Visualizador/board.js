class Board {
    constructor(rows, cols, square_size, matrix){
        this.rows = rows;
        this.cols = cols;
        this.square_size = square_size;
        this.matrix = matrix;
    }

    show(pg) {
        for (let col = 0; col < this.cols; col++) {
            for (let row = 0; row < this.rows; row++) {
                pg.stroke(100);

                let cell = this.matrix[row][col];

                if (cell) {
                    // Casillas base ('@', 'I', 'G', '.')
                    if (cell === '@') {
                        pg.fill(0,0,0); // Color negro para '@'
                    } else if (cell === 'I') {
                        pg.fill(0, 255, 0); // Verde para 'I'
                    } else if (cell === 'G') {
                        pg.fill(255, 0, 0); // Rojo para 'G'
                    } else if (cell === '.') {
                        pg.noFill(); // No relleno para '.'
                    } else if (cell === 'H') {
                        pg.fill(0, 0, 225); // Azul para 'H' (hielo)
                    } else if (cell === 'A') {
                        pg.fill(255, 205, 0); // Amarillo para 'A' (arena)
                    }                
                    pg.rect(col * this.square_size, row * this.square_size, this.square_size, this.square_size);
                

                } else {
                    pg.noFill();
                    pg.rect(col * this.square_size, row * this.square_size, this.square_size, this.square_size);
                }
            }
        }
    }
}