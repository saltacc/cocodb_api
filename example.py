import shutil

import coco_db

# create an instance of the database class

# 123.123.123.123 is the IP
# 5555 is the port
# example is the source name
# 0000.... is the auth key
# username is your username
db = coco_db.Database('123.123.123.123', 5555, 'example', '00000000-0000-0000-0000-00000000000', 'username')


# gets the total images
db.get_entry_total()

# gets the metadata for a current entry in the database
# 123456 is the entry ID
db.get_entry_meta(123456)

# download an image from the database as bytes
# 123456 is the entry ID
image, ext = db.get_entry_image(123456, return_image_ext=True)

# upload an image to the database as bytes

# image is the image as bytes
# 'test'+ext is the filename
# 123456 is the entry ID
# 0 is the unix timestamp of when the original image was uploaded (don't use 0, this is for an example)
# 'foo':'bar' is the metadata of the image
db.upload_image(image, 'test'+ext, 123456, 0, {'foo': 'bar'})

# get a stream to an image from the database
# 123456 is the entry ID
image, ext = db.get_entry_image(123456, stream=True, return_image_ext=True)

# stream an image to the database

# images is the image as a stream
# 'test'+ext is the filename
# 123456 is the entry ID
# 0 is the unix timestamp of when the original image was uploaded (don't use 0, this is for an example)
# 'foo':'bar' is the metadata of the image
db.upload_image(image, 'test'+ext, 123456, 0, {'foo': 'bar'})

