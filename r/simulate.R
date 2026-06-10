parse_named_args <- function(args) {
  result <- list()
  for (arg in args) {
    if (grepl("^--[^=]+=", arg)) {
      key   <- sub("^--([^=]+)=.*", "\\1", arg)
      value <- sub("^--[^=]+=", "", arg)
      result[[key]] <- value
    }
  }
  result
}

opts <- parse_named_args(commandArgs(trailingOnly = TRUE))

inputs_path  <- if (!is.null(opts$inputs))  opts$inputs  else "data/inputs"
outputs_path <- if (!is.null(opts$outputs)) opts$outputs else "data/outputs"

message("[INFO] Starting simulation")
message("[INFO] inputs_path:  ", inputs_path)
message("[INFO] outputs_path: ", outputs_path)

# TODO: implement simulation logic here
