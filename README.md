# Surfeit

## What is Surfeit?
Surfeit is a set of utilities, an expanded todo list, and a GTD environment for Linux, written in Python. Initially, this was just a set of utilities I wrote for myself, but now I'm expanding it into a more generalizable set of utilities.

## Installation
Since Python isn't a compiled language, and Surfeit isn't on PyPI quite yet, installation requires:
1. Installing dependencies; this project manages dependencies with `pipenv`, so you should run `pip install --user pipenv && pipenv install --system`.
2. Moving `surf/` to a stable location, e.g.: `mv -p ./surf/ ~/.local/bin/surf`
3. Creating a bash/zsh/sh alias to run it, e.g.: `echo 'alias surf="python3 ~/.local/bin/surf/src/main.py"' >> ~/.config/zsh/.zshrc`, or wherever your shell rcfile is
4. Sourcing and running this aliased command, e.g.: `source ~/.config/zsh/.zshrc && surf --help`

## Usage

### Subcommands
Currently, Surfeit has two subcommands: `edit` and `peek`. Two more are currently planned, `echo` (a weekly review LaTeX-generating subcommand) and `seek` (an interactive TUI interface).

`edit` opens a set of vim/nvim buffers with access to all of the underlying YAML files that hold your program's local data; that is, your GTD destinations (inbox, trash, next actions, &c.). Currently, I find I prefer using vim directly, however I do plan on creating a TUI interface at some point to bypass this.

`peek` interprets these YAML files into a LaTeX document that shows a sufficient overview of the most important destinations and items for the day/week &c. It is very similar to the Current View of David Allen's own [Ultimate GTD App](https://www.dropbox.com/s/d9sdbghzooy4rpy/DA_software.pdf?dl=1). It shows unprocessed inbox items, projects without next actions, tickler items due today, next actions, your calendar, projects, &c.

### `edit` Formatting
`edit` opens a set of vim/nvim buffers holding your destination files (specified in YAML 1.1). Surfeit creates these in `$XDG_DATA_HOME`, which *should* be specified. If your system doesn't have XDG directories set (this is **EXCEPTIONALLY** rare), either fork and modify the source code or else temporarily set it with `export XDG_DATA_HOME=/your/preferred/dir/`. The different files represent different destinations. [For a (semi-)complete list of GTD destinations, see the outer components on this diagram.](https://archive.is/TjVdW) Note that in Surfeit, there is no trash destination. All of these destinations have different item specifications. For example, an inbox destination might look like this:
```
---
inbox:
  - Get the milk
  - Funny idea I had
  - ...
```
... whereas a next actions destination could look more like this:
```
---
na:
  - label: "Example Next Action Item"
    time: 20m
    project: "Example Project"
  - label: "Skinny item" # Contains no attributes other than its label
```
For a full specification of YAML 1.1, [see here](https://yaml.org/spec/1.1/). A decent grasp of the formatting is expected (luckily it's very very easy and readable). Since some attributes are optional, there are both maximal and minimal variants of each item; maximal variants contain specify possible attribute, minimal variants specify only those attributes *required* for interpretation, anything less would cause a runtime error. Following, there is provided a list of the maximal (all attributes covered) and minimal (only necessary attributes covered) specifications of each variety of item:

#### Inbox Item
Just a string. The maximal and minimal variants are both:
```
---
inbox:
  - Item
```

#### Someday/Maybe Item
Just a string. The maximal and minimal variants are both:
```
---
incubate:
  - Item
```

#### Waiting For Item
Just a string. The maximal and minimal variants are both:
```
---
incubate:
  - Item
```

#### Next Action Item
Minimal variant:
```
---
na:
  - label: "Item"
```
Maximal variant:
```
---
na:
  - label: "Item"
    time: 20m
    energy: low
    priority: !!!
    file: "~/image.png"
    link: "https://www.google.com"
    project: "Attached Project"
```
Note: Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Tickler Item
Minimal variant:
```
---
tickler:
  - label: "Item"
    date: 2021-01-01
```
Maximal variant:
```
---
tickler:
  - label: "Item"
    date: 2021-01-01
    link: "https://www.google.com"
    file: "~/image.png"
```
Note: Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Reference Item
Minimal variant:
```
---
references:
  - label: "Item"
```
Maximal variant:
```
---
references:
  - label: "Item"
    link: "https://www.google.com"
    file: "~/image.png"
    project: "Attached Project"
```

#### Calendar Item
Minimal variant:
```
---
calendar:
  - label: "Item"
    date: 2021-01-01
```
Maximal variant:
```
---
calendar:
  - label: "Item"
    date: 2021-01-01
    time: "13:30"
    link: "https://www.google.com"
    file: "~/image.png"
    project: "Attached project"
```
Note: Times *must* be specified in HH:MM format; seconds may not be specified and AM/PM may not be specified. Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Project Item
The minimal and maximum variant are both:
```
---
projects:
  - label: "Item"
    plan:
      - "Why I want to do this..." # Purpose & principles
      - "How it'll look..." # Outcome vision
      - "Some scatterbrained ideas I had..." # Brainstorm
      - "The steps we have to take..." # Organized
```
