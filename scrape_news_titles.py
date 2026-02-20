from tempfile import NamedTemporaryFile
import webbrowser
from bs4 import BeautifulSoup

def view_in_browser(html):
    with NamedTemporaryFile("wb", delete=False, suffix=".html") as file:
        file.write(html.encode('utf'))
    webbrowser.open_new_tab(f"file://{file.name}")



soup = BeautifulSoup(html_code, 'html.parser')

def custom_selector(tag, text_sample):
	return tag.name=='a' and text_sample in tag.text and ( tag.has_attr("class") or tag.has_attr("id") )

def count_children(main_tag):
    return len(main_tag.find_all())

def find_childmost_tags(main_tag):
    child_list = []
    for tag in main_tag.find_all():
        if count_children(tag) == 0:
            child_list.append(tag)
    return child_list

def find_childmost_with_text(main_tag):
    child_list = find_childmost_tags(main_tag)
    tags_with_text = []
    for tag in child_list:
        if tag.text != '':
            tags_with_text.append(tag)
    return tags_with_text

tags_with_text = find_childmost_with_text(soup)
len(tags_with_text)

def first_parent_with_class(main_tag):
    temp_tag = main_tag
    while temp_tag.has_attr('class') == False:
        temp_tag = temp_tag.parent
    return temp_tag

def get_class_with_string(tags_with_text_list, sample_str):
    i = 0
    for tag in tags_with_text_list:
        if sample_str in tag.text:
            selected_tag = tag
            i += 1
    if i > 1:
        print("Too many matches with the given string!")
        return 0
    tag_with_class = first_parent_with_class(selected_tag)
    return tag_with_class.attrs['class'][0]

