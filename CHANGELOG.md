# v0.2.0

## New themes

- feat(new theme): add new theme solarized
- feat(new theme): add new theme ayu and its variant ayu mirage
- feat(new theme): add new theme molokai
- feat(new theme): add new theme atomone
- feat(new theme): add new theme solarized

## New commands

- feat(new command): add new command `motheme download` to download themes
- feat(new command): add new command `motheme font` to manage font templates
- feat(new command): add new command `motheme ls` to list themes and fonts

## New features

- feat(motheme remove): add flag `-a/--all` to remove all downloaded themes

## Deprecated

- deprecated(motheme update): deprecating the `motheme update` command, use
  `motheme download` instead
- deprecate(motheme themes): deprecating the `motheme themes` command, use `motheme ls`
  instead

## Bug fixes

- fix(typo): store data inside `motheme` instead of `mtheme`
- fix(msg): replace `mtheme themes` with `motheme ls --not-installed`

## Improvements

- refactor(nord): modify `nord` theme implementation
