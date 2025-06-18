library(argparse)
library(readr)
library(tidyr)
library(stringr)
library(dplyr)

parser <- ArgumentParser(description='merge gene score file list to a OTU-like file')

parser$add_argument('--fs', help='nodes file', nargs='+', required='True')
parser$add_argument('--out_f', help='output filename', required='True')

args <- parser$parse_args()

print(args)

lst <- lapply(args$fs, read_tsv, col_names=c('Coordinates','score'))
names(lst) <- str_replace(args$fs,  '.*[/]', '')

raw_data <- bind_rows(lst, .id = "Sample")
df <- raw_data %>% spread(Sample,score,fill=0)
write_tsv(df, args$out_f)

