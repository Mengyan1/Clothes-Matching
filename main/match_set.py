""" Collation set """

import constant
import itertools


class MatchSet(object):
    """Match set.

       One example:
           [[1,2], [3], [4,5,6]]
    """

    def __init__(self, _match_set):
        self._match_set = _match_set

    def to_matched_item_pairs(self):
        matched_item_pairs = []
        matched_group_pairs = list(itertools.combinations(self._match_set, 2))
        for first_group, second_group in matched_group_pairs:
            matched_item_pairs.extend(list(itertools.product(first_group, second_group)))
        return matched_item_pairs

    @staticmethod
    def to_matched_cat_pairs(matched_item_pairs, item_infos):
        matched_cat_pairs = []
        for first_item, second_item in matched_item_pairs:
            #if item_infos.has_key(first_item) and item_infos.has_key(second_item):
            if (first_item in item_infos) and (second_item in item_infos):
                first_item_cat_id = item_infos[first_item].get_cat_id()
                second_item_cat_id = item_infos[second_item].get_cat_id()
                matched_cat_pairs.append(
                    (min(first_item_cat_id, second_item_cat_id), max(first_item_cat_id, second_item_cat_id)))
        return matched_cat_pairs


if __name__ == '__main__':
    import util

    print ('Bingo')
    collation_list = [['1463018', '230955'],
                      ['1596334', '1704853'],
                      ['2226122', '284814', '36278', '480281']]
    match_set = MatchSet(collation_list)
    matched_item_pairs = match_set.to_matched_item_pairs()
    item_info = util.load_item_info(constant.ITEM_FILE, constant.ITEM_IMAGE_PATHS)
    print (MatchSet.to_matched_cat_pairs(matched_item_pairs, item_info))
