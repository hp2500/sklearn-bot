import ConfigSpace
import sklearnbot
import typing


def get_available_config_spaces():
    """
    Returns a list of all available configuration spaces. To be used in
    example scripts, to determine which classifiers this can be ran with. 

    Returns
    -------
    config_spaces : list[str]
        A list of all available configuration spaces.
    """
    return [
        'adaboost',
        'decision_tree',
        'gradient_boosting',
        'neural_network',
        'random_forest',
        'sgd',
        'svc'
    ]


def get_config_space(classifier_name: str, seed: typing.Optional[int]) \
        -> ConfigSpace.ConfigurationSpace:
    """
    Maps string names to a stored instantiation of the configuration space.

    Parameters
    ----------
    classifier_name: str
        The string name of the config space

    seed: int or None
        Will be passed to the Configuration Space object, and used for random
        sampling. Leave to None to assign a random seed (often preferred)

    Returns
    -------
    ConfigSpace.ConfigurationSpace
        An instantiation of the ConfigurationSpace
    """
    if classifier_name not in get_available_config_spaces():
        raise ValueError('Classifier search space not implemented: %s' % classifier_name)
    return getattr(sklearnbot.config_spaces, classifier_name).get_hyperparameter_search_space(seed)
