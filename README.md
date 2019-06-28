# ExcludeFromGitignore

A small utility to exclude files and directories based on .gitignore in Sublime Text projects.

It can be used either as a command-line python tool (just pass the filename of the Sublime Text project),
or if you clone it into your sublime text packages folder it can be used as a command directly from the
command pallette (recommended).

## Dependencies
- Python 3
- `git` installed and available on the path

## FAQs (or, things that people might ask)
- *What is the difference from <https://github.com/apc999/sublime-text-gitignore>?*

  At the time of writing that plugin reads .gitignore file(s) itself, whereas this plugin calls the git program
  to find out which files & directories are excluded.
- *What is the difference from <https://packagecontrol.io/packages/Gitignored%20File%20Excluder>?*

  At the time of writing that plugin runs constantly in the background, whereas this one only runs when you trigger it.
  In addition that plugin does not appear to use the `window.set_project_data()` API that Sublime Text provides.

- *Why is this plugin not on Package Control?*

  Package control describes in their [documentation for submitting a package](https://packagecontrol.io/docs/submitting_a_package)
  that before submitting a package you should check if it's similar to any existing package, and change
  that package instead to avoid confusion. I agree that this is a good idea, and this package is very similar
  in intent and function to the above package(s). However as I wrote it for my use I've not put in the
  effort to integrate changes with the existing plugins, so I'm keeping it separate for now. Accordingly
  I have not published it on Package Control.
