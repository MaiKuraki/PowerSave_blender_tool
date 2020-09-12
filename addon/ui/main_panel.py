import bpy
from .. import utils


class PowerSavePanel(bpy.types.Panel):
    bl_idname = 'POWERSAVE_PT_PowerSavePanel'
    bl_category = 'PowerSave'
    bl_label = 'PowerSave'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        prefs = utils.common.prefs()

        layout = self.layout
        column = layout.column()

        if self.is_popover:
            layout.ui_units_x = prefs.popover_width

            if prefs.panel_tab == 'POWERSAVE':
                text = 'PowerSave'
            elif prefs.panel_tab == 'POWERLINK':
                text = 'PowerLink'
            else:
                text = 'Unknown'

            row = column.row()
            row.label(text=text)
            row.prop(prefs, 'panel_tab', expand=True, icon_only=True)
            column.separator()

        if prefs.panel_tab == 'POWERSAVE' or not self.is_popover:
            powersave_draw(self, column)

        elif prefs.panel_tab == 'POWERLINK':
            powerlink_draw(self, column)


def popover(self, context):
    layout = self.layout
    panel = PowerSavePanel.bl_idname
    icon = utils.ui.get_icon()
    layout.popover(panel, text='', icon_value=icon)


def powersave_draw(self, column):
    prefs = utils.common.prefs()
    filepaths = bpy.context.preferences.filepaths

    box = column.box().column()
    if hops_prefs():
        try:
            box.operator('hops.powersave', text='PowerSave (hops)')
        except:
            box.operator('powersave.powersave')
    else:
        box.operator('powersave.powersave')
    box.prop(prefs, 'powersave_name', text='')

    column.separator()

    box = column.box().column()
    flow = box.grid_flow(align=True)
    flow.operator('powersave.load_previous', text='', icon='REW')
    flow.operator('powersave.load_next', text='', icon='FF')
    box.operator('powersave.open_project_folder')

    column.separator()

    box = column.box().column()
    box.prop(prefs, 'use_autosave')
    col = box.column()
    col.enabled = prefs.use_autosave
    col.prop(prefs, 'autosave_interval')
    col.prop(prefs, 'autosave_to_copy')
    box.prop(prefs, 'save_on_startup')

    column.separator()

    box = column.box().column()
    icon = 'CHECKBOX_HLT' if bpy.data.use_autopack else 'CHECKBOX_DEHLT'
    box.operator('file.autopack_toggle', text='Toggle Autopack', icon=icon)
    box.operator('powersave.purge_orphans', text='Purge Orphans')

    column.separator()
    box = column.box().column()
    box.prop(filepaths, 'use_auto_save_temporary_files')
    col = box.column()
    col.enabled = filepaths.use_auto_save_temporary_files
    col.prop(filepaths, 'auto_save_time')
    box.prop(filepaths, 'save_version')


def powerlink_draw(self, column):
    wm = bpy.context.window_manager
    if hasattr(wm, 'powerlink'):
        wm.powerlink.draw(self, column)

    else:
        column.separator()
        box = column.box().column()
        box.label(text='Check out PowerLink!')

        url = 'https://gumroad.com/l/powerlink'
        utils.ui.draw_op(box, 'Gumroad', 'wm.url_open', {'url': url})

        url = 'https://blendermarket.com/products/powerlink'
        utils.ui.draw_op(box, 'BlenderMarket', 'wm.url_open', {'url': url})


def hops_prefs():
    wm = bpy.context.window_manager
    if hasattr(wm, 'Hard_Ops_folder_name'):
        return bpy.context.preferences.addons[wm.Hard_Ops_folder_name].preferences
