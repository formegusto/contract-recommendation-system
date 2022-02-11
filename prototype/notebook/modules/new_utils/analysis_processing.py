from modules.common.calc_datas import db_process


def analysis_processing_single(result):
    in_db = dict()
    in_db['changePer'] = dict()
    for main_target, sub_target, item_name in db_process:
        items = dict()

        for contract in ['comp', 'single']:
            percentages = result[main_target][sub_target][contract].columns.tolist(
            )
            values = result[main_target][sub_target][contract].values.reshape(
                -1).tolist()

            item = [{
                "percentage": int(percentage),
                "value": values[idx]
            } for idx, percentage in enumerate(percentages)]

            items[contract] = item

        change_per = int(result[1]['pos_change_per'][sub_target][0])
        in_db[item_name] = items
        in_db['changePer'][item_name] = change_per

    return in_db
