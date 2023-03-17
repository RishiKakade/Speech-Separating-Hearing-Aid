
let y = {
    theta: null,
    new_theta : null
};

let b = {
    theta: null,
    new_theta : null
};

let o = {
    theta: null,
    new_theta : null
};

let g = {
    theta: null,
    new_theta :null
};


function draw_speaker_animation(x_pos,y_pos,width) {
    push();
    parse_angles(o,b,y,g);

    // background(220);

    // translate to make origin the middle
    translate(x_pos, y_pos);

    strokeWeight(2);
    fill(255, 255, 255);

    stroke(0, 0, 0);

    // rect(-100, -100, 200, 200);
    ellipse(0, 0, width)

    line(0, 0.75*width/2, 0, -0.75*width/2);
    line(0.75*width/2,0, -0.75*width/2,0);

    draw_triangle(y, 255, 204, 0, width);
    draw_triangle(b, 30, 129, 176, width);
    draw_triangle(o, 226, 135, 67, width);
    draw_triangle(g, 76, 168, 72, width);
    pop();
}


function draw_triangle(x, r, g, b, width) {
    if (x.new_theta === null) {
        return 0;
    }

    let x1 = width/2;
    let y1 = tan(-5*PI/180.0)*x1;


    let x2 = width/2;
    let y2 = tan(5*PI/180.0)*x2;

    fill(r, g, b);

    rotate(x.theta*PI/-180.0);
    triangle(0, 0, x1, y1, x2, y2);
    rotate(x.theta*PI/180.0);

    if (round(x.new_theta)-round(x.theta) > 0 ) {
        x.theta = x.theta + 1;
    }else if (round(x.new_theta)-round(x.theta) < 0) {
        x.theta = x.theta - 1;
    } else {
        x.theta = x.new_theta;
    }
  
}

function parse_angles(v1,v2,v3,v4) {
    // prev, curr, and voices arrays should have same length
    // let prev = prev_angle_str.split(", ")
    let curr = current_angle_string.split(", ");

    let voices = [v1, v2, v3, v4];

    for (let i = 0; i < curr.length; i++) { 
        if (curr[i] === "None" ) {
            voices[i].new_theta = null;
        } else {
            voices[i].new_theta = parseInt(curr[i]);
        }
    }
  
  
}
