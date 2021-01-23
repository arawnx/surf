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
- Funny idea I had
- ...
```
... whereas a next actions destination could look more like this:
```
- label: "Example Next Action Item"
  time: 20m
  project: "Example Project"
- label: "Skinny item" # Contains no attributes other than its label
```
For a full specification of YAML 1.1, [see here](https://yaml.org/spec/1.1/). A decent grasp of the formatting is expected (luckily it's very very easy and readable). Since some attributes are optional, certain fields will be marked optional with a comment (comments in YAML begin with a `#` sign). Following, there is a list of the schemas for the destination files in YAML:

#### Inbox Item
Just a string:
```
- Item
```

#### Someday/Maybe Item
Just a string:
```
- Item
```

#### Waiting For Item
Just a string:
```
- Item
```

#### Next Action Item
```
- label: "Item"
  context: @FRED # Optional
  time: 20m # Optional
  energy: low # Optional
  priority: !!! # Optional
  file: "~/image.png" # Optional
  link: "https://www.google.com" # Optional
  project: "Attached Project" # Optional
```
Note: Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Tickler Item
```
- label: "Item"
  date: 2021-01-01
  link: "https://www.google.com" # Optional
  file: "~/image.png" # Optional
```
Note: Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Reference Item
```
- label: "Item"
  link: "https://www.google.com" # Optional
  file: "~/image.png" # Optional
  project: "Attached Project" # Optional
```
Note: Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Calendar Item
```
- label: "Item"
  date: 2021-01-01
  time: "13:30" # Optional
  link: "https://www.google.com" # Optional
  file: "~/image.png" # Optional
  project: "Attached project" # Optional
```
Note: Times *must* be specified in HH:MM format; seconds may not be specified and AM/PM may not be specified. Both `link` and `file` specify the LaTeX hyperlink to attach, with the former marking a URL and the latter marking a local path. Therefore, both may not be specified in the same item.

#### Project Item
```
- label: "Item"
  plan: # Optional
    - "Why I want to do this..." # Purpose & principles, optional
    - "How it'll look..." # Outcome vision, optional
    - "Some scatterbrained ideas I had..." # Brainstorm, optional
    - "The steps we have to take..." # Organized, optional
```
Note: The `plan` fields must be in order. If you want to specify an outcome vision without purpose and principles (why would you do this?), simply mark purpose and principles null with a `~` sign.

#### Horizons of Focus
These are formatted uniquely. There are a fixed set of five horizons of focus, corresponding to [those in GTD, excluding the projects, which have their own file.](https://gettingthingsdone.com/2011/01/the-6-horizons-of-focus/) Therefore, the file should be formatted as follows:
```
"Purpose and Principles":
    - label: "Christ"
      description: "Some stuff I have..." # Optional
"Vision": # 3-5 years
    - label: "Learn German"
      description: "Some stuff I have..." # Optional
"Goals and Objectives": # 1-2 years
    - label: "Start a company"
      description: "Some stuff I have..." # Optional
"Areas of Focus, Responsibility, and Interest":
    - label: "Job"
      description: "Some stuff I have..." # Optional
    - label: "Family"
      description: # Optional
          - "List"
          - "Another Item..."
```
... dictionary (file) holding a series of lists (horizons) of dictionaries (items). `description`s can be either lists or strings
