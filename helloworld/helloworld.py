# downloading images source: https://pypi.org/project/google-images-download/

from google_images_download import google_images_download #importing library

response = google_images_download.googleimagesdownload()

                # list of arguments
arguments = {"keywords":"drift car, nissan 350z, modified car","limit":5,"print_urls":True}
paths = response.download(arguments) # passing arguments
print(paths)

# if ran in filezilla, will create a download file with all images inside

