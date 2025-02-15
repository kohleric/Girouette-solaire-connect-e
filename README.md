# Girouette-solaire (wifi)
Girouette (vitesse hélice + direction) transmission wifi reception serveur odroid
arduino, esp 32, odroid + capteurs / cpp, python, js

![20240309_090421-2048x1152](https://github.com/user-attachments/assets/61bde070-6b61-4a26-8d92-7d956e217c00)

Affichage des données en temps réel (real time data streaming of La girouette) : vitesse hélice et direction, pression et température atmosphérique, tension des batteries
![P-T-V-RPM-bat_girouette](https://github.com/user-attachments/assets/9867da0d-0234-48f2-a581-f6334a2b5944)


    Hall effect sensor switch : two combined with a magnetic angle encoder tio determine absolute direction and two other for RPM measurment,
    Arduino Nano : measuring propeller speed and girouette direction at 22,5° resolution (digital bus at full speed), battery voltage and temperature (analog at 1Hz)-> data sent by UART 115200 baud at 1Hz after pre-processing (min/max averag during last s),
    ESP32 Wrover : measuring atmospheric pressure and temperature (via i2c bus at 1Hz) -> completion of data sent via wifi at odroid,
    Odroid XU4 : data archiving and massive calculations + illustration, generation for the girouette.eu site -> data sent by FTP by wifi,
    girouette.eu : wordpress


