import os
import json


def load(path):
    file = open(path)
    lines = file.readlines()
    pdx_h, pdx_v = get_pdx(lines)
    return dict(pdx_v)


def loads(string):
    lines = str(string).splitlines()
    pdx_h, pdx_v = get_pdx(lines)
    return pdx_v


def dump_dict(content_dict, path):
    assert type(content_dict) == dict
    file = open(path, 'w')
    lines = []

    file.writelines(lines)


def set_pdx(content_dict, cycle=0):
    # print(colored("Started new cycle with value " + str(cycle), "yellow"))
    lines = []
    if type(content_dict) == dict:
        for idea_key in content_dict.keys():
            # lines.append(idea_key + " = " + "{\n")
            # print("Type of content_dict: " + str(type(content_dict)))
            # print("Type of content_dict[idea]: " + str(type(content_dict[idea_key])))
            if not type(content_dict[idea_key]) == str:
                lines.append("\t" * cycle + idea_key + " = {\n")
                # print(colored("Appended " + idea_key + " = {\n", "green"))

                for i, (k, v) in enumerate(content_dict[idea_key].items()):
                    # print(str(k) + ": " + str(v))
                    if len(v) > 1 and type(v) == dict and type(v[list(v.keys())[-1]]) != (float or int):
                        lines += set_pdx({k: v}, cycle + 1)
                    else:
                        print(k, v)
                        if type(v) != str:
                            vkl = list(v.keys())
                            vvl = list(v.values())
                            if (vkl == [] or vkl is None) or (vvl == [] or vvl is None):
                                break
                            v_key = vkl[len(vkl) - 1]
                            v_val = vvl[len(vvl) - 1]
                        else:
                            v_key = k
                            v_val = v
                        lines.append("\t" * (cycle+1) + str(v_key) + " = " + str(v_val) + "\n")
                        # print(colored("Appended " + lines[-1], 'green'))
                lines.append("\t" * cycle + "}\n")
            # else:
            # print(content_dict[idea_key] + " :" + str(content_dict[idea_key]))
    return lines


def get_pdx(lines, cycle=0):
    header = None
    values = {}

    i = 0
    new_lines = []  # Create subset of value lines
    while i < (len(lines)):
        # print("i: " + str(i))
        line = lines[i]
        if line.strip() != ("" or "}" or '\n') and len([*line.strip()]) > 0:
            if ([*line][0] != "#" or cycle > 0) \
                    and line.strip():
                # print("Valid line: " + str(ascii(line)))
                parts = line.split("#")[0].split("=")
                if len(parts) > 1:
                    # print("Line contains value")
                    if [*(parts[1].strip())][-1] == "{":
                        header = parts[0].strip()
                        # print("Header: " + header)
                        # print("Cycle: " + str(cycle))

                        new_lines = []  # Create subset of value lines

                        if i != len(lines) - 1:
                            ii = i + 1
                            value_line = str(lines[ii])
                            closed_bracket_skip = 0
                            if cycle == 0:
                                closed_bracket_skip = 1
                            while value_line.find("}") == -1 or closed_bracket_skip > 0:
                                value_line = lines[ii]

                                # print("VL: " + value_line[:-1])
                                if value_line.find("{") != -1:
                                    # print("Found an open bracket!")
                                    closed_bracket_skip += 1
                                    # print("Closed bracket skip is now: " + str(closed_bracket_skip))

                                if value_line.find("}") != -1:
                                    # print("Found a closed bracket!")
                                    closed_bracket_skip -= 1

                                new_lines.append(value_line)
                                if ii < len(lines) - 1:
                                    ii += 1
                                else:
                                    # print("Index too big")
                                    break
                            # print("Finished space between { and } in cycle " + str(cycle))
                            # print("Value Lines: " + str(new_lines))

                            i += len(new_lines)  # Skip new lines to not add their values directly into the set
                            # print("i was added to. i is now: "+ str(i))
                        new_header, new_values = get_pdx(new_lines, cycle=cycle + 1)  # This seems dangerous, and it's
                        # because it is
                        # print("Received header: " + str(new_header))
                        # print("Received values: " + str(new_values))

                        if new_header is None and cycle > 0:
                            values[header] = new_values
                        else:
                            if new_values.get(new_header):
                                values[header] = new_values
                            else:
                                values[new_header] = new_values
                    else:
                        if parts[1].split("#")[0].strip() is not None:
                            values[str(parts[0].strip())] = (parts[1].split("#")[0]).strip()

                elif [*line.strip()][0] == "#" and cycle > 0 and len(lines) == 2:
                    values = {}
                    # print("Added line as reference")
                else:
                    values[str(parts[0].strip())] = line
        # else:
        # print("invalid line: " + line.strip())
        i += 1

    # if values.get(header):
    #    header = None
    # print("Header [end]: " + str(header))
    # print("Values: " + str(values))
    # if new_lines:
    #     print("With lines: " + str(new_lines))
    return header, values


'''tst_dict = load("test_idas.txt")
print(tst_dict)
tst_lines = set_pdx(tst_dict)
print("-----Final Lines------")
s = ""
for line in tst_lines:
    s += line
print(s)'''
