local socket = require("socket")

-- CONFIGURATION
local FILE_PATH = "c:/Users/GRH/Desktop/Projects/CAREN-Therapist-UI/backend/data_test.csv"      -- Path to your CSV file
local HOST = "127.0.0.1"          -- Destination IP
local PORT = 12345                -- Destination port
local USE_UDP = true             -- Set to true for UDP, false for TCP

-- Open CSV file
local file = io.open(FILE_PATH, "r")
if not file then
    error("Could not open file: " .. FILE_PATH)
end

-- Create socket
local client
if USE_UDP then
    client = socket.udp()
    client:setpeername(HOST, PORT)
else
    client = assert(socket.tcp())
    assert(client:connect(HOST, PORT))
end

-- Read and send each line
for line in file:lines() do
    -- Send line as string
    if USE_UDP then
        client:send(line)
    else
        client:send(line .. "\n")
    end
    print("Sent: " .. line)
    socket.sleep(0.5) -- Wait 1 second
end

file:close()
client:close()