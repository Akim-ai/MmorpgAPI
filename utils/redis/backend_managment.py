from utils.redis.settings import connect_redis
import json


def set_data_task(prepare_new_data):
    def set_data(*args, **kwargs):
        r = connect_redis()
        prepare_new_data_name = prepare_new_data.__name__
        if not prepare_new_data_name.split('_')[0] == 'prepare':
            raise Exception('Set data task must start with "prepare_" then you can write function name.')
        database_key = prepare_new_data_name.replace('prepare_', '')
        data = r.get(database_key)

        new_data: dict
        key: str

        if not data:
            new_data, key = prepare_new_data(*args, **kwargs)
            new_data = json.dumps(new_data)
            r.set(database_key, new_data)
            return f'Created first task with key: {key}'
        data = json.loads(data)
        new_data, key = prepare_new_data(data=data, *args, **kwargs)
        data.update(new_data)
        data = json.dumps(data)
        r.set(database_key, data)
        return f'Added new task with key: {key}'
    return set_data


def get_data_task(data_actions):
    def get_data(*args, **kwargs) -> str:
        r = connect_redis()
        data_actions_name = data_actions.__name__

        name_check = data_actions_name.split('_')
        if not name_check[0] == 'periodic':
            raise Exception(
                'To act with data in periodic task the function'
                ' must start with "periodic_" and then name of prepare function.'
            )

        database_key = data_actions_name.replace('periodic_', '')
        data = r.get(database_key)
        if not data:
            return f'periodic_{database_key} have not data to work with.'

        data = json.loads(data)

        success: bool
        success = data_actions(data=data, *args, **kwargs)
        if success:
            r.delete(database_key)
            return f'{data_actions_name} succeed.'
        return f'{data_actions_name} failed.'
    return get_data


