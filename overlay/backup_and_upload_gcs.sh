#!/bin/bash

# FULLY AUTOMATED ATI ENGINE BACKUP TO GCS, SPLIT 50MB CHUNKS

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="ATI_ENGINE_BACKUP_${TIMESTAMP}.zip"
PARTS_PREFIX="ATI_ENGINE_PART_${TIMESTAMP}_"
GCS_BUCKET="gs://ati-oracle-engine/backups/"

# 1. Zip the entire Soap directory (absolute path for Cloud Shell)
cd ~
zip -r "${BACKUP_NAME}" Soap/

# 2. Split into 50MB parts
split -b 50m "${BACKUP_NAME}" "${PARTS_PREFIX}"

# 3. Upload all parts to your real GCS bucket
for part in ${PARTS_PREFIX}*; do
  echo "Uploading $part to $GCS_BUCKET"
  gsutil cp "$part" "$GCS_BUCKET"
done

# 4. Remove local backup files to free space
rm -f "${BACKUP_NAME}" ${PARTS_PREFIX}*

echo "ATI Engine: Backup, split, and upload complete."
