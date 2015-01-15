# -*- coding: utf-8 -*-


# -----------------------------------------------------------------------------
# HOOKS:
# -----------------------------------------------------------------------------
def before_all(context):
    #setup_context_with_global_params_test(context)
    print("before_all")

def after_all(context):
    print("after_all")

def before_feature(context, feature):
    print("before_feature")

def after_feature(context, feature):
    print("after_feature")

def before_scenario(context, scenario):
    print("before_scenario")

def after_scenario(context, scenario):
    print("after_scenario")

def before_step(context, step):
    print("before_step")

def after_step(context, step):
    print("after_step")

# -----------------------------------------------------------------------------
# SPECIFIC FUNCTIONALITY:
# -----------------------------------------------------------------------------
def setup_context_with_global_params_test(context):
    context.global_name = "env:Alice"
    context.global_age = 12
