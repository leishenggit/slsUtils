library(tidyverse)

df <- tibble(
  g1 = c(1, 1, 2, 2, 2),
  g2 = c(1, 2, 1, 2, 1),
  a = sample(5),
  b = sample(5)
)

#To make this function work, we need to do two things.
#1. quote the input ourselves 
#2. tell group_by() not to quote its input 
#use !! to say that you want to unquote an input so that it’s evaluated

my_summarise <- function(df, group_var) {
  group_var <- enquo(group_var)
  print(group_var)
  
  df %>%
    group_by(!!group_var) %>%
    summarise(a = mean(a))
}

my_summarise(df, g1)


my_summarise2 <- function(df, expr) {
  expr <- enquo(expr)
  
  quo(summarise(df,
            mean = mean(!! expr),
            sum = sum(!! expr),
            n = n()
  ))
}

my_summarise2(df, a)

my_summarise2(df, a * b)

#You can also wrap quo() around the dplyr call to see what will happen from dplyr’s perspective.
#This is a very useful tool for debugging.

my_mutate <- function(df, expr) {
  expr <- enquo(expr)
  mean_name <- paste0("mean_", quo_name(expr))
  sum_name <- paste0("sum_", quo_name(expr))
  
  mutate(df,
         !! mean_name := mean(!! expr),
         !! sum_name := sum(!! expr)
  )
}

my_mutate(df, a)

# extend my_summarise() to accept any number of grouping variables.
my_summarise <- function(df, ...) {
  group_var <- enquos(...)
  
  df %>%
    group_by(!!! group_var) %>%
    summarise(a = mean(a))
}

my_summarise(df, g1, g2)
