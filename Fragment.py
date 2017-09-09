from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import Geom, GeomNode
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import GeomTriangles, GeomVertexWriter
from panda3d.core import Shader
import sys


class Demo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self) # 初期化

        vs = open('vs_water.glsl', "r", encoding="UTF-8").read()
        fs = open('fs_water.glsl', "r", encoding="UTF-8").read()

        props = WindowProperties()
        props.setTitle('Fragment')
        Win_size = (1920, 1080) # ウィンドウサイズ
        props.setSize(Win_size) # ウィンドウのサイズを設定
        props.setCursorHidden(True) # マウスカーソルを隠す
        base.win.requestProperties(props)

        self.AspectRaito = float(Win_size[0]/Win_size[1]) # アスペクト比を計算
        
        self.accept("escape", sys.exit) # 終了
        self.disableMouse() # マウスカーソルを非表示
        self.setFrameRateMeter(True) # ＦＰＳを表示

        camera.setPos(0,-2,0) # カメラを配置
        format = GeomVertexFormat.getV3()
        
        mesh = GeomVertexData('', format, Geom.UHDynamic) # メッシュを用意
        vertex = GeomVertexWriter(mesh, 'vertex') # 頂点オブジェクト
        vertex.addData3(-1, 0, -1) # 頂点を追加
        vertex.addData3(-1, 0,  1)
        vertex.addData3(1, 0,  1)
        vertex.addData3(1, 0, -1)
        tri = GeomTriangles(Geom.UHDynamic) # 面オブジェクト
        tri.addVertices(0,  2,  1) # 面のインデックスを追加
        tri.addVertices(0,  3,  2) 
        node = GeomNode('')
        geo = Geom(mesh) # ジオメトリオブジェクト
        geo.addPrimitive(tri) # プリミティブにする
        node.addGeom(geo)
        self.panel = render.attachNewNode(node) # レンダーオブジェクトとして追加
        
        shader = Shader.make(Shader.SL_GLSL, vs, fs)
        self.panel.setShader(shader)
        resolution = self.win.getXSize(), self.win.getYSize()
        self.panel.setShaderInput('resolution', resolution)
        
        taskMgr.add(self.Loop, 'update') # メインループ

    def Loop(self, task):
        self.panel.setShaderInput('time', task.time) # シェーダーに送る

        x,y = 0,0# マウスの位置を初期化
        if self.mouseWatcherNode.hasMouse(): # マウスの位置を取得
            x=self.mouseWatcherNode.getMouseX()
            y=self.mouseWatcherNode.getMouseY()
        self.panel.setShaderInput('mouse', (x*self.AspectRaito,y)) # シェーダーに送る
        return task.cont
      
Demo().run()
