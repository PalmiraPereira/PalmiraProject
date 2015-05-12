__author__ = 'Palmira Pereira'
text_file = open("triangle_upload.dat", "w")

text_file.write("TITLE=\"TRIANGLE UPLOAD\"\n")
text_file.write("VARIABLES= \"X\",\"Y\"\n")
text_file.write("ZONE N=3, E=1,F=FEPOINT ET=Triangle\n")
text_file.write("1 1\n")
text_file.write("2 1\n")
text_file.write("1 2\n")
text_file.write("\n")
text_file.write("1 2 3\n")

text_file.close()