# Refractoring changes done

## General Changes throughout the project
- Changed variable names in all files to make the code more readable and maintainable
- Added correct spacimng, tabs etc
- removed unused imports

## views.py
- check ownership of user (TODO Solved)- Security Issue resolved
## frecapi.py

###  get_face_encoding 
- combined get_face_encoding and get_face_encoding_b64 to a single function using a flag to tell if its b64 or not thereby increasing readability and reducing redundancy.
-added check whether encoding is null, raise exception else proceed, also check if image is null raise exception
### mark_faces
- printed the exception for debugging when face not found
### get_known_faces
- if no file provided, raise exception
- if image cannot be loaded raise exception
- if more than one face found, print error and dont add any face

### is_person_in_photo
- if more than one face detected in the person's photo raise exception
## common.py
### random_string
- separated all function calls to make it easy to read, understand and edit
### jinja2_filter_datefmt
- Updated name of this function
- if date is not string then raise exception