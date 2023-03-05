# mypaste-cli

[![Tests](https://github.com/fvicent/mypaste-cli/actions/workflows/test.yml/badge.svg)](https://github.com/fvicent/mypaste-cli/actions/workflows/test.yml)

CLI for uploading files to [mypaste.dev](https://www.mypaste.dev) directly from the terminal.

# Usage

```
mypaste file-to-upload.js
```

The CLI will require your API key (available in your [account settings](https://www.mypaste.dev/user/settings/)) the first time and then store it in your system vault for later usage.

Run `mypaste --help` for the remaining options.

# Installation

Python 3.10 or greater is required.

Since we are alpha software, installation needs to be done from this repository using [`pipx`](https://pypa.github.io/pipx/), which will install the CLI in an isolated environment (that's great!):

```
pipx git+https://github.com/fvicent/mypaste-cli.git
```

