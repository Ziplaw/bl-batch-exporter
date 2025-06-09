bl_info = {
    "name": "Batch Exporter",
    "author": "Ziplaw",
    "version": (1, 0),
    "blender": (3, 6, 14),
    "description": "Exports in FBX in a given directory",
}


import bpy
import os

class BatchExportPropertyGroup(bpy.types.PropertyGroup):
    filepath : bpy.props.StringProperty(
        name="Path",
        description="Path to export all models",
        default="C:/tmp/",
        )
    only_selected : bpy.props.BoolProperty(
        name="Only Selected",
        description="Only export selected models",
        default=True,
        )
    apply_rotations : bpy.props.BoolProperty(
        name="Apply Rotation and Scale",
        description="Apply Rotation and Scale before exporting",
        default=False,
        )
    move_to_world_center : bpy.props.BoolProperty(
        name="Reset Position",
        description="Moves each object to 0,0,0 before exporting and back to their original position afterwards",
        default=True,
        )
    export_settings : bpy.props.EnumProperty(
        items=
        [
            ('UNITY', "Unity", "Unity's Export Settings",1),
            ('UE5', "Unreal Engine 5", "Unreal Engine 5's Export Settings",2),
        ],
        name="Export Settings",
        description="",
        default='UNITY'
        )
        
        
    def draw(self,context):
        self.layout.prop(self,"export_settings")

class BatchExportOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.batch_export_operator"
    bl_label = "Batch Export"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        props = context.scene.BatchExportPropertyGroup
        
        if props.only_selected:
            selected_objects = context.selected_objects
        else:
            selected_objects = bpy.data.objects
        
        
        for object in selected_objects:
            object.select_set(False)
        
        for object in selected_objects:
            object.select_set(True)
            
            if props.apply_rotations:
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                
            op_x = object.location.x
            op_y = object.location.y
            op_z = object.location.z
            
            if props.move_to_world_center:
                object.location = 0,0,0
                            
            match props.export_settings:
                case 'UNITY':
                    bpy.ops.export_scene.fbx(filepath= (f"{props.filepath}/{object.name}.fbx"),use_selection=True,apply_scale_options='FBX_SCALE_ALL',object_types={'MESH'},bake_space_transform=True, apply_unit_scale=True, add_leaf_bones=False, use_armature_deform_only=False, bake_anim=False,axis_forward='-Z', axis_up = 'Y')
                    
                case 'UE5':
                    bpy.ops.export_scene.fbx(filepath= (f"{props.filepath}/{object.name}.fbx"),use_selection=True,apply_scale_options='FBX_SCALE_ALL',object_types={'MESH'},bake_space_transform=True, apply_unit_scale=True, add_leaf_bones=False, use_armature_deform_only=False, bake_anim=False,axis_forward='-Z', axis_up = 'Y')
                    
                case _:
                    raise Exception('Export Settings not Implemented')
            
            if props.move_to_world_center:
                object.location = op_x,op_y,op_z
        
        os.startfile(props.filepath)
        return {'FINISHED'}

class BatchExporter(bpy.types.Panel):
    """Creates a Panel for exporting objects in batch."""
    bl_label = "Batch Exporter"
    bl_idname = "PT_BatchExporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Batch Export'

    def draw(self, context):
        layout = self.layout

        props = context.scene.BatchExportPropertyGroup

        layout.prop(props, "filepath")
        layout.prop(props, "only_selected")
        layout.prop(props, "apply_rotations")
        layout.prop(props, "move_to_world_center")
        layout.prop(props, "export_settings")
        
        row = layout.row()
        op = row.operator("object.batch_export_operator")


def register():
    bpy.utils.register_class(BatchExporter)
    bpy.utils.register_class(BatchExportOperator)
    bpy.utils.register_class(BatchExportPropertyGroup)
    bpy.types.Scene.BatchExportPropertyGroup = bpy.props.PointerProperty(
            type=BatchExportPropertyGroup)


def unregister():
    bpy.utils.unregister_class(BatchExporter)
    bpy.utils.unregister_class(BatchExportOperator)
    bpy.utils.unregister_class(BatchExportPropertyGroup)
    del bpy.types.Scene.MyPropertyGroup


if __name__ == "__main__":
    register()