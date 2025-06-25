# magespace_importer

`magespace_importer` is a Python-based tool designed to simplify importing models from a list of URLs into [mage.space](https://mage.space/)

It opens each URL in a new browser tab, and lets you perform the model import there. After you've imported a model, close the tab. To finish processing, close all browser tabs.

## Installation

Ensure _Python_ 3.10 or _higher_ is installed on your system. You can then install the package using pip:

```bash
python3 -m pip  install --upgrade git+https://github.com/twardoch/magespace-importer
```

## Usage

Prepare a text file containing a list of URLs to models you want to import, one URL per line, and save it as `magespace.txt` in your current folder.

For example, for models from CivitAI, you can use URLs like:

```text
https://civitai.com/api/download/models/243915?type=Model&format=SafeTensor&size=pruned&fp=fp16
https://civitai.com/api/download/models/163063?type=Model&format=SafeTensor
```

> Note: If a model page on CivitAI has one Download button, you can use the CivitAI model page URL. But if the model page has a download dropdown, you must click it and copy the download URL (typically SafeTensors).

Then, use the tool in command line with optional arguments:

```bash
magespace_importer
```

| A   | B   | C   |
| --- | --- | --- |
| AAA |

- The tool will open a new Chrome browser window where you'll need to log into <https://mage.space/> using your credentials, then click the Terminal window and press Enter.

- Then the tool open each URL in a new tab. You can then manually finalize the import in each tab. After you've imported a model, close the tab. To finish processing, close all browser tabs.

### Optional Arguments

- `--models_path`: Path to the text file containing model URLs (one URL per line), defaults to `magespace.txt` in the current folder.
- `--driver_path`: Optional path to the ChromeDriver executable.
- `--url_import`: Custom URL for the model import page, defaults to `https://www.mage.space/models/import`.

Example:

```bash
magespace_importer --models_path /path/to/magespace.txt
```

or if `magespace.txt` is in the current folder:

```bash
magespace_importer
```
