from pylatex import *
from datetime import date

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

def peek_pdf(dests: dict):
    doc = Document()

    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("hyperref"))
    doc.preamble.append(Command("hypersetup", "colorlinks=true, linkcolor=blue, filecolor=magenta, urlcolor=blue"))

    # Outstanding...
    with doc.create(Section("Outstanding...", numbering=False)):
        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
            # Unprocessed inbox items
            itemize.add_item(TextColor("red", f"{len(dests['inbox'])} Unprocessed inbox items"))
            if len(dests["inbox"]) > 0:
                itemize.append(TextColor("red", ":"))
                with doc.create(Itemize()) as itemize_sub:
                    for item in dests["inbox"]:
                        itemize_sub.add_item(f"{item['label']}")

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

    # Next Actions
    with doc.create(Section("Next Actions", numbering=False)):
        contexts = set([elem["context"] for elem in dests["next-actions"] if elem.get("context") != None])
        orphaned_items = [elem for elem in dests["next-actions"] if elem.get("context") == None]
        if len(orphaned_items) > 0:
            with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                for item in orphaned_items:
                    if "project" in item:
                        itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                        if "link" in item:
                            itemize.append(Command("href", arguments=[item["link"], item["label"]]))
                        elif "file" in item:
                            itemize.append(Command("href", arguments=[f"run:{item['file']}", item["label"]]))
                        else:
                            itemize.append(item["label"])
                    else:
                        if "link" in item:
                            itemize.add_item(Command("href", arguments=[item["link"], item["label"]]))
                        elif "file" in item:
                            itemize.add_item(Command("href", arguments=[f"run:{item['file']}", item["label"]]))
                        else:
                            itemize.add_item(item["label"])

                    if "priority" in item:
                        itemize.append(Command("quad"))
                        itemize.append(TextColor("red", utils.italic(item["priority"])))

                    if "time" in item:
                        itemize.append(Command("quad"))
                        itemize.append(SmallText(TextColor("magenta", item["time"])))

                    if "energy" in item:
                        itemize.append(Command("quad"))
                        itemize.append(SmallText(TextColor("orange", item["energy"])))

        for context in contexts:
            with doc.create(Subsection(context, numbering=False)):
                relevant_items = [elem for elem in dests["next-actions"] if elem.get("context") == context]
                with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                    for item in relevant_items:
                        if "project" in item:
                            itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                            if "link" in item:
                                itemize.append(Command("href", arguments=[item["link"], item["label"]]))
                            elif "file" in item:
                                itemize.append(Command("href", arguments=[f"run:{item['file']}", item["label"]]))
                            else:
                                itemize.append(item["label"])
                        else:
                            if "link" in item:
                                itemize.add_item(Command("href", arguments=[item["link"], item["label"]]))
                            elif "file" in item:
                                itemize.add_item(Command("href", arguments=[f"run:{item['file']}", item["label"]]))
                            else:
                                itemize.add_item(item["label"])

                        if "priority" in item:
                            itemize.append(Command("quad"))
                            itemize.append(TextColor("red", utils.italic(item["priority"])))

                        if "time" in item:
                            itemize.append(Command("quad"))
                            itemize.append(SmallText(TextColor("magenta", item["time"])))

                        if "energy" in item:
                            itemize.append(Command("quad"))
                            itemize.append(SmallText(TextColor("orange", item["energy"])))

    doc.generate_pdf('lists', clean_tex=False)
