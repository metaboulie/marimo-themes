# new commands

- [ ] motheme preview

    Show a preview or description of a theme before applying it

- [ ] motheme validate

    Validate a theme file structure

- [ ] motheme random: A random command to apply a random theme

    - user can input a sequence of themes, if no input, get all themes in the cache
      folder

    - random assignment algorithm
        1. count the number of files in total
        2. randomly split the total number into `num_themes` groups
        3. randomly order the files and split them to these groups
        4. for each group, run the `apply_theme` method

- [x] motheme create: Create a new custom theme

    - arg: `theme_name`
    - make a duplication of an existed theme and print the path to it

# improvements

- [ ] add custom css path and html head path to `marimo.toml`

# docs

- [x] in readme, recommend add `motheme` as `uv tool install motheme` and use it with
      `uvx motheme <command>`

# new features

- [x] --git-ignore flag

    ignore files that are in .gitignore

- [x] --quiet flag

    print nothing

- [x] add -r flag back and more help messages

- [ ] [integrate with custom html head](https://docs.marimo.io/guides/configuration/html_head/?h=html#custom-html-head)

# new themes

# a notebook for creating themes

# github

- [ ] add test to valid css file
