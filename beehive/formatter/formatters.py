# -*- coding: utf-8 -*-

import sys
from beehive.formatter.base import StreamOpener
from beehive.textutil import compute_words_maxsize
from beehive.importer import LazyDict, LazyObject


# -----------------------------------------------------------------------------
# FORMATTER REGISTRY:
# -----------------------------------------------------------------------------
formatters = LazyDict()


def register_as(formatter_class, name):
    """
    Register formatter class with given name.

    :param formatter_class:  Formatter class to register.
    :param name:  Name for this formatter (as identifier).
    """
    formatters[name] = formatter_class

def register(formatter_class):
    register_as(formatter_class, formatter_class.name)


def list_formatters(stream):
    """
    Writes a list of the available formatters and their description to stream.

    :param stream:  Output stream to use.
    """
    formatter_names = sorted(formatters)
    column_size = compute_words_maxsize(formatter_names)
    schema = u"  %-"+ str(column_size) +"s  %s\n"
    for name in formatter_names:
        stream.write(schema % (name, formatters[name].description))


def get_formatter(config, stream_openers):
    # -- BUILD: Formatter list
    default_stream_opener = StreamOpener(stream=sys.stdout)
    formatter_list = []
    for i, name in enumerate(config.format):
        stream_opener = default_stream_opener
        if i < len(stream_openers):
            stream_opener = stream_openers[i]
        formatter_list.append(formatters[name](stream_opener, config))
    return formatter_list


# -----------------------------------------------------------------------------
# SETUP:
# -----------------------------------------------------------------------------
def setup_formatters():
    # -- NOTE: Use lazy imports for formatters (to speed up start-up time).
    _L = LazyObject
    register_as(_L("beehive.formatter.plain:PlainFormatter"), "plain")
    register_as(_L("beehive.formatter.pretty:PrettyFormatter"), "pretty")
    register_as(_L("beehive.formatter.json:JSONFormatter"), "json")
    register_as(_L("beehive.formatter.json:PrettyJSONFormatter"), "json.pretty")
    register_as(_L("beehive.formatter.null:NullFormatter"), "null")
    register_as(_L("beehive.formatter.progress:ScenarioProgressFormatter"),
                "progress")
    register_as(_L("beehive.formatter.progress:StepProgressFormatter"),
                "progress2")
    register_as(_L("beehive.formatter.progress:ScenarioStepProgressFormatter"),
                "progress3")
    register_as(_L("beehive.formatter.rerun:RerunFormatter"), "rerun")
    register_as(_L("beehive.formatter.tags:TagsFormatter"), "tags")
    register_as(_L("beehive.formatter.tags:TagsLocationFormatter"),
                "tags.location")
    register_as(_L("beehive.formatter.steps:StepsFormatter"), "steps")
    register_as(_L("beehive.formatter.steps:StepsDocFormatter"), "steps.doc")
    register_as(_L("beehive.formatter.steps:StepsUsageFormatter"), "steps.usage")
    register_as(_L("beehive.formatter.sphinx_steps:SphinxStepsFormatter"),
                "sphinx.steps")
    register_as(_L("beehive.formatter.html:HTMLFormatter"), "html")


# -----------------------------------------------------------------------------
# MODULE-INIT:
# -----------------------------------------------------------------------------
setup_formatters()
