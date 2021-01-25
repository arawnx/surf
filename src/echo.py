from pylatex import *
from pylatex.utils import *
from pylatex.section import *
import peek
from datetime import date, timedelta

def create_calendar_overdue(dests: dict, doc):
    with doc.create(Subsection("Overdue Calendar Items", numbering=False)):
        overdue_items = [elem for elem in dests["calendar"]
                if elem["datetime"].date() < date.today()]

        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
            for item in overdue_items:
                if "project" in item:
                    itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], italic(f"{item['label']}")]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", italic(f"{item['label']}")]))
                    else:
                        itemize.add_item(item["label"])
                else:
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], italic(f"{item['label']}")]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", italic(f"{item['label']}")]))
                    else:
                        itemize.add_item(item["label"])

def create_calendar_upcoming(dests: dict, doc):
    with doc.create(Subsection("Upcoming Calendar Items", numbering=False)):
        upcoming_items = [elem for elem in dests["calendar"]
                if elem["datetime"].date() > date.today()]

        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
            for item in upcoming_items:
                if "project" in item:
                    itemize.add_item(TextColor("darkgray", f"[{item['project']}] "))
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], italic(f"{item['label']}")]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", italic(f"{item['label']}")]))
                    else:
                        itemize.add_item(item["label"])
                else:
                    if "link" in item:
                        itemize.add_item(Command("href", arguments=[item["link"], italic(f"{item['label']}")]))
                    elif "file" in item:
                        itemize.add_item(Command("href", arguments=[f"run:{item['file']}", italic(f"{item['label']}")]))
                    else:
                        itemize.add_item(item["label"])

def create_next_actions(dests: dict, doc):
    with doc.create(Subsection("Next Actions", numbering=False)):
        contexts = set([elem["context"] for elem in dests["next-actions"] if elem.get("context") != None])
        orphaned_items = [elem for elem in dests["next-actions"] if elem.get("context") == None]
        if len(orphaned_items) > 0:
            with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                for item in orphaned_items:
                    peek.create_next_action_item(item, itemize)

        for context in contexts:
            with doc.create(Subsubsection(context, numbering=False)):
                relevant_items = [elem for elem in dests["next-actions"] if elem.get("context") == context]
                with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                    for item in relevant_items:
                        peek.create_next_action_item(item, itemize)

def create_get_clear(dests: dict, doc):
    with doc.create(Section("Get Clear", numbering=False)):
        with doc.create(Enumerate()) as enum:
            enum.add_item(italic("Collect Loose Papers and Materials"))
            enum.append(Command("qquad"))
            enum.append("Pull out all miscellaneous pieces of paper, business cards, receipts, and so on that have crept into the crevices of your desk, clothing, and accessories. Put it all in your in-tray for processing.")

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Get ``In'' to Empty"))
            enum.append(Command("qquad"))
            enum.append("Review any meeting notes and miscellaneous scribbles on notepaper or in your mobile devices. Decide and list any action items, projects, waiting-fors, calendar events, nd someday/maybes, as appropriate. File any reference notes and materials. Get the ``in'' areas of e-mails, texts, and voice mails to zero. Be ruthless with yourself, processing all notes and thoughts relative to interactions, projects, new initiatives, and input that have come your way since your last download, and purging those not needed.")
            with doc.create(Subsection("Inbox", numbering=False)):
                doc.append(Command("sloppy"))
                with doc.create(Itemize(options=NoEscape(r'label={--}'))) as itemize_sub:
                    for item in dests["inbox"]:
                        itemize_sub.add_item(f"{item['label']}")
                doc.append(Command("fussy"))

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Empty Your Head"))
            enum.append(Command("qquad"))
            enum.append("Put into writing or text (in appropriate categories) and new projects, action items, waiting-fors, someday/maybes, and so forth that you haven't yet captured and clarified.")

