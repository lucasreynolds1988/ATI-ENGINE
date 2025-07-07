import os
from fpdf import FPDF
import json

def export_pdf(job_id, outfile=None):
    infile = f"{job_id}.arbiter.json"
    if not os.path.isfile(infile):
        print(f"{infile} not found.")
        return
    with open(infile) as f:
        sop = json.load(f)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"SOP Pipeline Report: {job_id}", ln=True, align="C")
    for k, v in sop.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)
    out = outfile or f"{job_id}.report.pdf"
    pdf.output(out)
    print(f"Exported {out}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        export_pdf(sys.argv[1])
    else:
        print("Usage: python pipeline_dashboard_pdf_export.py <job_id>")
