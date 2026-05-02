bl_info = {
    "name": "FBX_Exporter",
    "author": "gmcky139",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "Node Editor > Sidebar > FBX_Exporter",
    "description": "FBXとメタデータ(JSON)をUnityへ自動エクスポートします",
    "category": "Import-Export",
    "support": "COMMUNITY",
    "warning": ""
}

import bpy
import importlib
from . import ui
from . import operator

if "bpy" in locals():
    # 2回目以降の読み込み（チェックのオンオフ時や上書き時）はメモリから強制リロードする
    import importlib
    importlib.reload(ui)
    importlib.reload(operator)
else:
    # 初回読み込み時
    import bpy
    from . import ui
    from . import operator

pyfiles = [
    ui,
    operator
]

for p in pyfiles:
    if str(p) in locals():
        importlib.reload(p)

classes = [
    operator.EXPORT_OT_fbx_auto,
    ui.VIEW3D_PT_fbx_export,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.fbx_export_path = bpy.props.StringProperty(
        name="Export Path",
        description="コンテナ内のUnity Assetsマウント先",
        default="C:\\Users\\akutanezumi\\github\\AutoImportTest\\Assets\\FBX",
        subtype='DIR_PATH'
    )

def unregister():

    del bpy.types.Scene.fbx_export_path

    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()
