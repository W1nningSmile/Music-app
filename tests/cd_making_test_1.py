from PIL import Image, ImageOps

template_path = "cd_images/template.png"
photo_path = "songs\Album\Sheer Heart Attack\cover.png"
output_path = "cd_images/test_cd.png"


template = Image.open(template_path).convert("RGBA")
photo = Image.open(photo_path).convert("RGBA")

squared_photo = ImageOps.fit(photo, (736, 736), Image.Resampling.LANCZOS)

final_disc = Image.alpha_composite(squared_photo, template)

final_disc.save(output_path, "PNG")
print(f"Saving to {output_path} succeeded")

#spinning part
frames = []

for ang in range(0,360, 5):
    rotated_frame = final_disc.rotate(-ang, resample=Image.Resampling.BICUBIC)
    frames.append(rotated_frame)

frames[0].save(
    "cd_images/gif_output.gif", #gif output path
    save_all = True,
    append_images=frames[1:], #dont take frame 0 or else we will have 2 at angle 0
    duration =40,
    loop=0 #inf loop
)

#scrapped bc it took too much time to load and it doesnt look as good as i imagined :/ -->do some tests to find a way to reimplement (change frame amount/duration to make loading faster?) -> retouche template to make it cleaner