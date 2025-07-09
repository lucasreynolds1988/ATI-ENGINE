def load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Manifest not found: {MANIFEST_PATH}")
        return []
    with open(MANIFEST_PATH, 'r') as f:
        return json.load(f)

def check_critical_protection(manifest_entries):
    protected_entries = manifest_entries if isinstance(manifest_entries, list) else manifest_entries.get('protected', [])
    missing = []

    for path in CRITICAL_DIRS:
        full_path = os.path.join(BASE_PATH, path)
        if not any(entry['path'] == full_path for entry in protected_entries):
            print(f"⚠️  Missing directory in manifest: {path}")
            missing.append(full_path)

    for filename in CRITICAL_FILES:
        full_path = os.path.join(BASE_PATH, 'core', filename)
        if os.path.exists(full_path):
            file_sha = sha256sum(full_path)
            if not any(entry['path'] == full_path and entry.get('sha256') == file_sha for entry in protected_entries):
                print(f"⚠️  File not protected or SHA mismatch: {filename}")
                missing.append(full_path)
        else:
            print(f"❌ Missing file: {full_path}")
            missing.append(full_path)

    if not missing:
        print("✅ All critical files/directories are protected.")
    else:
        print(f"\n🔴 {len(missing)} items missing or unprotected. Please add to manifest.")
