#!/bin/bash

echo "🔐 [TOWER GATEWAY] Starting multi-cloud system lock..."

# Set working dir
cd ~/Soap || exit 1

# 1. GitHub Push
echo "📦 [GitHub] Committing changes..."
git add .
git commit -m "🔐 Tier 6: Full system save via unlock_tower_gateway.sh"
git push origin main

# 2. GCS Backup
echo "☁️ [GCS] Creating ZIP snapshot..."
ZIPNAME="ATI_OMEGA_TOWER_$(date +"%Y%m%d_%H%M%S").zip"
cd ~
zip -r "$ZIPNAME" Soap -x "*__pycache__*" "*.log" "*.tmp" "*venv/*" "*.part*" "*.zip"
gsutil cp "$ZIPNAME" gs://ati-oracle-engine/backups/

# 3. MongoDB Upload (chunk-safe)
echo "🧠 [MongoDB] Uploading system to chunk-safe memory..."
cd ~/Soap
python3 core/mongo_safe_upload_v2.py --source ~/Soap/

# 4. Manifest SHA Check
echo "🔍 [Manifest] Auditing..."
python3 core/manifest_auditor.py

# 5. Final Log
echo "✅ [TOWER LOCKED] GitHub + GCS + MongoDB synced."
echo "🚀 System is safe. You may now spin down or power up with confidence."
