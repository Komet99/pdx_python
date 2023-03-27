from collections import OrderedDict


def load(path):
    file = open(path)
    lines = file.readlines()
    pdx_h, pdx_v = get_pdx(lines)
    return pdx_v


def loads(string):
    lines = str(string).splitlines()
    pdx_h, pdx_v = get_pdx(lines)
    return pdx_v


def dump_dict(content_dict, path):
    file = open(path, 'w')
    lines = set_pdx(content_dict)
    file.writelines(lines)
    file.close()


def set_pdx(content_dict, cycle=0):
    # print(colored("Started new cycle with value " + str(cycle), "yellow"))
    lines = []
    if type(content_dict) is (OrderedDict or dict):
        for idea_key in content_dict.keys():
            # print("Type of content_dict: " + str(type(content_dict)))
            # print("Type of content_dict[idea]: " + str(type(content_dict[idea_key])))
            if type(content_dict[idea_key]) is OrderedDict or \
                    type(content_dict[idea_key]) is dict:
                lines.append("\t" * cycle + idea_key + " = {\n")
                for k, v in content_dict[idea_key].items():
                    # print(str(k) + ": " + str(v))
                    if type(v) is OrderedDict or \
                            type(v) is dict and \
                            bool(v.items()) is True:
                        # print("Value is a dictionary: " + str(v))
                        lines += set_pdx(OrderedDict({k: v}), cycle + 1)
                    elif type(v) is OrderedDict or \
                            type(v) is dict and \
                            bool(v.items()) is False:
                        lines.append("\t" * (cycle + 1) + k + " = {\n")
                        lines.append("\t" * (cycle + 2) + "#Some Reference\n")
                        lines.append("\t" * (cycle + 1) + "}\n")
                    else:
                        lines.append("\t" * (cycle + 1) + str(k) + " = " + str(v) + "\n")
                lines.append("\t" * cycle + "}\n")
            else:
                lines.append("\t" * cycle + str(idea_key) + " = " + str(content_dict[idea_key]) + "\n")
    return lines


def get_pdx(lines, cycle=0):
    """
    Let me try to explain this function in case I will work on it again and forget everything

    lines: Lines is the lines to read; this is an array of strings.
    cycle: This is where it gets complicated. Cycle is the amount of iterations this function has done.

    The way this function works:
    It first goes through each line individually, starting at the top. While the line is either a Value, such as
        idea_cost = -0.1
    or an idea, meaning a value containing other values, such as
        start = {
            idea_cost = -0.1
            improve_relation_modifier = 0.25
        }
    the program will continue.

    The program will first split a line by its =, so

            "start = {"
    would be
            ["start","{"]

    and

            "idea_cost = -0.1"
    would be
            ["idea_cost","0.1"].

    This way, the program can first determine whether the line contains a header-value (such as start),
    by testing if the second part is a "{". If so, the first part would become the value "header",
    which will be returned. Now, the following lines are the values fitting the header. These values however can contain
    further header-values inside them.
    The solution is a somewhat wacky one:
    The program finds the amount of lines it has to read in that value and reads them using this function once again,
    simply pasting the header and value contents as they are being read. Some malfunctions would now occur, because
    it could happen, that a value looked like this:
        the_shroud_of_turin = {
            #effect in SAV_ideas
            #papal_influence = 1
            #prestige = 0.5
        }
    In this case, the values would be nothing, as all lines were skipped. This would later pose a problem, because pdx
    code cannot execute completely empty header-values (which means their code actually interprets comments, how
    terribly inefficient! qwq).
    To prevent this issue, a value "cycle" is passed, that tells the program to apply a different ruleset, in which
    comments are noticed and simply changed to "#Some Reference".
    "cycle" could easily be a bool, but having it as an integer makes debugging simpler and
    helps to illustrate how the program works, while also making it secure to always arrive back at its original state.
    """

    header = None
    values = OrderedDict()

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
                # This will take only the part that stands before a comment. Extremely important for situations like:
                '''
                the_shroud_of_turin = { #effect in SAV_ideas
                #		papal_influence = 1
                #		prestige = 0.5
                    }
                '''
                # The comment would otherwise be misinterpreted by the system
                if len(parts) > 1:
                    # Line contains an "=" -> contains a value
                    if [*(parts[1].strip())][-1] == "{":
                        header = parts[0].strip()
                        # print("New Header: " + header)
                        # print("Cycle: " + str(cycle))

                        new_lines = []  # Create subset of value lines
                        '''
                        This is specifically for header-values, which go like this:
                        header = {
                            blabla = 1
                            booboo = -0.1
                        }
                        '''

                        if i != len(lines) - 1:
                            ii = i + 1
                            closed_bracket_skip = 0
                            value_line = lines[ii]
                            if cycle == 0:
                                closed_bracket_skip = 1
                            while value_line.find("}") == -1 or closed_bracket_skip > 0:
                                value_line = lines[ii]

                                # print("VL in cycle " + str(cycle) + ": " + value_line[:-1])
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
                        else:
                            print("Program failed due to missing bracket")
                            # print("Finished space between { and } in cycle " + str(cycle))
                            # print("Value Lines: " + str(new_lines))

                        i += len(new_lines)  # Skip new lines to not add their values directly into the set
                        # print("i was added to. i is now: " + str(i))
                        new_header, new_values = get_pdx(new_lines, cycle=cycle + 1)
                        # This seems dangerous, and it's because it is
                        # This should in theory resolve everything in the right order. However, it does not.

                        if new_header is None and cycle > 0:
                            values[header] = new_values
                        elif cycle > 0:
                            values[new_header] = new_values
                        else:
                            values[header] = new_values
                    else:
                        values[str(parts[0].strip())] = (parts[1]).strip()
                        # For simple values, such as
                        '''
                        idea_cost = -0.1
                        '''
                        # This does the trick

                elif [*line.strip()][0] == "#" and cycle > 0:
                    # Originally there was a check here which tested
                    # whether len(lines) == 2. Didn't understand it, removed it.
                    values = {}
                    # print("Added line as reference")
                # if not, it's an invalid line
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


def test():
    tst_dict = load("tst.txt")
    print("Ideaset as array: " + str(tst_dict))
    tst_lines = set_pdx(tst_dict)
    print("-----Final Lines------")
    s = ""
    for line in tst_lines:
        s += line
    print(s)


test()
