#version 330


in vec2 in_pos;


out vec4 color;

void main() {

    color = vec4(1, 1, 1, 1);


    gl_Position = vec4(in_pos, 0.0, 1);
}

