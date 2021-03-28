from collections import defaultdict

SOLIDITY_TO_BQ_TYPES = {
    'address': 'STRING',
}

dataset_name = '<INSERT_DATASET_NAME>'
table_prefix = '<TABLE_PREFIX>'
table_description = ''


def contract_to_table_definitions(abi, contract_address):
    result = {}
    for a in filter_by_type(abi, 'event'):
        abi_item_key = get_abi_item_key(abi, a)
        result[abi_item_key] = abi_to_table_definition(a, contract_address, 'log')
    for a in filter_by_type(abi, 'function'):
        abi_item_key = get_abi_item_key(abi, a)
        result[abi_item_key] = abi_to_table_definition(a, contract_address, 'trace')
    return result


def abi_to_table_definition(abi, contract_address, parser_type):
    table_name = create_table_name(abi)
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


def create_table_name(abi):
    if abi.get('type') == 'event':
        return table_prefix + '_event_' + abi['name']
    else:
        return table_prefix + '_call_' + abi['name']


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


def get_abi_item_key(abi, abi_item):
    name_counts = defaultdict(int)
    for a in abi:
        if 'name' in a:
            name_counts[a['name']] += 1

    is_ambiguous = name_counts[abi_item['name']] > 1

    key = abi_item['name']
    if is_ambiguous:
        input_types = [i['type'] for i in abi_item.get('inputs', [])]
        if input_types:
            key = abi_item['name'] + '_' + '_'.join(input_types)
    return key
