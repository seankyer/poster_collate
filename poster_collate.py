#!/usr/local/bin/python3

import subprocess
import csv
import os
import sys

from pdfrw import PdfReader
from pdfrw import PdfWriter

MISSED_POSTERS = []



def main(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        poster_output = PdfWriter()
        page_count = 0
        poster_count = 0
        document_count = 1
        for row in csv_reader:
            poster_name = row[0].replace(" ", "") + ".pdf"
            file_path = os.path.join("/Users/prepress-2/Documents/Posters_11x17", poster_name)
            print(file_path)

            # Check is file can be found, if not make note for manual adjustment later on
            if not os.path.isfile(file_path):
                MISSED_POSTERS.append(poster_name + " " + row[2])
                continue

            poster = PdfReader(file_path)
            poster = poster.pages[0]
            for n in range(int(row[2])):
                if page_count < 25:
                    poster_output.addpage(poster)
                    page_count += 1
                    poster_count += 1
                else:
                    poster_output.write("/Users/prepress-2/Desktop/JerrysPosters_{}.pdf".format(document_count))
                    poster_output = PdfWriter()
                    poster_output.addpage(poster)
                    page_count = 1
                    poster_count += 1
                    document_count += 1

    poster_output.write("/Users/prepress-2/Desktop/JerrysPosters_{}.pdf".format(document_count))

    show_missed(poster_count)


def show_missed(poster_count):
    text = ""
    if MISSED_POSTERS:
        print("Files Missed: ")
        text = "Files Missed: "
        for i in MISSED_POSTERS:
            text = text + ", \n{}".format(i)
            title_alert = "Missed Poster Files: "

        os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title_alert))

    f = open("/Users/prepress-2/Desktop/JerryPosterResult.txt", "w")
    f.write(text)
    f.write("\n\nTotal Posters: {}".format(poster_count))
    f.close()

if __name__ == '__main__':
    #csv_path = "test.csv"
    csv_path = sys.argv[1]
    main(csv_path)
