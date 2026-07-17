import json
from pathlib import Path
from typing import Any

from docx import Document
from pypdf import PdfReader

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CV_CACHE_FILE = DATA_DIR / "cv_cache.json"


def find_cv() -> Path:
    for filename in ("CV.pdf","CV.docx","CV.txt"):
        cv_file = ROOT_DIR / filename

        if cv_file.is_file():
            return cv_file

    raise FileNotFoundError(
        "Add CV.pdf, CV.docx, or CV.txt to the project root."
    )


def read_cv(cv_file: Path) -> str:
    extension = cv_file.suffix.lower()

    if extension == ".pdf":
        text = "\n".join(
            page.extract_text() or ""
            for page in PdfReader(cv_file).pages
        )

    elif extension == ".docx":
        text = "\n".join(
            paragraph.text
            for paragraph in Document(cv_file).paragraphs
            if paragraph.text.strip()
        )

    elif extension == ".txt":
        text = cv_file.read_text(encoding="utf-8")

    else:
        raise ValueError(f"Unsupported CV format: {extension}")

    text = text.strip()

    if not text:
        raise ValueError("The CV contains no readable text.")

    return text


def cache_is_valid(cv_file: Path) -> bool:
    return (
        CV_CACHE_FILE.is_file()
        and CV_CACHE_FILE.stat().st_mtime
        >= cv_file.stat().st_mtime
    )


def load_cached_cv() -> dict[str, Any] | None:
    try:
        data = json.loads(
            CV_CACHE_FILE.read_text(encoding="utf-8")
        )

        if not isinstance(data, dict):
            return None

        return data

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):
        return None


def save_cv_cache(cv_data: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    CV_CACHE_FILE.write_text(
        json.dumps(
            cv_data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


