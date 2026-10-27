import glob
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = []
checks = 0


def check(label, ok, detail=""):
    global checks
    checks += 1
    status = "ok" if ok else "FAIL"
    print(("check: %s %s %s" % (status, label, detail)).rstrip())
    if not ok:
        failures.append(label)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def main():
    from pypdf import PdfReader

    sheets = sorted(glob.glob(os.path.join(ROOT, "sheets", "*.html")))
    pdfs = sorted(glob.glob(os.path.join(ROOT, "printables", "*.pdf")))
    pdf_names = {os.path.basename(p) for p in pdfs}
    sheet_stems = {os.path.splitext(os.path.basename(s))[0] for s in sheets}

    check("seven sheet sources exist in sheets/", len(sheets) >= 7, "found %d" % len(sheets))

    for stem in sorted(sheet_stems):
        check("pdf built for %s" % stem, ("%s.pdf" % stem) in pdf_names)

    for path in sheets:
        name = os.path.basename(path)
        text = read_bytes(path).decode("utf-8", "replace")
        check("getting-started page in %s" % name, "Getting started" in text)
        check("multiple pages in %s" % name, text.count('class="pg"') >= 2)

    for path in pdfs:
        name = os.path.basename(path)
        try:
            reader = PdfReader(path)
            pages = len(reader.pages)
        except Exception as exc:
            check("pdf opens %s" % name, False, str(exc))
            continue
        check("pdf opens %s" % name, True, "pages=%d" % pages)
        check("at least 2 pages in %s" % name, pages >= 2, "got %d" % pages)
        try:
            first_page_text = reader.pages[0].extract_text() or ""
        except Exception:
            first_page_text = ""
        check("getting-started text on page 1 of %s" % name, "Getting started" in first_page_text)

        all_text = ""
        for page in reader.pages:
            try:
                all_text += (page.extract_text() or "") + "\n"
            except Exception:
                pass
        check("unbranded %s (no company name inside)" % name, "Asdale" not in all_text)
        check("unbranded %s (no site domain inside)" % name, "asdaledynamics" not in all_text.lower().replace(" ", ""))

    license_path = os.path.join(ROOT, "LICENSE")
    if os.path.exists(license_path):
        license_text = read_bytes(license_path).decode("utf-8", "replace")
        check(
            "LICENSE has exact copyright line",
            "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text,
        )
    else:
        check("LICENSE file exists", False)

    readme_path = os.path.join(ROOT, "README.md")
    if os.path.exists(readme_path):
        readme_text = read_bytes(readme_path).decode("utf-8", "replace")
        check("README.md credits Asdale Dynamics, LLC", "Asdale Dynamics, LLC" in readme_text)
    else:
        check("README.md exists", False)

    secret_patterns = [
        (r"AKIA[0-9A-Z]{16}", "aws key"),
        (r"BEGIN [A-Z ]*PRIVATE KEY", "private key"),
        (r"ghp_[A-Za-z0-9]{20,}", "github token"),
        (r"sk-[A-Za-z0-9_\-]{20,}", "api key"),
        (r"(api[_-]?key|secret|password|passwd|token)[ ]*[=:][ ]*[\"']?[A-Za-z0-9_\-]{16,}", "credential assignment"),
    ]
    skip_parts = (".git", "printables")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip_parts]
        for filename in filenames:
            full = os.path.join(dirpath, filename)
            rel = os.path.relpath(full, ROOT)
            ext = os.path.splitext(filename)[1].lower()
            if ext not in (".html", ".css", ".sh", ".py", ".md", ""):
                continue
            try:
                blob = read_bytes(full).decode("utf-8", "replace")
            except OSError:
                continue
            for pattern, label in secret_patterns:
                if re.search(pattern, blob):
                    check("no %s in %s" % (label, rel), False)

    if failures:
        print("checks: %d of %d checks failed" % (len(failures), checks))
        return 1
    print("checks: %d of %d checks passed" % (checks, checks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
