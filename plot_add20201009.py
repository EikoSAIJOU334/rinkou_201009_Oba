#!/usr/bin/env python3

import os, re, sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import plot20201009


def extract_file_name(dirname):
    """
    Extract sample name and ChIP names
    returned df will be:
    sample     ChIP                                               file
0    E119  H3K4me3  20201009_nakato_testdata/E119-H3K4me3.jaccard.csv
1    E100  H3K4me3  20201009_nakato_testdata/E100-H3K4me3.jaccard.csv
2    E124  H3K27ac  20201009_nakato_testdata/E124-H3K27ac.jaccard.csv
3    E117  H3K9me3  20201009_nakato_testdata/E117-H3K9me3.jaccard.csv
4    E118  H3K4me3  20201009_nakato_testdata/E118-H3K4me3.jaccard.csv
    """
    # トリプルクオーテーションを使いこなしている！

    file_list = os.listdir(dirname)
    # ディレクトリ中のファイル名をリストとして取り出す
    s = pd.Series(file_list)
    # pd.Seriesはベクトル、pd.DataFrameは二次元
    df = s.str.extract('(?P<sample>.*)-(?P<ChIP>.*)\.jaccard\.csv',expand=True)
    # str.extract()は、文字列要素を持つ列を正規表現で複数に分割
    # 第一引数に正規表現の()で囲まれたグループ部分にマッチする文字列ごとに分割される
    # expand = Trueにすると、抽出されたグループが新しい列となる
    # 正規表現パターンに名前付きグループ(?P<name>...)を使うと名前がそのまま列名（カラム名）になる。
    # つまりこの場合、<sample>と<ChIP>が列名として使われる。
    df["file"] = dirname+s
    # できたdfに、"file"列を追加、ファイルごとにpathを付けたものができる
    return df


def plot_one(df1,col_name,label,ChIP):
    """
    Plot result from a DataFrame.
    Save image as "ChIP/label.Jaccard.pdf"
    x axis: 0-500
    """

    # Plot settings
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(df1[col_name], label=label, color="red")

    # axis settings
    ax.set_xlim(0,500)
    # ax.set_ylim(0,4)

    # Title & legend settings
    ax.legend(loc='upper right')
    ax.set_title(col_name)

    # Saving settings
    save_name =  "{}/{}.Jaccard.pdf".format(ChIP,label)
    plt.savefig(save_name)
    plt.close()
    # without plt.close() -> RuntimeWarning: More than 20 figures have been opened.
    return


def my_makedirs(directory):
    """
    Make directorys by unique ChIP name.
    If directory already exists, do nothing.
    """
    if not os.path.isdir(directory):
        # (directory)がなかったら作る。
        # os.path.isdir()は、ディレクトリの存在確認
        os.makedirs(directory)
    else:
        pass
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="plot each result of SSP files")
    parser.add_argument("Dir", help="directory path", type=str)

    args = parser.parse_args()
    dirname = args.Dir

    extracted_filename = extract_file_name(dirname)
    # extract_file_nameのコマンドがよくわからない。
    # pythonのコマンド？？
    # 何が出来上がる？？データフレーム？

# make dir by ChIP name
    ChIPs = extracted_filename["ChIP"].unique()
    # .unique()は、ユニークな要素の値のリストをNumPy配列ndarrayで返す
    for i in ChIPs:
        # ユニークな要素ごとにディレクトリを作成する
        my_makedirs(i)

# plot each file
    for i in range(len(extracted_filename)):
        line = extracted_filename.iloc[i]
        data = plot20201009.read_file(line["file"])
        label = "{}-{}".format(line["sample"],line["ChIP"])
        plot_one(data,"per control",label,line["ChIP"])
