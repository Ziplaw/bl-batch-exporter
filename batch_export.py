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
            bpy.ops.export_scene.fbx(filepath= (f"{props.filepath}/{object.name}.fbx"),use_selection=True,apply_scale_options='FBX_SCALE_ALL',object_types={'MESH'},bake_space_transform=True, apply_unit_scale=True, add_leaf_bones=False, use_armature_deform_only=False, bake_anim=False,axis_forward='-Z', axis_up = 'Y')
        
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