# BAudioExtractor

BAudioExtractor is a tool to generate VITS training data by scraping and extracting Japanese audio and transcripts from [Blue Archive Wiki](https://bluearchive.wiki/).

## Prerequisites

Before using this tool, make sure you have the following installed:

- Python 3.8+
- pip
- [ffmpeg](http://www.ffmpeg.org/) or [libav](http://libav.org/)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/taufiq30s/BAudioExtractor.git
```

2. **Create Virtual Environment (optional)**

```bash
python -m venv venv
source venv/bin/activate   # For Linux
venv\Scripts\activate      # For Windows
```

3. **Update pip and install requirements**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```


## Usage

```bash
python3 -m extract.py -id 10 -r 0.7 -name "ibuki" --path "/dataset/ibuki" url
```

- `-id` `--id` ID of the speaker that will be added to the dataset (Default: 10).
- `-r` `--ratio` Dataset split ratio for train and validation in decimal (Default: 0.7)
- `-name` `--character_name` Character name that will be added to the dataset (Default: "ibuki").
- `--path` Set root path of audio that will be added in dataset (Default: "/content/MyDrive/datasets")
- `url` URL of Blue Archive Wiki that contain character's audio and transcript. (For example: https://bluearchive.wiki/wiki/Ibuki/audio)

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/taufiq30s/BAudioExtractor/blob/master/LICENSE) file for more information.
