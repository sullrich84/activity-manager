import subprocess


def get_1password_secret(item_path) -> str:
    try:
        cmd = ["op", "read", item_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Fehler beim Auslesen von 1Password Secret {item_path}: {e}")
