SOLIDITY_TO_BQ_TYPES = {
    'address': 'STRING',
}

table_description = ''


def abi_to_table_definitions_for_solana(
        abi,
        dataset_name,
        contract_name,
        contract_address=None,
        include_functions=False
):
    result = {}
    for a in abi.get('events') if abi.get('events') else []:
        parser_type = 'log'
        table_name = create_table_name(a, contract_name, parser_type)
        result[table_name] = abi_to_table_definition(a, contract_address, dataset_name, contract_name, parser_type)
    if include_functions:
        for a in abi.get('instructions') if abi.get('instructions') else []:
            parser_type = 'instruction'
            table_name = create_table_name(a, contract_name, parser_type)
            result[table_name] = abi_to_table_definition(a, contract_address, dataset_name, contract_name, parser_type)
    return result


def abi_to_table_definition(abi, contract_address, dataset_name, contract_name, parser_type):
    table_name = create_table_name(abi, contract_name, parser_type)
    result = {}
    result['parser'] = {
        'type': parser_type,
        'contract_address': contract_address,
        'idl': abi,
        'field_mapping': {}
    }

    inputs = abi.get('args') if parser_type == 'instruction' else abi.get('fields')
    result['table'] = {
        'dataset_name': dataset_name,
        'table_name': table_name,
        'table_description': table_description,
        'schema': [
            {
                'name': x.get('name'),
                'description': '',
                'type': 'STRING'  # we sometimes get parsing errors, so safest to make all STRING
            } for x in inputs
        ]
    }
    return result


def create_table_name(abi, contract_name, parser_type):
    if parser_type == 'log':
        return contract_name + '_event_' + abi['name']
    else:
        return contract_name + '_call_' + abi['name']


def get_columns_from_event_abi(event_abi):
    return [a.get('name') for a in event_abi['inputs']]

