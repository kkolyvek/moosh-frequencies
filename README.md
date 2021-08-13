<h1 align="center"><strong>Shark Tail-Beat Frequency Processing</strong></h1>

<p align="center">
  <img src="https://img.shields.io/github/languages/top/kkolyvek/moosh-frequencies">
</p>

## Description

This repository contains processes to analyze shark tail-beat frequencies from drone footage using OpenCV.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Bugs](#bugs)
4. [Future Development](#future-development)
5. [Contributing](#contributing)
6. [License](#license)

## Installation

The program depends on the following python packages. Please make sure they are installed.

- `opencv-python`
- `numpy`
- `matplotlib`

## Usage

There are two main obstacles when using this program. First, the program is extremely slow. While I'm sure there are some inefficiencies I'm not aware of and could help performance, I think the unfortunate reality is that running heavy image processing algorithms on 3840 x 2160 videos is slow. To work around this I recommend trimming videos to short lengths with high visibility bits.

Second, the program is highly dependent on playing around with the filtered HSV values in `filter.py`. The ideal masking for any given video clip can change drastically due to a number of factors such as time of day, color of water, weather, etc. I recommend the following process when finding frequencies:

1. Trim raw footage to a length that includes only clear shots of the target. Compressing the video to smaller resolutions also helps run the program faster.
2. In `main.py`, add your video's filepath and run the program with `display_vid` as the active function. This will run the filtering and contouring algorithms and display the results without saving to a file, allowing you to fine tune the masks in `filter.py`. I recommend using a site like [this color picker](https://imagecolorpicker.com/en) to help get a grasp on what color values need to be removed from the picture. Just take a screenshot of a frame of the video and click around the site.
3. Once satisfied with the results, run `main.py` with `display_freq` as the active function. This will display plots of tail slope over time and prominent frequencies.

You can also choose to save the processed video by running `main.py` with `create_vid` as the active function. It will save a .avi file to your working directory.

## Bugs

None that I am currently aware of.

## Future Development

For the time being, the success of the program is highly dependent on playing around with the filtered HSV values in `filter.py`. It would be nice in the future to at least partly automate this step.

## Contributing

For further questions, comments, and suggestions, please reach out through [GitHub](https://github.com/kkolyvek) or via email at kk674@cornell.edu.

## License

Copyright (c) Moosh Systems 2021

---
