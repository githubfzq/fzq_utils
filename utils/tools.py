from argparse import ArgumentParser, Namespace
from pathlib import Path
import re
from utils.ip_util.digitalocean import DigitalOcean
from utils.pdf_util.utils import images_to_pdf
from utils.note_util.html import batch_html2text
from utils.note_util.text import batch_remove_pattern_lines


def update_digitalocean(args: Namespace):
    obj = DigitalOcean()
    obj.add_ssr_ip()
    obj.update()
    print('Firewall IPs in digitalocean are updated automatically!')

def img2pdf(args: Namespace):
    images_to_pdf(args.images, args.output)

def html2text(args: Namespace):
    batch_html2text(args.input, args.output)

def txt_clean(args: Namespace):
    batch_remove_pattern_lines(args.input, args.output, args.patterns)



def main():
    parser = ArgumentParser()
    subparser = parser.add_subparsers(title='Utilities', description='Commandlines of personal utilities.')
    # dititalocean util
    digitalocean_parser = subparser.add_parser('digitalocean')
    digitalocean_parser.set_defaults(func = update_digitalocean)
    # PDF util
    pdf_parser = subparser.add_parser('pdf')
    pdf_parser.set_defaults(func=img2pdf)
    pdf_parser.add_argument('--images', type=str, nargs='+', help='Input images.')
    pdf_parser.add_argument('-o', '--output', type=str, help='Output PDF path.')
    # note util
    note_parser = subparser.add_parser('note')
    note_parser.add_argument('input', type=Path, help='Input HTML directory.')
    note_parser.add_argument('output', type=Path, help='Output HTML directory.')
    note_parsers = note_parser.add_subparsers(title='note', description='Commandline tools for processing notes.')
    html_parser = note_parsers.add_parser('html')
    html_parser.set_defaults(func=html2text)
    text_parser = note_parsers.add_parser('text')
    text_parser.add_argument('patterns', type=re.compile, nargs='+', help='Pattern to be removed.')
    text_parser.set_defaults(func=txt_clean)
    # parse arguments
    try:
        args = parser.parse_args()
    except re.error as e:
        print('Illegal pattern!', e)
    else:
        args.func(args)
