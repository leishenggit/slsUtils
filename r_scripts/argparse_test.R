library("argparse")

parser <- ArgumentParser(description='Process some integers')

parser$add_argument('integers', metavar='N', type="integer", nargs='+', help='an integer for the accumulator')

parser$add_argument('--sum', dest='accumulate', action='store_const', const='sum', default='max',
                    help='sum the integers (default: find the max)')

#args <- parser$parse_args(c("--sum", "1", "2", "3"))
#accumulate_fn <- get(args$accumulate)
#print(accumulate_fn(args$integers))

args <- parser$parse_args()
accumulate_fn <- get(args$accumulate)
print(accumulate_fn(args$integers))