import os
import json


def load(path):
    file = open(path)
    lines = file.readlines()
    pdx_h, pdx_v = get_pdx(lines)
    return pdx_v
    # print(pdx_v)


def get_pdx(lines):
    header = None
    values = {}

    i = 0
    new_lines = []  # Create subset of value lines
    while i < (len(lines)):
        # print("i: " + str(i))
        line = lines[i]

        if [*line][0] != "#" and line.strip() != ("" or "}"):
            # print("Valid line: " + line[:-1])
            parts = line.split("=")
            if len(parts) > 1:
                # print("Line contains value")
                if [*(line.strip())][-1] == "{":
                    header = parts[0].strip()
                    # print("Header: " + header)

                    new_lines = []  # Create subset of value lines

                    if i != len(lines) - 1:
                        ii = i + 1
                        value_line = str(lines[ii])
                        closed_bracket_skip = 0

                        while value_line.find("}") == -1 or closed_bracket_skip > 0:
                            value_line = lines[ii]

                            # print("VL: " + value_line[:-1])
                            if value_line.find("{") != -1:
                                closed_bracket_skip += 1

                            if value_line.find("}") != -1:
                                closed_bracket_skip -= 1


                            new_lines.append(value_line)
                            if ii < len(lines) - 1:
                                ii += 1
                            else:
                                # print("Index too big")
                                break
                        # print("New Lines: " + str(new_lines))

                        i += len(new_lines)  # Skip new lines to not add their values directly into the set
                        # print("i was added to. i is now: "+ str(i))
                    new_header, new_values = get_pdx(new_lines)  # This seems dangerous, and it's because
                    # print("Received header: " + str(new_header))
                    # print("Received values: " + str(new_values))
                    # it is

                    if new_header is None:
                        values[header] = new_values
                    else:
                        if new_values.get(new_header):
                            values[header] = new_values
                        else:
                            values[new_header] = new_values
                else:
                    values[str(parts[0].strip())] = parts[1].split("#")[0].strip()
        i += 1

    if values.get(header):
        header = None
    print("Header [end]: " + str(header))
    print("Values: " + str(values))
    if new_lines:
        print("With lines: " + str(new_lines))
    return header, values
