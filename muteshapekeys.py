bl_info = {
    "name": "Mute/Unmute Shape Keys",
    "author": "Zeromaniac x ChatGPT",
    "version": (1, 0),
    "blender": (3, 6, 0),  # Blender version 3.6
    "description": "Mute or unmute shape keys in bulk. 3D Viewport -> Tools",
    "category": "Object",
}

import bpy

# Operator to mute or unmute all shape keys
class OBJECT_OT_MuteUnmuteAllShapeKeys(bpy.types.Operator):
    bl_idname = "object.mute_unmute_all_shape_keys"
    bl_label = "Mute/Unmute All Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            # Get all shape keys
            shape_keys = obj.data.shape_keys.key_blocks
            # Check the current state of muting
            mute_all = all(shape_key.mute for shape_key in shape_keys)  # Check if all are muted

            # Toggle mute/unmute for all shape keys
            for shape_key in shape_keys:
                shape_key.mute = not mute_all

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Object does not have shape keys")
            return {'CANCELLED'}

# Operator to flip the mute state of all shape keys except the basis
class OBJECT_OT_FlipAllShapeKeys(bpy.types.Operator):
    bl_idname = "object.flip_all_shape_keys"
    bl_label = "Flip All Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            shape_keys = obj.data.shape_keys.key_blocks

            # Iterate through all shape keys and flip their mute state, skipping the 'Basis'
            for shape_key in shape_keys:
                if shape_key.name != "Basis":  # Skip the basis shape key
                    shape_key.mute = not shape_key.mute  # Flip the mute state

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Object does not have shape keys")
            return {'CANCELLED'}

# Custom panel in the N-Panel
class MESH_PT_MuteShapeKeysPanel(bpy.types.Panel):
    bl_label = "Mute Shape Keys"
    bl_idname = "MESH_PT_mute_shape_keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'  # This makes it show up in the N-Panel under the "Tool" tab

    def draw(self, context):
        layout = self.layout
        obj = context.object

        # Only show the buttons if the selected object has shape keys
        if obj and obj.type == 'MESH' and obj.data.shape_keys:
            layout.operator(OBJECT_OT_MuteUnmuteAllShapeKeys.bl_idname, text="Mute/Unmute All Shape Keys")
            layout.operator(OBJECT_OT_FlipAllShapeKeys.bl_idname, text="Flip All Shape Keys")
        else:
            layout.label(text="No Shape Keys Found")

# Register and unregister functions
def register():
    bpy.utils.register_class(OBJECT_OT_MuteUnmuteAllShapeKeys)
    bpy.utils.register_class(OBJECT_OT_FlipAllShapeKeys)
    bpy.utils.register_class(MESH_PT_MuteShapeKeysPanel)  # Register the custom panel

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_MuteUnmuteAllShapeKeys)
    bpy.utils.unregister_class(OBJECT_OT_FlipAllShapeKeys)
    bpy.utils.unregister_class(MESH_PT_MuteShapeKeysPanel)  # Unregister the custom panel

if __name__ == "__main__":
    register()
