import numpy as np
import random
import scipy.sparse as sp

from lightfm.datasets.movielens import fetch_movielens


def generate_dummy_data(num_users=15000, num_items=30000, interaction_density=.00045, pos_int_ratio=.5):

    n_user_features = int(num_users * 1.2)
    n_user_tags = num_users * 3
    n_item_features = int(num_items * 1.2)
    n_item_tags = num_items * 3
    n_interactions = (num_users * num_items) * interaction_density

    user_features = sp.lil_matrix((num_users, n_user_features))
    for i in range(num_users):
        user_features[i, i] = 1

    for i in range(n_user_tags):
        user_features[random.randrange(num_users), random.randrange(num_users, n_user_features)] = 1

    item_features = sp.lil_matrix((num_items, n_item_features))
    for i in range(num_items):
        item_features[i, i] = 1

    for i in range(n_item_tags):
        item_features[random.randrange(num_items), random.randrange(num_items, n_item_features)] = 1

    interactions = sp.lil_matrix((num_users, num_items))
    for i in range(int(n_interactions * pos_int_ratio)):
        interactions[random.randrange(num_users), random.randrange(num_items)] = 1

    for i in range(int(n_interactions * (1 - pos_int_ratio))):
        interactions[random.randrange(num_users), random.randrange(num_items)] = -1

    return interactions, user_features, item_features


def generate_movielens_data(min_positive_rating=4.0):

    data = fetch_movielens(indicator_features=True, genre_features=True)

    train_interactions = data['train']
    test_interactions = data['test']
    item_features = data['item_features']

    train_interactions.data = np.array([1 if value >= min_positive_rating else -1
                                        for value in train_interactions.data])
    test_interactions.data = np.array([1 if value >= min_positive_rating else -1
                                       for value in test_interactions.data])

    num_users = train_interactions.shape[0]
    user_features = sp.csr_matrix(sp.identity(num_users), dtype=np.float32)

    return train_interactions, test_interactions, user_features, item_features