def create_projects(dests: dict, doc):
    with doc.create(Subsection("Projects", numbering=False)):
        for project in dests["projects"]:
            with doc.create(Subsubsection(project["label"], numbering=False)):
                if "plan" in project:
                    # Purpose and Principles
                    if len(project["plan"]) > 0:
                        with doc.create(Paragraph("Purpose & Principles", numbering=False)):
                            if isinstance(project["plan"][0], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][0]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][0])
                    # Outcome Vision
                    if len(project["plan"]) > 1:
                        with doc.create(Paragraph("Outcome Vision", numbering=False)):
                            if isinstance(project["plan"][1], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][1]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][1])

                    # Brainstorm
                    if len(project["plan"]) > 2:
                        with doc.create(Paragraph("Brainstorm", numbering=False)):
                            if isinstance(project["plan"][2], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][2]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][2])

                    # Outline
                    if len(project["plan"]) > 3:
                        with doc.create(Paragraph("Outline", numbering=False)):
                            if isinstance(project["plan"][3], list):
                                with doc.create(Itemize()) as itemize:
                                    for item in project["plan"][3]:
                                        itemize.add_item(item)
                            else:
                                doc.append(project["plan"][3])

                # Relevant Items
                relevant_nas = [elem for elem in dests["next-actions"] if elem.get("project") == project["label"]]
                with doc.create(Paragraph("Next Actions", numbering=False)):
                    if len(relevant_nas) > 0:
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            for item in relevant_nas:
                                peek.create_next_action_item(item, itemize, False)
                    else:
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            itemize.add_item("No next actions defined!")

                relevant_refs = [elem for elem in dests["references"] if elem.get("project") == project["label"]]
                if len(relevant_refs) > 0:
                    with doc.create(Paragraph("Reference Items", numbering=False)):
                        with doc.create(Itemize(options=NoEscape(r'label={}'))) as itemize:
                            for item in relevant_refs:
                                peek.create_reference_item(item, itemize, False)

                doc.append(Command("vspace", "10mm"))

def create_horizons(dests: dict, doc):
    doc.append(NewPage())
    with doc.create(Subsection("Purpose & Principles", numbering=False)):
        for item in dests["horizons"]["purpose"]:
            with doc.create(Subsubsection(item["label"], numbering=False)):
                if item.get("description") != None:
                    with doc.create(Paragraph("Description", numbering=False)):
                        if isinstance(item["description"], list):
                            with doc.create(Itemize()) as itemize:
                                for sub_item in item["description"]:
                                    itemize.add_item(sub_item)
                        else:
                            doc.append(item["description"])

                doc.append(Command("vspace", "10mm"))

    doc.append(NewPage())
    with doc.create(Subsection("Vision", numbering=False)):
        for item in dests["horizons"]["vision"]:
            with doc.create(Subsubsection(item["label"], numbering=False)):
                if item.get("description") != None:
                    with doc.create(Paragraph("Description", numbering=False)):
                        if isinstance(item["description"], list):
                            with doc.create(Itemize()) as itemize:
                                for sub_item in item["description"]:
                                    itemize.add_item(sub_item)
                        else:
                            doc.append(item["description"])

                doc.append(Command("vspace", "10mm"))

    doc.append(NewPage())
    with doc.create(Subsection("Goals and Objectives", numbering=False)):
        for item in dests["horizons"]["goals"]:
            with doc.create(Subsubsection(item["label"], numbering=False)):
                if item.get("description") != None:
                    with doc.create(Paragraph("Description", numbering=False)):
                        if isinstance(item["description"], list):
                            with doc.create(Itemize()) as itemize:
                                for sub_item in item["description"]:
                                    itemize.add_item(sub_item)
                        else:
                            doc.append(item["description"])

                doc.append(Command("vspace", "10mm"))

    doc.append(NewPage())
    with doc.create(Subsection("Areas of Focus, Responsibility, and Interest", numbering=False)):
        for item in dests["horizons"]["areas-of-focus"]:
            with doc.create(Subsubsection(item["label"], numbering=False)):
                if item.get("description") != None:
                    with doc.create(Paragraph("Description", numbering=False)):
                        if isinstance(item["description"], list):
                            with doc.create(Itemize()) as itemize:
                                for sub_item in item["description"]:
                                    itemize.add_item(sub_item)
                        else:
                            doc.append(item["description"])

                doc.append(Command("vspace", "10mm"))

