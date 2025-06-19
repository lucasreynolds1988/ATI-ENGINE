import os, shutil, subprocess, time, datetime, hashlib, json, logging
from pymongo import MongoClient
from google.cloud import storage

HOME_DIR = "/home/lucasreynolds1988"
ROOT_DIR = "/root/soap_storage"
ROTORDIR = os.path.expanduser("~/Soap")
LOGDIR = os.path.join(ROTORDIR, "logs")
CACHE_FILE = os.path.join(ROTORDIR, ".rotor-cache.json")
BUCKET_NAME = "ati-rotor-bucket"
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"

INCLUDE_EXTENSIONS = [".tar.gz", ".part_", ".whl", ".pdf", ".log", ".sqlite3", ".zip", ".py"]

os.makedirs(LOGDIR, exist_ok=True)
logging.basicConfig(filename=os.path.join(LOGDIR, "rotor.log"),
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

client = MongoClient(MONGO_URI)
db = client["soap"]
fs_files = db["fs.files"]
fs_chunks = db["fs.chunks"]

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def upload_to_github(file_path):
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Offload: {os.path.basename(file_path)}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        logging.info(f"✅ GitHub upload complete: {os.path.basename(file_path)}")
        return True
    except subprocess.CalledProcessError as e:
        logging.warning(f"❌ GitHub upload failed: {file_path} — {e}")
        return False

def upload_to_mongo(file_path):
    try:
        if db.command("dbStats")["fsUsedSize"] > 500 * 1024 * 1024:
            logging.warning("❌ MongoDB full — skipping.")
            return False
        file_id = fs_files.insert_one({"filename": file_path, "uploadDate": datetime.datetime.utcnow()}).inserted_id
        with open(file_path, "rb") as f:
            chunk_size = 255 * 1024
            for n, chunk in enumerate(iter(lambda: f.read(chunk_size), b"")):
                fs_chunks.insert_one({"files_id": file_id, "n": n, "data": chunk})
        logging.info(f"✅ MongoDB upload complete: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        logging.warning(f"❌ MongoDB error: {e}")
        return False

def upload_to_gcs(file_path):
    try:
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        logging.info(f"✅ GCS upload complete: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        logging.warning(f"❌ GCS upload failed: {e}")
        return False

def collect_files(root_dirs):
    collected = []
    for root_dir in root_dirs:
        for root, dirs, files in os.walk(root_dir):
            for f in files:
                if any(f.endswith(ext) or ext in f for ext in INCLUDE_EXTENSIONS):
                    collected.append(os.path.join(root, f))
    return collected

def main():
    print("🧠 Rotor V5 online — full-system alternator activated")
    logging.info("Rotor V5 spin initiated.")
    cache = load_cache()

    all_files = collect_files([HOME_DIR, ROOT_DIR])
    print(f"📦 Files detected: {len(all_files)}")

    for path in all_files:
        try:
            checksum = sha256sum(path)
        except:
            logging.warning(f"⚠️ Skipped unreadable file: {path}")
            continue

        if checksum in cache:
            logging.info(f"🔁 Duplicate skipped: {path}")
            continue

        success1 = upload_to_github(path)
        time.sleep(2)
        success2 = upload_to_mongo(path)
        time.sleep(2)
        success3 = upload_to_gcs(path)
        time.sleep(2)

        if all([success1, success2, success3]):
            os.remove(path)
            logging.info(f"🧹 Deleted: {path}")
            cache[checksum] = os.path.basename(path)
        else:
            logging.warning(f"⚠️ Upload incomplete: {path}")

    save_cache(cache)
    logging.info("✅ Rotor V5 mission complete.")
    print("✅ Rotor V5 complete.")

if __name__ == "__main__":
    main()
