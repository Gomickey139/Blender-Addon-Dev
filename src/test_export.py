import bpy
import json
import os

# 先ほどマウントしたターゲットパス（コンテナ内から見たUnityのフォルダ）
EXPORT_DIR = "/workspace/UnityAssets"

def run_test_export():
    # 既存のオブジェクトをすべて削除してクリーンにする
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # テスト用のオブジェクト（Cube）を生成
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.active_object
    obj.name = "Test_Pipe_COL" # 名前にCOLを入れてCollider生成をテスト

    # パスの構築
    fbx_path = os.path.join(EXPORT_DIR, f"{obj.name}.fbx")
    json_path = os.path.join(EXPORT_DIR, f"{obj.name}.json")

    # FBXエクスポート（Unity向けの座標変換・Geometry Nodes等の適用を含む）
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        axis_forward='-Z',
        axis_up='Y',
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        use_mesh_modifiers=True,
        mesh_smooth_type='OFF'
    )

    # メタデータ（JSON）の生成
    metadata = {
        "scale_factor": 1.0,
        "generate_colliders": "COL" in obj.name,
        "is_static": True,
        "vfx_type": "horror_leaking_steam" # ホラー演出用のカスタムデータ
    }

    with open(json_path, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"--- Export Success ---")
    print(f"FBX: {fbx_path}")
    print(f"JSON: {json_path}")

if __name__ == "__main__":
    run_test_export()