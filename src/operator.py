import bpy
import json
from . import util

class MY_OT_SaveItem(bpy.types.Operator):
    bl_idname = "global.save_item"
    bl_label = "Save Item"

    def execute(self, context):
        if context.selected_nodes:
            data = util.SerializeNodes(context)
            item = context.window_manager.global_list.add()
            item.name = "Nodes"
            item.node_data = json.dumps(data)
        return {'FINISHED'}


class MY_OT_RemoveItem(bpy.types.Operator):
    bl_idname = "global.remove_item"
    bl_label = "Remove Item"

    def execute(self, context):
        wm = context.window_manager
        index = wm.global_list_index
        
        if 0 <= index < len(wm.global_list):
            wm.global_list.remove(index)

            if index > 0:
                wm.global_list_index = index - 1
                
        return {'FINISHED'}

class MY_OT_Load(bpy.types.Operator):
    bl_idname = "global.load"
    bl_label = "Load to Node Editor"

    def execute(self, context):
        wm = context.window_manager
        index = wm.global_list_index

        if 0 <= index < len(wm.global_list):
            item = wm.global_list[index]
            
            # ★重要: 文字列を「辞書」に戻す
            if item.node_data:
                try:
                    data = json.loads(item.node_data)
                    util.DeserializeNodes(context, data)
                except json.JSONDecodeError:
                    self.report({'ERROR'}, "データの読み込みに失敗しました")

        return {'FINISHED'}

class MY_OT_Reload(bpy.types.Operator):
    bl_idname = "global.reload"
    bl_label = "Reload from File"

    def execute(self, context):
        return {'FINISHED'}