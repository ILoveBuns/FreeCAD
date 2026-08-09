# SPDX-License-Identifier: LGPL-2.1-or-later

# ***************************************************************************
# *   Copyright (c) 2026 FreeCAD Project Association                        *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This file is free software; you can redistribute it and/or modify it  *
# *   under the terms of the GNU Lesser General Public License (LGPL)       *
# *   as published by the Free Software Foundation; either version 2.1 of  *
# *   the License, or (at your option) any later version.                   *
# *                                                                         *
# ***************************************************************************

"""Unit tests for the Draft Clone GUI command."""

from types import SimpleNamespace
import unittest
from unittest import mock

from draftguitools import gui_clone


class DraftCloneGui(unittest.TestCase):
    """Tests for the Clone GUI command."""

    def test_created_clone_is_autogrouped(self):
        """The Clone command should autogroup each created object."""
        source = SimpleNamespace(Name="Body", Shape=object())
        clone = SimpleNamespace(Name="Clone")
        document = mock.Mock(Objects=[source, clone])
        command = gui_clone.Clone()

        with (
            mock.patch.object(gui_clone.App, "ActiveDocument", document),
            mock.patch.object(gui_clone.Gui, "addModule"),
            mock.patch.object(gui_clone.Gui, "doCommand") as do_command,
            mock.patch.object(
                gui_clone.Gui.Selection,
                "getSelection",
                return_value=[source],
            ),
            mock.patch.object(gui_clone.Gui.Selection, "clearSelection"),
            mock.patch.object(gui_clone.Gui.Selection, "addSelection"),
            mock.patch.object(command, "finish"),
        ):
            command.proceed()

        self.assertEqual(
            do_command.call_args_list,
            [
                mock.call("clone0 = Draft.make_clone(FreeCAD.ActiveDocument.Body)"),
                mock.call("Draft.autogroup(clone0)"),
            ],
        )
