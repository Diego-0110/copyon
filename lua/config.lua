---@type Config
return {
    processors = {
        {
            id = "upper",
            process = function (str_in)
                return string.upper(str_in)
            end,
            desc = "Convert all letters to uppercase"
        },
        {
            id = "lower",
            process = function (str_in)
                return string.lower(str_in)
            end,
            desc = "Convert all letters to lowercase"
        },
        {
            id = "reverse",
            process = function (str_in)
                return string.reverse(str_in)
            end,
            desc = "Invert the text"
        }
    }
}
