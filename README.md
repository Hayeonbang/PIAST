# PIAST Dataset

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2411.02551-<COLOR>.svg)](https://arxiv.org/abs/2411.02551)
[![Datasets](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Datasets-yellow)](https://huggingface.co/datasets/Hayeonbang/PIAST)
[![Demo page](https://img.shields.io/badge/Demo-page-hotpink)](https://hayeonbang.github.io/PIAST_dataset/)



![PIAST](./PIAST.png)

This is the repository for the **PIAST dataset**, which contains a collection of piano performance audio, transcribed MIDI and corresponding text data. You can see the demo of the dataset on this [link](https://hayeonbang.github.io/PIAST_dataset/).

## Update log
- **Nov 13, 2024**: The MIDI files and text data for both PIAST-AT and PIAST-YT have been uploaded! However, due to a data preprocessing issue, some files are missing compared to the numbers reported in the paper. These will be added in a future version update, so please stay tuned!


## Dataset
Our dataset has two subsets; **PIAST-YT** and **PIAST-AT** (details can be found in the [paper](https://arxiv.org/abs/2411.02551)). Both subsets contain audio, MIDI and text data. 
- **Audio**: We provide the list of the *YouTube IDs* and the corresponding codes for downloading
- **MIDI, Text**: Transcribed MIDI and the text data are available on the [Hugging Face](https://huggingface.co/datasets/Hayeonbang/PIAST)

## Download
```bash
pip install youtube-dl ffmpeg pydub
```

```python
python yt_main.py
python at_main.py
```

## Experiment
Code for the experiments in the paper will be updated soon! 

## License
This project is under the CC-BY-NC 4.0 license.

## Citation
Citation format will be updated soon

## Author Information
For further inquiries, please reach out to me at hayeonbang@kaist.ac.kr.