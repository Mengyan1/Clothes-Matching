from clothes_matcher import ItemKNNMatcher
import util
import constant
from match_set import MatchSet




def generate_target():
    # generate target from expert matching files
    match_sets = util.load_match_set(constant.MATCH_SET_FILE)
    match_pairs = []
    for match_set in match_sets:
        match_pairs += match_set.to_matched_item_pairs()
    return match_pairs

def generate_recommendation(source_list, k):
    # generate test results of ItemkNNMatcher
    recommendation_pairs = []
    for source in source_list:
        recommend_item_list = ItemKNNMatcher().find_matched_clothes(source, k)
        recommendation_pairs += [(source, target) for target in recommend_item_list]
    return recommendation_pairs

if __name__ == '__main__':

    match_pairs = generate_target()
    match_pairs = match_pairs[:1000]
    source_list = [pair[0] for pair in match_pairs]
    #print ('match_pairs:' , match_pairs)
    #print ('source_list:', source_list)
    recommendation_pairs = generate_recommendation(source_list, k=10)
    print ('recommendation_pairs:', recommendation_pairs[:100])

    precision = len(set(recommendation_pairs).difference(set(match_pairs)))*0.01/len(set(recommendation_pairs))
    recall = len(set(recommendation_pairs).difference(set(match_pairs)))*0.01/len(set(match_pairs))
    print ('Precision is :', precision)
    print ('Recall is:', recall)








    #c = list(set(a).difference(set(b))
































