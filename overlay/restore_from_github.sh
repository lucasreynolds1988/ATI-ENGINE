#!/bin/bash

echo "🧠 Restoring ATI Rotor Fusion Engine..."

cd ~
rm -rf Soap
wget https://github.com/lucasr610/Soap_backup/raw/main/ATI_RotorFusion_FullBackup.zip -O ATI.zip
unzip ATI.zip
cd Soap

echo "🚀 Launching rotors..."
python3 spin_up.py
python3 cloud_stream_relay.py &

echo "✅ Restore complete. System is now running."
