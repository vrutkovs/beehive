# -*- coding: utf-8 -*-
"""
Use beehive4cmd0 step library (predecessor of beehive4cmd).
"""

# -- REGISTER-STEPS:
# import beehive4cmd0.__all_steps__
import beehive4cmd0.command_steps
import beehive4cmd0.passing_steps
import beehive4cmd0.failing_steps
import beehive4cmd0.note_steps

assert beehive4cmd0.note_steps
assert beehive4cmd0.failing_steps
assert beehive4cmd0.passing_steps
assert beehive4cmd0.command_steps
