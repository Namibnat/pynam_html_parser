

import textwrap

import yaml
from flask import Flask, render_template, request

app = Flask(__name__)


class HTMLParser:
    def __init__(self):
        self.head = """
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <link rel='stylesheet' href='style.css'>
        </head>

        <body>
        """
        self.lines = []
        self.foot = """
        </body>

        </html>
        """

    def write_html_file(self):
        output_lines = "\n".join(self.lines)
        html = "".join([self.head, output_lines, self.foot])
        html = textwrap.dedent(html)
        with open('templates/index.html', 'w') as fp:
            fp.write(html)

    def make_section(self, class_name, section):
        self.lines.append(f"\n<div class='{class_name}'>")
        for _, items in section.items():
            self.wrap_text_with_html_tags(items['text'], items['tag'])
        self.lines.append("</div>")

    def make_form(self, section):
        self.lines.append(f"\n<div class='content'>")
        form_tag = ['<form ']
        for attr, value in section['attr'].items():  # {'method': 'post', 'action': '/data'}
            form_tag.append(f"{attr}='{value}'")
        form_tag.append('>')
        self.lines.append(" ".join(form_tag))
        for form_elem, value in section['elem'].items():
            if form_elem == 'label':
                self.lines.append(f"<label for={value['for']}>{value['text']}</{form_elem}>")
            if form_elem == 'input':
                new_elem = f"""<input type="{value['type']}" id="{value['id']}" name="{value['name']}">"""
                self.lines.append(new_elem)
        button = """<button type="submit">Submit</button>"""
        self.lines.append(button)
        self.lines.append("</form>")
        self.lines.append("</div>")
        

    def wrap_text_with_html_tags(self, line, element):
        line = f"<{element}>{line}</{element}>"
        self.lines.append(line)



def main():
    passer = HTMLParser()
    with open('input.yml', 'r') as fp:
        content = yaml.safe_load(fp)
    for name, section in content.items():
        if name == 'form':
            passer.make_form(section)
        else:
            passer.make_section(name, section)

    passer.write_html_file()
    app.run()


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_post_data():
    return f"<h1>Hello {request.form['name']}</h1>"


if __name__ == '__main__':
    main()

