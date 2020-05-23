import os, sys, argparse


def walk_thru_dir(file_dir, recursive=False, phrases=[], tag='[]'):
    os.chdir(file_dir)

    os.walk(file_dir)

    left_tag = tag[0]
    right_tag = tag[1]

    for root, dirs, files in os.walk(file_dir):

        for filename in files:
            new_filename = clean_name(filename, left_tag=left_tag, right_tag=right_tag, phrases=phrases)

            if new_filename:
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
                print("Renamed '{}' to '{}'".format(filename, new_filename))


def clean_name(file, left_tag=None, right_tag=None, phrases=None):

    if file[0] in  [ '.', '_' ]:
        return

    filename = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    new_filename = filename.replace('.',' ').replace('_', ' ').strip()

    if (new_filename.count(left_tag) + new_filename.count(right_tag)) % 2 == 1:
        print("Could not remove tags from '{}'! Has mismatching delimeters.".format(file))

        return


    if left_tag and right_tag:
        while left_tag in new_filename and right_tag in new_filename:
            tag = new_filename[ new_filename.find(left_tag) : new_filename.find(right_tag) + 1]
            new_filename = new_filename.replace(tag, '')
            new_filename = new_filename.strip()


    if phrases and any(phrase in new_filename for phrase in phrases):
        for phrase in phrases:
            new_filename = new_filename.replace(phrase, '').strip()

    if not new_filename:
        print("Could not remove tags from '{}'! Result filename is None.".format(file))

        # return


    new_file = '{}{}'.format(new_filename.strip(), extension)

    if new_file == file:
        # print("No tags found in '{}'! Nothing changed.".format(file))

        return 


    # print(new_file)
    return(new_file)



if __name__ == "__main__":


    parser = argparse.ArgumentParser()

    parser.add_argument('file_dir', help='root filepath')
    parser.add_argument('-R', '--recursive', help="Process files recursively", action="store_true")
    parser.add_argument('-t', '--tag', help="Specify a pair of characters the signify a tag. Default is '[]'")
    parser.add_argument('-p', '--phrases', help='List of phrases to be removed from filenames')
    args = parser.parse_args()

    file_dir = args.file_dir

    recursive = args.recursive
    tag = args.tag
    phrases = args.phrases

    walk_thru_dir(file_dir, recursive)