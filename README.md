<div align="center">
  <img src="https://raw.githubusercontent.com/mirkobrombin/Twitz/master/data/pm.mirko.Twitz.svg" width="64">
  <h1 align="center">Twitz</h1>
  <p align="center">A Twitch client for Linux (unpretentious)</p>
  <p align="center"><b>Twitz is under development</b> and you may encounter bugs using it. I ask you to remain calm and report them in the best possible way by opening an issue. Thanks for your attention.</p>
</div>

<br/>

<div align="center">
  <a href="https://www.codefactor.io/repository/github/mirkobrombin/twitz">
    <img src="https://www.codefactor.io/repository/github/mirkobrombin/twitz/badge" alt="CodeFactor" />
  </a>
  <a href="https://github.com/mirkobrombin/Twitz/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg">
  </a>
  <a href="https://github.com/mirkobrombin/Twitz/actions">
    <img src="https://github.com/mirkobrombin/Amusiz/workflows/Build%20release%20packages/badge.svg">
  </a>
  <a href="https://aur.archlinux.org/packages/twitz/">
    <img alt="AUR version" src="https://img.shields.io/aur/version/twitz">
  </a>
</div>

<br />

<div align="center">
    <img  src="https://raw.githubusercontent.com/mirkobrombin/Twitz/main/data/screenshot.png">
</div>

## Installation

### Ubuntu 20.04+
**.deb** available from the [Releases](https://github.com/mirkobrombin/Twitz/releases).

<!--
### Snap
[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/twitz)
-->

### Build dependencies
- meson
- ninja
- libhandy
- WebKit2
- youtube-dl
- python3-mpv
- python3-opengl

### Working on
- Preferences

### Build
```bash
meson build
cd build
ninja install
```
