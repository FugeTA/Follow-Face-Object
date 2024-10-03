import pymel.core as pm

def bakeCustomToolPivot(objects):
    # スケールのピボットポイントからフリーズ前の情報を取得
    old = [0, 0, 0]  # translate(Vector)
    m = pm.xform(objects, q=True, m=True)  # 変換行列情報（double 16）
    p = pm.xform(objects, q=True, os=True, sp=True)  # ローカルのスケール用ピボット位置（Vector）
    old[0] = (p[0] * m[0] + p[1] * m[4] + p[2] * m[8] + m[12])
    old[1] = (p[0] * m[1] + p[1] * m[5] + p[2] * m[9] + m[13])
    old[2] = (p[0] * m[2] + p[1] * m[6] + p[2] * m[10] + m[14])
    
    # ピボットの移動情報をリセット
    pm.xform(objects, zeroTransformPivots=True)
    
    # 現在の位置情報(Vector)
    new = pm.getAttr(objects + ".translate")
    
    # 二つの位置情報を合わせて移動
    pm.move(objects,[old[0]-new[0], old[1]-new[1], old[2]-new[2]], pcp=True, pgp=True, ls=True, r=True)

def faceObject(nVector=[0,0,1],uVector=[0,1,0]):
    # 二つ選択されているか
    if len(pm.ls(sl=True)) <= 1 or len(pm.ls(sl=True)) > 2:
        pm.confirmDialog(t="Error",m="オブジェクトを二つ選択してください",b="閉じる")
        return
    
    s1 = pm.ls(sl=True)[0]  # 動かすオブジェクト
    s2 = pm.ls(sl=True)[1]  # 目標のオブジェクト
    
    # ノード作成
    cpm = pm.createNode("closestPointOnMesh")  #指定したポイントから一番近いメッシュの表面の座標を取得するノード
    mat = pm.createNode("decomposeMatrix")  # matrixから情報を取り出すノード、translateを抽出
    
    # 2番目のオブジェクトをフリーズする（メッシュにtransform情報を書き込む）
    if s2.t != [0,0,0] or s2.r != [0,0,0] or s2.s != [0,0,0]: 
        pm.makeIdentity(s2,a=True)
        
    # 1番目のオブジェクトのトランスフォームの状態を戻す
    bakeCustomToolPivot(s1)  
    
    #ノードに接続
    pm.connectAttr(pm.listRelatives(s2,s=True)[0]+".outMesh", cpm + ".im")  # shapeノードのメッシュ情報をinMeshに接続
    pm.connectAttr(s1+".worldMatrix", mat+".inputMatrix")  # matrixを分解
    pm.connectAttr(mat+".outputTranslate", cpm + ".ip")  # matrixから出力されたtranslateをinPositionに接続
    
    #移動回転
    pm.move(s1,pm.getAttr(cpm + ".p"),ws=True)  # 計算された位置にオブジェクトを移動
    nor = pm.normalConstraint(s2,s1,aim=nVector,u=uVector)  # ノーマル方向に向きを合わせる
    
    # 不要になったノードを削除
    pm.delete(cpm)
    pm.delete(nor)
    
    # 一番目のオブジェクトを選択しなおす
    pm.select(s1)

# 選択したボタンから方向を決定する
def selectVector(ws):
    vec = [[1,0,0],[0,1,0],[0,0,1]]
    sl1 = int(ws['rc1'].getSelect()[-1])-1
    sl2 = int(ws['rc2'].getSelect()[-1])-4
    faceObject(vec[sl1],vec[sl2])

# 同じ方向を選択できないようにする
def blockSameVector(ws):
    for i in range(6):
        ws['rb'+str(i+1)].setEnable(1)  # もっといいやり方がありそう
        
    for i in range(6):
        if ws['rc1'].getSelect() == "rButton"+str(i+1):
            ws['rb'+str(i+4)].setEnable(0)
            
        if ws['rc2'].getSelect() == "rButton"+str(i+1):
            ws['rb'+str(i-2)].setEnable(0)

            
def optionWindow():
    winname = 'FaceObjectOption'
    if pm.window(winname,ex=True)==True:  # すでにウィンドウがあれば閉じてから開く
        pm.deleteUI(winname)
    with pm.window(winname) as wn:
        with pm.autoLayout():
            ws={}
            with pm.frameLayout(l="Normal Vector"):
                with pm.horizontalLayout():
                    #法線方向
                    ws['rc1'] = pm.radioCollection()
                    ws['rb1'] = pm.radioButton("rButton1",l="X",cc=pm.Callback(blockSameVector,ws))
                    ws['rb2'] = pm.radioButton("rButton2",l="Y",cc=pm.Callback(blockSameVector,ws))
                    ws['rb3'] = pm.radioButton("rButton3",l="Z",sl=True,cc=pm.Callback(blockSameVector,ws))

            with pm.frameLayout(l="UP Vector"):
                with pm.horizontalLayout():
                    #アップベクトル
                    ws['rc2'] = pm.radioCollection()
                    ws['rb4']=pm.radioButton("rButton4",l="X",cc=pm.Callback(blockSameVector,ws))
                    ws['rb5']=pm.radioButton("rButton5",l="Y",sl=True,cc=pm.Callback(blockSameVector,ws))
                    ws['rb6']=pm.radioButton("rButton6",l="Z",cc=pm.Callback(blockSameVector,ws))
            with pm.horizontalLayout():
                pm.button(l='Create',c=pm.Callback(selectVector,ws))
                
    blockSameVector(ws)

if __name__ == '__main__':
    optionWindow()
