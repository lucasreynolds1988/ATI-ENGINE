import os
import yagmail

SENDER_EMAIL = "lucasreynolds1988@gmail.com"
APP_PASS_FILE = os.path.expanduser("~/Soap/secrets/email_app_pass.txt")
RECIPIENT_EMAIL = "lucasreynolds1988@gmail.com"

def send_output_email(output_file):
    if not os.path.isfile(APP_PASS_FILE):
        print(f"Missing app password at {APP_PASS_FILE}")
        return
    with open(APP_PASS_FILE, "r") as f:
        sender_pass = f.read().strip()
    with open(output_file, "r") as f:
        content = f.read()
    yag = yagmail.SMTP(SENDER_EMAIL, sender_pass)
    yag.send(
        to=RECIPIENT_EMAIL,
        subject=f"ATI Pipeline Output: {os.path.basename(output_file)}",
        contents=content
    )
    print(f"Emailed pipeline output: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        send_output_email(sys.argv[1])
    else:
        print("Usage: python pipeline_output_email.py <output_file>")
