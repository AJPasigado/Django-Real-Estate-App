import sys
import zipfile
import os
command = sys.argv[1]

if command == "dump":
    path = '../media/uploads/'
    def zipdir(path, ziph):
    # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    if __name__ == '__main__':
        zipf = zipfile.ZipFile('fixtures/media.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir('media/uploads', zipf)
        zipf.close()
        print("Media files dumped.")
if command == "load":
    with zipfile.ZipFile("fixtures/media.zip","r") as zip_ref:
        zip_ref.extractall("")
        print "Media files loaded."