import bpy
import os
import json

def load_from_json(FILE):
    if os.path.exists(FILE):
        try:
            with open(FILE, 'r') as f:
                data = json.load(f)

            wm = bpy.context.window_manager
            wm.global_list.clear()

            for d in data:
                item = wm.global_list.add()
                item.name = d["name"]
                item.node_data = d["node_data"]

            print("読み込み完了")  

        except json.JSONDecodeError:
            print("ファイルの中身は壊れている")

def store_to_json(FILE):
    wm = bpy.context.window_manager

    data_list = []

    for item in wm.global_list:
        data = {
            "name": item.name,
            "node_data": item.node_data
        }
        
        data_list.append(data)

    
    with open(FILE, 'w') as f:
        json.dump(data_list, f, indent=4)

def SerializeNodes(context):
    nodes = context.selected_nodes
    tree = context.space_data.node_tree

    data = {
        "node": [],
        "links": []
    }

    sel_names = [n.name for n in nodes]

    target_props = [
        "operation",        # Math, Vector Math, Boolean
        "blend_type",       # Mix Node
        "data_type",        # Mix Node (Float/Vector/Color...)
        "mode",             # Map Range
        "distribution",     # Brick Texture, Voronoi
        "subsurface_method" # Principled BSDF
        "noise_dimensions", # Noise Texture (2D/3D/4D)
        "noise_type",       # Noise Texture (fBM...)
        "normalize",        # Noise Texture (normalize)
        "feature",          # Voronoi (F1, F2...)
        "distance",         # Voronoi (Euclidean...)
        "use_clamp",        # Math Node Checkbox
        "clamp_result",     # Mix Node Checkbox
        "clamp_factor",     # Mix Node Checkbox (Old)
        "interpolation_type", # Map Range
        "color_mode",       # Gradient Texture
        "wave_type",        # Wave Texture
        "wave_profile",     # Wave Texture
        "rings_direction",  # Wave Texture
    ]

    for node in nodes:
        node_data = {
            "name": node.name,
            "id": node.bl_idname,
            "location": (node.location.x, node.location.y),
            "width": node.width,
            "inputs": [],
            "properties": {}
        }

        for prop_name in target_props:
            if hasattr(node, prop_name):
                val = getattr(node, prop_name)
                node_data["properties"][prop_name] = val

        for i, sock in enumerate(node.inputs):
            if not sock.is_linked and hasattr(sock, "default_value"):
                val = sock.default_value

                try:
                    val = list(val)
                except:
                    pass

                node_data["inputs"].append({"index": i, "value": val})
       
        data["node"].append(node_data)
    

    for link in tree.links:
        if link.from_node.name in sel_names and link.to_node.name in sel_names:
            link_data = {
                "from_node": link.from_node.name,
                "from_socket_index": -1,
                "to_node": link.to_node.name,
                "to_socket_index": -1
            }

            for i, sock in enumerate(link.from_node.outputs):
                if sock == link.from_socket:
                    link_data["from_socket_index"] = i
                    break
            
            for i, sock in enumerate(link.to_node.inputs):
                if sock == link.to_socket:
                    link_data["to_socket_index"] = i
                    break
            
            data["links"].append(link_data)

    return data


def DeserializeNodes(context, data):
    tree = context.space_data.node_tree

    for n in tree.nodes:
        n.select = False

    node_map = {}

    for n_data in data["node"]:
        new_node = tree.nodes.new(n_data["id"])
        new_node.location = n_data["location"]
        new_node.width = n_data["width"]
        new_node.select = True

        node_map[n_data["name"]] = new_node

        for prop, val in n_data["properties"].items():
            if hasattr(new_node, prop):
                try:
                    setattr(new_node,prop,val)
                except:
                    print(f"Property Error: {prop}")
        
        for inp in n_data["inputs"]:
            idx = inp["index"]
            val = inp["value"]

            if idx < len(new_node.inputs):
                try:
                    new_node.inputs[idx].default_value = val
                except:
                    pass
    

    for l_data in data["links"]:
        try:
            node_from = node_map[l_data["from_node"]]
            node_to = node_map[l_data["to_node"]]

            socket_out = node_from.outputs[l_data["from_socket_index"]]
            socket_in = node_to.inputs[l_data["to_socket_index"]]

            tree.links.new(socket_out, socket_in)

        except KeyError:
            print("Link Error: Node mapping failed")
        except IndexError:
            print("Link Error: Socket index mismatch")

    return {'FINISHED'}