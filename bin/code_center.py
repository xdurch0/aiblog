import re
import sys


def center_code(html_string):
    insert_start = '<div class="container">'
    code_starts = [match.start() for match in re.finditer("<pre>", html_string)]
    for ind, start in enumerate(code_starts):
        # gotta adjust for the shift each time we insert
        start = start + ind*len(insert_start)
        html_string = html_string[:start] + insert_start + html_string[start:]

    insert_stop = '</div>'
    code_stops = [match.start() for match in re.finditer("</pre>", html_string)]
    for ind, stop in enumerate(code_stops):
        stop = stop + ind*len(insert_stop) + len("</pre>")
        html_string = html_string[:stop] + insert_stop + html_string[stop:]

    return html_string


def main(filename):
    with open(filename, "r") as file:
        as_string = file.read()
    centered = center_code(as_string)

    with open(filename, "w") as file:
        file.write(centered)


if __name__ == "__main__":
    fname = sys.argv[1]
    main(fname)
