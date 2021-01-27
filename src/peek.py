from pylatex import *
from pylatex.utils import *
from datetime import date, timedelta

def projs_sans_next_actions(proj_dest: list, na_dest: list) -> list:
    defer = []

    proj_names = [proj["label"] for proj in proj_dest]
    na_projs = []
    for item in na_dest:
        if "project" in item:
            na_projs.append(item["project"])

    for proj in proj_names:
        if not proj in na_projs:
            defer.append(proj)

    return defer

def create_outstanding(dests: dict, doc):
    with doc.create(Section("Outstanding...", numbering=False)):
        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
            # Unprocessed inbox items
            itemize.add_item(TextColor("red", f"{len(dests['inbox'])} Unprocessed inbox items"))
            if len(dests["inbox"]) > 0:
                itemize.append(TextColor("red", ":"))
                doc.append(Command("sloppy"))
                with doc.create(Itemize()) as itemize_sub:
                    for item in dests["inbox"]:
                        itemize_sub.add_item(f"{item['label']}")
                doc.append(Command("fussy"))

            # Projects without next actions
            psna = projs_sans_next_actions(dests["projects"], dests["next-actions"])
            itemize.add_item(TextColor("red", f"{len(psna)} Projects without next actions"))
            if len(psna) > 0:
                itemize.append(TextColor("red", ":"))
                with doc.create(Itemize()) as itemize_sub:
                    for proj in psna:
                        itemize_sub.add_item(f"{proj}")

            # Past calendar items
            past_calendar = list(filter(lambda item: item["datetime"].date() < date.today(), dests["calendar"]))
            itemize.add_item(TextColor("red", f"{len(past_calendar)} Past calendar items"))
            if len(past_calendar) > 0:
                itemize.append(TextColor("red", ":"))
                with doc.create(Itemize()) as itemize_sub:
                    for item in past_calendar:
                        itemize_sub.add_item(f"{item['label']}")

            # Tickler items today
            tickler_today = list(filter(lambda item: item["date"] == date.today(), dests["tickler"]))
            itemize.add_item(TextColor("red", f"{len(tickler_today)} Tickler items due today"))
            if len(tickler_today) > 0:
                itemize.append(TextColor("red", ":"))
                with doc.create(Itemize()) as itemize_sub:
                    for item in tickler_today:
                        itemize_sub.add_item(f"{item['label']}")

