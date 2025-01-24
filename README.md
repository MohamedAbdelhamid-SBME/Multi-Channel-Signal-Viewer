# Multi-Port, Multi-Channel Signal Viewer #
![image](https://github.com/user-attachments/assets/df2b15cf-963f-4c65-b0f3-16e459cb7167)

**Signal Viewer** is a Python-based desktop application developed with PyQt5 for monitoring and visualizing medical signals. This tool enables users to interact with multi-port, multi-channel signals and provides robust features 

https://github.com/user-attachments/assets/ceddcf6f-96b0-4e86-a224-1d928e36b109

for viewing, processing, and reporting on the signals.

## Features

1. **Multi-Channel Signal Viewer**:
   - Open and display multiple signal files simultaneously.
   - Supports various medical signals (e.g., ECG, EMG, EEG), with both normal and abnormal examples.

2. **Dual Graphs**:
   - Two main identical graphs to load and compare signals.
   - Option to link or unlink graphs for synchronized or independent control.

3. **Real-Time Signal Streaming**:
   - Connect to a website emitting real-time signals and plot them dynamically.

4. **Signal Visualization**:
   - Cine mode: Display running signals over time, mimicking ICU monitors.
   - Rewind option to restart signals after completion.

5. **UI Controls**:
   - Change signal color.
   - Add labels/titles for clarity.
   - Show/hide signals.
   - Customize cine speed.
   - Zoom in/out, pan, and scroll signals.
   - Pause, play, rewind controls.
   - Move signals between graphs.

6. **Non-Rectangle Graph Support**:
   - Supports unique non-rectangle graphs for specific signals.

7. **Signal Glue**:
   - Combine parts of two signals using interpolation.
   - Customizable glue parameters: window size, signal gap/overlap, interpolation order.

8. **Exporting & Reporting**:
   - Generate detailed PDF reports with glued signal snapshots and statistical data (mean, standard deviation, min, max, duration).
   - Create well-organized, multi-page reports directly from the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/signal-viewer.git
## Troubleshooting:
**if you are having problems with the application, please consult the following troubleshooting tips:**

- Make sure that you have installed the required Python packages, such as NumPy, Pandas, and Qt.
- Make sure that you are using a supported signal format.
- Try restarting the application.
- If you are still having problems, please post a question on the project's GitHub page.