def create_get_current(dests: dict, doc):
    with doc.create(Section("Get Current", numbering=False)):
        with doc.create(Enumerate()) as enum:
            enum.add_item(italic("Review ``Next Actions'' Lists"))
            enum.append(Command("qquad"))
            enum.append("Mark off completed actions. Review for reminders of further action steps to record. Many times I've been moving so fast I haven't had a chance to mark off many completed items on my list, much less figure out what to do next. This is the time to do that.")
            create_next_actions(dests, doc)

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Review Previous Calendar Data"))
            enum.append(Command("qquad"))
            enum.append("Review the past two to three weeks of calendar entries in detail for remaining or emergent action items, reference information, and so on, and transfer that data into the active system. Grab every ``Oh! That reminds me ")
            enum.append(Command("ldots"))
            enum.append(" !'' with its associated actions. You will likely notice meetings and events that you attended, which trigger thoughts of what to do next about the content. Be able to archive your past calendar with nothing left uncaptured.")
            create_calendar_overdue(dests, doc)

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Review Upcoming Calendar"))
            enum.append(Command("qquad"))
            enum.append("Look at further calendar entries (long- and short-term). Capture actions about projects and preparations required for upcoming events. Your calendar is one of the best checklists to review regularly, to prevent last-minute stress and trigger creative front-end thinking.")
            enum.append(Command("footnote", options=["1"], arguments=["This is especially true if other people have authority to add entries to your calendar. It's very easy to be uncomfortably surprised with meetings you suddenly notice that were scheduled by someone else!"]))
            enum.append(" Upcoming travel, conferences, meetings, holidays, &c. should be assessed for projects to add to your ``Projects'' and ``Next Actions'' lists for any of those situations that are already on your radar but not yet on cruise control.")
            create_calendar_upcoming(dests, doc)

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Review ``Waiting For'' List"))
            enum.append(Command("qquad"))
            enum.append("Any needed follow-up? Need to send an e-mail to get a status on it? Need to add an item to someone's Agenda list to update when you'll talk with him or her? Record any next actions. Check off any already received.")
            with doc.create(Subsection("Waiting For", numbering=False)):
                doc.append(Command("sloppy"))
                with doc.create(Itemize(options=NoEscape(r'label={--}'))) as itemize_sub:
                    for item in dests["waiting-for"]:
                        itemize_sub.add_item(f"{item['label']}")
                doc.append(Command("fussy"))

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Review ``Projects'' (and ``Larger Outcome'') Lists"))
            enum.append(Command("qquad"))
            enum.append("Evaluate the status of projects, goals, and outcomes, one by one, ensuring that at least one current kick-start action for each is in your system. Browse through any active and relevant project plans, support materials, and any other work-in-progress material to trigger new actions, completions, waiting-fors, etc.")
            create_projects(dests, doc)
            create_horizons(dests, doc)

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Review Any Relevant Checklists"))
            enum.append(Command("qquad"))
            enum.append("Is there anything else that you haven't done, that you need or want to do, given your various engagements, interests, and responsibilities?")

def create_get_creative(dests: dict, doc):
    with doc.create(Section("Get Creative", numbering=False)):
        with doc.create(Enumerate()) as enum:
            enum.add_item(italic("Review ``Someday/Maybe'' List"))
            enum.append(Command("qquad"))
            enum.append("Check for any projects that may have become more interesting or valuable to activate, and transfer them to Projects. Delete any that have simply stayed around much longer than they should, as the world and your interest have changed enough to take them off even this informal radar. Add any emerging possibilities that you've just started thinking about.")
            with doc.create(Subsection("Someday/Maybe", numbering=False)):
                doc.append(Command("sloppy"))
                with doc.create(Itemize(options=NoEscape(r'label={--}'))) as itemize_sub:
                    for item in dests["someday-maybe"]:
                        itemize_sub.add_item(f"{item['label']}")
                doc.append(Command("fussy"))

            enum.append(Command("vspace", "10mm"))
            enum.add_item(italic("Be Creative and Courageous"))
            enum.append(Command("qquad"))
            enum.append("Are there any new, wonderful, hare-brained, creative, thought-provoking, risk-taking ideas you can capture and add into your system, or ``external brain''?")

def echo_pdf(dests: dict, path):
    doc = Document()

    doc.packages.append(Package("enumitem"))
    doc.packages.append(Package("hyperref"))
    doc.packages.append(Package("geometry"))
    doc.packages.append(Package("footmisc", options=["symbol"]))
    doc.preamble.append(Command("hypersetup", "colorlinks=true, linkcolor=blue, filecolor=purple, urlcolor=blue"))
    doc.preamble.append(Command("renewcommand", arguments=[Command("thefootnote")], extra_arguments=[Command("fnsymbol", arguments=["footnote"])]))

    # Get Clear
    create_get_clear(dests, doc)
    doc.append(NewPage())

    # Get Current
    create_get_current(dests, doc)
    doc.append(NewPage())

    # Get Creative
    create_get_creative(dests, doc)

    # Free Writing Space
    doc.append(Command("begin", "center"))
    for i in range(0, 3):
        doc.append(NewPage())
        doc.append(SmallText("Free Writing Space"))
        doc.append(Command("null"))
    doc.append(Command("end", "center"))

    doc.generate_pdf(path, clean_tex=False)
