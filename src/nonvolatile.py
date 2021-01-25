from pathlib import *
from xdg import xdg_data_home
import datetime
import yaml
import os

import validators

from item import *

def file_sanity_check(path: PurePath) -> bool:
    if not path.exists():
        return False
    if not path.is_file():
        return False
    return True

def dir_sanity_check(path: PurePath) -> bool:
    if not path.exists():
        return False
    if not path.is_dir():
        return False
    return True

def load_all_destination_dirs() -> list:
    dh_dir = xdg_data_home().joinpath("surfeit/")
    if not dir_sanity_check(dh_dir):
        dh_dir.mkdir()
    dest_dirs = list(map(dh_dir.joinpath, ["inbox", "next-actions", "calendar", "waiting-for", "tickler", "projects", "someday-maybe", "reference", "horizons"]))
    for path in dest_dirs:
        if not file_sanity_check(path):
            f = open(path, "w")
            f.write(f"# Newly created on {str(date.today())}")
            f.close()

    return dest_dirs

# Returns tuples matching file names (destination names) to the contents within
def read_all_from_dirs(dirs: list) -> list:
    files = list(map(open, dirs))
    defer = [(os.path.basename(elem.name), elem.read()) for elem in files]
    for fl in files:
        fl.close()
    return defer

def parse_all_from_strs(strsraw: list) -> list:
    return [(elem[0], yaml.load(elem[1], Loader=yaml.Loader)) for elem in strsraw]

def interp_simple(dictls) -> list:
    attrs = []
    for elem in dictls:
        if isinstance(elem, str):
            attrs.append({'label': elem})
        else:
            raise TypeError("Every inbox/waiting-for/someday-maybe item must be simply a string!")

    items = [Item(elem) for elem in attrs]
    return items

def interp_next_actions(dictls) -> list:
    attrs = []
    for elem in dictls:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every next action item must contain a 'label' attribute!")

        if "time" in elem:
            tmp["time"] = elem["time"]

        if "context" in elem:
            tmp["context"] = elem["context"]

        if "energy" in elem:
            tmp["energy"] = elem["energy"]

        if "priority" in elem:
            tmp["priority"] = elem["priority"]

        if "project" in elem:
            tmp["project"] = elem["project"]

        if "link" in elem:
            if validators.url(elem["link"]):
                tmp["link"] = elem["link"]
            else:
                raise TypeError(f"{elem['link']} is not a properly formatted URL!")
        elif "file" in elem:
            p = Path(elem["file"]).expanduser().resolve()
            tmp["file"] = p

        attrs.append(tmp)

    items = [Item(elem) for elem in attrs]
    return items

def interp_calendar(dictls) -> list:
    attrs = []
    for elem in dictls:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every calendar item must contain a 'label' attribute!")

        if "date" in elem:
            # PyYAML automagically understands that 2000-01-01 is a date object
            if isinstance(elem["date"], datetime.date):
                raw_date = elem["date"]
            else:
                raise TypeError("'date' attributes must be written in %Y-%m-%d format!")
            if "time" in elem:
                hour, minute = list(map(int, elem["time"].split(':')))
                tmp["datetime"] = datetime.datetime(raw_date.year, raw_date.month, raw_date.day, hour, minute)
            else:
                tmp["datetime"] = datetime.datetime(raw_date.year, raw_date.month, raw_date.day)
        else:
            raise KeyError("Every calendar item must contain a 'date' attribute!")

        if "link" in elem:
            if validators.url(elem["link"]):
                tmp["link"] = elem["link"]
            else:
                raise TypeError(f"{elem['link']} is not a properly formatted URL!")
        elif "file" in elem:
            p = Path(elem["file"]).expanduser().resolve()
            tmp["file"] = p

        if "project" in elem:
            tmp["project"] = elem["project"]

        attrs.append(tmp)

    items = [Item(elem) for elem in attrs]
    return items

