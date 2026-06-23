from PIL import Image, ImageOps #PIL = Pillow

template_path = "cd_images/template.png"
photo_path = "cd_images/test_album.jpg"
output_path = "cd_images/test_cd.png"


template = Image.open(template_path).convert("RGBA")
photo = Image.open(photo_path).convert("RGBA")

squared_photo = ImageOps.fit(photo, (736, 736), Image.Resampling.LANCZOS)
final_disc = Image.alpha_composite(squared_photo, template)

#creates a white underlayer to hide the black background
white_bg = Image.new("RGBA", final_disc.size, (255,255,255,255))
disc_on_white = Image.alpha_composite(white_bg, final_disc)

#final_disc.save(output_path, "PNG")
print(f"Saving to {output_path} succeeded")

#spinning part
frames = []

for ang in range(0,360, 4):
    rotated_frame = final_disc.rotate(-ang, resample=Image.Resampling.BILINEAR, fillcolor=(255,255,255,255)) #bilinear is faster than cubic
    frames.append(rotated_frame.convert("P", palette=Image.Palette.ADAPTIVE)) #aparently makes the gif size tiny while barely sacrificing quality

frames[0].save(
    "cd_images/gif_output.gif", #gif output path
    save_all = True,
    append_images=frames[1:], #dont take frame 0 or else we will have 2 at angle 0
    duration =45,
    loop=0, #inf loop
    optimize = True,
    disposal=2 #clears previous frames 
)

#scrapped bc it took too much time to load and it doesnt look as good as i imagined :/ -->do some tests to find a way to reimplement (change frame amount/duration to make loading faster?) -> retouche template to make it cleaner
#scrap what i said above, it might be usable now since its light and fast --> test it out soon?