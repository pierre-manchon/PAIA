# -*-coding: utf8 -*
"""
Function for basic processing and miscellanious cases
"""
from os import path
from pathlib import Path
from collections import Counter
from configparser import ConfigParser
from typing import AnyStr, List, Generator, Union


def var_dump(var, prefix=''):
    """
    You know you're a php developer when the first thing you ask for
    when learning a new language is 'Where's var_dump?????'
    https://stackoverflow.com/a/21791626
    """
    my_type = '[' + var.__class__.__name__ + '(' + str(len(var)) + ')]:'
    print(prefix, my_type, sep='')
    prefix += '    '
    for i in var:
        if type(i) in (list, tuple, dict, set):
            var_dump(i, prefix)
        else:
            if isinstance(var, dict):
                print(prefix, i, ': (', var[i].__class__.__name__, ') ', var[i], sep='')
            else:
                print(prefix, '(', i.__class__.__name__, ') ', i, sep='')


def format_dataset_output(dataset: AnyStr, name: AnyStr, ext: AnyStr = '') -> tuple[str, Union[AnyStr, str], str]:
    """
    :param dataset:
    :type dataset: AnyStr
    :param name: Name of the output file
    :type name: AnyStr
    :param ext: Extension of the output file. If blank, then the input file's etension will be used.
    :type ext: AnyStr
    :return: Dataset name, dataset extension, output path formatted
    :rtype: tuple[str, Union[AnyStr, str], str]
    """
    __ext = Path(dataset).suffix
    __dataset_name = Path(dataset).name.replace(__ext, '')

    if ext != '':
        __ext = ext
    else:
        pass

    __output_path = path.join(Path(dataset).parent, ''.join([__dataset_name, '_', name, __ext]))
    return __dataset_name, __ext, __output_path


def __gather(pixel_values: Generator) -> List:
    """
    Using a generator as an input, i __gather every value encountered into a list.

    :param pixel_values: Float value of a pixel in a raster band
    :type pixel_values: Generator
    :return: A list of all of the pixels found in a raster band
    :rtype: List
    """
    __cat = []
    for x in pixel_values:
        __cat.append(x)
    return __cat


def __get_value_count(pixel_array: List) -> Counter:
    """
    Using a list as an input, i

    :param pixel_array:  A list of all of the pixels found in a raster band
    :type pixel_array: List
    :return: Countered data
    :rtype: Counter
    """
    __nb = Counter()
    __nb.update(pixel_array)
    return __nb


def get_config_value(value):
    cfgparser = ConfigParser()
    cfgparser.read('./PAIA/config.cfg')
    return cfgparser.get('config', value)