def interp_tickler(dictls) -> list:
    attrs = []
    for elem in dictls:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every tickler item must contain a 'label' attribute!")

        if "date" in elem:
            if isinstance(elem["date"], datetime.date):
                tmp["date"] = elem["date"]
            else:
                raise TypeError("'date' attributes must be written in %Y-%m-%d format!")
        else:
            raise KeyError("Every tickler item must contain a 'date' attribute!")

        if "link" in elem:
            if validators.url(elem["link"]):
                tmp["link"] = elem["link"]
            else:
                raise TypeError(f"{elem['link']} is not a properly formatted URL!")
        elif "file" in elem:
            p = Path(elem["file"]).expanduser().resolve()
            tmp["file"] = p

    items = [Item(elem) for elem in attrs]
    return items

def interp_projects(dictls) -> list:
    attrs = []
    for elem in dictls:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every tickler item must contain a 'label' attribute!")

        if "plan" in elem:
            plan = tuple(elem["plan"])
            if len(plan) > 4:
                raise TypeError("Project plans must contain four or fewer items!")
            else:
                tmp["plan"] = plan

        attrs.append(tmp)

    items = [Item(elem) for elem in attrs]
    return items

def interp_references(dictls) -> list:
    attrs = []
    for elem in dictls:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every reference item must contain a 'label' attribute!")

        if "link" in elem:
            if validators.url(elem["link"]):
                tmp["link"] = elem["link"]
            else:
                raise TypeError(f"{elem['link']} is not a properly formatted URL!")
        elif "file" in elem:
            p = Path(elem["file"]).expanduser().resolve()
            tmp["file"] = p

        if "project" in elem:
            tmp["project"] = elem["project"]

        attrs.append(tmp)

    items = [Item(elem) for elem in attrs]
    return items

def interp_horizons(dictls) -> list:
    purpose = []
    for elem in dictls["Purpose and Principles"]:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every horizon item must contain a 'label' attribute!")

        if "description" in elem:
            tmp["description"] = elem["description"]

        purpose.append(tmp)

    vision = []
    for elem in dictls["Vision"]:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every horizon item must contain a 'label' attribute!")

        if "description" in elem:
            tmp["description"] = elem["description"]

        vision.append(tmp)

    goals = []
    for elem in dictls["Goals and Objectives"]:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every horizon item must contain a 'label' attribute!")

        if "description" in elem:
            tmp["description"] = elem["description"]

        goals.append(tmp)

    aof = []
    for elem in dictls["Areas of Focus, Responsibility, and Interest"]:
        tmp = {}
        if "label" in elem:
            tmp["label"] = elem["label"]
        else:
            raise KeyError("Every horizon item must contain a 'label' attribute!")

        if "description" in elem:
            tmp["description"] = elem["description"]

        aof.append(tmp)

    return {
        "purpose": purpose,
        "vision": vision,
        "goals": goals,
        "areas-of-focus": aof
    }

def get_all_dests() -> list:
    dest_dirs = load_all_destination_dirs()
    parsed = parse_all_from_strs(read_all_from_dirs(dest_dirs))
    inbox, next_actions, calendar, waiting_for, tickler, projects, someday_maybe, reference, horizons = [elem[1] for elem in parsed]

    inbox_items = interp_simple(inbox)
    next_action_items = interp_next_actions(next_actions)
    calendar_items = interp_calendar(calendar)
    waiting_for_items = interp_simple(waiting_for)
    tickler_items = interp_tickler(tickler)
    projects_items = interp_projects(projects)
    someday_maybe_items = interp_simple(someday_maybe)
    reference_items = interp_references(reference)
    horizon_items = interp_horizons(horizons)

    return {
        'inbox': inbox_items,
        'next-actions': next_action_items,
        'calendar': calendar_items,
        'waiting-for': waiting_for_items,
        'tickler': tickler_items,
        'projects': projects_items,
        'someday-maybe': someday_maybe_items,
        'references': reference_items,
        'horizons': horizon_items
    }
