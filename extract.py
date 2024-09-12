import os
import re
import requests
from pydub import AudioSegment
from io import BytesIO
import random
import argparse
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

def get_webpage(url):
    print("Geting audio page...")
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    print("Success")
    return BeautifulSoup(res.text, 'html.parser')

def extract_data(raw, path):
    print("Extracting audio urls and transcripts")
    res = {}
    urls = []
    rows = raw.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) > 1:  # Ensure there is a second <td> element
            span_file_tags = tds[1].find_all("span", {"typeof" : "mw:File"})
            if len(span_file_tags) == 0:
                continue

            ## Get Transcripts
            transcripts = []
            transcript_tags = tds[2].find_all("p")
            for tag in transcript_tags:
                transcripts.extend(tag.get_text(strip=True, separator="\n").splitlines())

            ## Generate Dictionary and get urls
            file_urls = []
            for span_file_tag in span_file_tags:
                audio_tags = span_file_tag.find_all(attrs={"data-transcodekey" : "mp3"})
                for tag in audio_tags:
                    file_urls.append(tag['src'])

            if len(file_urls) > 1:
                for i in range(len(file_urls)):
                    res[f"{path}/{file_urls[i].split('/')[-1].replace('ogg.mp3', 'wav')}"] = transcripts[i] if len(transcripts) > 0 else ""
                    urls.append(f'https:{file_urls[i]}')
            else:
                res[f"{path}/{file_urls[0].split('/')[-1].replace('ogg.mp3', 'wav')}"] = " ".join(transcripts) if len(transcripts) > 0 else ""
                urls.append(f'https:{file_urls[0]}')
    return res, urls

def convert_to_wav_and_store_it(audio_stream, out_path):
    audio = AudioSegment.from_file(audio_stream)
    audio = audio.set_frame_rate(22050)
    audio.export(out_path, format="wav", parameters=["-ac", "1"])
    print("Success")

def download_file(urls):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    out_dir = os.path.join(script_dir, "audio")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for url in urls:
        filename = url.split('/')[-1]
        name = filename.split(".")[0]
        filepath = os.path.join(out_dir, f"{name}.wav")
        if os.path.exists(filepath): continue

        print(f'Downloading {filename}...')
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        print("Success.")

        out_path = os.path.join(out_dir, f"{filename.split('.')[0]}.wav")
        print(f'Converting {filename} to .wav')
        convert_to_wav_and_store_it(BytesIO(r.content), out_path)

def generate_train_and_val_dataset(data, speaker_id, chara_name, ratio=0.7):
    print("Generate Train and Validation file")
    items = list(data.items())
    random.shuffle(items)
    split_idx = int(len(items) * ratio)

    train_data = dict(items[:split_idx])
    val_data = dict(items[split_idx:])

    with open(f'{chara_name}_train.txt', 'w', encoding='utf-8') as f:
        for key, value in train_data.items():
            f.write(f'{key}|{speaker_id}|{value}\n')

    with open(f'{chara_name}_val.txt', 'w', encoding='utf-8') as f:
        for key, value in val_data.items():
            f.write(f'{key}|{speaker_id}|{value}\n')
    print("Success")

def main():
    parser = argparse.ArgumentParser(
        description="Generate VITS training data by Scrape and extract Japanese audio files and transcripts from Blue Archive Wiki"
    )
    parser.add_argument('url', help='Blue Archive Wiki Audio URL. (example: https://bluearchive.wiki/wiki/Ibuki/audio)')
    parser.add_argument('-id', type=int, default=10, help='ID of the speaker to be added to the dataset (default: 10)')
    parser.add_argument('-r', '--ratio', type=float, default=0.7, help='Ratio for the split (default: 0.7)')
    parser.add_argument('-name', '--character_name', default="ibuki", help='Character that will be added at dataset (default: ibuki)')
    parser.add_argument('--path', default="/content/MyDrive/datasets", help='Set root path of audio that will be added in dataset. (default: "/content/MyDrive/datasets")')

    args = parser.parse_args()

    print("Blue Archive VITS Extractor")
    raw = get_webpage(args.url)
    data, urls = extract_data(raw, args.path.rstrip("/"))
    download_file(urls)
    generate_train_and_val_dataset(data, args.id, args.character_name, args.ratio)
    print("Done")

if __name__ == "__main__":
    main()
