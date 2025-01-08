bl_info = {
    "name": "Zeros Shape Key Utils",
    "author": "Zeromaniac x ChatGPT",
    "version": (2, 0),
    "blender": (3, 6, 0),
    "location": "Shape Keys Context Menu",
    "description": "Adds more options to the shape key context menu.",
    "category": "Object",
}

import bpy
import os
import bpy.utils.previews

# Function to get the script directory
def get_icon_path(filename):
    script_directory = os.path.dirname(__file__)
    return os.path.join(script_directory, filename)

# Register the custom icons
def register_custom_icons():
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    
    # Load the icons
    script_path = os.path.dirname(__file__)  # Get the script's directory
    custom_icons.load("flip", os.path.join(script_path, "flip.png"), 'IMAGE')
    custom_icons.load("unmute_icon", os.path.join(script_path, "unmute_icon.png"), 'IMAGE')
    custom_icons.load("mute_icon", os.path.join(script_path, "mute_icon.png"), 'IMAGE')
    custom_icons.load("move_up_icon", os.path.join(script_path, "move_up_icon.png"), 'IMAGE')
    custom_icons.load("move_down_icon", os.path.join(script_path, "move_down_icon.png"), 'IMAGE')
    
# Unregister the icons
def unregister_custom_icons():
    global custom_icons
    if custom_icons:
        bpy.utils.previews.remove(custom_icons)
        custom_icons = None

# Function to mute/unmute all shape keys
def mute_unmute_all(obj, mute_state):
    if obj and obj.data.shape_keys:
        for key_block in obj.data.shape_keys.key_blocks:
            if key_block.name != "Basis":
                key_block.mute = mute_state
        print(f"All shape keys {'muted' if mute_state else 'unmuted'}")
    else:
        print("No shape keys found on the selected object.")

# Function to invert mute state of shape keys
def invert_muted(obj):
    if obj and obj.data.shape_keys:
        for key_block in obj.data.shape_keys.key_blocks:
            if key_block.name != "Basis":
                key_block.mute = not key_block.mute
        print("Inverted shape key mute states")
    else:
        print("No shape keys found on the selected object.")

# Operator to invert muted state of shape keys
class OBJECT_OT_InvertMutedShapeKeys(bpy.types.Operator):
    """Invert muted state of all shape keys"""
    bl_idname = "object.invert_muted_shape_keys"
    bl_label = "Invert Shape Key Mute State"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        invert_muted(obj)
        return {'FINISHED'}

# Operator to mute all shape keys
class OBJECT_OT_MuteAllShapeKeys(bpy.types.Operator):
    bl_idname = "object.mute_all_shape_keys"
    bl_label = "Mute All Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        mute_unmute_all(obj, True)
        return {'FINISHED'}

# Operator to unmute all shape keys
class OBJECT_OT_UnmuteAllShapeKeys(bpy.types.Operator):
    bl_idname = "object.unmute_all_shape_keys"
    bl_label = "Unmute All Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        mute_unmute_all(obj, False)
        return {'FINISHED'}
        
# Operator to move the shape key up by 10 places
class OBJECT_OT_MoveShapeKeyUp(bpy.types.Operator):
    bl_idname = "object.move_shape_key_up"
    bl_label = "Move Shape Key Up by 10"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        if shape_keys:
            active_shape_key = obj.active_shape_key
            active_index = shape_keys.key_blocks.find(active_shape_key.name)
            if active_index > 9:
                for _ in range(10):
                    bpy.ops.object.shape_key_move(type='UP')
                print(f"Moved shape key {active_shape_key.name} up by 10 places")
            else:
                self.report({'WARNING'}, "Cannot move the shape key up by 10 places, already at top.")
        return {'FINISHED'}

# Operator to move the shape key down by 10 places
class OBJECT_OT_MoveShapeKeyDown(bpy.types.Operator):
    bl_idname = "object.move_shape_key_down"
    bl_label = "Move Shape Key Down by 10"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.object
        shape_keys = obj.data.shape_keys
        if shape_keys:
            active_shape_key = obj.active_shape_key
            active_index = shape_keys.key_blocks.find(active_shape_key.name)
            if active_index < len(shape_keys.key_blocks) - 10:
                for _ in range(10):
                    bpy.ops.object.shape_key_move(type='DOWN')
                print(f"Moved shape key {active_shape_key.name} down by 10 places")
            else:
                self.report({'WARNING'}, "Cannot move the shape key down by 10 places, already at bottom.")
        return {'FINISHED'}

# Modify the shape key context menu to include the icons
def shape_key_context_menu(self, context):
    layout = self.layout
    layout.separator()

    # Invert muted state button with custom icon
    layout.operator(
        OBJECT_OT_InvertMutedShapeKeys.bl_idname,
        text="Invert Shape Key Mute State",
        icon_value=custom_icons["flip"].icon_id
    )
    
    # Unmute all shape keys button with custom icon
    layout.operator(
        OBJECT_OT_UnmuteAllShapeKeys.bl_idname,
        text="Unmute All Shape Keys",
        icon_value=custom_icons["unmute_icon"].icon_id
    )
    
    # Mute all shape keys button with custom icon
    layout.operator(
        OBJECT_OT_MuteAllShapeKeys.bl_idname,
        text="Mute All Shape Keys",
        icon_value=custom_icons["mute_icon"].icon_id
    )
    
    layout.separator()  # Add a separator between the two groups

    # Move shape key down by 10 places with custom icon
    layout.operator(
        OBJECT_OT_MoveShapeKeyDown.bl_idname,
        text="Move Shape Key Down by 10",
        icon_value=custom_icons["move_down_icon"].icon_id
    )
    
    # Move shape key up by 10 places with custom icon
    layout.operator(
        OBJECT_OT_MoveShapeKeyUp.bl_idname,
        text="Move Shape Key Up by 10",
        icon_value=custom_icons["move_up_icon"].icon_id
    )

# Register and unregister functions for the add-on
def register():
    register_custom_icons()  # Load the custom icons
    
    bpy.utils.register_class(OBJECT_OT_InvertMutedShapeKeys)
    bpy.utils.register_class(OBJECT_OT_MuteAllShapeKeys)
    bpy.utils.register_class(OBJECT_OT_UnmuteAllShapeKeys)
    bpy.utils.register_class(OBJECT_OT_MoveShapeKeyUp)
    bpy.utils.register_class(OBJECT_OT_MoveShapeKeyDown)
    
    # Append to the shape key context menu
    bpy.types.MESH_MT_shape_key_context_menu.append(shape_key_context_menu)

def unregister():
    unregister_custom_icons()  # Remove the custom icons
    
    # Remove the operators from the context menu
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_key_context_menu)
    
    # Unregister the operator classes
    bpy.utils.unregister_class(OBJECT_OT_InvertMutedShapeKeys)
    bpy.utils.unregister_class(OBJECT_OT_MuteAllShapeKeys)
    bpy.utils.unregister_class(OBJECT_OT_UnmuteAllShapeKeys)
    bpy.utils.unregister_class(OBJECT_OT_MoveShapeKeyUp)
    bpy.utils.unregister_class(OBJECT_OT_MoveShapeKeyDown)

if __name__ == "__main__":
    register()
