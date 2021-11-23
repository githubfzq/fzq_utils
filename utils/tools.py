from argparse import ArgumentParser, Namespace
from utils.ip_util.digitalocean import DigitalOcean
from utils.pdf_util.utils import images_to_pdf


def update_digitalocean(args: Namespace):
    obj = DigitalOcean()
    obj.add_ssr_ip()
    obj.update()
    print('Firewall IPs in digitalocean are updated automatically!')

def img2pdf(args: Namespace):
    images_to_pdf(args.images, args.output)


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
    # parse arguments
    args = parser.parse_args()
    args.func(args)
