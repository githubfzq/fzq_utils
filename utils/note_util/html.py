from pathlib import Path
from bs4 import BeautifulSoup


def html_to_text(output_dir, file_path):
    with file_path.open("r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    output_file_path = output_dir / (file_path.stem + ".txt")
    with output_file_path.open("w", encoding="utf-8") as f:
        text = soup.text
        lines = text.splitlines()
        lines = filter(lambda x: x.strip(), lines)
        f.writelines(line+'\n' for line in lines)

def batch_html2text(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    for file_path in input_dir.glob("*.html"):
        html_to_text(output_dir, file_path)

