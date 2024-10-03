# Follow-Face-Object

## 概要
オブジェクトを別のオブジェクトの最も近い表面上に配置するツール。
## 要件
[pymel](https://github.com/LumaPictures/pymel)
## 使い方
1.ドキュメントのmaya/使用バージョン/script内に.pyファイルを移動する。  
2.以下のコマンドを実行する。
```
import faceObject
faceObject.optionWindow()
```
または
```
import faceObject
faceObject.faceObject()
```
## 説明
1.オブジェクトを二つ選択 
2.faceObject()、optionWindow()のどちらかを実行
　前者は法線方向にＺ軸、アップベクトルにＹ軸が自動で割り当てられる。    
3.optionWindowの場合、それぞれの軸を選択し、実行。
## 作者
[Twitter](https://x.com/cotte_921)

## ライセンス
[MIT](LICENSE)
