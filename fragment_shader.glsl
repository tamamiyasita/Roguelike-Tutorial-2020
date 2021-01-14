#version 330

// fragment shaderはvertex shaderから色を渡され　それをピクセルとして出力する

// ここで頂点シェーダーから色を渡される
in vec4 color;

// フレームバッファに書き込まれるピクセル
out vec4 fragColor;

void main() {
    // ポイントを埋める
    fragColor = vec4(color)
}