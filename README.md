# Python-Dash-LSTM-rainfall

[![Generic badge](https://img.shields.io/badge/language-python%203.6.10-navy.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/IDE-VS%20Code%201.61.2-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/ML%20package-tensorflow.keras%202.2-orange.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/ML%20model-LSTM-purple.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/interactive-dash-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/data%20type-monthly%20average%20rainfall-yellow.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/data%20source-UK%20MetOffice-red.svg)](https://shields.io/)
-
# Table of contents
- [1. Rationale](#1-rationale)
- [2. Architecture](#2-architecture)
- [3. Snapshots](#3-snapshots)

<i><a href='http://ecotrust-canada.github.io/markdown-toc/'><font size="10">Table of contents generated with markdown-toc</font></a></i>

## 1. Rationale


-

## 2. Architecture


-

## 3. Snapshots
- **Rainfall time series for the 6 locations**. </br> 
These represent monthly average rainfall in mm from January 2000 to September 2021.
<img src="images/Rainfall_time_series.png" width="700" height="400"/></br>
- **Accuracy vs Loss as measured during training for the 6 locations**.</br>
The areas circled in black represent batches of data where the model failed to perform with the same accuracy. The reason for this is most likely in the physical process behind the data collection: when extreme events occur, such as severe storms, the rainfall measurements can be many times larger than the average values. Also, because these events are few and far between, it becomes difficult for a model to take them into account, and they end up being assimilated as noise. This noise affects the ability of the model to generalise, leading to poorer predictions.
<img src="images/Accuracy_vs_Losses.png" width="700" height="400"/></br>
