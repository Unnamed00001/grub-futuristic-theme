# Futuristic GRUB Theme

A dark blue GRUB 2 theme for **1920x1080** screens, with a rounded selection bar, 28 colored distro icons, Cascadia Code text and a blue-bordered terminal.

<!-- Add a screenshot here:
![Boot menu](screenshots/menu.png)
-->

## Features

- Dark blue background with the title and the key hints (Enter / Navigate / Edit) drawn into the image
- Boot menu sized for 7 visible entries, with a rounded blue selection bar and side padding
- Countdown text in the bottom-right corner ("Auto start in 10s")
- Terminal (`c`) and edit (`e`) screens: black background with a blue rounded border
- Cascadia Code font (converted to GRUB's `.pf2` format)
- 28 colored 84x84 icons: Windows, Ubuntu, Arch, CentOS, Debian, Deepin, elementary, EndeavourOS, Fedora, FreeBSD, Garuda, Gentoo, Kali, Linux Mint, Mageia, Manjaro, MX, openSUSE, Parrot, Pop!_OS, Red Hat, Slackware, Solus, Tails, Void, Zorin, UEFI firmware settings and a generic `unknown` fallback

## Repository structure

```
.
├── theme.txt          theme definition (layout, fonts, colors)
├── background.png     1920x1080 background with title and key hints
├── fonts/             Cascadia Code .pf2 files (sizes 16, 20, 24, 30)
├── icons/             <class>.png, one per system
├── menu/              selected_*.png and item_*.png (9-slice pieces)
├── terminal/          terminal_box_*.png (9-slice pieces)
└── tools/             scripts that generate the images + grub-teste.cfg
```

`theme.txt` uses only the **16** and **20** font sizes. The 24 and 30 files are extras you can use if you edit the theme.

## Requirements

- GRUB 2 with graphical output (gfxterm) and PNG support
- A screen (or `GRUB_GFXMODE`) of 1920x1080
- Root access to edit `/boot` and `/etc`

Developed and tested on Ubuntu with UEFI, dual-booting Windows. Other distros should work, but the commands below (`update-grub`, paths) are the Debian/Ubuntu ones and have not been tested elsewhere.

## Installation

**Back up your GRUB configuration first:**

```bash
sudo cp /etc/default/grub /etc/default/grub.backup
```

### 1. Copy the theme

From the root of the cloned repository:

```bash
sudo mkdir -p /boot/grub/themes/futurista
sudo cp -r . /boot/grub/themes/futurista
sudo rm -rf /boot/grub/themes/futurista/.git
```

### 2. Point GRUB to the theme

Edit `/etc/default/grub` so these lines exist and are **not** commented out:

```
GRUB_THEME="/boot/grub/themes/futurista/theme.txt"
GRUB_GFXMODE=1920x1080
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=10
```

`GRUB_TIMEOUT_STYLE=menu` matters: with `hidden` and a timeout of `0`, the menu (and the theme) never appears.

Also make sure `GRUB_TERMINAL=console` stays commented out, otherwise GRUB ignores themes.

### 3. Load the fonts

`theme.txt` cannot load font files by itself. GRUB must load them with `loadfont` in `grub.cfg`, which you can generate with a script in `/etc/grub.d/`:

```bash
sudo nano /etc/grub.d/04_futurista_fonts
```

```sh
#!/bin/sh
cat << 'EOT'
loadfont /boot/grub/themes/futurista/fonts/Cascadia16.pf2
loadfont /boot/grub/themes/futurista/fonts/Cascadia20.pf2
EOT
```

Make it executable. **This step is required:** an editor can create the file without the execute bit, and `update-grub` silently ignores non-executable scripts.

```bash
sudo chmod +x /etc/grub.d/04_futurista_fonts
ls -l /etc/grub.d/04_futurista_fonts    # should start with -rwxr-xr-x
```

If you change the fonts used in `theme.txt`, add a matching `loadfont` line for each size.

### 4. Update GRUB and reboot

```bash
sudo update-grub
sudo grep -n loadfont /boot/grub/grub.cfg    # your loadfont lines should appear
sudo reboot
```

If Windows does not show up, `os-prober` is probably disabled. Add `GRUB_DISABLE_OS_PROBER=false` to `/etc/default/grub` and run `sudo update-grub` again.

If the theme fails to load, GRUB still boots normally, just with the plain text menu.

### Uninstall

```bash
sudo rm /etc/grub.d/04_futurista_fonts
sudo rm -rf /boot/grub/themes/futurista
sudo cp /etc/default/grub.backup /etc/default/grub
sudo update-grub
```

## Updating the theme

After changing files in the repository, copy them again:

```bash
sudo rm -rf /boot/grub/themes/futurista
sudo mkdir -p /boot/grub/themes/futurista
sudo cp -r . /boot/grub/themes/futurista
sudo rm -rf /boot/grub/themes/futurista/.git
```

`update-grub` is only needed when `/etc/default/grub` or the fonts script change.

## Icons

GRUB looks for `icons/<class>.png`, where `<class>` comes from the `--class` options of each menu entry. To list the classes your system generates:

```bash
sudo grep -o "\-\-class [a-z0-9_-]*" /boot/grub/grub.cfg | sort -u
```

If an entry shows no icon, copy or rename a PNG so its name matches the class. Icons should be square PNGs with a transparent background (84x84 here, drawn at 42x42 by `icon_width` / `icon_height`).

The names that GRUB shows (for example "Windows Boot Manager") come from `update-grub`, not from the theme.

## Preview without rebooting

[grub2-theme-preview](https://github.com/hartwork/grub2-theme-preview) runs GRUB inside QEMU:

```bash
sudo apt install qemu-system-x86 ovmf grub-pc-bin grub-efi-amd64-bin grub-common xorriso mtools pipx
pipx install grub2-theme-preview

grub2-theme-preview --grub-cfg tools/grub-teste.cfg --timeout 10 --resolution 1920x1080 .
```

- `tools/grub-teste.cfg` has fake entries with the right `--class` values, so every icon can be seen.
- `--timeout 10` is needed because the tool otherwise overrides the timeout with 30 seconds.
- Fonts in `fonts/` are loaded automatically by the preview tool.
- If the window is too big for your screen, add `--display gtk,zoom-to-fit=on`.

> **Snap VS Code:** if you run the preview from the integrated terminal of a Snap-packaged VS Code and QEMU fails with `symbol lookup error ... libpthread`, run the command from a normal terminal, or unset the Snap variables:
> `env -u GTK_PATH -u GTK_EXE_PREFIX -u GIO_MODULE_DIR -u LOCPATH -u GTK_IM_MODULE_FILE -u GSETTINGS_SCHEMA_DIR -u XDG_DATA_DIRS grub2-theme-preview ...`

## Customizing

### Menu layout (`theme.txt`)

| Property | Value | What it does |
|---|---|---|
| `left`, `top`, `width`, `height` | `28%`, `38%`, `44%`, `45%` | Position and size of the menu box |
| `item_height` + `item_spacing` | `60` + `6` | Each entry takes 66 px; box height / 66 = visible entries |
| `icon_width`, `icon_height` | `42` | Icon size |
| `item_icon_space` | `25` | Space between icon and text |
| `item_color`, `selected_item_color` | `#7E9CD2`, `#FFFFFF` | Text colors |

To show a different number of entries, change `height` so it is slightly larger than `N * (item_height + item_spacing)` pixels (1080 px screen).

### Terminal

The terminal frame is drawn **outside** the text area, so `terminal-border` must equal the corner size of the images (`M + R` in `tools/make_terminal.py`, currently 24) and the box must leave room around it (2% and 3% margins).

### Regenerating the images

The 9-slice images are generated with Python and [Pillow](https://pillow.readthedocs.io/). Run the scripts from the repository root:

```bash
python3 tools/make_selected.py    # menu/selected_*.png  (the blue bar)
python3 tools/make_item.py        # menu/item_*.png      (transparent, same sizes)
python3 tools/make_terminal.py    # terminal/terminal_box_*.png
```

Run `make_item.py` again every time you change `make_selected.py`. The invisible `item_*.png` pieces must have the same size as the `selected_*.png` ones, otherwise entries shift a few pixels when you move the selection. The left and right pieces are wider than the corners (`PAD_X`) to keep the icon away from the bar's edge.

### Fonts

GRUB cannot resize fonts: each size is a separate `.pf2` file, and the name used in `theme.txt` must match the name stored inside the file.

```bash
grub-mkfont -s 24 -o fonts/Cascadia24.pf2 /usr/share/fonts/truetype/cascadia-code/CascadiaCode.ttf
strings fonts/Cascadia24.pf2 | sed -n 3p       # Cascadia Code Regular 24
```

Then use `font = "Cascadia Code Regular 24"` and add the `loadfont` line to the fonts script.

### Background

`background.png` must be exactly 1920x1080. The title and the key hints are part of the image, so they are not translated by GRUB. Keep the area of the boot menu and the countdown empty, because GRUB draws them on top.

## Known limitations

- Made for 1920x1080 only; other resolutions have not been tested.
- The title and key hints are static (part of the background image).
- Letter spacing cannot be set in GRUB themes.
- Bold weights are not available: the Cascadia Code `.ttf` is a variable font, and `grub-mkfont` only reads its default weight.

## Credits and licenses

- **Theme:** MIT License. See [`LICENSE`](LICENSE).
- **Font:** [Cascadia Code](https://github.com/microsoft/cascadia-code) by Microsoft, licensed under the SIL Open Font License 1.1. The `.pf2` files in `fonts/` are converted from it. If you redistribute them, include the OFL license text.
- **Icons:** from [relliv/OperatingSystemIcons](https://github.com/relliv/OperatingSystemIcons), resized to 84x84. That repository does not state a license, so check with its author before redistributing.
- **Trademarks:** all operating system names and logos belong to their respective owners. They are used here only to identify the systems in the boot menu, and no endorsement is implied.
- **Preview tool:** [grub2-theme-preview](https://github.com/hartwork/grub2-theme-preview) by Sebastian Pipping.

## Contributing

Issues and pull requests are welcome, especially new icons, other resolutions and tests on other distros.