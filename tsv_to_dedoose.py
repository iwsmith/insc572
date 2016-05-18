#!/usr/bin/env python3
from functools import partial

HEADERS = {
        "Have you read the above Consent to Participate and agree to participate in this study?" : "Consent",
        "Which region of the United States do you live in?" : "Region",
        "Do you live in an urban, suburban, or rural area?" : "Urban/Suburban/Rural",
        "Which racial/ethnic group(s) do you identify with?" : "Race",
        "What is your religious affiliation? Mark all that apply." : "Religion",
        "What is your sexual identity?" : "Sexual Identity",
        "Describe how you have used Grindr?" : "Grindr Use",
        "Have you ever uploaded a profile picture to Grindr?" : "Have Profile Photo",
        "Why have you never uploaded a profile picture to Grindr?" : "Why No photo",
        "Describe your current Grindr profile picture." : "Current Photo",
        "Have you ever used a profile picture in which you were unidentifiable (e.g. torso shot) or not present (e.g. car, beach) in the picture ?" : "Ever Unidentifiable",
        "When have you used an unidentifiable picture on your Grindr profile?" : "When Unidentifiable",
        "Why do you always use a profile picture that is not identifiable?" : "Why Always Unidentifiable",
        "Why do you sometimes use a picture that is not identifiable?" : "Why Sometimes Unidentifiable",
        "Why do you change between identifiable pictures and unidentifiable pictures?" : "Why Alternate Idenifiable",
        "What do you think of other users who are not identifiable in their profile picture?" : "Unidentifiable Others: Your Thoughts",
        "Why do you believe these users choose to be unidentifiable?": "Unidentifiable Others: Why",
        "How \"Out\" Are You? [mother/caretaker]": "Out: mother",
        "How \"Out\" Are You? [father/caretaker]": "Out: father",
        "How \"Out\" Are You? [siblings (sisters, brothers)]": "Out: siblings",
        "How \"Out\" Are You? [extended family/relatives]": "Out: extended family",
        "How \"Out\" Are You? [my new straight friends]": "Out: new straight friends",
        "How \"Out\" Are You? [my work peers]": "Out: work peers",
        "How \"Out\" Are You? [my work supervisor(s)]": "Out: work supervisor",
        "How \"Out\" Are You? [members of my religious community (e.g., church, mosque, temple)]": "Out: religious community",
        "How \"Out\" Are You? [leaders of my religious community (e.g., church, mosque, temple)]": "Out: religious leaders",
        "How \"Out\" Are You? [strangers, new acquaintances]": "Out: strangers",
        "How \"Out\" Are You? [my old straight friends]": "Out: old straight friends",
        "Have you ever perceived discrimination because of your sexual orientation?": "Descrimination",
        "I am treated with less courtesy than other people are.": "Descrimination: Less Courtesy",
        "I am treated with less respect than other people are.": "Descrimination: Less Respect",
        "I receive poorer service than other people at restaurants or stores.": "Descrimination: Poor Service",
        "People act as if they think I am not smart.": "Descrimination: Dumb",
        "People act as if they are afraid of me.": "Descrimination: Fear",
        "People act as if they think I am dishonest.": "Descrimination: Distrust",
        "People act as if they're better than me.": "Descrimination: Inferior",
        "I am called names or insulted.": "Descrimination: Insult",
        "I am threatened or harassed.": "Descrimination: Threatened",
        "Anything else you want us to know?": "Comments"
        }

RACES = { 
        "American Indian, Alaskan Native, Native Hawaiian",
        "African American, Black",
        "Asian (Japanese, Chinese, Korean, Filipino, Vietnamese)",
        "Hispanic, Latino",
        "Asian Indian",
        "White" 
        }

RELIGIONS = {
        "Agnostic",
        "Atheist",
        "Buddhist",
        "Catholic",
        "Christian",
        "Hindu",
        "Jewish",
        "Muslim",
        "New Age",
        "No religious affiliation",
        "Pagan",
        "Protestant",
        "Sikh",
        "Spiritual (not religious)"
        }

SEXUAL_IDENTITY = {
        "Asexual",
        "Bisexual",
        "Demisexual",
        "Gay",
        "Heteroflexible",
        "Homoflexible",
        "Lesbian",
        "Pansexual",
        "Queer",
        "Questioning",
        "Sapiosexual",
        "Straight"
        }

def filter_column(known, entry):
    if entry and entry not in known:
        return "Other"
    return entry

FIELDS = {
        "Consent": lambda x: x == "Yes, I have read the Consent to Participate and agree to participate.",
        "Race": partial(filter_column, RACES),
        "Religion": partial(filter_column, RELIGIONS),
        "Sexual Identity": partial(filter_column, SEXUAL_IDENTITY)
        }

def update_field(quote, field):
    return HEADERS.get(field, field)

def update_head(line, delimiter="\t", quote='"'):
    fields = [ s.strip().strip('"') for s in line.split(delimiter) ]
    new_fields = list(map(partial(update_field, quote), fields))
    return new_fields

def update_row(row_dict):
    for k, v in row_dict.items():
        if k in FIELDS:
            row_dict[k] = FIELDS[k](v)
    return row_dict

if __name__ == "__main__":
    import argparse
    import sys
    from csv import DictReader, DictWriter, QUOTE_ALL
    parser = argparse.ArgumentParser(description="Convert TSV to a format Dedoose likes")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--delimiter', '-d', default="\t")
    args = parser.parse_args()

    header = update_head(args.infile.readline(), delimiter=args.delimiter)

    rows = DictReader(args.infile, fieldnames=header, dialect='excel-tab')
    writer = DictWriter(args.outfile, fieldnames=header, quoting=QUOTE_ALL)

    writer.writeheader()
    writer.writerows(map(update_row, rows))
