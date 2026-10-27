import glob
import os
import sys


def validate_dir(directory):
    try:
        from pypdf import PdfReader
    except ImportError:
        PdfReader = None

    pdfs = sorted(glob.glob(os.path.join(directory, "*.pdf")))
    if not pdfs:
        print("validate: FAIL no PDFs found in %s" % directory)
        return 1

    failures = []
    for path in pdfs:
        name = os.path.basename(path)
        problems = []
        try:
            with open(path, "rb") as handle:
                data = handle.read()
        except OSError as exc:
            print("validate: FAIL %s (unreadable: %s)" % (name, exc))
            failures.append(name)
            continue

        if len(data) < 2000:
            problems.append("file too small (%d bytes)" % len(data))
        if not data.startswith(b"%PDF-"):
            problems.append("missing %%PDF header")
        trailer = data.rstrip()
        if not trailer.endswith(b"%%EOF"):
            problems.append("missing %%EOF trailer")

        pages = -1
        if PdfReader is not None:
            try:
                reader = PdfReader(path)
                pages = len(reader.pages)
                if pages < 2:
                    problems.append("expected at least 2 pages, got %d" % pages)
            except Exception as exc:
                problems.append("pypdf could not open: %s" % exc)
        else:
            count = data.count(b"/Type /Page") - data.count(b"/Type /Pages")
            pages = max(count, 0)
            if pages < 2:
                problems.append("expected at least 2 page objects, found %d" % pages)

        if problems:
            failures.append(name)
            for problem in problems:
                print("validate: FAIL %s (%s)" % (name, problem))
        else:
            print("validate: PASS %s (pages=%d, %d KB)" % (name, pages, len(data) // 1024))

    if failures:
        print("validate: %d of %d PDFs failed" % (len(failures), len(pdfs)))
        return 1
    print("validate: all %d PDFs valid" % len(pdfs))
    return 0


def main():
    if len(sys.argv) != 2:
        print("usage: validate.py <dir-with-pdfs>")
        return 2
    return validate_dir(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
