myfun <- function(name,status=c("score","height")){
  ## Arguments:
  # name   --  name of NBA player
  # status --  data type
  ## Return:
  # result --  related data about NBA player
  # Verify Arguments
  stopifnot(is.character(name),length(name)==1)
  status <- match.arg(status)
  # Data source
  dat <- data.frame(name=c("Pual","Kobe","James","Duncan","O'Neal"),
                    height=c(183,198,206,211,216),
                    score=c(43,81,61,53,61),
                    team=c("Clippers","Lakers","Cavaliers","Lakers","Spurs"),
                    stringsAsFactors = F)
  # Format and return results
  index <- match(name,dat$name)
  if(is.na(index)){
    result <- paste("There is no data about ",name,sep="")
  } else if(status=="score"){
    score <- dat$score[index]  # Extract highest score data
    result <- paste("The highest score of " ,name,"'s career was ",score,sep="") 
  } else {
    height <- dat$height[index] # Extract height data
    result <- paste(name,"'s height is ",height,sep="") 
  }
  return(result)
}

myfun(123,status = "s")
myfun("Durant",status = "s")
