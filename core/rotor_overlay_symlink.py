import os

def symlink_overlay(target_dir):
    overlay = os.path.expanduser("~/Soap/overlay")
    link_path = os.path.join(target_dir, "overlay_link")
    if os.path.islink(link_path) or os.path.exists(link_path):
        os.unlink(link_path)
    os.symlink(overlay, link_path)
    print(f"Created symlink: {link_path} -> {overlay}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        symlink_overlay(sys.argv[1])
    else:
        print("Usage: python rotor_overlay_symlink.py <target_dir>")
