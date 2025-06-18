import argparse
import pandas as pd

def split_dataframe(input_file, column_indices):
    # 读取数据框文件
    df = pd.read_csv(input_file)
    
    # 根据指定的列索引进行分割
    for idx in column_indices:
        unique_values = df.iloc[:, idx].unique()  # 使用 iloc 获取指定列索引的列
        for value in unique_values:
            sub_df = df[df.iloc[:, idx] == value]  # 使用 iloc 进行筛选
            output_file = f"column_{idx}_{value}.csv"  # 文件名包含列索引
            sub_df.to_csv(output_file, index=False)
            print(f"Saved {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split dataframe based on specified column indices')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input CSV file')
    parser.add_argument('--column_indices', type=int, nargs='+', required=True, help='Column indices to split the dataframe on')

    args = parser.parse_args()

    input_file = args.input_file
    column_indices_to_split = args.column_indices

    split_dataframe(input_file, column_indices_to_split)
