#!/usr/bin/env python3

import sys
import gi
from gi.repository import GObject

gi.require_version("Gimp", "3.0")
from gi.repository import Gimp, Gio, GLib

import subprocess
import tempfile
import os

# Path to the rembg binary. Adjust this if rembg is not in your PATH or if you want to use a specific version.
REMBG_BINARY = "/home/erick/.local/bin/rembg"

class RembgPlugin(Gimp.PlugIn):

    def do_query_procedures(self):
        return ["python-fu-rembg"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name,
            Gimp.PDBProcType.PLUGIN,
            self.run, None
        )

        procedure.set_image_types("*")
        procedure.set_menu_label("Remove Background (REMBG)")
        procedure.add_menu_path("<Image>/Filters/AI")

        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        if not drawables:
            return procedure.new_return_values(
                Gimp.PDBStatusType.CALLING_ERROR,
                GLib.Error(message="No drawable was provided.")
            )

        drawable = drawables[0]

        tmp_input = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_output = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp_input.close()
        tmp_output.close()

        try:
            Gimp.progress_init("Remove Background with REMBG...")
            Gimp.progress_update(0.1)

            export_image = Gimp.Image.new_with_precision(
                image.get_width(),
                image.get_height(),
                image.get_base_type(),
                image.get_precision()
            )

            copied_layer = Gimp.Layer.new_from_drawable(drawable, export_image)
            export_image.insert_layer(copied_layer, None, 0)

            _, offset_x, offset_y = drawable.get_offsets()
            copied_layer.set_offsets(offset_x, offset_y)

            Gimp.progress_update(0.3)

            export_proc = Gimp.get_pdb().lookup_procedure("file-png-export")
            export_config = export_proc.create_config()

            export_config.set_property("run-mode", Gimp.RunMode.NONINTERACTIVE)
            export_config.set_property("image", export_image)
            export_config.set_property("file", Gio.File.new_for_path(tmp_input.name))

            export_result = export_proc.run(export_config)
            if export_result.index(0) != Gimp.PDBStatusType.SUCCESS:
                export_image.delete()
                Gimp.progress_end()
                return procedure.new_return_values(
                    export_result.index(0),
                    GLib.Error(message="Failed to export the temporary PNG image.")
                )

            export_image.delete()

            Gimp.progress_update(0.5)

            completed = subprocess.run(
                [REMBG_BINARY, "i", tmp_input.name, tmp_output.name],
                check=False,
                capture_output=True,
                text=True
            )
            if completed.returncode != 0:
                message = completed.stderr.strip() or completed.stdout.strip() or "rembg failed."
                Gimp.progress_end()
                return procedure.new_return_values(
                    Gimp.PDBStatusType.EXECUTION_ERROR,
                    GLib.Error(message=message)
                )

            Gimp.progress_update(0.8)

            load_proc = Gimp.get_pdb().lookup_procedure("gimp-file-load-layer")
            load_config = load_proc.create_config()

            load_config.set_property("run-mode", Gimp.RunMode.NONINTERACTIVE)
            load_config.set_property("image", image)
            load_config.set_property("file", Gio.File.new_for_path(tmp_output.name))

            result = load_proc.run(load_config)
            if result.index(0) != Gimp.PDBStatusType.SUCCESS:
                Gimp.progress_end()
                return procedure.new_return_values(
                    result.index(0),
                    GLib.Error(message="Failed to load the processed layer.")
                )

            new_layer = result.index(1)
            image.insert_layer(new_layer, None, 0)

            Gimp.progress_update(1.0)
            Gimp.progress_end()

            return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, None)
        finally:
            for path in (tmp_input.name, tmp_output.name):
                if os.path.exists(path):
                    os.unlink(path)

Gimp.main(RembgPlugin.__gtype__, sys.argv)
