# Raspberry Pi Face Recognition CCTV Camera

Welcome to the Raspberry Pi Face Recognition CCTV Camera project! This project aims to provide a simple yet powerful solution for setting up a surveillance system using Raspberry Pi and facial recognition technology.

## Features

- **Facial Recognition:** Identify authorized individuals and detect unknown faces in real-time.
- **Real-Time Alerts:** Receive instant notifications on unrecognized faces for prompt action.
- **User-Friendly Interface:** Easy setup and configuration through a user-friendly interface.
- **Privacy Protection:** All recognition data stored locally on the Raspberry Pi for enhanced privacy.
- **Integration:** Seamlessly integrate with other smart home devices for enhanced automation.

## Requirements

- Raspberry Pi board (tested on Raspberry Pi 3 and Raspberry Pi 4)
- PiCamera module
- Python 3.x
- OpenCV
- Facial recognition library (e.g., dlib, OpenCV's built-in face recognition)

## Installation

1. Clone this repository to your Raspberry Pi:

   ```
   git clone https://github.com/Art3mis17/face-recognition-cctv.git
   ```

2. Install the required dependencies

3. Run the main script:

   ```
   python cctv.py
   ```

## Usage

1. Upon running the script, the CCTV camera will start capturing frames from the PiCamera module.
2. Faces detected in the frames will be compared against the recognition database.
3. If a recognized face is detected, appropriate action will be taken based on your configuration.
4. If an unrecognized face is detected, a notification will be sent to the configured recipients.

## Contributing

Contributions to this project are welcome! Feel free to submit bug reports, feature requests, or pull requests via GitHub.

## Acknowledgements

- Thanks to the Raspberry Pi community for their continuous support and inspiration.
- Special thanks to the developers of the facial recognition libraries used in this project.
- Project made by Madhavv Arul, Saran Anbu and Jabin Joshua
  
## Contact

For any inquiries or support, please contact saranmass234@gmail.com.

---

Enjoy peace of mind with the Raspberry Pi Face Recognition CCTV Camera!
