#version 330

// vertex_shaderは頂点の位置を取得する、後にin_posで位置を設定し、そのデータを渡す
// また、vertex_shaderは頂点の色も出力する、色はRGBとalpha(RGBA)形式で、0から1までのfloat値を設定する。
// 色番号255が1に相当するので(1,1,1,1)は白になる、最後の1(alpha値)で透明度を変える事が出来る

// (x, y) に渡す位置
in vec2 in_pos;

// fragment_shaderに出力する色
out vec4 color;

void main() {
    // RGBAカラーを設定する
    color = vec4(1,1,1,1);

    // 位置を設定する(x,y,x,w に)
    gl_Position = vec4(in_pos, 0.0, 1)
}

