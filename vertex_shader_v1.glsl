#version 330

//time since burst start
uniform float time;

uniform vec2  r; // resolution
//(x, y) position passed in
in vec2 in_pos;

// velocity of particle
in vec2 in_vel;
// color of particle
in vec3 in_color;

// fade rate
in float in_fade_rate;

//output the color to the fragment shader
out vec4 color;

void main() {

    // calculate alpha based on time and fade rate
    float alpha = 1.0 - (in_fade_rate * time);
    


    // set the RGBA color
    color = vec4(abs(cos(in_color[2])), in_color[0], in_color[1], alpha);
    // if(alpha < 0.7) alpha =  1.0 - (in_fade_rate * (time*300));
    // if(alpha < time) color = vec4(1,1,1,0.3+alpha);

    if(in_fade_rate > time) if(alpha < 0.6) color = vec4(1,1,abs(sin(time*5)),0.4+alpha);

    if(alpha < 0.0) alpha = 0;


    // adjust velocity based on grabity
    vec2 new_vel = in_vel;
    new_vel[1] -= time * 0.2;

    // calculate a new position

    // calculate a new position
    //vec2 new_pos = in_pos + (time * in_vel);
    float f = 0.0;
    for(float i = 0.0; i < 10.0; i++){
        float s = sin(time + i * 0.628318) * 0.5;
        float c = cos(time + i * 0.628318) * 0.5;
        f += 0.0025 / abs(length(512 + vec2(c, s)) - 0.5);
    }
    vec2 new_pos = in_pos + (sin(time) * new_vel);
    // set the position (x, y, z, w)
    gl_Position = vec4(new_pos, f, 1);
}

// void main(void){
//     vec2 p = (in_pos);
//     vec3 destColor = vec3(1.0, 0.3, 0.7);
//     float f = 0.0;
//     for(float i = 0.0; i < 10.0; i++){
//         float s = sin(time + i * 0.628318) * 0.5;
//         float c = cos(time + i * 0.628318) * 0.5;
//         f += 0.0025 / abs(length(p + vec2(c, s)) - 0.9);
//     }
//     color = vec4(vec3(destColor * f), 1.0);
//     gl_Position = vec4(vec3(f), 1.0);
// }