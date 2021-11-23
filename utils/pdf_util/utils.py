from PIL import Image

def images_to_pdf(images, saving_path):
    imgs = [Image.open(p) for p in images]
    imgs[0].save(saving_path, 'PDF', save_all=True, resolution=100.0, append_images=imgs[1:])