---@class Processor
---@field id string unique identifier for the processor
---@field process function function to execute when the clipboard change
---@field desc? string optional description of the processsor

---@class Config
---@field processors Processor[] list of available processors
