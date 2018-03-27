import os
import util
import constant
from match_set import MatchSet
import heapq


class ItemKNN(object):
    @staticmethod
    def learn_category_matching_relationship(matched_category_pairs, neigh_size=5):
        """ Learn category matching relationship from collation set, and store them into a local file.

            Args:
                matched_category_pairs: a list of matched category pairs obtained from collation set.
                neigh_size: neighborhood size, for each source category, we only need to keep its more relevant top neigh_size category.

            Return:
                a table with three columns like
                source category            matched category            probability
                1001                       1002                         0.2
                1001                       1005                         0.5
                1001                       1100                         0.3
                ...                        ...                          ...

                The above table is expected to be stored into a local file.
        """
        cat_pair_counts = {}
        cat_freq = {}
        for first_cat, second_cat in matched_category_pairs:
            if (first_cat, second_cat) in cat_pair_counts:
                cat_pair_counts[(first_cat, second_cat)] = cat_pair_counts[(first_cat, second_cat)] + 1
                cat_pair_counts[(second_cat, first_cat)] = cat_pair_counts[(second_cat, first_cat)] + 1
            else:
                cat_pair_counts[(first_cat, second_cat)] = 1
                cat_pair_counts[(second_cat, first_cat)] = 1

            if first_cat in cat_freq:
                cat_freq[first_cat] = cat_freq[first_cat] + 1
            else:
                cat_freq[first_cat] = 1

            if second_cat in cat_freq:
                cat_freq[second_cat] = cat_freq[second_cat] + 1
            else:
                cat_freq[second_cat] = 1

        # compute dense category pairwise relationship
        cat_model = {}
        for first_cat, second_cat in cat_pair_counts.keys():
            if first_cat not in cat_model:
                cat_model[first_cat] = {}
            cat_model[first_cat][second_cat] = 1.0 * cat_pair_counts[(first_cat, second_cat)] / cat_freq[first_cat]

        # compute sparse category pairwise relationship by k-nearest neighbor and write it into a local file
        if os.path.exists(constant.CAT_RELATION_FILE):
            os.remove(constant.CAT_RELATION_FILE)

        with open(constant.CAT_RELATION_FILE, 'a') as output_file:
            for source_cat_id in cat_model.keys():
                keys = heapq.nlargest(neigh_size, cat_model[source_cat_id])
                sum_probs = 0.0
                for key in keys:
                    sum_probs = sum_probs + cat_model[source_cat_id][key]
                for key in keys:
                    output_file.write(str(source_cat_id) + ' ' + str(key) + ' ' + str(cat_model[source_cat_id][key] / sum_probs) + '\n')

        return None

    @staticmethod
    def learn_item_relationship(purchased_item_pairs, neigh_size=200):
        """ Learn item matching relationship from purchased history, and store them into a local file.

            Args:
                purchased item paris: a list of purchased item pairs obtained from item purchased histogry.
                neigh_size: neighborhood size, for each source item, we only need to keep its more relevant top neigh_size items.

            Return:
                a table with three columns like
                source item              purchased item               probability
                1                         2                           0.15
                1                         8                           0.6
                1                         10                          0.15
                1                         20                          0.1

                The above table is expected to be stored into a local file.
        """
        item_pair_counts = {}
        item_freq = {}
        for first_item, second_item in purchased_item_pairs:
            if (first_item, second_item) in item_pair_counts:
                item_pair_counts[(first_item, second_item)] = item_pair_counts[(first_item, second_item)] + 1
                item_pair_counts[(second_item, first_item)] = item_pair_counts[(second_item, first_item)] + 1
            else:
                item_pair_counts[(first_item, second_item)] = 1
                item_pair_counts[(second_item, first_item)] = 1

            if first_item in item_freq:
                item_freq[first_item] = item_freq[first_item] + 1
            else:
                item_freq[first_item] = 1

            if second_item in item_freq:
                item_freq[second_item] = item_freq[second_item] + 1
            else:
                item_freq[second_item] = 1

        # compute dense item pairwise relationship
        item_model = {}
        for first_item, second_cat in item_pair_counts.keys():
            if first_item not in item_model:
                item_model[first_item] = {}
            item_model[first_item][second_cat] = 1.0 * item_pair_counts[(first_item, second_cat)] / item_freq[first_item]

        # compute sparse item pairwise relationship by k-nearest neighbor and write it into a local file
        if os.path.exists(constant.ITEM_RELATION_FILE):
            os.remove(constant.ITEM_RELATION_FILE)

        with open(constant.ITEM_RELATION_FILE, 'a') as output_file:
            for source_item_id in item_model.keys():
                keys = heapq.nlargest(neigh_size, item_model[source_item_id])
                sum_probs = 0.0
                for key in keys:
                    sum_probs = sum_probs + item_model[source_item_id][key]
                for key in keys:
                    output_file.write(str(source_item_id) + ' ' + str(key) + ' ' + str(item_model[source_item_id][key] / sum_probs) + '\n')

        return None


if __name__ == '__main__':

    # learn category relationship model
    match_sets = util.load_match_set(constant.MATCH_SET_FILE)
    item_infos = util.load_item_info(constant.ITEM_FILE, constant.ITEM_IMAGE_PATHS)
    match_cat_pairs = []
    for match_set in match_sets:
        match_cat_pairs.extend(MatchSet.to_matched_cat_pairs(match_set.to_matched_item_pairs(), item_infos))
    ItemKNN.learn_category_matching_relationship(match_cat_pairs)

    # learn item relationship model
    item_infos = util.load_item_info(constant.ITEM_FILE, constant.ITEM_IMAGE_PATHS)
    purchase_history = util.load_bought_history(constant.BOUGHT_HISTORY)
    matched_item_pairs = []
    count = 1
    for items_from_one_user in purchase_history.values():
        matched_item_pairs.extend(items_from_one_user.to_valid_item_pairs(item_infos))
        count = count + 1
        if count >= 100000:
            break
    ItemKNN.learn_item_relationship(matched_item_pairs)