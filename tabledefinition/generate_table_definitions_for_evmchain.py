SOLIDITY_TO_BQ_TYPES = {
    'address': 'STRING',
}

table_description = ''


def abi_to_table_definitions_for_evmchain(
        abi,
        dataset_name,
        contract_name,
        contract_address=None,
        include_functions=False
):
    result = {}
    if contract_address is not None:
        contract_address = contract_address.lower()
    for a in filter_by_type(abi, 'event'):
        table_name = create_table_name(a, contract_name)
        result[table_name] = abi_to_table_definition(a, contract_address, dataset_name, contract_name, 'log')
    if include_functions:
        for a in filter_by_type(abi, 'function'):
            table_name = create_table_name(a, contract_name)
            result[table_name] = abi_to_table_definition(a, contract_address, dataset_name, contract_name, 'trace')
    return result


def abi_to_table_definition(abi, contract_address, dataset_name, contract_name, parser_type):
    table_name = create_table_name(abi, contract_name)
    result = {}
    result['parser'] = {
        'type': parser_type,
        'contract_address': contract_address,
        'abi': abi,
        'field_mapping': {}
    }
    result['table'] = {
        'dataset_name': dataset_name,
        'table_name': table_name,
        'table_description': table_description,
        'schema': [
            {
                'name': x.get('name'),
                'description': '',
                'type': 'STRING'  # we sometimes get parsing errors, so safest to make all STRING
            } for x in abi['inputs']
        ]
    }
    return result


def create_table_name(abi, contract_name):
    if abi.get('type') == 'event':
        return contract_name + '_event_' + abi['name']
    else:
        return contract_name + '_call_' + abi['name']


def s2bq_type(type):
    return SOLIDITY_TO_BQ_TYPES.get(type, 'STRING')


def filter_by_type(abi, type):
    for a in abi:
        if a['type'] == type:
            yield a


def get_columns_from_event_abi(event_abi):
    return [a.get('name') for a in event_abi['inputs']]


def create_struct_fields_from_event_abi(event_abi):
    return ', '.join(['`' + a.get('name') + '` ' + s2bq_type(a.get('type')) for a in event_abi['inputs']])
