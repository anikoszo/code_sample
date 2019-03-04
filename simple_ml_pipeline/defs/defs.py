import sqlite3
import pandas as pd


def del_cols(df, col_list):
    """

    :param df: dataframe on apply
    :param col_list: parameters on apply
    :return: transformed dataframe
    """
    for col in col_list:
        del df[col]
    return df


def sqlite_connect(name):
    """
     create or connect to database
     :param name: database name
     :return: connection to database
     or create the database
    """
    conn = sqlite3.connect(name)
    return conn


class Palindrome:
  @staticmethod
  def is_palindrome(word):

    if word.lower() == word.lower()[::-1]:
      return "true"
    else:
       return "false"
word = input()
print(Palindrome.is_palindrome(word))