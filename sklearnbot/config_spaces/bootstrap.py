import ConfigSpace
import sklearn
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
    return ['decision_tree']


def get_config_space(classifier: sklearn.base.BaseEstimator, seed: typing.Optional[int]) \
        -> ConfigSpace.ConfigurationSpace:
    """
    Maps string names to a stored instantiation of the configuration space.

    Parameters
    ----------
    classifier: str
        The string name of the config space

    seed: int or None
        Will be passed to the Configuration Space object, and used for random
        sampling. Leave to None to assign a random seed (often preferred)

    Returns
    -------
    ConfigSpace.ConfigurationSpace
        An instantiation of the ConfigurationSpace
    """
    if classifier == 'decision_tree':
        return sklearnbot.config_spaces.decision_tree.get_hyperparameter_search_space(seed)
    else:
        raise ValueError()
