import os

def healthcheck():
    scripts = [
        "watson_phase.py", "father_phase.py", "mother_phase.py",
        "arbiter_phase.py", "soap_phase.py",
        "rotor_watson.py", "rotor_father.py", "rotor_mother.py", "rotor_arbiter.py", "rotor_soap.py",
        "pipeline_supervisor.py", "pipeline_timed_rotor.py", "eye_brancher.py", "rotor_turbo_pipeline.py"
    ]
    base = os.path.expanduser("~/Soap/agents")
    missing = [s for s in scripts if not os.path.isfile(os.path.join(base, s))]
    if missing:
        print("Missing agent pipeline files:")
        for m in missing:
            print(" -", m)
    else:
        print("All agent/rotor/pipeline files present.")

if __name__ == "__main__":
    healthcheck()
