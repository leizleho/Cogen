import os
from jinja2 import Template, Environment, FileSystemLoader


def write_code(tpl_path, tpl_file, kwargs, output_obj, out_dir=None):
    """Function to generate code with the given params:
    tpl_path = directory path for the template file
    tpl_file = name of the template file
    kwargs = key-value pair of variables used in tpl_file
    output_obj = {"output_path" : "_____","output_file" :"_____"}
    """
    template_path = os.path.join(os.path.dirname(__file__), tpl_path)
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(tpl_file)
    output = template.render(kwargs=kwargs)

    # Create directory if directory does not exist
    if not out_dir:
        out_dir = f'./builds/{output_obj["output_path"]}'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_name = f'{out_dir}/{output_obj["output_file"]}'
    file_output = open(file_name, 'w')
    file_output.write(output)
    file_output.close()
