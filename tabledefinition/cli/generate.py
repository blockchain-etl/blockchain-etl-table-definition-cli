# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import os
import pathlib

import click


from tabledefinition.generate_table_definitions import abi_to_table_definitions


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-i', '--abi-file', required=True, show_default=True, type=str, help='Path to ABI file')
@click.option('-d', '--dataset-name', default='<DATASET_NAME>', show_default=True, type=str, help='Dataset name')
@click.option('-n', '--contract-name', default='<CONTRACT_NAME>', show_default=True, type=str, help='Contract name')
@click.option('-a', '--contract-address', show_default=True, type=str, help='Contract address')
@click.option('-o', '--output-dir', default='output', type=str, help='The output directory for table definitions.')
def generate(abi_file, dataset_name, contract_name, contract_address, output_dir):
    """Generate table definitions for the provided ABI file."""

    with open(abi_file, 'r') as abi_file_handle:
        abi = abi_file_handle.read()
        abi = json.loads(abi)
        table_definition_map = abi_to_table_definitions(
            abi,
            dataset_name,
            contract_name,
            contract_address
        )

        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        for key, value in table_definition_map.items():
            output_filename = os.path.join(output_dir, key + '.json')
            with open(output_filename, 'w') as output_file_handle:
                output_file_handle.write(json.dumps(value, indent=4))

        print(str(len(table_definition_map)) + ' table definitions have been written to the ' + output_dir + ' directory')