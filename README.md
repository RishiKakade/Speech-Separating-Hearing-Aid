# Speech-Separating-Hearing-Aid

This is our final year design project, which focuses on improving the performance of hearing aids using neural beamforming and source separation techniques.

## Project Overview
The goal of this project is to enhance the listening experience of hearing aid users by localizing speakers and separating out background noise. Our approach uses a neural beamformer to locate the direction of the speaker, then applly source separation to isolate the speaker's voice from surrounding sounds. This results in a clearer, more intelligible audio signal for the user.

## System Architecture
The block diagram for our system is shown below:

![Block Diagram](/assets/diagram.png)

## Demo

[Demo Video](https://youtu.be/Zgwmc42L5wk)

## Contributors

- Rishi Kakade
- Aditya Srinivasan
- Yulia Kluev
- Ojorumi Aneke
- Kiersten Overton
- Kunal Chandan

## Acknowledgements

Our beamformer was [Cone of Silence](https://arxiv.org/pdf/2010.06007.pdf) and the source separation was done using [Conv-TasNet](https://arxiv.org/abs/1809.07454)
