import os
import pandas as pd
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = 'A program for merge two columns files, first column is gene id, second column is value')
    parser.add_argument('-i', '--input', help='input file.', type=str, nargs="+", required=True)
    parser.add_argument('-o', '--output', help='output file.', type=str, required=True)
    parser.add_argument('--samples', help='input counts file include mutiple samples', action="store_true")
    args = parser.parse_args()
    # 获取文件夹中所有文件的文件名
    file_names = args.input
    # 创建一个空的DataFrame来存储合并后的数据
    merged_data = pd.DataFrame()
    if args.samples:
        for file_name in file_names:
            # 读取当前文件的数据
            data = pd.read_csv(file_name, sep='\t', header=0)
            # 将数据合并到主DataFrame中
            if merged_data.empty:
                merged_data = data
            else:
                merged_data = pd.merge(merged_data, data, on='FEATURE_ID', how='outer').fillna(0)
    else:
        for file_name in file_names:
            # 读取当前文件的数据
            data = pd.read_csv(file_name, sep='\t', header=None, names=['FEATURE_ID', os.path.basename(file_name)])
            data = data[data.iloc[:, 1] != 0]
            # 将数据合并到主DataFrame中
            if merged_data.empty:
                merged_data = data
            else:
                merged_data = pd.merge(merged_data, data, on='FEATURE_ID', how='outer').fillna(0)
    # 将合并后的数据保存到一个新文件中
    merged_data.to_csv(args.output, index=False, sep='\t')
