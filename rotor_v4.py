import os, shutil, subprocess, time, datetime, hashlib, json, logging
from pymongo import MongoClient
from google.cloud import storage
from bson.objectid import ObjectId

ROTORDIR = os.path.expanduser("~/Soap")
LOGDIR = os.path.join(ROTORDIR, "logs")
CACHE_FILE = os.path.join(ROTORDIR, ".rotor-cache.json")
FAILED_FILE = os.path.join(ROTORDIR, "rotor_failed.json")
BUCKET_NAME = "ati-rotor-bucket"
MONGO_URI = "mongodb+srv://lucasreynolds1988:Service2244@ai-sop-dev.nezgetk.mongodb.net/?retryWrites=true&w=majority&appName=ai-sop-dev"

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

def free_space_gb():
    s = shutil.disk_usage("/")
    return round(s.free / (1024 ** 3), 2)

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

def add_failure(path):
    if os.path.exists(FAILED_FILE):
        with open(FAILED_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(path)
    with open(FAILED_FILE, "w") as f:
        json.dump(list(set(data)), f)

def split_file(path, chunk_size=90 * 1024 * 1024):
    print(f"🪓 Splitting {os.path.basename(path)}")
    with open(path, "rb") as f:
        i = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_name = f"{path}.part_{chr(97 + i)}{chr(97 + i)}"
            with open(part_name, "wb") as part:
                part.write(chunk)
            i += 1
    os.remove(path)

def upload_to_github(file_path):
    try:
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", f"Offload: {os.path.basename(file_path)}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        logging.info(f"✅ GitHub upload complete: {os.path.basename(file_path)}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ GitHub upload failed: {file_path} — {e}")
        add_failure(file_path)
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
        logging.error(f"❌ MongoDB error: {e}")
        add_failure(file_path)
        return False

def upload_to_gcs(file_path):
    try:
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        logging.info(f"✅ GCS upload complete: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        logging.error(f"❌ GCS upload failed: {e}")
        add_failure(file_path)
        return False

def main():
    print("🧠 Rotor V4 online — adaptive alternator spin initiated")
    logging.info("Rotor V4 boot sequence started.")
    cache = load_cache()

    print(f"📊 Free disk space: {free_space_gb()} GB")

    files = [f for f in os.listdir(ROTORDIR) if f.endswith(".tar.gz")]
    for f in files:
        full_path = os.path.join(ROTORDIR, f)
        split_file(full_path)

    parts = sorted([f for f in os.listdir(ROTORDIR) if ".part_" in f])
    for part in parts:
        path = os.path.join(ROTORDIR, part)
        checksum = sha256sum(path)

        if checksum in cache:
            logging.info(f"⚠️ Skipping duplicate: {part}")
            continue

        success1 = upload_to_github(path) if free_space_gb() > 0.3 else False
        time.sleep(2)
        success2 = upload_to_mongo(path)
        time.sleep(2)
        success3 = upload_to_gcs(path)
        time.sleep(2)

        if all([success1, success2, success3]):
            cache[checksum] = part
            os.remove(path)
            logging.info(f"🧹 Cleanup complete: {part}")
        else:
            logging.warning(f"⚠️ Incomplete upload: {part}")

    save_cache(cache)
    logging.info("✅ Rotor V4 mission complete.")
    print("✅ Rotor V4 mission complete.")

if __name__ == "__main__":
    main()
