from argparse import ArgumentParser, Namespace
from pathlib import Path
import re
from utils.pdf_util.utils import images_to_pdf
from utils.note_util.html import batch_html2text
from utils.note_util.text import batch_remove_pattern_lines
from utils.note_util.flomo import save_file_to_flomo, save_dir_to_flomo
from utils.config import (
    get_digitalocean_token,
    set_digitalocean_token,
    get_flomo_url,
    set_flomo_url,
)


def config_digitalocean(args: Namespace):
    if args.token:
        set_digitalocean_token(args.token)
    else:
        token = get_digitalocean_token()
        print(f"Current DigitalOcean token: {token}")


def update_digitalocean(args: Namespace):
    from utils.ip_util.digitalocean import DigitalOcean

    obj = DigitalOcean()
    obj.add_ssr_ip()
    obj.update()
    print("Firewall IPs in digitalocean are updated automatically!")


def img2pdf(args: Namespace):
    images_to_pdf(args.images, args.output)


def html2text(args: Namespace):
    batch_html2text(args.input, args.output)


def txt_clean(args: Namespace):
    batch_remove_pattern_lines(args.input, args.output, args.patterns)


def config_flomo(args: Namespace):
    if args.url:
        set_flomo_url(args.url)
    else:
        url = get_flomo_url()
        print(f"Current Flomo URL: {url}")


def flomo_save(args: Namespace):
    if args.input.is_file():
        save_file_to_flomo(args.input)
        print(f"{args.input.name} is saved to Flomo!")
    elif args.input.is_dir():
        save_dir_to_flomo(args.input)
        print(f"Files in '{args.input.name}' are saved to Flomo!")


def main():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(description="Tools for personal utilities.")
    # dititalocean util
    digitalocean_parser = subparser.add_parser("digitalocean", help="DigitalOcean Tool")
    digitalocean_parsers = digitalocean_parser.add_subparsers(
        description="Commands of DigitalOcean."
    )
    dg_config_parser = digitalocean_parsers.add_parser(
        "config", help="Config DigitalOcean API token."
    )
    dg_config_parser.add_argument(
        "--token",
        type=str,
        help="Set digitalOcean API token. Leave empty to get token from current config.",
    )
    dg_config_parser.set_defaults(func=config_digitalocean)
    dg_update_parser = digitalocean_parsers.add_parser(
        "update", help="Update DigitalOcean Firewall IPs."
    )
    dg_update_parser.set_defaults(func=update_digitalocean)
    # PDF util
    pdf_parser = subparser.add_parser("pdf", help="PDF Processing Tool")
    pdf_parser.set_defaults(func=img2pdf)
    pdf_parser.add_argument("--images", type=str, nargs="+", help="Input images.")
    pdf_parser.add_argument("-o", "--output", type=str, help="Output PDF path.")
    # note util
    note_parser = subparser.add_parser("note", help="Note Processing Tool")
    note_parsers = note_parser.add_subparsers(
        title="note", description="Commandline tools for processing notes."
    )
    # note.html util
    html_parser = note_parsers.add_parser("html", help="HTML Processing Tool")
    html_parser.add_argument("input", type=Path, help="Input HTML directory.")
    html_parser.add_argument("output", type=Path, help="Output HTML directory.")
    html_parser.set_defaults(func=html2text)
    # note.txt util
    text_parser = note_parsers.add_parser("text", help="Plain-text Processing Tool")
    text_parser.add_argument("input", type=Path, help="Input TXT directory.")
    text_parser.add_argument("output", type=Path, help="Output TXT directory.")
    text_parser.add_argument(
        "patterns", type=re.compile, nargs="+", help="Pattern to be removed."
    )
    text_parser.set_defaults(func=txt_clean)
    # note.flomo util
    flomo_parser = note_parsers.add_parser("flomo", help="Flomo Processing Tool")
    flomo_parsers = flomo_parser.add_subparsers(description="Commands of Flomo.")
    flomo_config_parser = flomo_parsers.add_parser("config", help="Config Flomo URL")
    flomo_config_parser.add_argument(
        "--url", type=str, help="Set Flomo URL. Leave empty to get from current config."
    )
    flomo_config_parser.set_defaults(func=config_flomo)
    flomo_save_parser = flomo_parsers.add_parser(
        "save", help="Save content from text to Flomo."
    )
    flomo_save_parser.add_argument(
        "input", type=Path, help="Input TXT file or directory."
    )
    flomo_save_parser.set_defaults(func=flomo_save)

    # parse arguments
    try:
        args = parser.parse_args()
    except re.error as e:
        print("Illegal pattern!", e)
    else:
        args.func(args)
