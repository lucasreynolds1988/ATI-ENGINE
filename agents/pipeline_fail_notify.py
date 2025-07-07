import os
import subprocess
import yagmail

SENDER_EMAIL = "lucasreynolds1988@gmail.com"
RECIPIENT_EMAIL = "lucasreynolds1988@gmail.com"
APP_PASS_FILE = os.path.expanduser("~/Soap/secrets/email_app_pass.txt")

def send_failure_email(input_file):
    if not os.path.isfile(APP_PASS_FILE):
        print(f"Missing app password at {APP_PASS_FILE}")
        return
    with open(APP_PASS_FILE, "r") as f:
        sender_pass = f.read().strip()
    yag = yagmail.SMTP(SENDER_EMAIL, sender_pass)
    subject = f"ATI Pipeline Failure: {os.path.basename(input_file)}"
    body = f"The pipeline failed for input file: {input_file}."
    yag.send(to=RECIPIENT_EMAIL, subject=subject, contents=body)
    print(f"Failure email sent to {RECIPIENT_EMAIL}")

def run_with_notify(input_file):
    try:
        subprocess.run([
            "python3", os.path.expanduser("~/Soap/agents/pipeline_supervisor.py"),
            input_file
        ], check=True)
    except Exception as e:
        print("Pipeline failed. Sending email notification...")
        send_failure_email(input_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_with_notify(sys.argv[1])
    else:
        print("Usage: python pipeline_fail_notify.py <input_file>")