def create_next_action_item(item, parent_list, include_project=True):
    if "project" in item and include_project:
        parent_list.add_item(TextColor("darkgray", f"[{item['project']}] "))
        if "link" in item:
            parent_list.append(Command("href", arguments=[item["link"], italic(item["label"])]))
        elif "file" in item:
            parent_list.append(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
        else:
            parent_list.append(item["label"])
    else:
        if "link" in item:
            parent_list.add_item(Command("href", arguments=[item["link"], italic(item["label"])]))
        elif "file" in item:
            parent_list.add_item(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
        else:
            parent_list.add_item(item["label"])

    if "priority" in item:
        parent_list.append(Command("quad"))
        parent_list.append(TextColor("red", utils.italic(item["priority"])))

    if "time" in item:
        parent_list.append(Command("quad"))
        parent_list.append(SmallText(TextColor("magenta", item["time"])))

    if "energy" in item:
        parent_list.append(Command("quad"))
        parent_list.append(SmallText(TextColor("orange", item["energy"])))

def create_reference_item(item, parent_list, include_project=True):
    if "project" in item and include_project:
        parent_list.add_item(TextColor("darkgray", f"[{item['project']}] "))
        if "link" in item:
            parent_list.append(Command("href", arguments=[item["link"], italic(item["label"])]))
        elif "file" in item:
            parent_list.append(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
        else:
            parent_list.append(item["label"])
    else:
        if "link" in item:
            parent_list.add_item(Command("href", arguments=[item["link"], italic(item["label"])]))
        elif "file" in item:
            parent_list.add_item(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
        else:
            parent_list.add_item(item["label"])

def create_next_actions(dests: dict, doc):
    with doc.create(Section("Next Actions", numbering=False)):
        contexts = set([elem["context"] for elem in dests["next-actions"] if elem.get("context") != None])
        orphaned_items = [elem for elem in dests["next-actions"] if elem.get("context") == None]
        if len(orphaned_items) > 0:
            with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                for item in orphaned_items:
                    create_next_action_item(item, itemize)

        for context in contexts:
            with doc.create(Subsection(context, numbering=False)):
                relevant_items = [elem for elem in dests["next-actions"] if elem.get("context") == context]
                with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                    for item in relevant_items:
                        create_next_action_item(item, itemize)

def create_calendar(dests: dict, doc):
    with doc.create(Section("Calendar", numbering=False)):
        overdue_items = [elem for elem in dests["calendar"]
                if elem["datetime"].date() < date.today()]
        today_items = [elem for elem in dests["calendar"]
                if elem["datetime"].date() == date.today()]
        future_items = [elem for elem in dests["calendar"]
                if timedelta(days=0) < elem["datetime"].date() - date.today() < timedelta(days=90)]

        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
            for item in overdue_items:
                if "project" in item:
                    itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                    if "link" in item:
                        itemize.append(Command("href", arguments=[item["link"], TextColor("red", italic(f"{item['label']} [URL link]"))]))
                    elif "file" in item:
                        itemize.append(Command("href", arguments=[f"run:{item['file']}", TextColor("red", italic(f"{item['label']} [file link]"))]))
                    else:
                        itemize.append(TextColor("red", item["label"]))
                else:
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], TextColor("red", italic(f"{item['label']} [URL link]"))]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", TextColor("red", italic(f"{item['label']} [file link]"))]))
                    else:
                        itemize.add_item(TextColor("red", item["label"]))

            for item in today_items:
                if "project" in item:
                    itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                    if "link" in item:
                        itemize.append(Command("href", arguments=[item["link"], TextColor("green", italic(f"{item['label']} [URL link]"))]))
                    elif "file" in item:
                        itemize.append(Command("href", arguments=[f"run:{item['file']}", TextColor("green", italic(f"{item['label']} [file link]"))]))
                    else:
                        itemize.append(TextColor("green", item["label"]))
                else:
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], TextColor("green", italic(f"{item['label']} [URL link]"))]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", TextColor("green", italic(f"{item['label']} [file link]"))]))
                    else:
                        itemize.add_item(TextColor("green", item["label"]))

            for item in future_items:
                if "project" in item:
                    itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                    if "link" in item:
                        itemize.append(Command("href", arguments=[item["link"], italic(item["label"])]))
                    elif "file" in item:
                        itemize.append(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
                    else:
                        itemize.append(item["label"])
                else:
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], italic(item["label"])]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", italic(item["label"])]))
                    else:
                        itemize.add_item(item["label"])

def create_projects(dests: dict, doc):
    with doc.create(Section("Projects", numbering=False)):
        for project in dests["projects"]:
            with doc.create(Subsection(project["label"], numbering=False)):
                if "plan" in project:
                    # Purpose and Principles
                    if len(project["plan"]) > 0:
                        with doc.create(Subsubsection("Purpose & Principles", numbering=False)):
                            if isinstance(project["plan"][0], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][0]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][0])
                    # Outcome Vision
                    if len(project["plan"]) > 1:
                        with doc.create(Subsubsection("Outcome Vision", numbering=False)):
                            if isinstance(project["plan"][1], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][1]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][1])

                    # Brainstorm
                    if len(project["plan"]) > 2:
                        with doc.create(Subsubsection("Brainstorm", numbering=False)):
                            if isinstance(project["plan"][2], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][2]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][2])

                    # Outline
                    if len(project["plan"]) > 3:
                        with doc.create(Subsubsection("Outline", numbering=False)):
                            if isinstance(project["plan"][3], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][3]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][3])

                # Relevant Items
                relevant_nas = [elem for elem in dests["next-actions"] if elem.get("project") == project["label"]]
                with doc.create(Subsubsection(f"Next Actions", numbering=False)):
                    if len(relevant_nas) > 0:
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            for item in relevant_nas:
                                create_next_action_item(item, itemize, False)
                    else:
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            itemize.add_item("No next actions defined!")

                relevant_refs = [elem for elem in dests["references"] if elem.get("project") == project["label"]]
                if len(relevant_refs) > 0:
                    with doc.create(Subsubsection("Reference Items", numbering=False)):
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            for item in relevant_refs:
                                create_reference_item(item, itemize, False)

                doc.append(Command("vspace", "10mm"))

def peek_pdf(dests: dict, path):
    doc = Document()

    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("hyperref"))
    doc.preamble.append(Command("hypersetup", "colorlinks=true, linkcolor=blue, filecolor=purple, urlcolor=blue"))

    # Outstanding...
    create_outstanding(dests, doc)

    # Next Actions
    create_next_actions(dests, doc)

    # Calendar
    doc.append(NewPage())
    create_calendar(dests, doc)

    # Projects
    doc.append(NewPage())
    create_projects(dests, doc)

    doc.generate_pdf(path, clean_tex=False)
